import sys
from BIFParser import BIFParser
from BayesNetwork import BayesNetwork
from BayesNode import BayesNode
import random
import time


def enumeration_ask(X, e, bn):
    """return the probability distribution of variable X given evidence e"""
    """e.x enumeration_ask(B, {'J':True, 'M':True}, bn) = P(B|j,m)"""
    Q = {}
    for xi in bn.get_domain_by_variable(X):
        Q[xi] = enumerate_all(bn.variables, extend(e, X, xi), bn)
    return normalize(Q)


def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0
    V, rest = variables[0], variables[1:]
    v_node = bn.get_node_by_variable(V)
    if V in e.keys():
        return float(v_node.get_conditional_prob(e[V], e) * enumerate_all(rest, e, bn))
    else:
        return float(sum(v_node.get_conditional_prob(v, e) * enumerate_all(rest, extend(e, V, v), bn)
                         for v in bn.get_domain_by_variable(V)))


def prior_sample(bn):
    x = {}
    for node in bn.nodes:
        x[node.variable] = node.sample(x)
    return x


def rejection_sampling(X, e, bn, N=100000):
    counts = {val: 0 for val in bn.get_domain_by_variable(X)}
    for i in range(N):
        x = prior_sample(bn)
        if is_consistent_with(x, e):
            val = x[X]
            counts[val] += 1
    return normalize(counts)


def is_consistent_with(event, evidence):
    return all(evidence.get(k, event[k]) == event[k] for k in event.keys())


def likelihood_weighting(X, e, bn, N=100000):
    W = {val: 0 for val in bn.get_domain_by_variable(X)}
    for i in range(N):
        x, w = weighted_sample(bn, e)
        val = x[X]
        W[val] += w
    return normalize(W)


def weighted_sample(bn, e):
    w = 1
    event = dict(e)
    for node in bn.nodes:
        if node.variable in e.keys():
            w = w * node.get_conditional_prob(e[node.variable], event)
        else:
            event[node.variable] = node.sample(event)
    return event, w


def gibbs_ask(X, e, bn, N=200000):
    G = {val: 0 for val in bn.get_domain_by_variable(X)}
    x = dict(e)
    Z = [var for var in bn.variables if var not in e.keys()]

    # initialize x with random values for the variables in Z
    for Zi in Z:
        x[Zi] = random.choice(bn.get_domain_by_variable(Zi))

    for j in range(N):
        for Zi in Z:
            x[Zi] = get_markov_blanket_sample(Zi, x, bn)
            G[x[X]] += 1

    return normalize(G)


def get_markov_blanket_sample(X, e, bn):
    Xnode = bn.get_node_by_variable(X)
    Q = {}
    for xi in bn.get_domain_by_variable(X):
        ei = extend(e, X, xi)
        Q[xi] = Xnode.get_conditional_prob(xi, e) * product([Yj.get_conditional_prob(ei[Yj.variable], ei)
                                                             for Yj in Xnode.children])
    return 'T' if normalize(Q)['T'] > random.uniform(0.0, 1.0) else 'F'


def product(numbers):
    result = 1.0
    for x in numbers:
        result *= x
    return float(result)


def normalize(P):
    total = 0
    normailized_P = P.copy()
    for key in P:
        total += P[key]
    for key in P:
        normailized_P[key] = normailized_P[key] / total
    return normailized_P


def extend(s, variable, value):
    s2 = s.copy()
    s2[variable] = value
    return s2


if __name__ == '__main__':
    arguments = sys.argv
    length = len(arguments)
    bif_file = arguments[1]
    X = arguments[2]
    e = {}
    for i in range(3, length, 2):
        if arguments[i+1] == 'true':
            e[arguments[i]] = 'T'
        else:
            e[arguments[i]] = 'F'

    print('query variable:', X)

    parser = BIFParser()
    bn = BayesNetwork()
    _, nodes = parser.parse(bif_file)
    for node in nodes:
        bn.add_node(node)

    start = time.time()
    P_1 = enumeration_ask(X, e, bn)
    end = time.time()
    print('Exact Inference: ', P_1, ' Runtime:', end - start, 's')

    start = time.time()
    P_2 = rejection_sampling(X, e, bn)
    end = time.time()
    print('Rejection Sampling (using 100000 samples):', P_2, ' Runtime:', end - start, 's')

    start = time.time()
    P_3 = likelihood_weighting(X, e, bn)
    end = time.time()
    print('Likelihood Weighting (using 100000 samples):', P_3, ' Runtime:', end - start, 's')

    start = time.time()
    P_4 = gibbs_ask(X, e, bn)
    end = time.time()
    print('Gibbs Sampling (using 100000 samples):', P_4, ' Runtime:', end - start, 's')
