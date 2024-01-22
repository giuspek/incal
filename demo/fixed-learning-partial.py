from pywmi.sample import uniform
from pywmi import Domain
from pysmt.typing import REAL, BOOL
from pysmt.shortcuts import serialize, Solver
import random
from pywmi.smt_check import evaluate
from incal.violations.core import RandomViolationsStrategy
from incal.k_cnf_smt_learner import KCnfSmtLearner
from incal.incremental_learner import IncrementalLearner
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
print(labels)
print(data)

# In alternative, you can create your list of data as numpy arrays, where the bool are simply treated as 0/1 for false/true respectively

###############################################################################################################################

# TEST2: fixed k,h Learning, only part of the data

# KCnfSmtLearner(k,h,s1,s2)
# k: number of clauses
# h: number of half-spaces
# s1: Strategy to select samples (AllViolationsStrategy, RandomViolationsStrategy, WeightedRandomViolationsStrategy,MaxViolationsStrategy)
# s2: string containing what symmetries to enable 
#   - h: horizontal symmetries
#   - v: vertical symmetries
#   - m: Mutually exclusive
#   - n: Normalized
learner = KCnfSmtLearner(3, 3, RandomViolationsStrategy(n), "hvmn")

# Then you call the learn_artial function to learn the SMT formula, and print it
# Notice that you must all give the function the solver, using PySMT, and a set of indexes to get the partition of data to learn
# In this case I want to learn only the first 4 random generated data
# PS: the output of learn_partial is the single formula :/
solver = Solver()
learned_theory = learner.learn_partial(solver, domain, data, labels, set([0,1,2,3]))
print("Output formula:")
print(serialize(learned_theory))

############################################################################################################################