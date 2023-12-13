from attrs import define, field

from src.helpers.background_style_enum import BackgroundStyle
from src.helpers.limits import Limits


@define(frozen=True, slots=False)
class Plot(object):
    style: BackgroundStyle = field(init=True)
    limits: Limits = field(init=True)
    speed: float = field(init=True)
    supported_formats = field(
        default=('3g2', '3pg', 'amv', 'asf', 'avi', 'dirac', 'drc', 'flv', 'gif', 'm4v', 'mp2', 'mp3', 'mp4',
                 'mjpeg', 'mpeg', 'mpegets', 'mov', 'mkv', 'mxf', 'mxf_d10', 'mxf_opatom', 'nsv', 'null', 'ogg',
                 'ogv', 'rm', 'roq', 'vob', 'webm'), init=False)
