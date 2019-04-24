# coding utf-8
import re
import _thread
""" KB is simply the conjunction of all the statements it contains,
    whereas alpha is a single statement.
    adopt tree as data structure for a sentence in propositional logic
"""
connective_list = '==> <==> ~ | &'.split(' ')


class LogicalExpression:
    #  either connective or symbol must be None
    #  because one node cannot contain both a connective and a symbol
    #  if a node is a symbol, then connective is None and children is None
    #  if a node is not a symbol, then symbol is none, connective is the top-level connective of that sentence
    #  and children is the sentences that connective connects
    def __init__(self, symbol=None, connective=None, children=None):
        self.symbol = symbol
        self.connective = connective
        self.children = children

    def __invert__(self):
        return LogicalExpression(connective='~', children=[self])


def concatenate(list1, list2):
    result = list1[:]
    for i in range(len(list2)):
        result.append(list2[i])
    return result


"""" the priority of propositional connectives is () > ~ > & > | > ==> > <==> 
     given a sentence like A <==> ~ ( B | C & D ) to build a tree
     the root node is always the connective of lowest-level priority(outside of bracket).
     In this case, the root node is <==>
"""


def parser(sentence):
    sentence = sentence.replace(' ', '')
    children = []
    root_node = get_root_connective_node(sentence)
    child_list = sentence.split(root_node)
    for child in child_list:
        children.append(sentence_parser_func(child))

    expr = LogicalExpression(connective=root_node, children=children)
    return expr


def sentence_parser_func(sentence):
    if is_symbol(sentence):
        return LogicalExpression(symbol=sentence)
    elif contain_brackets(sentence):
        root_node = get_root_connective_node(sentence)
        children = []
        child_list = sentence.split(root_node)
        for child in child_list:
            children.append(sentence_parser_func(child))
        return LogicalExpression(connective=root_node, children=children)
    elif '==>' in sentence:
        node1 = LogicalExpression(connective='==>')
    elif '<==>' in sentence:
        node1 = LogicalExpression(connective='<==>')
    elif '~' in sentence:
        node1 = LogicalExpression(connective='~')
    elif '|' in sentence:
        node1 = LogicalExpression(connective='|')
    elif '&' in sentence:
        node1 = LogicalExpression(connective='&')


def parse_with_bracket(sentence):
    if '(' in sentence and ')' in sentence:
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        p2 = re.compile(r'[(](.*)[)]', re.S)
        count = 0
        for item in list(sentence):
            if item is '(':
                count += 1
                right_bracket_count += 1
            elif item is ')':
                count -= 1
            if count > 1:
                break
        if count == 0:
            subsentence_list = re.findall(p1, sentence)
        elif count > 1:
            subsentence_list = re.findall(p2, sentence)
        return subsentence_list


def contain_brackets(sentence):
    if '(' in sentence and ')' in sentence:
        return True
    else:
        return False


def get_root_connective_node(sentence):
    if '(' in sentence and ')' in sentence:
        count = 0
        right_bracket_count = 0
        for item in list(sentence):
            if item is '(':
                count += 1
                right_bracket_count += 1
            elif item is ')':
                count -= 1
            if count > 1:
                break
        if count == 0 and right_bracket_count > 1:
            subsentence = re.sub(r'[(](.*?)[)]', '', sentence)
        elif count == 0 and right_bracket_count == 1:
            if sentence[:1] is '(' and sentence[len(sentence) - 1:len(sentence)] is ')':
                p = re.compile(r'[(](.*?)[)]', re.S)
                subsentence = re.findall(p, sentence)
                subsentence = subsentence[0]
            else:
                subsentence = re.sub(r'[(](.*?)[)]', '', sentence)
        elif count > 1:
            subsentence = re.sub(r'[(](.*)[)]', '', sentence)
        return get_root_connective_node(subsentence)
    elif '<==>' in sentence:
        return '<==>'
    elif '==>' in sentence:
        return '==>'
    elif '|' in sentence:
        return '|'
    elif '&' in sentence:
        return '&'
    elif '~' in sentence:
        return '~'


