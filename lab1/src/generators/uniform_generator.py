import numpy as np
from functools import partial
from .base_generator import DiscreteRandomGenerator


class UniformRandomGenerator(DiscreteRandomGenerator):

    def __init__(self, min_value=0, max_value=100):
        super(self.__class__, self).__init__(partial(np.random.randint,
                                                     low=min_value,
                                                     high=max_value + 1))

        self.generator = self._generate_random()

    def _generate_random(self):
        while True:
            value = self.generating_method()
            self.values_with_counts[value] += 1
            yield value
