# INCAL
INCAL is an incremental SMT constraint learner

## Installation

To install the package locally, it is sufficient to run the following command in the main directory

```
pip install -e .
```

Make sure to use Python3.

## How to use

The **demo** directory contains 3 files to easily understand the basics of INCAL:

- *fixed-learning-alldata*: Given fixed values of clauses *k* and half-spaces *h*, learn a CNF(k,h) formula with all given data
- *fixed-learning-partial*: Given fixed values of clauses *k* and half-spaces *h*, learn a CNF(k,h) formula using only a partition of the entire set of data  
- *incremental-learning.py*: Try to incrementally fit the data into a CNF(k,h), increasing k and h step-by-step until a solution is found.
