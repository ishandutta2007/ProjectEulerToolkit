# -*- coding: utf-8 -*-

"""
Project Euler Toolkit

Dependencies:
    shutil
    fractions
    itertools
    collections
    cython, Cython

    numpy: arrays and matrices
    pulp: linear and non-linear optimization
    gmpy2: integers, rationals, etc.

@author: Jasper Wu
"""


# dependency test
#   - cython
#   - numpy
#   - gmpy2
#
# other dependencies possibly used
#   - scipy
#   - sympy
#   - pulp: https://pythonhosted.org/PuLP/
#   - ortools: https://developers.google.com/optimization/

DEPENDENCIES = ['cython', 'numpy', 'gmpy2']

for pkg in DEPENDENCIES:
    try:
        __import__(pkg)
    except:
        print("WARNING: Fail to import {}!".format(pkg))


# cython extensions
from . import ext


# useful functions in current package
from . combinatoric import (
    C, C_mod, MP,

    multiset_permutations,
    limited_combinations,

    all_subsets,
    all_partitions,
    seq_partitions,
)

from . formula import (
    sqrt, is_square, isqrt, iroot, gcd, ggcd,
    fac, fac_mod, cprod,
    sum_mod, pow_mod, mat_pow_mod, legendre_symbol,
    padic, max_subarray,

    pythag_triple_tree,
    co_prime_tree,
    stern_brocot_tree,

    rational_continous_frac,
    irrational_continous_frac,
    continous_frac_convergent,
)

from . prime import (
    primes_list,
    is_prime,
    prime_divisor_decomp,
    all_divisors,
    euler_phi,
    mobius,
    mobius_list,
    factor_sieve,
)

from . utils import (
    timepast,
    clear_cython_cache,
)

from . import equation


__all__ = [
    'combinatoric',
    'equation',
    'formula',
    'generator',
    'prime',
    'utils',
]
