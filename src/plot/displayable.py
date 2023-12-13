from abc import ABC, abstractmethod

from attrs import define
from loguru import logger

from src.colors.color import Color


@define(slots=False)
class Displayable(ABC):

    color: Color

    @logger.catch
    @abstractmethod
    def draw(self):
        raise NotImplementedError("The draw method is not implemented.")
