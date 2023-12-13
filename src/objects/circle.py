from attrs import define
from matplotlib.patches import Circle as matplotCircle

from src.objects.object import Object
from src.plot.displayable import Displayable


@define
class Circle(Displayable, matplotCircle):
    pass
