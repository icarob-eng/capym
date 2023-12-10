from enum import Enum


class BackgroundStyle(Enum):
    DARK = 'dark_background'
    LIGHT = 'light_background'

    def __dict__(self):
        return {'value': self.value}
