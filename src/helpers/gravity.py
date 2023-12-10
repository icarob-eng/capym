import numpy

from numpy import array

from src.objects.object import Object


def gravity(from_this: Object, to_this: Object, constant_of_gravitation: float) -> array:
    difference_between_position_vectors = from_this.position - to_this.position

    return ((constant_of_gravitation * from_this.mass * to_this.mass) / (difference_between_position_vectors ** 2)) * (
            difference_between_position_vectors / (numpy.linalg.norm(difference_between_position_vectors)))
