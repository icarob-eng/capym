import uuid

from fontTools.varLib.errors import UnsupportedFormat
from matplotlib import pyplot as plt
from attrs import define, field
from matplotlib.animation import FuncAnimation, writers
from pathlib import Path
from loguru import logger

from src.plot.plot import Plot
from src.main.simulation import Simulation
from src.objects.object import Object


@define(slots=False)
class SimulationPlot(Simulation, Plot):
    follow: uuid = field(default=uuid.uuid4(), init=False)
    title: str = field(default="", init=True)

    @property
    def simulation_duration(self):
        return self.final_instant - self.initial_instant

    def __animate_frame(self, moment: float) -> None:
        plt.cla()
        plt.axis('scaled')

        if self.follow is None or self.follow not in [element.uuid for element in self.objects]:
            plt.xlim(self.limits.x)
            plt.ylim(self.limits.y)
        else:

            obj: Object = filter(lambda element: element.uuid == self.follow, self.objects)

            plt.xlim(self.limits.x + obj.position)
            plt.ylim(self.limits.y + obj.position)

        x_coordinates = [element.position[0] for element in self.snapshots[moment]]
        y_coordinates = [element.position[1] for element in self.snapshots[moment]]
        plt.scatter(x_coordinates, y_coordinates)
        plt.title(self.title)

    @logger.catch
    def animate(self, save_as: Path = None) -> None:
        animation = FuncAnimation(plt.gcf(), self.__animate_frame, frames=self.moments, interval=self.step)

        if save_as is not None:
            if save_as.suffix.split('.')[1] in self.supported_formats:

                fps = self.number_of_snapshots
                if fps > 30:
                    fps = 30

                ffmpeg = writers['ffmpeg']
                writer = ffmpeg(fps=fps)
                animation.save(save_as, writer)
                logger.info(f"Saved on {save_as}")

            else:
                raise UnsupportedFormat(f"Unsupported format.")

        logger.info(f"Display {self.title}...")
        plt.show()
