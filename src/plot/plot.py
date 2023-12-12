import attrs.setters
from attrs import define, field

from src.helpers.background_style_enum import BackgroundStyle
from src.helpers.limits import Limits


@define(frozen=True)
class Plot(object):
    style: BackgroundStyle
    limits: Limits
    speed: float
