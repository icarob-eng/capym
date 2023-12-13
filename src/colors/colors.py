from enum import Enum

from src.colors.color import Color


class Colors(Enum):
    red: Color = Color(255, 0, 0)
    green: Color = Color(0, 255, 0)
    blue: Color = Color(0, 0, 255)

    black: Color = Color(0, 0, 0)
    white: Color = Color(255, 255, 255)
