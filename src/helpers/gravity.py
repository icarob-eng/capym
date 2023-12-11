import numpy

from numpy import array

from src.objects.object import Object


def gravity(from_this: Object, to_this: Object, gravitational_constant: float) -> array:
    difference_between_position_vectors = from_this.position - to_this.position

    return ((gravitational_constant * from_this.mass * to_this.mass) / (difference_between_position_vectors ** 2)) * (
            difference_between_position_vectors / (numpy.linalg.norm(difference_between_position_vectors)))
