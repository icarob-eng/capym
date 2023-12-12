from abc import ABC

from numpy import array
from matplotlib.patches import Circle as matplotCircle

from src.objects.object import Object
from src.plot.displayable import Displayable
from src.colors.color import Color
from attrs import define


@define
class Circle(Object, Displayable, matplotCircle):

    def draw(self):
        pass
