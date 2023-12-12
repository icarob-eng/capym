import uuid

from matplotlib import pyplot as plt
from attrs import define, field

from src.plot.plot import Plot
from src.main.simulation import Simulation
from src.objects.object import Object


@define
class SimulationPlot(Plot, Simulation):
    follow: uuid = field(default=uuid.uuid4(), init=False)

    @property
    def simulation_duration(self):
        return self.final_instant - self.initial_instant

    def __animate_frame(self) -> None:
        plt.cla()
        plt.axis('scaled')

        if self.follow is None or self.follow in [element.uuid for element in self.objects]:
            plt.xlim(self.limits.x)
            plt.ylim(self.limits.y)
        else:

            obj: Object = filter(lambda element: element.uuid == self.follow, self.objects)

            plt.xlim(self.limits.x + obj.position)
            plt.ylim(self.limits.y + obj.position)
