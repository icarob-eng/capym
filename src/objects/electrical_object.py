import numpy
from numpy import array

from object import Object


class ElectricalObject(Object):
    def __init__(self,
                 mass: float,
                 position: tuple,
                 velocity: tuple,
                 electric_charge: float = 0):
        super().__init__(mass, position, velocity)
        self.electric_charge = electric_charge

    def acceleration_contribution(self, other, gravitational_constant: float, **kwargs) -> array:
        return self.__gravitational_acceleration(other, gravitational_constant) \
            + self.__electrical_acceleration(other, kwargs['electrical_constant'])

    def __electrical_acceleration(self, other, electrical_constant):
        if isinstance(other, self.__class__) or issubclass(other, self.__class__):
            distance_vector = other.position - self.position

            if (numpy.linalg.norm(distance_vector)) == 0:
                raise Exception('Two objects can\'t be in the same position')

            return (electrical_constant * self.electric_charge * other.electric_charge
                    / numpy.linalg.norm(distance_vector)
                    *
                    distance_vector / numpy.linalg.norm(distance_vector)) / self.mass
            # (k*q1*q2/|r| * r/|r|)/m
        else:
            raise Exception('The other argument must be a Object.')
