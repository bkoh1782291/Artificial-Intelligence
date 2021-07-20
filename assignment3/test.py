import sys
from random import random

class CPT:
    def __init__(self, name_inp):
        self.name = name_inp
        self.parents = []
        self.size = 0
        self.table = []
        self.test = 0

def main(args=None):
    graphfile_path = args[0]
    with open (graphfile_path, "r") as file1:
        graphfile_data=file1.read().splitlines()

    queryfile_path = args[1]
    with open (queryfile_path, "r") as file2:
        queryfile_data=file2.read().splitlines()

    # Extracting number of variables
    n = int(graphfile_data.pop(0))
    # print(n)

    while (graphfile_data[0] == ""):
        graphfile_data.pop(0)

    # Extracting random variables
    node_list = []
    for var in graphfile_data.pop(0).split():
        node_list.append(CPT(var))
    # print(node_list)

    while (graphfile_data[0] == ""):
        graphfile_data.pop(0)

    # Extacts parents data and puts into CPT objects
    for i in xrange(0,n):
        row = graphfile_data.pop(0)
        values = row.split()
        for j in xrange(0,n):
            if int(values[j]) == 1:
                # node_list[j].parents.append(node_list[i])
                node_list[j].parents.append(i)
                node_list[j].size = node_list[i].size + 1

    # for i in xrange(0,n):
    #     print(node_list[i].parents)
    # print('\n')

    # Extracts CPT data
    for i in xrange(0,n):
        while (graphfile_data[0] == ""):
            graphfile_data.pop(0)
        while (graphfile_data[0] != ""):
            row = graphfile_data.pop(0)
            values = row.split()
            table = []
            for j in xrange(0,len(values)):
                table.append(float(values[j]))
            #node_list[i].table.append(table[1])
            node_list[i].table.append(table[0])
            if (len(graphfile_data) == 0):
                break

    # for i in xrange(0,n):
    #     print(node_list[i].table)
    # print('\n')

    # Extracting the query
    query = queryfile_data.pop(0)

    # Extracting and setting the test variable
    test_var = query[query.find('P(')+2:query.find('|')].strip()
    for i in xrange(0,n):
        if node_list[i].name == test_var:
            test_var_index = i

    # Extracting the first evidence variables
    evidence_vars = []
    ev_var = query[query.find('|')+2:query.find('=')]
    if query[query.find('=')+1:query.find('=')+6].find('true') != -1:
        evidence_bool = 1
    else:
        evidence_bool = 0
    evidence_vars.append([ev_var, evidence_bool])

    # Extracting any subsequent evidence variables
    while (query.find(',') != -1):
        query = query[query.find(',')+1::].strip()
        ev_var = query[0:query.find('=')]
        if query[query.find('=')+1:query.find('=')+6].find('true') != -1:
            evidence_bool = 1
        else:
            evidence_bool = 0
        evidence_vars.append([ev_var, evidence_bool])

    # Default sampling list
    default_sample_list = []
    for i in xrange(0,n):
        found = -1
        for j in xrange(0,len(evidence_vars)):
            if node_list[i].name == evidence_vars[j][0]:
                found = j
        if found != -1:
            default_sample_list.append(evidence_vars[found][1])
        else:
            default_sample_list.append(-1)

    # print(default_sample_list)

    # Sampling
    n_samples = 100000
    samples = []
    for s in xrange(0,n_samples):
        # initialising sample list and weights for each new sample
        sample_list = default_sample_list[:]
        weight = 1

        # looping through the node list
        for i in xrange(0,n):

            # if the node has parents, we will look at the cpt value based on current sampling
            if node_list[i].size != 0:
                index = ""
                for j in xrange(0,len(node_list[i].parents)):
                    index += str(sample_list[node_list[i].parents[j]])
                index_2 = int(index,2)
                # print(index, index_2)

            # if no parents, we will look at its only value
            else:
                index_2 = 0

            # if node is not evidence, sample and add result sample_list
            if sample_list[i] == -1:
                u = random()
                if u <= node_list[i].table[index_2]:
                    sample_list[i] = 1
                else:
                    sample_list[i] = 0
            # if node is true evidence, update the weight
            elif sample_list[i] == 1:
                weight = weight*node_list[i].table[index_2]
            # if node is false evidence, update the weight
            elif sample_list[i] == 0:
                weight = weight*(1-node_list[i].table[index_2])

        # loops through current samples. If that sample already exists, increases the count
        exists = 0
        for k in xrange(0,len(samples)):
            if samples[k][0] == sample_list:
                samples[k][2]+=1
                exists = 1
                break
        # if the sample doesn't already exist, adds it and sets the count to 1
        if exists == 0:
            samples.append([sample_list, weight, 1])

    print(samples)
    t_sum = 0
    f_sum = 0
    for i in xrange(0,len(samples)):
        if samples[i][0][test_var_index] == 1:
            t_sum += samples[i][1]*samples[i][2]
        elif samples[i][0][test_var_index] == 0:
            f_sum += samples[i][1]*samples[i][2]

    total = t_sum + f_sum
    v1 = t_sum/total
    v2 = f_sum/total
    print("{:.4f} {:.4f}".format(v1,v2))

if __name__ == "__main__":
    main(sys.argv[1:])