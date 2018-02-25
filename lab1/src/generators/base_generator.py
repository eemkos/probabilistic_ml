import numpy as np


class DiscreteRandomGenerator(object):

    def __init__(self, generating_method=np.random.randint, min_value=0, max_value=100):
        self.generating_method = generating_method
        self.min_value = min_value
        self.max_value = max_value
        self.values_with_counts = {val: 0 for val in range(min_value, max_value + 1)}
        self.calls_counter = 0
        self.generator = self._generate_random()

    def _generate_random(self):
        raise NotImplementedError

    def __call__(self):
        self.calls_counter += 1
        return next(self.generator)
