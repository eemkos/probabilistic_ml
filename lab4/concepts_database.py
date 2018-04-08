import numpy as np
import math
from estimates_calculations import Concept

odd = lambda: Concept('odd', lambda x: x%2==1)
even = lambda: Concept('even', lambda x: x%2==0)

def _multiplies_of_N():
    concepts = []
    def checker_gen(v):
        return lambda x: x%v==0
    for i in range(3, 501):
        concepts.append(Concept('multiples_of_%d'%i, checker_gen(i)))
    return concepts

multiplies_of_N = lambda: _multiplies_of_N()
powers_of_2 = lambda: Concept('pow_of_2', lambda x: 2 ** int(math.log(x,2)) == x)

def gen_base_concepts():
    concepts = []
    o = odd()
    o.prior = 0.8
    concepts.append(o)
    e = even()
    e.prior = 0.8
    concepts.append(e)
    moN = multiplies_of_N()
    for m in moN:
        m.prior = 0.1
    concepts += moN
    po2 = powers_of_2()
    po2.prior = 0.6
    concepts.append(po2)
    return concepts
