from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import animation
from IPython.display import HTML
import numpy as np


class AnimatedDistplot():
    """An animated distplot using matplotlib.animations.FuncAnimation.
    source: https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
    customized.
    """
    def __init__(self, possible_values, rand_generator, figsize=(8,6), frames=50, draws_per_frame=100):
        self.possible_values = possible_values
        self.data_generator = rand_generator
        self.draws_per_frame = draws_per_frame
        self.data = []
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ani = animation.FuncAnimation(self.fig, self.update, 
                                           init_func=plt.clf,
                                           frames=frames,
                                           interval=50)

    def update(self, i):
        """Update the distplot."""
        plt.cla()
        for _ in range(self.draws_per_frame):
            self.data.append(self.data_generator())
        self.dist = sns.distplot(np.asarray(self.data), bins=len(self.possible_values))

    def show(self):
        plt.show()
        
    def __call__(self):
        return HTML(self.ani.to_jshtml())