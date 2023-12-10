from enum import Enum

from color import Color


class Colors(Enum):
    red: Color = Color(255, 0, 0)
    green: Color = Color(0, 255, 0)
    blue: Color = Color(0, 0, 255)

    def __dict__(self):
        return {"value": self.value}
