
import numpy
import uuid
import json

from numpy import array
from uuid import UUID


class Object(object):

    def __init__(self, mass: float, position: tuple, velocity: tuple, acceleration: tuple = (0, 0)):
        super().__init__()
        self.__uuid = uuid.uuid4()
        self.__mass = mass
        self.__position = array(position, dtype=numpy.float32)
        self.__velocity = array(velocity, dtype=numpy.float32)
        self.__acceleration = array(acceleration, dtype=numpy.float32)

    def __dict__(self) -> dict:
        return {
            'uuid': self.__uuid.hex,
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
    def position(self) -> array:
        return self.__position

    @position.setter
    def position(self, position: tuple):
        self.__position = numpy.array(position)

    @position.setter
    def position(self, position: numpy.array):
        self.__position = position

    @property
    def velocity(self) -> numpy.array:
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: tuple):
        self.__velocity = numpy.array(velocity)

    @velocity.setter
    def velocity(self, velocity: array):
        self.__velocity = velocity

    @property
    def acceleration(self) -> array:
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration: tuple):
        self.__acceleration = numpy.array(acceleration)

    @acceleration.setter
    def acceleration(self, acceleration: array):
        self.__acceleration = acceleration

    def gravitational_acceleration(self, to, constant_of_gravitation: float) -> array:
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
