import random


class BayesNode:
    def __init__(self, variable, parents, cpt):
        self.variable = variable
        self.parents = parents
        self.cpt = cpt
        self.children = []

    def get_conditional_prob(self, value, event):
        """ get_probablity(True, {J:True, M:True})
        query the probability of current node is true given J is true and M is true."""
        if len(self.parents) == 0:
            p = self.cpt[()]
        else:
            event_names = self.get_event_names(event, self.parents)
            p = self.cpt[event_names]
        return float(p) if value is 'T' else float(1 - float(p))

    def get_event_names(self, event, variables):
        if len(event) == len(variables) and isinstance(event, tuple):
            return event
        else:
            return tuple([event[var] for var in variables])

    def sample(self, event):
        p = self.get_conditional_prob('T', event)
        return 'T' if p > random.uniform(0.0, 1.0) else 'F'
