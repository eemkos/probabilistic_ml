from matplotlib import pyplot as plt
from matplotlib import animation
from IPython.display import HTML
import numpy as np


class AnimatedScatter():
    """An animated scatter plot using matplotlib.animations.FuncAnimation.
    source: https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
    
    customized.
    """
    def __init__(self, possible_values, rand_generator):
        self.possible_values = possible_values
        self.data_generator = rand_generator

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, 
                                           init_func=self.setup_plot,
                                           frames = 100,
                                           interval=40, 
                                           blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        #x, y, s, c = self.stream()
        self.scat = self.ax.scatter([], [], animated=True)
        self.ax.axis([min(self.possible_values), 
                      max(self.possible_values), 
                      0, 1])

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def update(self, i):
        """Update the scatter plot."""
        for _ in range(100):
            self.data_generator()
        
        # Set x and y data...
        #self.scat.set_offsets(data[:2, :].T))
        fun = lambda arg: 1.*self.data_generator.values_with_counts[arg] / self.data_generator.calls_counter
        y = [fun(a) for a in self.possible_values]
        self.scat.set_offsets(np.asarray([self.possible_values, y]).T)
        self.ax.set_ylim((0, round((max(y) + 0.05) * 50) / 50))
        return self.scat,

    def show(self):
        plt.show()
        
    def __call__(self):
        return HTML(self.ani.to_jshtml())