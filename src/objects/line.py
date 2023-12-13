import numpy as np
from attrs import define, field

from src.objects.object import Object
from .electrical_object import ElectricalObject


@define
class Line(ElectricalObject):
    direction: np.array = field()
    normal_direction: np.ndarray = field(init=False)

    @normal_direction.default
    def _normal_direction(self):
        return np.array((- self.direction[1], self.direction[0]))

    @direction.validator
    def validate_direction(self, attribute, value):
        if not isinstance(value, np.ndarray):
            raise ValueError("The vector must be a numpy array.")

        norm = np.linalg.norm(value)
        if not np.isclose(norm, 1.0):
            normalized_vector = value / norm
            setattr(self, attribute.name, normalized_vector)

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
