# coding utf-8

def pl_resolution(kb, alpha):
    kb.append(get_invert_clause(alpha))
    clause_list = kb.copy()
    new = set()
    while True:
        n = len(clause_list)
        pairs = [(clause_list[i], clause_list[j])
                 for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            if False in resolvents:
                return True
            new = get_union_set(set(resolvents), new)

        if is_subset(new, set(clause_list)):
            return False
        for c in new:
            if is_exist(c, clause_list) is False:
                clause_list.append(c)


def pl_resolve(ci, cj):
    clause_result = []
    ci_disjunct_list = disjuncts(ci)
    cj_disjunct_list = disjuncts(cj)
    for di in ci_disjunct_list:
        for dj in cj_disjunct_list:
            if di == get_invert_clause(dj) or get_invert_clause(di) == dj:
                dnewi = remove_symbol_from_clause(di, ci_disjunct_list)
                dnewj = remove_symbol_from_clause(dj, cj_disjunct_list)
                dnew = unique(concatenate(dnewi, dnewj))
                new = associate('|', dnew)
                clause_result.append(new)
    return clause_result


def associate(connective, logical_expression_list):
    args = disassociate(connective, logical_expression_list)
    if len(args) == 0:
        return False
    elif len(args) == 1:
        return args[0]
    else:
        return '|'.join(args)


def disassociate(opr, clauses):
    result = []

    def collect(lg_expr_list):
        for expr in lg_expr_list:
            if opr in expr:
                collect(expr.split(opr))
            else:
                result.append(expr)

    collect(clauses)
    return result


def disjuncts(clauses):
    return disassociate('|', [clauses])


def remove_symbol_from_clause(symbol, seq):
    return [item for item in seq if item is not symbol]


def get_invert_clause(s):
    if '~' in s:
        s = s.replace('~', '')
    else:
        s = '~' + str(s)
    return s


def is_equal(s1, s2):
    if '|' not in s1 and '|' not in s2:
        return s1 == s2
    elif '|' in s1 and '|' in s2:
        s1_set = set(s1.split('|'))
        s2_set = set(s2.split('|'))
        if s1_set.issubset(s2_set) and s2_set.issubset(s1_set):
            return True
        else:
            return False
    else:
        return False


def is_subset(set1, set2):
    n = len(set1)
    count = 0
    for s1 in set1:
        flag = False
        for s2 in set2:
            if is_equal(s1, s2):
                flag = True
        if flag is True:
            count += 1
        else:
            return False
    if n == count:
        return True


def is_exist(s, c_list):
    for c in c_list:
        if is_equal(s, c):
            return True
    return False


def get_union_set(set1, set2):
    result_set = set2.copy()
    for s1 in set1:
        flag = False
        for s2 in set2:
            if is_equal(s1, s2):
                flag = True
        if flag is False:
            result_set.add(s1)
    return result_set


def concatenate(list1, list2):
    result = list1[:]
    for i in range(len(list2)):
        result.append(list2[i])
    return result


def unique(s):
    return list(set(s))


def test_resolution():
    print('-------Test with resolution-based prover-------')
    # Modus Ponens:    kb = {P, P ==> Q}    alpha = Q
    print('\ntest case -- Modus Ponens')
    kb1 = 'P'
    kb2 = '~P|Q'
    alpha = 'Q'
    kb = [kb1, kb2]
    print(pl_resolution(kb, alpha))

    # Wumpus World (simple)
    print('\ntest case -- Wumpus World(sample)')
    kb1 = '~P_1_1'
    kb2 = '~B_1_1|P_1_2|P_2_1'
    kb3 = '~P_1_2|B_1_1'
    kb4 = '~P_2_1|B_1_1'
    kb5 = '~B_2_1|P_1_1|P_2_2|P_3_1'
    kb6 = '~P_1_1|B_2_1'
    kb7 = '~P_2_2|B_2_1'
    kb8 = '~P_3_1|B_2_1'
    kb9 = '~B_1_1'
    kb10 = 'B_2_1'
    alpha = 'P_1_2'
    kb = [kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10]
    print(pl_resolution(kb, alpha))

    # Horn Clauses (Russell & Norvig)
    print('\ntest case -- Horn Clauses (Russell & Norvig)')
    kb1 = '~Mythical|Immortal'
    kb2 = '~Immortal|Mythical'
    kb3 = 'Mythical|Mammal'
    kb4 = '~Immortal|Horned'
    kb5 = '~Mammal|Horned'
    kb6 = '~Horned|Magical'
    alpha1 = 'Mythical'
    alpha2 = 'Magical'
    alpha3 = 'Horned'
    kb = [kb1, kb2, kb3, kb4, kb5, kb6]
    print('Mythical? ' + str(pl_resolution(kb, alpha1)))
    print('Magical? ' + str(pl_resolution(kb, alpha2)))
    print('Horned? ' + str(pl_resolution(kb, alpha3)))

    # Liars and Truth-tellers
    print('\ntest case -- Liars and Truth-tellers')
    kb1 = '~A|C'
    kb2 = '~C|A|~A'
    kb3 = '~B|~C'
    kb4 = 'C|B'
    kb5 = '~C|B|~A'
    kb6 = 'C|~B'
    kb7 = 'C|A'
    alpha1 = 'A'
    alpha2 = 'B'
    alpha3 = 'C'
    kbA = [kb1, kb2, kb3, kb4, kb5, kb6, kb7]
    kbB = [kb1, kb2, kb3, kb4, kb5, kb6, kb7]
    kbC = [kb1, kb2, kb3, kb4, kb5, kb6, kb7]
    print('(a) OSSMB 82-12:')
    print('Amy is truthful? ' + str(pl_resolution(kbA, alpha1)))
    print('Bob is truthful? ' + str(pl_resolution(kbB, alpha2)))
    print('Cal is truthful? ' + str(pl_resolution(kbC, alpha3)))

    kb1 = '~A|~C'
    kb2 = 'A|C'
    kb3 = '~B|A'
    kb4 = '~B|C'
    kb5 = '~A|~C|B'
    kb6 = '~C|B'
    alpha1 = 'A'
    alpha2 = 'B'
    alpha3 = 'C'
    kbA = [kb1, kb2, kb3, kb4, kb5, kb6]
    kbB = [kb1, kb2, kb3, kb4, kb5, kb6]
    kbC = [kb1, kb2, kb3, kb4, kb5, kb6]
    print('(b) OSSMB 83-11:')
    print('Amy is truthful? ' + str(pl_resolution(kbA, alpha1)))
    print('Bob is truthful? ' + str(pl_resolution(kbB, alpha2)))
    print('Cal is truthful? ' + str(pl_resolution(kbC, alpha3)))

if __name__ == '__main__':
    test_resolution()



