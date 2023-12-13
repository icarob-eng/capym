import random
from attrs import define, field


@define(frozen=True)
class Color(object):

    red: int = field()
    green: int = field()
    blue: int = field()

    @staticmethod
    def random() -> 'Color':

        begin = 0
        end = 255

        red = random.randint(begin, end)
        green = random.randint(begin, end)
        blue = random.randint(begin, end)

        return Color(red, green, blue)
