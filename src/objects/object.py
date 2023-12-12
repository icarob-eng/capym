import numpy
import uuid

from numpy import array
from loguru import logger
from attrs import define, field


@define(auto_attribs=True)
class Object(object):
    uuid: uuid = field(default=uuid.uuid4(), init=False)
    mass: float
    position: array
    velocity: array

    def acceleration_contribution(self, other, gravitational_constant: float, **kwargs) -> array:
        return self.__gravitational_acceleration(other, gravitational_constant)

    @logger.catch
    def __gravitational_acceleration(self, other: 'Object', gravitational_constant: float) -> array:
        distance_vector = other.position - self.position

        if (numpy.linalg.norm(distance_vector)) == 0:
            raise Exception('Two objects can\'t be in the same position')

        return (gravitational_constant * other.mass / numpy.linalg.norm(distance_vector)
                *
                distance_vector / numpy.linalg.norm(distance_vector))
        # Gm/|r| * r/|r|
