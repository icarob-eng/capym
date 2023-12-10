import random

class Color(object):

    __begin = 0
    __end = 255

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.__red: int = red
        self.__green: int = green
        self.__blue: int = blue

    def __str__(self):
        return f"Color(Red: {self.__red}, Green: {self.__green}, Blue: {self.__blue})"

    def __eq__(self, other):
        if isinstance(type(other), Color) or issubclass(type(other), Color):
            return self.__red == other.red and self.__green == other.green and self.__blue == other.blue
        return False

    def __dict__(self) -> dict:
        return {"red": self.__red, "green": self.__green, "blue": self.__blue}

    def __float__(self) -> tuple[float, float, float]:
        return self.__red / 255, self.__green / 255, self.__blue / 255

    @staticmethod
    def random() -> 'Color':

        red = random.randint(Color.__begin, Color.__end)
        green = random.randint(Color.__begin, Color.__end)
        blue = random.randint(Color.__begin, Color.__end)

        return Color(red, green, blue)

    @property
    def red(self) -> float:
        return self.__red

    @property
    def green(self) -> float:
        return self.__green

    @property
    def blue(self) -> float:
        return self.__blue
