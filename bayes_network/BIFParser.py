from BayesNode import BayesNode
from xml.dom.minidom import parse
import xml.dom.minidom
import re


class BIFParser:

    def parse(self, bif_file):
        my_bif_file = preprocess_xml_file(bif_file)
        DOMTree = xml.dom.minidom.parse(my_bif_file)
        collection = DOMTree.documentElement
        variables = self.get_variables(collection)
        prob_distributions = self.get_probability_distribution(collection)
        return variables, prob_distributions

    def get_variables(self, collection):
        results = []
        variables = collection.getElementsByTagName('VARIABLE')
        for variable in variables:
            NAME = variable.getElementsByTagName('NAME')[0]
            name = NAME.childNodes[0].data
            results.append(name)
        return results

    def get_probability_distribution(self, collection):
        results = []
        definitions = collection.getElementsByTagName('DEFINITION')
        for definition in definitions:
            FOR = definition.getElementsByTagName('FOR')[0]
            variable = FOR.childNodes[0].data
            GIVEN = definition.getElementsByTagName('GIVEN')
            parents = []
            if GIVEN is not None:
                for i in range(len(GIVEN)):
                    parents.append(GIVEN[i].childNodes[0].data)
            TABLE = definition.getElementsByTagName('TABLE')
            cpt = {}
            if len(parents) == 0:
                prob_dist = TABLE[0].childNodes[0].data.split()
                cpt[()] = prob_dist[0]
                node = BayesNode(variable, parents, cpt)
                results.insert(0, node)
            elif len(parents) == 1:
                prob_dist = TABLE[0].childNodes[0].data.strip().replace('\n', ' ').split()
                cpt[('T',)] = prob_dist[0]
                cpt[('F',)] = prob_dist[2]
                node = BayesNode(variable, parents, cpt)
                results.append(node)
            elif len(parents) == 2:
                prob_dist = TABLE[0].childNodes[0].data.strip().replace('\n', ' ').split()
                cpt[('T', 'T')] = prob_dist[0]
                cpt[('T', 'F')] = prob_dist[2]
                cpt[('F', 'T')] = prob_dist[4]
                cpt[('F', 'F')] = prob_dist[6]
                node = BayesNode(variable, parents, cpt)
                results.append(node)
        return results


def preprocess_xml_file(bif_file):
    my_file_name = 'zji-'+bif_file
    fr = open(bif_file, 'r')
    xml_content = fr.read()
    new_content = re.sub(r'<!--.*?-->', '', xml_content)
    fw = open(my_file_name, 'w')
    fw.write(new_content)
    fr.close()
    fw.close()

    f = open(my_file_name, 'r')
    lines = f.readlines()
    f.close()
    fnew = open(my_file_name, 'w')
    for line in lines:
        fnew.write(line.strip())
        fnew.write('\n')
    fnew.close()
    return my_file_name
