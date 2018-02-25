from .base_generator import DiscreteRandomGenerator


class LinearCongruentialGenerator(DiscreteRandomGenerator):

    def __init__(self, min_value=0, max_value=100):
        super(self.__class__, self).__init__(self._lc_generate, min_value, max_value)
        self.a = 16634525
        self.b = 1013904223
        self.m = 2 ** 32
        self.mod_max = (self.max_value - self.min_value) + 1
        self.last_generated = 33

        self.generator = self._generate_random()

    def _lc_generate(self):
        value = (self.a * self.last_generated + self.b) % self.m
        self.last_generated = value
        value = value % self.mod_max
        value += self.min_value

        return value

    def _generate_random(self):
        while True:
            value = self.generating_method()
            self.values_with_counts[value] += 1
            yield value
