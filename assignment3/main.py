import sys
import re

class nodes:
	def __init__(self, Name):
		self.name = Name
		self.number_parents = 0
		self.parents = []
		self.CPT = []

class query:
	def __init__(self, Name):
		self.query = Name
		self.evidence = []

def main(args=None):
	NetworkPath = args[0]
	QueryPath = args[1]

	with open (NetworkPath, "r") as myfile:
		NetworkLines=myfile.read().splitlines()

	with open (QueryPath, "r") as myfile:
		QueryLine=myfile.read().splitlines()

	num_nodes = int(NetworkLines.pop(0))

	while (NetworkLines[0] == ""):
		NetworkLines.pop(0)

	array = []
	for names in NetworkLines.pop(0).split():
		array.append(nodes(names))

	while (NetworkLines[0] == ""):
		NetworkLines.pop(0)

	for j in xrange(0,num_nodes):
		line = NetworkLines.pop(0)
		elements = line.split()
		for i in xrange(0,num_nodes):
			if int(elements[i]) == 1:
				array[i].parents.append(array[j])
				array[i].number_parents += 1

	while (NetworkLines[0] == ""):
		NetworkLines.pop(0)

	empty = False
	for j in xrange(0,num_nodes):
		line = NetworkLines.pop(0)
		while(line != "" and empty == False):
			elements = line.split()
			array[j].CPT.append(tuple(elements))
			if NetworkLines:
				line = NetworkLines.pop(0)
			else:
				empty = True


	for i in xrange(0,num_nodes):
		print('Node name: {0}'.format(array[i].name))
		print('Probability pair tuples: {0}'.format(array[i].CPT))
		print('Number of parents: {0}'.format(array[i].number_parents))
		if(0 < array[i].number_parents):
			for j in xrange(0,array[i].number_parents):
				print('Parent of the node: {0}'.format(array[i].parents[j].name))
		print('\n')

	line = QueryLine.pop(0)
	elements = line.split()
	elements.remove('|')
	elements[0] = elements[0].replace("P(", "")
	Query = query(elements[0])
	for i in xrange(1,len(elements)):
		elements[i] = elements[i].replace(",", "")
		elements[i] = elements[i].replace(")", "")
		elements[i] = elements[i].replace("=", " ")
		Query.evidence.append(tuple(elements[i].split()))

	print('Query: {0}'.format(Query.query))
	print('Evidence: {0}'.format(Query.evidence))


if __name__ == "__main__":
	main(sys.argv[1:])