from attrs import define

from src.objects.object import Object
from src.plot.displayable import Displayable


@define
class Particle(Object, Displayable):
    name: str

    def draw(self):
        pass
