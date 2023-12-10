import copy
import json
import uuid
import numpy

from numpy import array, arange
from pathlib import Path

from src.objects.object import Object


class Simulation(object):

    def __init__(self,
                 interval: float,
                 objects: array,
                 final_moment: float,
                 initial_moment: float = 0.0,
                 constant_of_gravitation: float = 6.6708e-11
                 ):

        if numpy.dtype(objects) == numpy.dtypes.ObjectDType:
            self.__objects = objects
        else:
            raise ValueError("The objects must be descendent of Object class.")

        self.__constant_of_gravitation = constant_of_gravitation

        self.__initial_moment = initial_moment
        self.__final_moment = final_moment
        self.__interval = interval

        self.__historical_moments: dict[float, array] = {}

    def __dict__(self) -> dict:
        return {
            "interval": self.__interval,
            "objects": self.__objects,
            "number_of_objects": len(self.__objects),
            "initial_moment": self.__initial_moment,
            "final_moment": self.__final_moment,
            "constant_of_gravitation": self.constant_of_gravitation,
        }

    def __copy__(self) -> 'Simulation':
        return Simulation(initial_moment=self.initial_moment, objects=self.objects, final_moment=self.final_moment,
                          interval=self.interval, constant_of_gravitation=self.constant_of_gravitation)

    def __deepcopy__(self, memo) -> 'Simulation':
        return Simulation(
            initial_moment=copy.deepcopy(self.__initial_moment, memo),
            interval=copy.deepcopy(self.__interval, memo),
            final_moment=copy.deepcopy(self.__final_moment, memo),
            constant_of_gravitation=copy.deepcopy(self.__constant_of_gravitation, memo),
            objects=copy.deepcopy(self.__objects, memo)
        )

    def __str__(self):
        return (f"Simulation(initial_moment={self.initial_moment}, final_moment={self.__final_moment}, "
                f"interval={self.interval}, objects={self.objects}, "
                f"constant_of_gravitation={self.constant_of_gravitation}")

    def __contains__(self, item: Object | uuid) -> bool:
        if isinstance(item, Object) or issubclass(item, Object):
            return item in self.__objects
        else:
            return item in self.uuids

    def __add__(self, other: Object) -> 'Simulation':
        if isinstance(other, Object) or issubclass(type(other), Object):
            numpy.append(self.__objects, other)
        return self

    @property
    def interval(self) -> float:
        return self.__interval

    @property
    def objects(self) -> array:
        return self.__objects

    @property
    def initial_moment(self) -> float:
        return self.__initial_moment

    @property
    def constant_of_gravitation(self) -> float:
        return self.__constant_of_gravitation

    @property
    def final_moment(self) -> float:
        return self.__final_moment

    @property
    def number_of_objects(self) -> int:
        return len(self.__objects)

    @property
    def history(self) -> dict[float, array]:
        return self.__historical_moments

    @property
    def number_of_history(self) -> int:
        return len(arange(self.initial_moment, self.final_moment, self.interval))

    @property
    def moments(self) -> array:
        return self.__generate_moments_with_homogeneous_intervals()

    @property
    def was_simulated(self) -> bool:
        return len(self.__historical_moments) == 0

    @property
    def uuids(self) -> array:
        return array([element.uuid for element in self.__objects])

    @property
    def historical_moments(self) -> array:
        return array([moment for (moment, _) in self.__historical_moments])

    def get_data_of_object_at(self, object_uuid: uuid.UUID, moment: float) -> Object:

        if self.initial_moment <= moment <= self.final_moment:
            intervals = self.__generate_moments_with_homogeneous_intervals()

            index_of_the_closest = numpy.abs(intervals - moment).argmin()
            closest = intervals[index_of_the_closest]

            return list(filter(lambda element: element.uuid == object_uuid, self.history[closest]))[0]

        raise ValueError("The moment informed is outside the simulation range.")

    def __generate_moments_with_homogeneous_intervals(self) -> array:
        return array(
            [moment for moment in arange(self.initial_moment, self.final_moment, self.interval)]
        )

    def simulate(self, previously_simulated: float):

        objects_snapshot = array(self.objects, copy=True)

        self.__historical_moments[previously_simulated] = objects_snapshot

        for obj in self.objects:
            obj_acceleration_previously_value = obj.acceleration
            for interacts_with in objects_snapshot:
                if obj.uuid != interacts_with.uuid:
                    obj.acceleration += obj.gravitational_acceleration(interacts_with, self.constant_of_gravitation)

            obj.velocity += obj.acceleration * self.interval
            obj.position += obj.velocity * self.interval

            obj.acceleration = obj_acceleration_previously_value

    def run(self):
        intervals = self.__generate_moments_with_homogeneous_intervals()
        for interval in intervals:
            self.simulate(interval)

    def to_json(self):
        return json.dumps(self.__dict__())

    def save_to_file(self, file_path: Path):
        if self.was_simulated:
            if file_path.parent.exists() and file_path.parent.is_dir():
                if not file_path.exists():
                    file = open(file_path, 'w')
                    file.write(self.to_json())
                else:
                    raise FileExistsError("The file already exists.")
            else:
                NotADirectoryError("The parent directory does not exists.")
        else:
            raise RuntimeError("The history is empty.")

    def get_history_by_object(self, object_uuid: uuid):
        return array([obj for (_, objs_snapshot) in self.__objects for obj in objs_snapshot if obj.uuid == object_uuid])
