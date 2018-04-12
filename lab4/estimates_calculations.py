import numpy as np
from collections import OrderedDict
import math


class Concept:
    
    NUM_RANGE = list(range(1,501))#{'min':1, 'max':500}
    
    def __init__(self, name, checker, prior=1, size=None):
        self.name = name
        self.checker = checker
        self.prior = prior
        if size is None:
            self.size = len(self.gen_dataset())
        else:
            self.size = size
            
    def gen_dataset(self):
        return [x for x in Concept.NUM_RANGE if self.checker(x)]
            
    @staticmethod
    def normalize_priors(concepts):
        sum_of_priors = sum([c.prior for c in concepts])
        for c in concepts:
            c.prior /= sum_of_priors
            
    def __str__(self):
        return 'Name: {:20s}\tPrior: {:.2f},\tSize: {:d}'.format(self.name+',', 
                                                              self.prior, 
                                                              self.size)
    

def likelihood(data, hypothesis):
    if all([hypothesis.checker(x) for x in data]):
        return (1/hypothesis.size)**len(data)
    else:
        return 0
    
    
def posteriors(data, hypotheses):
    denominator = 0
    numerators = dict()
    for h in hypotheses:
        numerators[h.name] = likelihood(data, h) * h.prior
        denominator += numerators[h.name]
        
    for k in numerators:
        numerators[k] /= denominator
        
    return numerators


def MAP(data, concepts):
    log_posteriori = np.asarray([aposteriori_estimation(data, c) for c in concepts])
    return concepts[np.argmax(log_posteriori)]

def aposteriori_estimation(data, c):
    eps=1e-9
    lik = likelihood(data, c)
    if lik == 0:
        return -np.inf
    return np.log(+eps)+np.log(c.prior+eps) 

def MAP_value(data, concepts):
    log_posteriori = np.asarray([aposteriori_estimation(data, c) for c in concepts])
    return np.max(log_posteriori)

def MAP_arg(data, concepts):
    log_posteriori = np.asarray([aposteriori_estimation(data, c) for c in concepts])
    return np.argmax(log_posteriori)



def MLE(data, concepts):
    log_likelihood = np.asarray([likelihood_estimation(data, c) for c in concepts])
    return concepts[np.argmax(log_likelihood)]

def likelihood_estimation(data, c):
    eps = 1e-9
    lik = likelihood(data, c)
    if lik == 0:
        return -np.inf
    return np.log(likelihood(data, c)+eps)

def MLE_value(data, concepts):
    log_likelihood = np.asarray([likelihood_estimation(data, c) for c in concepts])
    return np.max(log_likelihood)

def MLE_arg(data, concepts):
    log_likelihood = np.asarray([likelihood_estimation(data, c) for c in concepts])
    return np.argmax(log_likelihood)
