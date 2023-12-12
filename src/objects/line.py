from electrical_object import ElectricalObject


class Line(ElectricalObject):
    def __int__(self,
                mass: float,
                position: tuple,
                direction: tuple,
                electric_charge: float = 0):
        super().__init__(mass, position, (0, 0), electric_charge)
        