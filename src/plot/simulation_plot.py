import uuid
from pathlib import Path

from attrs import define, field
from fontTools.varLib.errors import UnsupportedFormat
from loguru import logger
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from numpy import array, ndarray

from src.main.simulation import Simulation
# from src.objects.object import Object
from src.objects.particle import Particle
from src.plot.plot import Plot


@define
class SimulationPlot(Simulation, Plot):
    objects: ndarray[Particle] = field(factory=ndarray, init=True)
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
            obj = next((element for element in self.objects if element.uuid == self.follow), None)

            if obj is not None:
                plt.xlim(self.limits.x + obj.position[0])
                plt.ylim(self.limits.y + obj.position[1])

        # x_coordinates = [element.position[0] for element in self.snapshots[moment]]
        # y_coordinates = [element.position[1] for element in self.snapshots[moment]]
        # colors = [element.color for element in self.objects]

        for obj in self.snapshots[moment]:
            plt.scatter(obj.position[0], obj.position[1], label=obj.name, color=obj.color.to_mathplot_color, marker='o')
            plt.title(self.title)

    @logger.catch
    def animate(self, save_as: Path = None) -> None:
        animation = FuncAnimation(plt.gcf(), self.__animate_frame, frames=self.moments, interval=self.step)

        if save_as is not None:
            if save_as.suffix.split('.')[1] in self.supported_formats:

                fps = min(self.number_of_snapshots, 30)

                ffmpeg = writers['ffmpeg']
                writer = ffmpeg(fps=fps)
                try:
                    animation.save(save_as, writer)
                    logger.info(f"Saved on {save_as}")
                except Exception as e:
                    logger.error(f"Error saving animation: {e}")

            else:
                raise UnsupportedFormat(f"Unsupported format.")

        logger.info(f"Display {self.title}...")
        plt.show()
