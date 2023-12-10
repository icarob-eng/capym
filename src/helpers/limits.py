class Limits:
    def __init__(self, x: tuple[float, float], y: tuple[float, float]):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> tuple[float, float]:
        return self.__x

    @property
    def y(self) -> tuple[float, float]:
        return self.__y
