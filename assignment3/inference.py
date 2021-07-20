# Brian Koh
# a1782291
# Artificial Intelligence Assignment 3
# usage : python2 inference.py [network.txt] [query.txt]

import sys
import random

"""
    initializing class CPT
"""
class cpt:
    def __init__(self, name, parents, probabilities):
        self.name = name
        self.parents = parents
        self.probabilities = probabilities

"""
    initializing class query
"""
class query:
        def __init__(self, Name):
            self.query = Name
            self.evidence = {}

"""
    initializing class for bayesian network
"""
class BN:
    def __init__(self, nums, variables, graph, cpts):
        self.nums = nums
        self.variables = variables
        self.graph = graph
        self.cpts = cpts
        self.evidence = None
        self.query = None

    def check_evidence(self, var, evidence):
        if var in evidence:
            return True
        else:
            return False

"""
    function to calculate likelihood weighting
    inputs:
    evidence    evidence variables as an event
    node_list   bayesian network
    var_index   query variable
    n_samples   number of samples to runs

    output:
    returns an estimate of P(X|e)
"""
def likelihood_weighting(bayes_net,number_of_samples):
        positive = 0.0
        negative = 0.0

        Condition = {'FF':0, 'FT':1, 'TF':2, 'TT':3, 'F':0, 'T':1}

        for n in range(number_of_samples):
            dict = {}
            w = 1
            vars = bayes_net.variables
            for i in xrange(0,len(vars)):

                if bayes_net.check_evidence(vars[i],bayes_net.evidence) == True:
                    dict[vars[i]] = bayes_net.evidence[vars[i]]
                    p_i = -1
                    if(dict[vars[i]] == 'true'):
                        p_i = 0
                    else:
                        p_i = 1

                    if len(bayes_net.cpts[i].parents) == 0:
                        w = w * bayes_net.cpts[i].probabilities[0][p_i]

                    elif len(bayes_net.cpts[i].parents) == 2:
                        condi = ''

                        for parent in bayes_net.cpts[i].parents:
                            if dict[parent] == 'true':
                                condi += 'T'
                            elif dict[parent] == 'false':
                                condi += 'F'

                        index = Condition[condi]
                        w = w * bayes_net.cpts[i].probabilities[index][p_i]

                    elif len(bayes_net.cpts[i].parents) == 1:
                        p = bayes_net.cpts[i].parents
                        if dict[p[0]] == 'false':
                            w = w * bayes_net.cpts[i].probabilities[0][p_i]
                        elif dict[p[0]] == 'true':
                            w = w * bayes_net.cpts[i].probabilities[1][p_i]

                elif bayes_net.check_evidence(vars[i],bayes_net.evidence) == False:
                    u = random.random()
                    if bayes_net.cpts[i].parents == []:
                        if u <= bayes_net.cpts[i].probabilities[0][0]:
                            dict[vars[i]] = 'true'
                        else:
                            dict[vars[i]] = 'false'

                    elif len(bayes_net.cpts[i].parents) == 2:
                        condi = ''

                        for parent in bayes_net.cpts[i].parents:
                            if dict[parent] == 'true':
                                condi += 'T'
                            elif dict[parent] == 'false':
                                condi += 'F'

                        if condi == 'FF' and u <= bayes_net.cpts[i].probabilities[0][0]:
                            dict[vars[i]] = 'true'
                        elif condi == 'FT' and u <= bayes_net.cpts[i].probabilities[1][0]:
                            dict[vars[i]] = 'true'
                        elif condi == 'TF' and u <= bayes_net.cpts[i].probabilities[2][0]:
                            dict[vars[i]] = 'true'
                        elif condi == 'TT' and u <= bayes_net.cpts[i].probabilities[3][0]:
                            dict[vars[i]] = 'true'
                        else:
                            dict[vars[i]] = 'false'

                    elif len(bayes_net.cpts[i].parents) == 1:
                        if u <= bayes_net.cpts[i].probabilities[0][0]:
                            dict[vars[i]] = 'true'
                        else:
                            dict[vars[i]] = 'false'

            query_value = bayes_net.query
            if dict[query_value] == 'true':
                positive += w
            elif dict[query_value] == 'false':
                negative += w

            sum = positive + negative
            p_true = positive/sum
            p_false = negative/sum

        print("{:.6f} {:.6f}".format(p_true, p_false))

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "please input arguments"

    elif len(sys.argv) == 3:

        filename1 = sys.argv[1]
        filename2 = sys.argv[2]

        ################################## read and parse network file ###################################
        network_file = open(sys.argv[1], 'r')

        with open (sys.argv[2], "r") as myfile:
            QueryLine = myfile.read().splitlines()

        # number of variables from network file
        N = int(network_file.readline())

        # read evidence variables
        network_file.readline()
        variables = network_file.readline()[:-1].split()
        j = 0
        for i in variables:
            variables[j]=i.rstrip("\r")
            j += 1

        # read network graph
        network_file.readline()
        graph = []
        for i in range(N):
            line = network_file.readline()[:-1].split()
            graph.append(list(map(int, line)))

        # read in CPTs
        network_file.readline()
        cpts = []
        for i in range(N):
            probabilities = []
            while True:
                line = network_file.readline()[:-1].split(' ')
                stripped_list = list(map(str.strip, line))

                if stripped_list != ['']:
                    probabilities.append(list(map(float, stripped_list)))
                else:
                    break
            CPT = cpt(variables[i], [], probabilities)
            cpts.append(CPT)

        network_file.close()
        for i in range(N):
            for j in range(N):
                if graph[i][j] == 1:
                    cpts[j].parents.append(variables[i])

        # call in and create BayesNetwork with likelihood weighting sampling
        bayesNetwork = BN(N, variables, graph, cpts)

        ############################### read and parse graph file ####################################
        line = QueryLine.pop(0)
        elements = line.split()
        elements.remove('|')
        elements[0] = elements[0].replace("P(", "")
        Query = query(elements[0])

        for i in range(1, len(elements)):
            elements[i] = elements[i].replace(",", "")
            elements[i] = elements[i].replace(")", "")
            elements[i] = elements[i].replace("=", " ")
            temp = elements[i].split()
            Query.evidence[temp[0]] = temp[1]

        bayesNetwork.query = Query.query
        bayesNetwork.evidence = Query.evidence

        likelihood_weighting(bayesNetwork, 1000000)