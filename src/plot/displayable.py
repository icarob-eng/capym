from src.colors.color import Color


class Displayable:

    def __init__(self, color: Color):
        self.__color = color

    @property
    def color(self) -> Color:
        return self.__color
