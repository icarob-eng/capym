import numpy as np

from electrical_object import ElectricalObject
from attrs import define, field

from src.objects.object import Object


@define
class Line(ElectricalObject):
    direction = field(factory=lambda i: np.array(i)/np.linalg.norm(np.array(i)))  # guarantees direction is unit vector
    normal_direction = np.array((- direction[1], direction[0]))

    def __gravitational_acceleration(self, other: Object, gravitational_constant: float) -> np.array:
        distance_vector = self.normal_direction.dot(other.position) * self.normal_direction

        return (gravitational_constant * other.mass / np.linalg.norm(distance_vector)
                *
                distance_vector / np.linalg.norm(distance_vector))

    def __electrical_acceleration(self, other: ElectricalObject, electrical_constant: float) -> np.array:
        if issubclass(other.__class__, Object):
            distance_vector = self.normal_direction.dot(other.position) * self.normal_direction
            (electrical_constant * self.electric_charge * other.electric_charge
             / np.linalg.norm(distance_vector)
             *
             distance_vector / np.linalg.norm(distance_vector)) / self.mass
            # (k*q1*q2/|r| * r/|r|)/m
