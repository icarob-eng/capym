from attrs import define

from src.colors.color import Color
from src.objects.object import Object


@define(slots=False)
class Displayable(Object):
    color: Color
