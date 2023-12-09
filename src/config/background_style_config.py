from enum import Enum


class BackgroundStyle(Enum):
    DARK = 'dark_background'
    LIGHT = 'light'

    def __dict__(self):
        return {'value': self.value}