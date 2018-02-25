from matplotlib import pyplot as plt
from matplotlib import animation
from IPython.display import HTML
import numpy as np
import seaborn as sns

class AnimatedHeatmap():
    """An animated heatmap using matplotlib.animations.FuncAnimation.
    source: https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
    customized.
    """
    def __init__(self, possible_values, rand_generator, 
                 frames=100, interval=40, step_samples=1000,
                 figsize=(8,8)):
        self.possible_values = possible_values
        self.min_value = min(possible_values)
        self.data = np.zeros((len(possible_values),
                              len(possible_values)))
        self.step_samples=step_samples
        self.data_generator = rand_generator
        self.last_drawn = self.data_generator()

        self.fig=plt.figure(figsize=figsize)
        self.ani = animation.FuncAnimation(self.fig, self.update,
                                           init_func=plt.clf,
                                           frames=frames,
                                           interval=interval)
        
    def update(self, i):
        plt.clf()
        for _ in range(self.step_samples):
            current_drawn = self.data_generator()
            self.data[self.last_drawn-self.min_value, current_drawn-self.min_value]+=1
            self.last_drawn = current_drawn

        hmn, hmx = self.data.min(), self.data.max()
        sns.heatmap((self.data - hmn) / (hmx-hmn), 
                    square=True, animated=True)

        
    def __call__(self):
        return HTML(self.ani.to_jshtml())