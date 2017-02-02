import sys
import csv
import numpy
import math
from collections import Counter
from Node import Node

global data_file, n_record, n_attr, input_data, visited


# Function used for input data configuration
def config(args="car_processed.csv"):
    print(args)
    global data_file, n_record, n_attr, input_data, visited
    data_file = args

    input_data = []
    m_data = 0
    n_data = 0
    with open(data_file, 'r') as f:
        f = csv.reader(f, delimiter=',')
        for line in f:
            m_data += 1
            vec = [int(i) for i in line]
            input_data.append(vec)
            n_data = len(vec)

    n_record = m_data
    n_attr = n_data - 1
    visited = [0] * n_attr


# Main function
def execute():
    root = Node()
    build_tree(input_data, root)
    traverse_tree(root, 0)


# Function to build Tree
# @param data   Data of passed in Node including Attribute data and label data
# @param parent passed in Node

# **-------------------Fill in here------------------------**/
# Note: You should break down data to matrix of attribute and array of records corresponding label

# Check if all records belong to one label -> add leaf node
# To add a node by:
# - Update parent's children list (parent.addChild())
# - Update children node's parent (child.setParent(parent))

# Find attribute not visited with minimum gini index using findGini

# If not found any attribute -> all attribute are visited -> find majority label and add leaf node
# Else
# - Create new Node with found attribute
# - Add new Node to parent
# - Mark visited[min Gini attribute] = 1

# Continue to build tree by building node for each value of new created node
def build_tree(data, parent):
    attribute = numpy.array(data)[:, 0:n_attr]
    label = numpy.array(data)[:, -1]

    class_count = Counter(label)

    attribute_count = len(numpy.vstack({tuple(row) for row in attribute}))



    if len(class_count) == 1 or attribute_count == 1 :
        max_label = class_count.most_common()
        leaf = Node(max_label[0][0])
        leaf.data = "LEAF : " + str(leaf.data)
        parent.add_child(leaf)
        leaf.set_parent(leaf)
        return leaf

    else:

        gini_list = [find_gini(attribute[:, n], label) for n in range(n_attr)]

        current_attribute = gini_list.index(min(gini_list))

        if visited[current_attribute] == 1:

            while visited[current_attribute] != 1:
                gini_list.remove(min(gini_list))
                current_attribute = gini_list.index(min(gini_list))

        current_attribute_node = Node(current_attribute)
        parent.add_child(current_attribute_node)
        current_attribute_node.set_parent(parent)

        visited[current_attribute] = 1

        current_attribute_list = attribute[:, current_attribute]

        current_attribute_unique = Counter(current_attribute_list)

        for each in current_attribute_unique:
            sub_records = []
            for line in data:
                if line[current_attribute] == each:
                    sub_records.append(line)

            current_value_edge = Node(each)
            current_value_edge.set_parent(current_attribute_node)
            current_value_edge.add_child(current_value_edge)

            current_value_node = build_tree(sub_records, current_attribute_node)
            current_value_node.data = str(current_value_node.data) + " IF VALUE = " + str(each)
            current_value_node.set_parent(current_value_edge)
            current_value_edge.add_child(current_value_node)

        return current_attribute_node


# Find gini index of given attribute data and corresponding Labels
# @param  att Attribute data
# @param  lab Label data
# @return gini index of an attribute
def find_gini(att, lab):
    # **-------------------Fill in here------------------------**/
    # These steps might help you:
    #  - Find number of different values in attribute, number of different labels
    #  - For each value i, find number of occurrences and number of corresponding labels to calculate ginisplit
    #  - gini = sum of all ginisplit

    divisions = Counter(att)
    tuple_list = []
    for i, j in zip(att, lab):
        tuple_list.append((i, j))

    gini_split = {i: -1 for i in divisions}

    for each in divisions:

        new_tuple_list = []
        for i in tuple_list:
            if i[0] == each:
                new_tuple_list.append(i[1])

        each_class_no = Counter(new_tuple_list)

        value = 0
        for j in each_class_no:
            value = value + math.pow((each_class_no[j] / divisions[each]), 2)

        gini_each = float(1 - value)

        gini_split[each] = gini_each

    final_gini = 0
    for gini in gini_split:
        final_gini = final_gini + ((divisions[gini] / sum(divisions.values())) * gini_split[gini])

    return final_gini


# Use DFS to traverse tree and print nicely with appropriate indent
# @param node traversing Node
# @param indent appropriate indent for each level
def traverse_tree(node, indent):
    # Print out current node with appropriate indent
    for i in range(indent):
        print('\t', end="")
    if (node.get_parent() is None):
        print("root")
    else:
        print("-/", node.get_data())

    # Recursive call all the children nodes
    children = []
    children = node.get_children()
    for i in range(node.get_n_child()):
        traverse_tree(children[i], indent + 1)


def main():
    arg = sys.argv[1:]
    if len(arg) > 0:
        config(arg)
    else:
        config()
    execute()


main()
