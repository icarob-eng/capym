import numpy as np
import uuid

from loguru import logger
from attrs import define, field


@define(auto_attribs=True)
class Object(object):
    uuid: uuid = field(default=uuid.uuid4(), init=False)
    mass: float
    position: np.array
    velocity: np.array

    def acceleration_contribution(self, other, gravitational_constant: float, **kwargs) -> np.array:
        return self.__gravitational_acceleration(other, gravitational_constant)

    @logger.catch
    def __gravitational_acceleration(self, other: 'Object', gravitational_constant: float) -> np.array:
        distance_vector = other.position - self.position

        if (np.linalg.norm(distance_vector)) == 0:
            raise Exception('Two objects can\'t be in the same position')

        return (gravitational_constant * other.mass / np.linalg.norm(distance_vector)
                *
                distance_vector / np.linalg.norm(distance_vector))
        # Gm/|r| * r/|r|
