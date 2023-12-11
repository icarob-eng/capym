from abc import ABC, abstractmethod
from loguru import logger

from src.colors.color import Color


class Displayable(ABC):

    def __init__(self, color: Color):
        self.__color = color

    @property
    def color(self) -> Color:
        return self.__color

    @logger.catch
    @abstractmethod
    def draw(self):
        raise NotImplementedError("The draw method is not implemented.")
