from attrs import define, field

from src.plot.displayable import Displayable


@define
class Particle(Displayable):
    name: str = field(init=True)

    def draw(self):
        pass
