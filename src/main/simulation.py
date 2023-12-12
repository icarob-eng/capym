import json
import uuid

import attrs.setters
import numpy

from numpy import array, arange
from pathlib import Path
from loguru import logger
from attrs import define, field

from src.objects.object import Object


@define(frozen=True)
class Simulation(object):
    step: float
    objects: array
    final_instant: float
    snapshots: dict[float, array] = field(default={}, init=False, on_setattr=attrs.setters.NO_OP)
    initial_instant: float = field(default=0.0)
    gravitational_constant: float = field(default=6.6708e-11)
    electrical_constant: float = field(default=1.5576e-9)

    @property
    def number_of_objects(self) -> int:
        return len(self.objects)

    @property
    def number_of_snapshots(self) -> int:
        return len(arange(self.initial_instant, self.final_instant, self.step))

    @property
    def instants(self) -> array:
        return self.__generate_instants_with_homogeneous_steps()

    @property
    def was_simulated(self) -> bool:
        return len(self.snapshots) == 0

    @property
    def uuids(self) -> array:
        return array([element.uuid for element in self.objects])

    @property
    def snapshots_instants(self) -> array:
        return array([instants for (instants, _) in self.snapshots])

    @logger.catch
    def get_data_of_object_at(self, object_uuid: uuid.UUID, instant: float) -> Object:

        if self.initial_instant <= instant <= self.final_instant:
            steps = self.__generate_instants_with_homogeneous_steps()

            index_of_the_closest = numpy.abs(steps - instant).argmin()
            closest = steps[index_of_the_closest]

            return list(filter(lambda element: element.uuid == object_uuid, self.snapshots_instants[closest]))[0]

        raise ValueError("The instant informed is outside the simulation range.")

    def __generate_instants_with_homogeneous_steps(self) -> array:
        return array(
            [instant for instant in arange(self.initial_instant, self.final_instant, self.step)]
        )

    def iterate(self, previously_simulated: float) -> None:
        objects_snapshot = array(self.objects, copy=True)

        self.snapshots[previously_simulated] = objects_snapshot

        for obj in self.objects:
            resultant_acceleration = numpy.array([0, 0])

            for interacts_with in objects_snapshot:
                if obj.uuid != interacts_with.uuid:
                    resultant_acceleration += obj.acceleration_contribution(
                        interacts_with, self.gravitational_constant, self.electrical_constant)

            obj.velocity += obj.acceleration * self.step
            obj.position += obj.velocity * self.step

    def run(self) -> None:
        steps = self.__generate_instants_with_homogeneous_steps()
        for step in steps:
            self.iterate(step)

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

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

    def get_snapshot_list_by_object(self, object_uuid: uuid) -> array:
        return array([obj for (_, objs_snapshot) in self.objects for obj in objs_snapshot if obj.uuid == object_uuid])

    def clear_snapshot_list(self, save_as: Path = None):
        if save_as is not None:
            self.save_to_file(file_path=save_as)

        snapshots = {}
