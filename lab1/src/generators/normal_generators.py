import numpy as np
from functools import partial
from .base_generator import DiscreteRandomGenerator


class NormalHardClippingGenerator(DiscreteRandomGenerator):

    def __init__(self, min_value=0, max_value=100, mean=0.5, std=0.1):
        super(self.__class__, self).__init__(partial(np.random.normal, loc=mean, scale=std),
                                             min_value, max_value)
        self.mean = mean
        self.std = std

    def _generate_random(self):
        while True:
            value = self.generating_method()
            # clipping
            value = 0 if value < 0 else value
            value = 1 if value > 1 else value
            # normalising to range [min_value;max_value]
            value *= (self.max_value - self.min_value)
            value += self.min_value
            value = int(value)
            self.values_with_counts[value] += 1.
            yield value


class NormalGentleClippingGenerator(DiscreteRandomGenerator):

    def __init__(self, min_value=0, max_value=100,
                 mean=0.5, std=0.1, sample_size=1000):
        super(self.__class__, self).__init__(partial(np.random.normal,
                                                     loc=0., scale=std,
                                                     size=sample_size),
                                             min_value, max_value)
        self.mean = mean
        self.std = std
        # temp_gen_sample helps to normalise sampled values into [0;1] range
        # on a bigger population in order to avoid hard clipping
        # which distorts the distribution
        self.temp_gen_sample = []

    def _generate_random(self):
        while True:
            if len(self.temp_gen_sample) == 0:
                self._sample_new_temp()
            value = self.temp_gen_sample.pop()
            value *= (self.max_value - self.min_value)
            value += self.min_value
            value = int(value)
            self.values_with_counts[value] += 1.
            yield value

    def _sample_new_temp(self):
        sample = self.generating_method()
        # generate and normalise to [min_value;max_value] range
        mx = sample.max()
        mn = sample.min()
        if np.abs(mn) < np.abs(mx):
            clip = np.abs(mn)
        else:
            clip = np.abs(mx)
        sample = sample.clip(-clip, clip)
        sample += self.mean
        if clip + self.mean > 1 or self.mean - clip < 0:
            sample -= (self.mean - clip)
            sample /= (2 * clip)
        self.temp_gen_sample = list(sample)


class NormalRejectionGenerator(DiscreteRandomGenerator):

    def __init__(self, min_value=0, max_value=100, mean=0.5, std=0.1):
        super(self.__class__, self).__init__(partial(np.random.normal, loc=mean, scale=std),
                                             min_value, max_value)
        self.mean = mean
        self.std = std

    def _generate_random(self):
        while True:
            value = self.min_value -1
            # rejection condition
            while value < self.min_value or value > self.max_value:
                value = self.generating_method()
                value *= (self.max_value - self.min_value)
                value += self.min_value
                value = int(value)
            self.values_with_counts[value] += 1.
            yield value