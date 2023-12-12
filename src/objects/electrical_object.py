import attr.setters
import numpy as np

from object import Object
from attrs import define, field


@define
class ElectricalObject(Object):
    electric_charge = field(factory=float, on_setattr=attr.setters.frozen)

    def acceleration_contribution(self, other, gravitational_constant: float, **kwargs) -> np.array:
        return self.__gravitational_acceleration(other, gravitational_constant) \
            + self.__electrical_acceleration(other, kwargs['electrical_constant'])

    def __electrical_acceleration(self, other: 'ElectricalObject', electrical_constant: float) -> np.array:
        if issubclass(other.__class__, ElectricalObject):
            distance_vector = other.position - self.position

            if (np.linalg.norm(distance_vector)) == 0:
                raise Exception('Two objects can\'t be in the same position')

            return (electrical_constant * self.electric_charge * other.electric_charge
                    / np.linalg.norm(distance_vector)
                    *
                    distance_vector / np.linalg.norm(distance_vector)) / self.mass
            # (k*q1*q2/|r| * r/|r|)/m
