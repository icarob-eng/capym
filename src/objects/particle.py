from src.objects.object import Object


class Particle(Object):

    def __init__(self, mass: float, position: tuple, velocity: tuple, color, name: str):
        super().__init__(mass, position, velocity)
        self.__name = name
        self.__color = color

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def color(self):
        return self.__color
