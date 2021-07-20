import sys
import string

class cpt:
    def __init__(self, name, parents, probabilities):
        self.name = name
        self.parents = parents
        self.probabilities = probabilities


################ start BN class ###############
class BN:
    def __init__(self, nums, variables, graph, cpts):
        self.nums = nums
        self.variables = variables
        self.graph = graph
        self.cpts = cpts
        index_list = [i for i in range(self.nums)]
        self.variables_dict = dict(zip(self.variables, index_list))
        self.TotalProbability = self.calculateTotalProbability()

    def calculateProbability(self, event):
        k1 = self.count(event, 2)
        k2 = self.count(event, 3)

        probability = []
        for i in range(2**k1):
            p = 0
            for j in range(2**k2):
                index = self.calculateIndex(self.int2bin_list(i, k1), self.int2bin_list(j, k2), event)
                p = p + self.TotalProbability[index]
            probability.append(p)
        return list(reversed([x/sum(probability) for x in probability]))

    def calculateTotalProbability(self):
        TotalProbability = [0 for i in range(2 ** self.nums)]
        for i in range(2 ** self.nums):
            p = 1
            binary_list = self.int2bin_list(i,self.nums)
            for j in range(self.nums):
                if self.cpts[j].parents == []:
                    p = p * (self.cpts[j].probabilities[0][1-binary_list[j]] * 1000)
                else:
                    parents_list = self.cpts[j].parents
                    parents_index_list = [self.variables_dict[k] for k in parents_list]
                    index = self.bin_list2int([binary_list[k] for k in parents_index_list])
                    p = p * (self.cpts[j].probabilities[index][1 - binary_list[j]] * 1000)
            TotalProbability[i] = p / 10 ** (self.nums * 3)
        return TotalProbability

    def int2bin_list(self, a, b):
        binary_list = list(map(int, list(bin(a).replace("0b", ''))))
        binary_list = (b - len(binary_list)) * [0] + binary_list
        return binary_list

    def bin_list2int(self, b):
        result = 0
        for i in range(len(b)):
            result = result + b[len(b)-1-i] * (2 ** i)
        return result

    def calculateIndex(self, i, j, event):
        index_list = []
        for k in range(len(event)):
            if event[k] == 2:
                index_list.append(i[0])
                del(i[0])
            elif event[k] == 3:
                index_list.append(j[0])
                del(j[0])
            else:
                index_list.append(event[k])

        return self.bin_list2int(index_list)

    def count(self, list, a):
        c = 0
        for i in list:
            if i == a:
                c = c + 1
        return c

#### end BN Class #####

def readBN(filename):
    f = open(filename, 'r')
    nums = int(f.readline())
    f.readline()
    variables = f.readline()[:-1].split(' ')
    f.readline()
    graph = []
    for i in range(nums):
        line = f.readline()[:-1].split(' ')
        graph.append(list(map(int, line)))
    f.readline()
    cpts = []
    for i in range(nums):
        probabilities = []
        while True:
            line = f.readline()[:-1].split(' ')
            stripped_list = list(map(str.strip, line))
            if stripped_list != ['']:
                # print(stripped)
                probabilities.append(list(map(float, stripped_list)))
            else:
                break
        CPT = cpt(variables[i], [], probabilities)
        cpts.append(CPT)
    f.close()
    for i in range(nums):
        for j in range(nums):
            if graph[i][j] == 1:
                cpts[j].parents.append(variables[i])

    bayesnet = BN(nums, variables, graph, cpts)
    return bayesnet

def readEvents(filename, variables):
    f = open(filename, 'r')
    events = []
    while True:
        line = f.readline()
        event = []
        if line == "\n":
            continue
        elif not line:
            break
        else:
            for v in variables:
                index = line.find(v)
                if index != -1:
                    if line[index+len(v)] == ' ' or line[index+len(v)] == ',':
                        event.append(2)
                    elif line[index+len(v)] == '=':
                        if line[index+len(v)+1] == 't':
                            event.append(1)
                        else:
                            event.append(0)
                else:
                    event.append(3)
            if len(event) != len(variables):
                sys.exit()
            events.append(event)
    return events

# main function
if __name__ == "__main__":
  bayesnet = readBN(sys.argv[1])
  events = readEvents(sys.argv[2], bayesnet.variables)
  for event in events:
      print(bayesnet.calculateProbability(event))