def is_symbol(x):
    if isinstance(x, str) and x[:1].isalpha():
        for connective in connective_list:
            if connective in x:
                return False
        return True
    else:
        return False


def extract_symbols(logical_expression):
    symbol_list = []
    if logical_expression.symbol is not None:
        if logical_expression.symbol not in symbol_list:
            symbol_list.append(logical_expression.symbol)
    else:
        for child in logical_expression.children:
            symbol_list = concatenate(symbol_list, extract_symbols(child))
    return symbol_list


def tt_entails(kb, alpha):
    kb_symbols = unique(extract_symbols(kb))
    alpha_symbols = unique(extract_symbols(alpha))
    symbol_list = unique(concatenate(kb_symbols, alpha_symbols))
    return tt_check_all(kb, alpha, symbol_list, {})


def tt_check_all(kb, alpha, symbols, model={}):
    if not symbols:
        if pl_true(kb, model):
            return pl_true(alpha, model)
        else:
            return True
    else:
        p, rest = symbols[0], symbols[1:]
        return (tt_check_all(kb, alpha, rest, extend(model, p, True)) and
                tt_check_all(kb, alpha, rest, extend(model, p, False)))


def pl_true(logical_expression, model):
    if logical_expression.symbol is not None:
        return model[logical_expression.symbol]
    elif logical_expression.connective is '&':
        for child in logical_expression.children:
            if pl_true(child, model) is False:
                return False
        return True
    elif logical_expression.connective is '|':
        for child in logical_expression.children:
            if pl_true(child, model) is True:
                return True
        return False
    elif logical_expression.connective is '==>':
        left = logical_expression.children[0]
        right = logical_expression.children[1]
        if pl_true(left, model) is True and pl_true(right, model) is False:
            return False
        else:
            return True
    elif logical_expression.connective is '<==>':
        left = logical_expression.children[0]
        right = logical_expression.children[1]
        if pl_true(left, model) == pl_true(right, model):
            return True
        else:
            return False
    elif logical_expression.connective is '~':
        children = logical_expression.children[0]
        return not pl_true(children, model)


def extend(s, var, val):
    s2 = s.copy()
    s2[var] = val
    return s2

def unique(s):
    return list(set(s))

