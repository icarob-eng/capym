from uuid import UUID

import numpy
import json

from numpy import ndarray, dtype
import uuid


class Object(object):

    def __init__(self, mass: float, position: tuple, velocity: tuple, acceleration: tuple = (0, 0)):
        self.__uuid = uuid.uuid4()
        self.__mass = mass
        self.__position = numpy.array(position)
        self.__velocity = numpy.array(velocity)
        self.__acceleration = numpy.array(acceleration)

    def __dict__(self) -> dict:
        return {
            'uuid': self.__uuid,
            'mass': self.__mass,
            'position': self.__position.tolist(),
            'velocity': self.__velocity.tolist(),
            'acceleration': self.__acceleration.tolist()
        }

    def __str__(self):
        return json.dumps(self.__dict__())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__) or issubclass(other, self.__class__):
            return self.__mass == other.mass and self.__position == other.position and self.__velocity == other.velocity and self.__acceleration == other
        else:
            return False

    @property
    def uuid(self) -> UUID:
        return self.__uuid

    @property
    def mass(self) -> float:
        return self.__mass

    @mass.setter
    def mass(self, mass: float):
        if mass >= 0:
            self.__mass = mass
        else:
            raise Exception('The mass of a body cannot be negative.')

    @property
    def position(self) -> ndarray:
        return self.__position

    @position.setter
    def position(self, position: tuple):
        self.__position = numpy.array(position)

    @position.setter
    def position(self, position: ndarray):
        self.__position = numpy.array(position)

    @property
    def velocity(self) -> ndarray:
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: tuple):
        self.__velocity = numpy.array(velocity)

    @velocity.setter
    def velocity(self, velocity: ndarray):
        self.__velocity = velocity

    @property
    def acceleration(self) -> ndarray:
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration: tuple):
        self.__acceleration = numpy.array(acceleration)

    @acceleration.setter
    def acceleration(self, acceleration: ndarray):
        self.__acceleration = acceleration

    def gravitational_acceleration(self, to, constant_of_gravitation: float) -> ndarray:
        if isinstance(to, self.__class__) or issubclass(to, self.__class__):
            distance_vector = to.position - self.position
            return ((
                            (constant_of_gravitation * to.mass) /
                            numpy.linalg.norm(distance_vector)
                    )
                    *
                    (
                            distance_vector /
                            numpy.linalg.norm(distance_vector)
                    ))
        else:
            raise Exception('The to argument must be a Object.')
