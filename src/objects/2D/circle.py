from abc import ABC

from numpy import array
from matplotlib.patches import Circle as matplotCircle

from src.objects.object import Object
from src.plot.displayable import Displayable
from src.colors.color import Color


class Circle(Object, Displayable, ABC, matplotCircle):

    def __init__(self, center: array, radius: float, mass: float, position: tuple, velocity: tuple, color: Color):
        super().__init__(mass, position, velocity)
        Displayable.__init__(self, color)
        matplotCircle.__init__(self, center, radius)
