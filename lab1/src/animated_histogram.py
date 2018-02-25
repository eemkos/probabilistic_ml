from matplotlib import pyplot as plt
from matplotlib import animation
from IPython.display import HTML
import numpy as np


class AnimatedHistogram():
    """An animated histogram plot using matplotlib.animations.FuncAnimation.
    source: https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
    customized.
    """
    def __init__(self, possible_values, rand_generator, figsize=(8,6), frames=50, draws_per_frame=100, color='green'):
        self.possible_values = possible_values
        self.data_generator = rand_generator
        self.data = []
        self.color = color
        self.draws_per_frame = draws_per_frame

        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ani = animation.FuncAnimation(self.fig, self.update, 
                                           init_func=self.setup_plot,
                                           frames=frames,
                                           interval=40)

    def setup_plot(self):
        """Initial drawing of the histogram plot."""
        self.hist = plt.hist(self.data, bins=len(self.possible_values), color=self.color)
        plt.clf()

    def update(self, i):
        """Update the histogram plot."""
        plt.cla()
        for _ in range(self.draws_per_frame):
            self.data.append(self.data_generator())

        self.hist = plt.hist(np.asarray(self.data), density=True,
                                 bins=len(self.possible_values), color=self.color)

    def show(self):
        plt.show()
        
    def __call__(self):
        return HTML(self.ani.to_jshtml())