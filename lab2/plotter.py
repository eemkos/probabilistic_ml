from matplotlib import pyplot as plt
from matplotlib import patches
import seaborn as sbn
import numpy as np


class MixturePlotter:
    
    MEAN_COLOR = 'k'
    MEAN_WIDTH = 2

    
    #STD_COLOR = '#ff00ff55'
    STD_COLOR = 'k'
    STD_WIDTH = 2
    STD_STYLE = '-'
    
    VAR_COLOR = '#00000099'
    VAR_WIDTH = 1
    VAR_STYLE = '--'
    
    @staticmethod
    def visualise_sample(mixture, visualise_mean=True, visualise_std=True, visualise_var=True, 
                         params_from_sample=True, figsize=(18,8)):
        plt.figure(figsize=figsize)
        for i in range(mixture.nb_gaussians):
            sample = mixture.samples[i]
            if params_from_sample:
                m, v, s = sample.mean(), sample.var(), sample.std()
            else:
                m, v, s = mixture.means[i], mixture.vars[i], mixture.stds[i]

            p = plt.scatter(range(len(sample)), sample, s=0.05)
            color = p.get_facecolor()[0]
            x = (i+1) / (mixture.nb_gaussians+1) * len(sample)
            
            if visualise_mean:
                plt.plot([-.025*len(sample), len(sample)], [m]*2, 
                         c=color, linewidth=MixturePlotter.MEAN_WIDTH)
            

            
            if visualise_std:
                std_plot = patches.ConnectionPatch((x, m-s), (x, m+s), 'data', 'data', 
                                                   arrowstyle="|-|,widthA=1, widthB=1",
                                                   linestyle=MixturePlotter.STD_STYLE,
                                                   lw=MixturePlotter.STD_WIDTH, 
                                                   color=color)
                p.axes.add_patch(std_plot)
            
            if visualise_var:
                ylim = p.axes.get_ylim()
                ylim = (min(ylim[0],m-v), max(ylim[1],m+v))
                p.axes.set_ylim(ylim[0], ylim[1])
                var_plot = patches.ConnectionPatch((x, m-v), (x, m+v), 'data', 'data', 
                                                   arrowstyle="|-|,widthA=1, widthB=1",
                                                   linestyle=MixturePlotter.VAR_STYLE,
                                                   lw=MixturePlotter.VAR_WIDTH, 
                                                   color=MixturePlotter.VAR_COLOR)
                p.axes.add_patch(var_plot)
    
    @staticmethod
    def visualise_pmf(mixture, visualise_mean=True, visualise_std=True, visualise_var=True, 
                      params_from_sample=True, figsize=(18,8)):

        plt.figure(figsize=figsize)
        plt.xlabel('Random Variable value', size=20)
        plt.ylabel('Probability', size=20)
        
        max_max_value=0
        
        for i in range(mixture.nb_gaussians):
            sample = mixture.samples[i]
            if params_from_sample:
                m, v, s = sample.mean(), sample.var(), sample.std()
            else:
                m, v, s = mixture.means[i], mixture.vars[i], mixture.stds[i]

            ax = sbn.distplot(sample)
            
            line = ax.get_lines()[-1]
            line_x_discr = [int(i) for i in line.get_xdata()]
            max_max_value = max(max_max_value, line.get_ydata().max())
            ax.set_ylim(0, 1.2*max_max_value)

            ind, l = None, 0
            while ind not in line_x_discr:
                ind = int(m-s+l)
                l-=1
                
            h = line.get_ydata()[line_x_discr.index(ind)]
            
            if visualise_mean:
                mean_plot = plt.plot([mixture.means[i]]*2, [0, line.get_ydata().max()], 
                                     c=MixturePlotter.MEAN_COLOR, 
                                     linewidth=MixturePlotter.MEAN_WIDTH)
                
            if visualise_var:
                var_plot = patches.ConnectionPatch((m-v, h), (m+v, h), 'data', 'data', 
                                                   arrowstyle="|-|,widthA=1, widthB=1",
                                                   linestyle=MixturePlotter.VAR_STYLE,
                                                   lw=MixturePlotter.VAR_WIDTH,
                                                   color=line.get_color())
                ax.add_patch(var_plot)
            
            if visualise_std:
                std_plot = patches.ConnectionPatch((m-s, h), (m+s, h), 'data', 'data', 
                                                   arrowstyle="|-|,widthA=1, widthB=1",
                                                   linestyle=MixturePlotter.STD_STYLE,
                                                   lw=MixturePlotter.STD_WIDTH, 
                                                   color=MixturePlotter.STD_COLOR)
                ax.add_patch(std_plot)
            
        sample = np.concatenate(mixture.samples)
        sbn.distplot(sample, hist=False, label='Mixture distribution')
        plt.legend(loc='right', fontsize=15)