import uuid

from src.objects.object import Object
from src.config.background_style_config import BackgroundStyle


class SimulationConfig(object):
    def __init__(self, interval: float, objects: list[Object],
                 background_config: BackgroundStyle, final_moment: float, limits: tuple[tuple, tuple],
                 follow: uuid = None, speed: float = None,
                 initial_moment: float = 0.0,
                 constant_of_gravitation: float = 6.6708e-11):
        self.__background_config = background_config
        self.__interval = interval
        self.__objects = objects
        self.__initial_moment = initial_moment
        self.__final_moment = final_moment
        self.__constant_of_gravitation = constant_of_gravitation
        self.__limits = limits
        if speed > 0.0:
            self.__speed = speed
        else:
            raise ValueError("Speed must be not 0")

        if follow in [obj.uuid for obj in objects] or follow is None:
            self.__follow = follow
        else:
            raise ValueError("The object's uuid must beá in the object list.")

    @property
    def interval(self) -> float:
        return self.__interval

    @property
    def objects(self) -> list[Object]:
        return self.__objects

    @property
    def initial_moment(self) -> float:
        return self.__initial_moment

    @property
    def background_config(self) -> BackgroundStyle:
        return self.__background_config

    @property
    def constant_of_gravitation(self) -> float:
        return self.__constant_of_gravitation

    @property
    def final_moment(self) -> float:
        return self.__final_moment

    @property
    def limits(self) -> tuple[tuple, tuple]:
        return self.__limits

    @property
    def follow(self) -> uuid:
        return self.__follow
