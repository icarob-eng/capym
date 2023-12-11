import sys

from pathlib import Path

from loguru import logger

from objects import *

from plot import *

from main import *

from helpers.limits import Limits
from helpers.background_style_enum import BackgroundStyle

from colors.color import Color
from colors.colors import Colors


def configure_logging(output: object | Path = sys.stderr):
    if output == sys.stderr:
        logger.add(output, format="{time:YYYY-MM-DD at HH:mm:ss}")
    elif output.parent.exists():
        if output.exists():
            raise FileExistsError("The target file already exists.")
        else:
            logger.add(output, format="{time:YYYY-MM-DD at HH:mm:ss")
    else:
        raise NotADirectoryError("The target log file parent directory does not exists.")
