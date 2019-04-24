
class BayesNetwork:

    def __init__(self):
        self.nodes = []
        self.variables = []

    def add_node(self, node):
        self.nodes.append(node)
        self.variables.append(node.variable)
        for parent in node.parents:
            self.get_node_by_variable(parent).children.append(node)

    def get_node_by_variable(self, variable):
        for node in self.nodes:
            if node.variable == variable:
                return node
        return None

    def get_domain_by_variable(self, variable):
        return ['T', 'F']


