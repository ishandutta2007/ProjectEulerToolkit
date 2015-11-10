# -*- coding: utf-8 -*-

"""
equation.py

Functions using to solve various equations.
Function list: 
    linear_modulo_equation
    square_modulo_prime_equation
    generalized_pell_equation
    gauss_jordan_elimination

@author: Jasper Wu
"""


import numpy as np


def linear_modulo_equation(a, b, n):
    """
    Solve linear modular equation 
        (a * x) % n = b
    or written in modular arithmatic
         a * x = b (mod n)
    Return (smallest non-negative solution, step, n)
    """
    
    from ProjectEulerToolkit.formula import gcd

    d = gcd(a, n)
    if b % d:
        raise ValueError('No Solution for ({} * x) % {} = {}!'.format(a, n, b))
    
    aa = a / d
    bb = b / d
    nn = n / d
    
    x0, x1, p, q = 0, 1, aa, nn
    while q != 1:
        p, q = q, p % q
        x0, x1 = x1, x0 - p / q * x1
    if (aa * x0) % nn != 1:
        x0 = -x0
    if x0 < 0:
        x0 = nn + x0
    sol = (x0 * bb) % n
    while sol > nn:
        sol = (sol + nn) % n
    return sol, nn, n

def square_modulo_prime_equation(n, p):
    """
    Solve linear modular equation 
        (x^2) % n = p
    or written in modular arithmatic
         x^2 = n (mod p)
    where:
        (1) p is an odd prime
        (2) n is a quadratic residue of p
    Return smallest solution a, noticing that (p-a) is also a solution.

    Using Tonelli-Shanks algorithm.
    Details see: http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
    """

    from ProjectEulerToolkit.formula import (
        pow, sqrt, is_square, legendre_symbol,
    )

    if is_square(n):
        r = int(sqrt(n))
    elif legendre_symbol(n, p) != 1:
        raise ValueError("n is not a quadratic residue of p!")
    elif p % 4 == 3:
        r = pow(n, (p + 1)/4, p)
    else:
        z = 1
        while legendre_symbol(z, p) != -1:
            z += 1

        q, s= p - 1, 0
        while q & 1 == 0:
            q >>= 1
            s += 1

        c = pow(z, q, p)
        r = pow(n, (q + 1)/2, p)
        t = pow(n, q, p)
        while t > 1:
            t2 = t
            for i in xrange(1, s):
                t2 = (t2 * t2) % p
                if t2 == 1:
                    break

            b = pow(c, 1 << (s-i-1), p)
            r = (r * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            s = i
        
    if 2 * r + 1 > p:
        r = p - r
    return r

def _pqa(d, p, q):
    """
    PQa algorithm for solving generalized Pell equation, which can be regarded as a generalized continued fraction expansion with convergent computation
    """

    from ProjectEulerToolkit.formula import sqrt

    sd = sqrt(d)
    a, i = int((p+sd)/q), 0
    X, Y, PQ = [q, a*q - p], [0, 1], [(p, q)] 
    while 1:
        p = a*q - p
        q = (d - p*p) / q
        a = int((p + sd) / q)
        
        if i == 0 and (p, q) in PQ:
            l = len(PQ) - PQ.index((p, q))
            i = 2 * len(PQ) - PQ.index((p, q))
        if len(PQ) == i:
            return l, X[1:-1], Y[1:-1], zip(*PQ)[1][1:]
        
        X.append(a * X[-1] + X[-2])
        Y.append(a * Y[-1] + Y[-2])
        PQ.append((p, q))

def generalized_pell_equation(d, n=1, nsol=1):
    """
    Solve generalized Pell equation 
        x**2 - d * y**2 = n
    Return smallest positive basic solution set, or enough solutions according to nsol
    """

    from ProjectEulerToolkit.formula import sqrt

    if d <= 0:
        raise ValueError("D must be positive non-perfect-square integer!")
    sd = int(sqrt(d))
    if sd * sd == d:
        raise ValueError("D must be positive non-perfect-square integer!")
        
    # Classical Pell Equation: x**2 - d * y**2 = 1 (or -1)
    # Using continued fraction expansion of d to solve 

    if abs(n) == 1:
        l, X, Y, Q = _pqa(d, 0, 1)
        if l%2:
            if n == 1:
                x, y = X[2*l-1], Y[2*l-1]
            else:
                x, y = X[l-1], Y[l-1]                
        else:
            if n == 1:
                x, y = X[l-1], Y[l-1]
            else:
                x, y = 0, 0

        if nsol == 1:
            return x, y

        sols = [(x, y)]
        for _ in xrange(nsol-1):
            xk, yk = sols[-1]
            if n == -1:
                xk, yk = x*xk + y*yk*d, y*xk + x*yk
            sols.append((x*xk + y*yk*d, y*xk + x*yk))
        return sols

    # Generalized Pell Equation: x**2 - d * y**2 = n (n != 0)
    # Using Lagrange-Matthews-Mollin (LMM) algorithm

    # 1. Find all int f > 0 satisfying:
    #     n % (f*f) == 0
    # Note: need high efficient prime divisor decompsition algorithm when n is large.

    # 2. For each f, set m = abs(n / (f*f)).
    
    # 3. For each m, find all int z satisfying:
    #     (z*z) % m = d % m
    #     -m/2 < z <= m/2 
    # Note: need high efficient quadratic residue algorithm to solve the first modular equation when m is large.

    # Here we just use brute-search to find all value of z.

    f, zdict = 1, {}
    while f < sqrt(abs(n)/2):
        if n % (f*f) == 0:
            m = n / (f*f)
            ma = abs(m)
            mb = int(ma/2)
            for z in xrange(-mb-(ma%2)+1, mb+1):
                if z*z % abs(m) == d % abs(m):
                    if (f, m) in zdict:
                        zdict[(f, m)].append(z)
                    else:
                        zdict[(f, m)] = [z]
        f += 1
    
    f = int(sqrt(abs(n)))
    if f*f == abs(n):
        zdict[(f, n/abs(n))] = [0]
    
    # 4. For each z according to each (f, m), run pqa(d, z, abs(m)).

    # 5. Search for first Qi = 1 or -1.

    # 6. If Xi**2 - d * Y**2 = m, (f * Xi, f * Yi) is a fundamental solution.

    # 7. Let (t, u) be the minimal positive solution of x**2 - d * y**2 = -1.
    #    If Xi**2 - d * Y**2 = -m, then (f*(t*X[i] + d*u*Y[i]), f*(u*X[i] + t*Y[i])) is a fundamental solution.

    # 8. Let (r, s) be the minimal positive solution of x**2 - d * y**2 = 1.
    #    If some fundmental solution (x, y) are not positive, we can use transformation:
    #    x' + y'*sqrt(d) = (x + y*sqrt(d)) * (1 or -1) * (r + s*sqrt(d))**k
    #    to find the minimal positive solution (x', y') in the equivalent class of (x, y)

    # 9. When all z are done, then we have a set of fundmental solutions (or minimal positive solutions) which are all in different equivalent classes.

    r, s = generalized_pell_equation(d, 1)
    t, u = generalized_pell_equation(d, -1)
    
    sols = []
    for (f, m), zlist in zdict.items():
        for z in zlist:
            l, X, Y, Q = _pqa(d, z, abs(m))
            for i,q in enumerate(Q):
                if q in (-1, 1):
                    x, y = X[i], Y[i]
                    diff = x**2 - d * y**2
                    if diff == m:
                        xg, yg = f*x, f*y
                        while xg < 0 or yg < 0:
                            if xg < 0 and yg < 0:
                                xg, yg = -xg, -yg
                            else:
                                xg, yg = r*xg + d*s*yg, s*xg + r*yg
                        sols.append((xg, yg))
                    elif t and u and diff == -m:
                        xg, yg = f*(t*x + d*u*y), f*(u*x + t*y)
                        while xg < 0 or yg < 0:
                            if xg < 0 and yg < 0:
                                xg, yg = -xg, -yg
                            else:
                                xg, yg = r*xg + d*s*yg, s*xg + r*yg
                        sols.append((xg, yg))
                    break

    # 10. Let (r, s) be the minimal positive solution of x**2 - d * y**2 = 1.
    #     We can expand the solution set. 

    sols = sorted(sols)

    if len(sols) >= nsol:
        return sols
    
    to_expand = sols[:]
    while len(sols) < nsol:
        to_expand = [(r*x + d*s*y, s*x + r*y) for x,y in to_expand]
        sols += to_expand
    return sols[:nsol]

def gauss_jordan_elimination(coeffs):
    """
    Gauss-Jordan elimination algorithm, can only be used when there are more variables than equations
    coeffs: 2D list, all elements float
    """

    from copy import deepcopy
    
    w, d = len(coeffs[0]), len(coeffs)
    coefmat = np.matrix(coeffs)

    for i in range(d):
        flag = 1
        j = i
        while flag and j < d:
            if abs(coefmat[i, j]) < 0.001:
                for k in range(i+1, d):
                    if abs(coefmat[k, j]) > 0.001:
                        flag = 0
                        coefmat[k], coefmat[i] = \
                            deepcopy(coefmat[i]), deepcopy(coefmat[k])
                        break
                if flag:
                    j += 1
            else:
                flag = 0
        
        if j == d:
            break
        
        if coefmat[i, j] != 1:
            coefmat[i] /= coefmat[i, j]
        
        for k in range(i+1, d):
            if coefmat[k, j]:
                coefmat[k] = coefmat[k] - coefmat[k, j] * coefmat[i]

    for i in range(1, d):
        for j in range(w):
            if abs(coefmat[i, j]) > 0.001:
                break
        
        for k in range(i):
            if coefmat[k, j]:
                coefmat[k] = coefmat[k] - coefmat[k, j] * coefmat[i]

    return coefmat