def test_tt_enumeration():
    print('-------Test with Truth-table enumeration algorithm-------')
    # Modus Ponens:    kb = {P, P ==> Q}    alpha = Q
    print('\ntest case -- Modus Ponens')
    P = LogicalExpression(symbol='P')
    Q = LogicalExpression(symbol='Q')
    notP = LogicalExpression(connective='~', children=[P])
    kb1 = LogicalExpression(connective='|', children=[notP, Q])
    kb = LogicalExpression(connective='&', children=[P, kb1])
    print(tt_entails(kb, Q))

    # Wumpus World (simple)
    print('\ntest case -- Wumpus World(sample)')
    P_1_1 = LogicalExpression(symbol='P_1_1')
    kb1 = LogicalExpression(connective='~', children=[P_1_1])
    P_1_2 = LogicalExpression(symbol='P_1_2')
    P_2_2 = LogicalExpression(symbol='P_2_2')
    P_2_1 = LogicalExpression(symbol='P_2_1')
    P_3_1 = LogicalExpression(symbol='P_3_1')
    B_1_1 = LogicalExpression(symbol='B_1_1')
    B_2_1 = LogicalExpression(symbol='B_2_1')
    P_1_2orP_2_1 = LogicalExpression(connective='|', children=[P_1_2, P_2_1])
    P_1_1orP_2_2orP_3_1 = LogicalExpression(connective='|', children=[P_1_1, P_2_2, P_3_1])
    kb2 = LogicalExpression(connective='<==>', children=[B_1_1, P_1_2orP_2_1])
    kb3 = LogicalExpression(connective='<==>', children=[B_2_1, P_1_1orP_2_2orP_3_1])
    kb4 = LogicalExpression(connective='~', children=[B_1_1])
    kb5 = B_2_1
    kb = LogicalExpression(connective='&', children=[kb1, kb2, kb3, kb4, kb5])
    alpha = P_1_2
    print(tt_entails(kb, alpha))

    # Horn Clauses (Russell & Norvig)
    print('\ntest case -- Horn Clauses (Russell & Norvig)')
    Mythical = LogicalExpression(symbol='Mythical')
    Immortal = LogicalExpression(symbol='Immortal')
    Mammal = LogicalExpression(symbol='Mammal')
    Horned = LogicalExpression(symbol='Horned')
    Magical = LogicalExpression(symbol='Magical')
    notMythical = LogicalExpression(connective='~', children=[Mythical])
    notImmortal = LogicalExpression(connective='~', children=[Immortal])
    notHorned = LogicalExpression(connective='~', children=[Horned])
    notMammal = LogicalExpression(connective='~', children=[Mammal])
    kb1 = LogicalExpression(connective='|', children=[notMythical, Immortal])
    kb2 = LogicalExpression(connective='|', children=[Mythical, notImmortal])
    kb3 = LogicalExpression(connective='|', children=[Mythical, Mammal])
    kb4 = LogicalExpression(connective='|', children=[notImmortal, Horned])
    kb5 = LogicalExpression(connective='|', children=[Horned, notMammal])
    kb6 = LogicalExpression(connective='|', children=[notHorned, Magical])
    kb = LogicalExpression(connective='&', children=[kb1, kb2, kb3, kb4, kb5, kb6])
    alpha1 = Mythical
    alpha2 = Magical
    alpha3 = Horned
    print('Mythical? ' + str(tt_entails(kb, alpha1)))
    print('Magical? ' + str(tt_entails(kb, alpha2)))
    print('Horned? ' + str(tt_entails(kb, alpha3)))

    # Liars and Truth-tellers
    print('\ntest case -- Liars and Truth-tellers')
    A = LogicalExpression(symbol='A')
    B = LogicalExpression(symbol='B')
    C = LogicalExpression(symbol='C')
    notA = LogicalExpression(connective='~', children=[A])
    notB = LogicalExpression(connective='~', children=[B])
    notC = LogicalExpression(connective='~', children=[C])
    kb1 = LogicalExpression(connective='|', children=[notA, C])
    kb2 = LogicalExpression(connective='|', children=[notB, notC])
    kb3 = LogicalExpression(connective='|', children=[notC, B, notA])
    kb4 = LogicalExpression(connective='|', children=[notB, C])
    kb5 = LogicalExpression(connective='|', children=[A, C])
    kb6 = LogicalExpression(connective='|', children=[C, B])
    kb7 = LogicalExpression(connective='|', children=[notC, A, notA])
    kb = LogicalExpression(connective='&', children=[kb1, kb2, kb3, kb4, kb5, kb6, kb7])
    print('(a) OSSMB 82-12:')
    print('Amy is truthful? ' + str(tt_entails(kb, A)))
    print('Bob is truthful? ' + str(tt_entails(kb, B)))
    print('Cal is truthful? ' + str(tt_entails(kb, C)))

    kb1 = LogicalExpression(connective='|', children=[notA, notC])
    kb2 = LogicalExpression(connective='|', children=[C, A])
    kb3 = LogicalExpression(connective='|', children=[notB, A])
    kb4 = LogicalExpression(connective='|', children=[notB, C])
    kb5 = LogicalExpression(connective='|', children=[notA, notC, B])
    kb6 = LogicalExpression(connective='|', children=[notC, B])
    kb = LogicalExpression(connective='&', children=[kb1, kb2, kb3, kb4, kb5, kb6])
    print('(b) OSSMB 83-11:')
    print('Amy is truthful? ' + str(tt_entails(kb, A)))
    print('Bob is truthful? ' + str(tt_entails(kb, B)))
    print('Cal is truthful? ' + str(tt_entails(kb, C)))


if __name__ == '__main__':
    test_tt_enumeration()
