from random import random

def normalize(prob_distr):
    total = sum(prob_distr)
    if total != 0:
        return map(lambda a: a / total, prob_distr)
    else:
        return prob_distr

def is_true_for(self, probability, model_build_up_so_far):
        conditions = {}
        if self.is_root():
            conditions = {self.variable : True}
        else:
            conditions = dict(model_build_up_so_far)

        true_probability = self.probability_of(conditions)

        if probability <= true_probability:
            return True
        else:
            return False



class Randomizer:
    def next_double(self):
        raise NotImplementedError("Randomizer is an abstract class")

class StandardRandomizer(Randomizer):
    def next_double(self):
        return random()




class BayesNet:
    def __init__(self, roots):
        self.roots = tuple(roots)
        self.variable_nodes = None

    def probability_of(self, var_name, value, evidence):
        """
        Get probability of a variable having specified value with a specified evidence.
        :param var_name (str): name of the variable
        :param value (bool): value of the variable
        :param evidence dict(str, bool): hash table with evidence that contains names of variables and their values
        :return: probability of variable having specified value, with a given evidence.
        """
        var_node = self._get_node_of(var_name)

        if var_node == None:
            raise ValueError("Unable to find a node with variable " + var_name)
        else:
            if var_node.is_root():
                var_table = {var_name: value}
                return var_node.probability_of(var_table)
            else:
                parent_values = {parent.variable : evidence[parent.variable] for parent in var_node.parents}

                probability = var_node.probability_of(parent_values)

                if value:
                    return probability
                else:
                    return 1 - probability

    def _get_variable_nodes(self):
        """
        Get nodes of variables in this bayes net.
        :return list(BayesNetNode): nodes of variables in this bayes net
        """
        if self.variable_nodes == None:
            new_variables_nodes = []
            parents = list(self.roots)
            traversed_parents = []

            while len(parents) != 0:
                new_parents = []
                for parent in parents:
                    if parent not in traversed_parents:
                        new_variables_nodes.append(parent)

                        for child in parent.children:
                            if child not in new_parents:
                                new_parents.append(child)

                        traversed_parents.append(parent)
                parents = new_parents
            self.variable_nodes = new_variables_nodes

        return self.variable_nodes

    def likelihood_weighting(self, var, evidence, number_of_samples, randomizer=StandardRandomizer()):
        true_probability = 0
        false_probability = 0

        for i in range(number_of_samples):
            x = {}
            w = 1

            for node in self._get_variable_nodes():
                if evidence.get(node.variable) != None:
                    w *= node.probability_of(x)
                    x[node.variable] = evidence[node.variable]
                else:
                    x[node.variable] = node.is_true_for(randomizer.next_double(), x)

            query_value = x[var]

            if query_value:
                true_probability += w
            else:
                false_probability += w

        return normalize([true_probability, false_probability])



def test_likelihood_weighting(self):
        randomizer = MockRandomizer([0.5, 0.5, 0.5, 0.5])

        net = self._create_wet_grass_network()
        evidence = {"Sprinkler" : True}
        (true_probability, false_probability) = net.likelihood_weighting("Rain", evidence, 1000, randomizer)

        self.assertAlmostEqual(1, true_probability)
        self.assertAlmostEqual(0, false_probability)