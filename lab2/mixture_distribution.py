import numpy as np


class CombinedGaussians:
    
    def __init__(self, nb_gaussians, sample_size, 
                 lower_bound=0, upper_bound=250, params=None):
        
        self.nb_gaussians = nb_gaussians
        self.sample_size = sample_size
        self.lower_b = lower_bound
        self.upper_b = upper_bound
        
        if params == None or len(params[0]) != len(params[1]) or len(params[0]) != nb_gaussians:
            self.means = np.random.uniform(lower_bound, upper_bound, nb_gaussians)
            self.vars = np.random.uniform(0, (upper_bound-lower_bound)*2, nb_gaussians)
            self.stds = np.sqrt(self.vars)
        else:
            self.means = np.asarray(params[0])
            self.vars = np.asarray(params[1])
            self.stds = np.sqrt(self.vars)
        
        self._create_sample()
        
        
    def _create_sample(self):
        sample_parts = []
        left_to_sample = self.sample_size
        sample_part_size = int(self.sample_size/self.nb_gaussians)
        for i in range(self.nb_gaussians-1):
            part = np.random.normal(self.means[i], self.stds[i], sample_part_size)
            part = np.asarray([int(x) for x in part])
            left_to_sample -= sample_part_size
            sample_parts.append(part)
            
        last_part = np.random.normal(self.means[-1], self.stds[-1], left_to_sample)
        sample_parts.append(last_part)
        self.samples = sample_parts