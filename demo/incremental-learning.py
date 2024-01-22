from pywmi.sample import uniform
from pywmi import Domain
from pysmt.typing import REAL, BOOL
from pysmt.shortcuts import serialize
import random
from pywmi.smt_check import evaluate
from incal.violations.core import RandomViolationsStrategy
from incal.k_cnf_smt_learner import KCnfSmtLearner
from incal.parameter_free_learner import learn_bottom_up
import numpy as np

n = 10

# IN this problem we have two real variables (x and y) and one Boolean variable (a)
# Domain needs:
#   1) List with name of all variables
#   2) Type for each variable
#   3) Range for each REAL variable (extreme included)
domain = Domain(["x", "y", "a"], {"x": REAL, "y": REAL, "a": BOOL}, {"x": (0, 1), "y": (0, 1)})
#domain = Domain(["x"], {"x": REAL}, {"x": (0,10)})
# Generate data 
data = uniform(domain, n)

# The labels (aka the output) should be provided as a different list, where every value > 0 is true, 0 is false
# In this case I assume the first three data are positive sample, whereas the others are negative
labels = [1]*3+[0]*7

def learn_f(_data, _labels, _i, _k, _h):
    learner = KCnfSmtLearner(_k, _h, RandomViolationsStrategy(0), "mvn")
    initial_indices = set(range(len(_data)))
    return learner.learn(domain, _data, _labels, initial_indices)

###############################################################################################################################

#Learns a CNF(k, h) SMT formula phi using the learner encapsulated in init_learner such that
#    C(k, h) = w_k * k + w_h * h is minimal.
#    :param data: List of tuples of assignments and labels
#    :param labels: Array of labels
#    :param learn_f: Function called with data, k and h: learn_f(data, k, h)
#    :param w_k: The weight assigned to k
#    :param w_h: The weight assigned to h
#    :param init_k:  The minimal value for k
#    :param init_h:  The minimal value for h
#    :param max_k:   The maximal value for k
#    :param max_h:   The maximal value for h
#    :return: A tuple containing: 1) the CNF(k, h) formula phi with minimal complexity C(k, h); 2) k; and 3) h
#    NOTICE: result is again a 3-element tuple :/
result, k, h = learn_bottom_up(data, labels, learn_f, 1, 1, init_k=1, init_h=0, max_k=None, max_h=None)
print("Final CNF(k={}, h={})".format(k, h))
print(serialize(result[2]))

############################################################################################################################