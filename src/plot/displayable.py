from abc import ABC, abstractmethod

import attr.setters
from loguru import logger
from attrs import field, define

from src.colors.color import Color


@define
class Displayable(ABC):

    color: Color = field(on_setattr=attr.setters.frozen)

    @logger.catch
    @abstractmethod
    def draw(self):
        raise NotImplementedError("The draw method is not implemented.")
