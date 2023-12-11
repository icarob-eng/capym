import copy
import json
import uuid
import numpy

from numpy import array, arange
from pathlib import Path
from loguru import logger

from src.objects.object import Object


class Simulation(object):

    @logger.catch
    def __init__(self,
                 step: float,
                 objects: array,
                 final_instant: float,
                 initial_instant: float = 0.0,
                 gravitational_constant: float = 6.6708e-11
                 ):

        if numpy.dtype(objects) == numpy.dtypes.ObjectDType:
            self.__objects = objects
        else:
            raise ValueError("The objects must be descendent of Object class.")

        self.__gravitational_constant = gravitational_constant

        self.__initial_instant = initial_instant
        self.__final_instant = final_instant
        self.__step = step

        self.__snapshots: dict[float, array] = {}

    def __dict__(self) -> dict:
        return {
            "step": self.__step,
            "objects": self.__objects,
            "number_of_objects": len(self.__objects),
            "initial_instant": self.__initial_instant,
            "final_instant": self.__final_instant,
            "gravitational_constant": self.gravitational_constant,
        }

    def __copy__(self) -> 'Simulation':
        return Simulation(initial_instant=self.initial_instant, objects=self.objects, final_instant=self.final_instant,
                          step=self.step, gravitational_constant=self.gravitational_constant)

    def __deepcopy__(self, memo) -> 'Simulation':
        return Simulation(
            initial_instant=copy.deepcopy(self.__initial_instant, memo),
            step=copy.deepcopy(self.__step, memo),
            final_instant=copy.deepcopy(self.__final_instant, memo),
            gravitational_constant=copy.deepcopy(self.__gravitational_constant, memo),
            objects=copy.deepcopy(self.__objects, memo)
        )

    def __str__(self) -> str:
        return (f"Simulation(initial_instant={self.initial_instant}, final_instant={self.__final_instant}, "
                f"step={self.step}, objects={self.objects}, "
                f"gravitational_constant={self.gravitational_constant}")

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
    def step(self) -> float:
        return self.__step

    @property
    def objects(self) -> array:
        return self.__objects

    @property
    def initial_instant(self) -> float:
        return self.__initial_instant

    @property
    def gravitational_constant(self) -> float:
        return self.__gravitational_constant

    @property
    def final_instant(self) -> float:
        return self.__final_instant

    @property
    def number_of_objects(self) -> int:
        return len(self.__objects)

    @property
    def snapshots(self) -> dict[float, array]:
        return self.__snapshots

    @property
    def number_of_snapshots(self) -> int:
        return len(arange(self.initial_instant, self.final_instant, self.step))

    @property
    def moments(self) -> array:
        return self.__generate_moments_with_homogeneous_steps()

    @property
    def was_simulated(self) -> bool:
        return len(self.__snapshots) == 0

    @property
    def uuids(self) -> array:
        return array([element.uuid for element in self.__objects])

    @property
    def snapshots_instants(self) -> array:
        return array([snapshot for (snapshot, _) in self.__snapshots])

    @logger.catch
    def get_data_of_object_at(self, object_uuid: uuid.UUID, moment: float) -> Object:

        if self.initial_instant <= moment <= self.final_instant:
            steps = self.__generate_moments_with_homogeneous_steps()

            index_of_the_closest = numpy.abs(steps - moment).argmin()
            closest = steps[index_of_the_closest]

            return list(filter(lambda element: element.uuid == object_uuid, self.snapshots_instants[closest]))[0]

        raise ValueError("The moment informed is outside the simulation range.")

    def __generate_moments_with_homogeneous_steps(self) -> array:
        return array(
            [moment for moment in arange(self.initial_instant, self.final_instant, self.step)]
        )

    def iterate(self, previously_simulated: float) -> None:

        objects_snapshot = array(self.objects, copy=True)

        self.__snapshots[previously_simulated] = objects_snapshot

        for obj in self.objects:
            obj_acceleration_previously_value = obj.acceleration
            for interacts_with in objects_snapshot:
                if obj.uuid != interacts_with.uuid:
                    obj.acceleration += obj.gravitational_acceleration(interacts_with, self.gravitational_constant)

            obj.velocity += obj.acceleration * self.step
            obj.position += obj.velocity * self.step

            obj.acceleration = obj_acceleration_previously_value

    def run(self) -> None:
        steps = self.__generate_moments_with_homogeneous_steps()
        for step in steps:
            self.iterate(step)

    def to_json(self) -> str:
        return json.dumps(self.__dict__())

    @logger.catch
    def save_to_file(self, file_path: Path) -> None:
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
            raise RuntimeError("The snapshot list is empty.")

    def get_history_by_object(self, object_uuid: uuid) -> array:
        return array([obj for (_, objs_snapshot) in self.__objects for obj in objs_snapshot if obj.uuid == object_uuid])

    def clear_snapshot_list(self, save_as: Path = None):
        if save_as is not None:
            self.save_to_file(file_path=save_as)

        self.__snapshots = {}
