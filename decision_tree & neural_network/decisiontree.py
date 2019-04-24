from math import log
import operator


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote, 0) + 1
    sorted_classCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_classCount[0][0]


def calculate_entropy(dataSet):
    numEntries = len(dataSet)
    class_counts = {}
    for record in dataSet:
        class_type = record[-1]
        class_counts[class_type] = class_counts.get(class_type, 0) + 1
    entropy = 0.0
    for class_type in class_counts.keys():
        prob = float(class_counts[class_type]) / numEntries
        entropy -= prob * log(prob, 2)
    return entropy


def choose_attribute(dataSet):
    num_of_attr = len(dataSet[0]) - 1
    num_of_record = len(dataSet)
    base_entropy = calculate_entropy(dataSet)
    best_info_gain = 0.0
    best_attr = -1
    for i in range(num_of_attr):
        attr_value_list = [record[i] for record in dataSet]
        unique_vals = set(attr_value_list)
        new_entropy = 0.0
        for value in unique_vals:
            subDataSet = split_by(dataSet, i, value)
            prob = len(subDataSet) / float(num_of_record)
            new_entropy += prob * calculate_entropy(subDataSet)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_attr = i
    return best_attr


def split_by(dataSet, attr_index, value):
    retDataSet = []
    for record in dataSet:
        if record[attr_index] == value:
            rest_record = record[:attr_index]
            rest_record.extend(record[attr_index + 1:])
            retDataSet.append(rest_record)
    return retDataSet


def load_data(filename):
    dataSet = []
    with open(filename, mode='r') as f:
        for line in f.readlines():
            record = line.strip().replace(' ', '').split(',')
            dataSet.append(record)
    return dataSet


def create_tree(dataSet, labels):
    class_list = [record[-1] for record in dataSet]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    if len(labels) == 0:
        return majorityCnt(class_list)
    best_attr_index = choose_attribute(dataSet)
    best_attr = labels[best_attr_index]
    decTree = {best_attr: {}}
    del (labels[best_attr_index])
    attr_vals = [record[best_attr_index] for record in dataSet]
    unique_vals = set(attr_vals)
    for value in unique_vals:
        sub_labels = labels[:]
        decTree[best_attr][value] = create_tree(split_by(dataSet, best_attr_index, value), sub_labels)
    return decTree


# def test(decTree, labels, test_record):
#     result = []
#     for record in test_record:
#         class_label = classify(decTree, labels, record)
#         result.append(class_label)
#     return result


def classify(decTree, labels, test_record):
    first_attr = list(decTree.keys())[0]
    sub_tree = decTree[first_attr]
    attr_index = labels.index(first_attr)
    for key in sub_tree.keys():
        if test_record[attr_index] == key:
            if type(sub_tree[key]).__name__ == 'dict':
                class_label = classify(sub_tree[key], labels, test_record)
            else:
                class_label = sub_tree[key]
        else:
            class_label = None
    return class_label

