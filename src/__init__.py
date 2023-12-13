import sys
from pathlib import Path

from loguru import logger


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
