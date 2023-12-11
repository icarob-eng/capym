from src.objects.electrical_object import ElectricalObject


class Particle(ElectricalObject):

    def __init__(self, mass: float, position: tuple, velocity: tuple, color, name: str, electrical_charge: float):
        super().__init__(mass, position, velocity)
        self.__name = name
        self.__color = color
        self.electric_charge = electrical_charge

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def color(self):
        return self.__color
