import sys
import uuid

import numpy.dtypes

from matplotlib import pyplot as plt

from matplotlib.animation import FuncAnimation, writers
from numpy import array
from pathlib import Path


from src.helpers.background_style_enum import BackgroundStyle
from src.plot.plot import Plot
from src.helpers.limits import Limits
from src.main.simulation import Simulation
from src.objects.object import Object


class SimulationPlot(Plot, Simulation):
    def __init__(self,
                 style: BackgroundStyle,
                 limits: Limits,
                 follow: uuid,
                 final_instant: float,
                 objects: array(dtype=numpy.dtypes.ObjectDType),
                 initial_instant: float = 0.0,
                 interval: float = 0.1,
                 speed: float = 1.0,
                 gravitational_constant: float = 6.6708e-11
                 ):
        super().__init__(style, limits, speed)
        Simulation.__init__(
            self=self,
            interval=interval,
            initial_instant=initial_instant,
            final_instant=final_instant,
            objects=objects,
            gravitational_constant=gravitational_constant
        )
        self.__follow = follow

    @property
    def follow(self) -> uuid:
        return self.__follow

    @property
    def simulation_duration(self):
        return self.final_instant-self.initial_instant

    def __animate_frame(self) -> None:
        plt.cla()
        plt.axis('scaled')

        if self.__follow is None or self.__follow in [element.uuid for element in self.objects]:
            plt.xlim(self.limits.x)
            plt.ylim(self.limits.y)
        else:

            obj: Object = filter(lambda element: element.uuid == self.follow, self.objects)

            plt.xlim(self.limits.x + obj.position)
            plt.ylim(self.limits.y + obj.position)
