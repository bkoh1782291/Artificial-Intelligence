"""
Brian Koh Lit Yang
a1782291
Artificial Intelligence Assignment 2
Wine Quality Prediction using Decision Tree Learning (DTL)
Usage
winequality.py [train] [test] [minleaf]
"""
# Wine Quality Prediction using Decision Tree Learning
# "trains" the dataset and produces predicted quality values based on dataset

from __future__ import division
from collections import Counter
import sys
import math
import copy

# constructor to initialize class
class Node:
    def __init__(self, leaf = False):
        self.leaf = leaf
        self.left = None
        self.right = None
        self.splitval = None
        self.label = None


class decision_tree:
    # decision tree learning algorithm implementation
    def DTL(self, data, minleaf):

        x = [tuple(at[0]) for at in data]
        x = set(x)

        y = []

        for sample in data:
            y.append(sample[1])

        # library function Counter
        # subclass for counting hashable objects
        y = Counter(y)

        # if(N < minleaf) or (yi=yj for all [i, j]) or (xi=xj for all [i, j])
        if(len(data) <= minleaf or len(y) == 1 or len(x) == 1):

            # declare leaf node as true/1
            new_leaf_node = Node(leaf = True)
            most_frequent = 0
            # most frequent label
            # if x > y then assign most frequent value | else x == y label unknown
            for counted_label, frequence in y.items():
                if frequence > most_frequent:
                    most_frequent = frequence
                    new_leaf_node.label = counted_label
                elif frequence == most_frequent:
                    new_leaf_node.label = "unknown"

            return new_leaf_node

        # call ChooseSPlit to find the best attribute and best splitval value
        [attr, splitval] = self.ChooseSplit(data)

        # ChooseSplit returns two values, left and right
        left, right = self.split_attr(data, attr, splitval)

        # Create new node n
        n = Node()
        n.attr = attr
        n.splitval = splitval
        n.left = self.DTL(left, minleaf)
        n.right = self.DTL(right, minleaf)

        return n


    # function to calculate the 'information' value of Node
    def I_value(self, data):

        val  = 0.0
        length = len(data)
        probability = 0

        attributes = []
        for sample in data:
            attributes.append(sample[1])

        # library function Counter
        # subclass for counting hashable objects
        attributes = Counter(attributes)

        for frequency in attributes.values():
            probability = (frequency / length)
            if probability != 0:
                val += -(probability * math.log(probability, 2))

            elif probability == 0:
                val = 0.0

        return val


    # function to split the attributes (attr) into two seperate values
    def split_attr(self, data, attr, splitval):

        right = []
        left = []

        for i in data:
            x = i[0]

            if x[attr] <= splitval:
                left.append(i)
            elif attr == None:
                continue
            else:
                right.append(i)

        return left, right


    # choosesplit function which chooses the best attr and split-value
    def ChooseSplit(self, data):

        attr = None
        splitval_best = None
        attribute_size = len(data[0][0])

        biggest_gain = 0
        for i in range(attribute_size):

            data.sort(key=lambda srt: srt[0][i])

            for row in range(len(data) - 1):
                splitval = 0.5 * (data[row][0][i] + data[row + 1][0][i])
                left, right = self.split_attr(data, i, splitval)

                # to calculate gain value
                gain = 0

                root_I_value = self.I_value(data)
                left_I_value = self.I_value(left)
                right_I_value = self.I_value(right)

                left_val = len(left)
                right_val = len(right)

                remainder_value = left_val / len(data) * left_I_value + right_val / len(data) * right_I_value

                if(len(left) != 0 or len(right) != 0):
                    gain = root_I_value - remainder_value
                elif (len(left) == 0 or len(right) == 0) :
                    gain = 0

                if gain > biggest_gain:
                    attr = i
                    biggest_gain = gain
                    splitval_best = splitval

        return (attr, splitval_best)

    # function to return the predicted wine quality value
    def predict_dtl(self,n, data):

        while not n.leaf:

            if data[n.attr] <= n.splitval:
                n = n.left
            else:
                n = n.right

        return n.label


# function to convert dataset into proper list for training dataset
# also removes un-important values
def convert_datasets(data, flag):

    if flag == 1:

        train = data
        data = []

        # Read the training set and convert string data to list
        train.readline()
        for values in train.readlines():
            attributes = []

            # remove whitespace and split values
            for col in values.strip().split():
                attributes.append(float(col)) # IMPORTANT must be float or else division is wrong

            label = attributes[-1]
            attributes.pop()
            data.append((attributes,label))

        return data

    elif flag == 2:

        test = data
        test_dataset = []

        test_sample.readline()
        for values in test_sample.readlines():
            attributes = []

            # remove whitespace and split values
            for col in values.strip().split():
                attributes.append(float(col)) # IMPORTANT must be float or else division is wrong

            test_dataset.append(attributes)

        return test_dataset


# main function
if __name__ == "__main__":

    train = []
    test_sample = []
    minleaf = 0

    # read in training and testing data set path to file
    # take in minleaf value as last arg
    if (len(sys.argv) < 4):
      print "please enter correct arguments [path to file] [path to file2] [minleaf]"
    elif(len(sys.argv) == 4):
        train = open(sys.argv[1])
        test_sample = open(sys.argv[2])
        minleaf = int(sys.argv[3])

        # convert the datasets to list and remove irrelevant words
        train_dataset = convert_datasets(train, 1)
        test_dataset = convert_datasets(test_sample, 2)

        # print out wine quality prediction
        D = decision_tree()

        # construct a decision tree by using the Decision Tree Learning Algorithm
        decision_tree = D.DTL(train_dataset, minleaf)

        # print out prediction
        for values in test_dataset:
          print(int(D.predict_dtl(decision_tree, values)))
