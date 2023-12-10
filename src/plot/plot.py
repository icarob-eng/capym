from src.helpers.background_style_enum import BackgroundStyle
from src.helpers.limits import Limits


class Plot(object):
    def __init__(self, style: BackgroundStyle, limits: Limits, speed: float = 1.0):
        self.__style = style
        self.__limits = limits
        self.__speed = speed

    def __str__(self):
        return f"Plotter(style={self.__style}, limits={self.__limits}, speed={self.__speed})"

    def __dict__(self) -> dict:
        return {
            'style': self.__style.value,
            'limits': self.__limits,
            'speed': self.__speed
        }

    @property
    def style(self) -> BackgroundStyle:
        return self.__style

    @property
    def limits(self) -> Limits:
        return self.__limits

    @property
    def speed(self) -> float:
        return self.__speed
