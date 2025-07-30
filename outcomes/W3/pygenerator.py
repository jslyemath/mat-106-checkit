import slye_math as sm
import random


def generate(**kwargs):
    mult_allowed = False
    if int(kwargs['course_progress']) > 1:
        mult_allowed = True

    # Yes, I realize there is a lot of repeated code in the child functions.
    # No, I don't have time to clean it up.

    def gen_inserts(excl_zero=False, excl_one=False):

        v = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n',
             'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        n = list(range(0, 23))

        if excl_zero == True:
            n[:] = (i for i in n if i != 0)

        if excl_one == True:
            n[:] = (i for i in n if i != 1)

        insert_list = random.choice([v, n])
        chosen_inserts = sm.samples(insert_list, k=20)
        return chosen_inserts

    ops = ['+', '\\times'] if mult_allowed else ['+']

    fill_ops = ['+', '-', '\\times']

    def create_comm(op='+', fill_op='+', inserts=['a', 'b', 'c', 'd', 'w', 'x', 'y', 'z'], used_versions=[]):
        for o in (op, fill_op):
            if o in ['\\times', '*', 'x', '×']:
                o = '\\times'

        op_str = {'+': 'Addition', '\\times': 'Multiplication'}

        ans = f'Commutative ({op_str[op]})'

        def vA(op, inserts, fill_op):
            fillers = random.choices([['', f' {fill_op} {inserts[0]}'],
                                      [f'{inserts[0]}  {fill_op} ', ''],
                                      [f'{inserts[0]}  {fill_op} ', f' {fill_op} {inserts[1]}']],
                                     [1.5, 1.5, 1],
                                     k=1)[0]

            middles = [f'({inserts[2]} {op} {inserts[3]})',
                       f'({inserts[3]} {op} {inserts[2]})']

            random.shuffle(middles)

            sides = [f'{fillers[0]}{middles[0]}{fillers[1]}',
                     f'{fillers[0]}{middles[1]}{fillers[1]}']

            random.shuffle(sides)

            return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'vA'

        def vB(op, inserts, fill_op):
            chunks = sm.samples([f'{inserts[7]}',
                                 f'({inserts[0]} {fill_op} {inserts[1]})',
                                 f'({inserts[2]} {fill_op} {inserts[3]})',
                                 f'({inserts[4]} {fill_op} {inserts[5]} {fill_op} {inserts[6]})'],
                                [2, 1, 1, 1],
                                k=2)

            sides = [f'{chunks[0]} {op} {chunks[1]}', f'{chunks[1]} {op} {chunks[0]}']

            random.shuffle(sides)

            return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'vB'

        def vC(op, inserts, fill_op):
            if op == '+':
                fill_op = '+'

            fillers = random.choice([['', f' {fill_op} {inserts[0]}'],
                                     [f'{inserts[0]}  {fill_op} ', ''],
                                     ['', '']])

            swappers = [f'{inserts[1]} {op} {inserts[2]}',
                        f'{inserts[2]} {op} {inserts[1]}']

            random.shuffle(swappers)

            sides = [f'{fillers[0]}{swappers[0]}{fillers[1]}',
                     f'{fillers[0]}{swappers[1]}{fillers[1]}']

            random.shuffle(sides)

            return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'vC'

        possible_versions = ['vA', 'vB', 'vC']

        available_versions = [x for x in possible_versions if x not in used_versions]

        if available_versions == []:
            available_versions = possible_versions

        comm_func = random.choice(available_versions)

        return locals()[comm_func](op, inserts, fill_op)

    def create_assoc(op='+', fill_op='+', inserts=['a', 'b', 'c', 'd', 'w', 'x', 'y', 'z']):
        for o in (op, fill_op):
            if o in ['\\times', '*', 'x', '×']:
                o = '\\times'

        op_str = {'+': 'Addition', '\\times': 'Multiplication'}

        ans = f'Associative ({op_str[op]})'

        if op == '+':
            fill_op = '+'

        fillers = random.choice([['', f' {fill_op} {inserts[0]}'],
                                 [f'{inserts[0]}  {fill_op} ', ''],
                                 ['', '']])

        swappers = [f'{inserts[1]} {op} ({inserts[2]} {op} {inserts[3]})',
                    f'({inserts[1]} {op} {inserts[2]}) {op} {inserts[3]}']

        random.shuffle(swappers)

        sides = [f'{fillers[0]}{swappers[0]}{fillers[1]}',
                 f'{fillers[0]}{swappers[1]}{fillers[1]}']

        random.shuffle(sides)

        return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'v0'

    def create_ident(op='+', fill_op='+', inserts=['a', 'b', 'c', 'd', 'w', 'x', 'y', 'z'], used_versions=[]):
        for o in (op, fill_op):
            if o in ['\\times', '*', 'x', '×']:
                o = '\\times'

        op_str = {'+': 'Addition', '\\times': 'Multiplication'}

        ans = f'Identity ({op_str[op]})'

        if op == '+':
            fill_op = random.choice(['+'])

        def vA(op, inserts, fill_op):
            op_ident = {'+': '0', '\\times': '1'}

            fillers = random.choice([['', f' {fill_op} {inserts[0]}'],
                                     [f'{inserts[0]}  {fill_op} ', ''],
                                     ['', '']])

            collapsers = [inserts[1], op_ident[op]]

            random.shuffle(collapsers)

            swappers = [f'{collapsers[0]} {op} {collapsers[1]}', f'{inserts[1]}']

            random.shuffle(swappers)

            sides = [f'{fillers[0]}{swappers[0]}{fillers[1]}',
                     f'{fillers[0]}{swappers[1]}{fillers[1]}']

            random.shuffle(sides)

            return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'vA'

        def vB(op, inserts, fill_op):
            op_ident = {'+': '0', '\\times': '1'}

            inner_fillers = random.choice([['', f' {fill_op} {inserts[2]}'],
                                           [f'{inserts[2]}  {fill_op} ', ''],
                                           ['', '']])

            collapsers = [inserts[3], op_ident[op]]

            random.shuffle(collapsers)

            swappers = [f'{collapsers[0]} {op} {collapsers[1]}', f'{inserts[3]}']

            random.shuffle(swappers)

            insides = [f'{inner_fillers[0]}{swappers[0]}{inner_fillers[1]}',
                       f'{inner_fillers[0]}{swappers[1]}{inner_fillers[1]}']

            random.shuffle(insides)

            outer_fillers = random.choice([['', f' {fill_op} {inserts[-1]}'],
                                           [f'{inserts[-1]}  {fill_op} ', '']])

            sides = [f'{outer_fillers[0]} ({insides[0]}) {outer_fillers[1]}',
                     f'{outer_fillers[0]} ({insides[1]}) {outer_fillers[1]}']

            random.shuffle(sides)

            return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'vB'

        possible_versions = ['vA', 'vB']

        available_versions = [x for x in possible_versions if x not in used_versions]

        if available_versions == []:
            available_versions = possible_versions

        indent_func = random.choice(available_versions)

        return locals()[indent_func](op, inserts, fill_op)

    def create_zero_prod(fill_op='+', inserts=['a', 'b', 'c', 'd', 'w', 'x', 'y', 'z']):
        if fill_op in ['\\times', '*', 'x', '×']:
            fill_op = '\\times'

        ans = 'Zero Product'

        fillers = random.choice([['', f' {fill_op} {inserts[0]}'],
                                 [f'{inserts[0]}  {fill_op} ', ''],
                                 ['', '']])

        times_zero_order = random.choice([f'{inserts[1]} \\times 0', f'0 \\times {inserts[1]}'])

        swappers = ['0', times_zero_order]

        random.shuffle(swappers)

        sides = [f'{fillers[0]}{swappers[0]}{fillers[1]}',
                 f'{fillers[0]}{swappers[1]}{fillers[1]}']

        random.shuffle(sides)

        return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'v0'

    def create_dist(inserts=['a', 'b', 'c', 'd', 'w', 'x', 'y', 'z']):
        fill_op = '+'

        inside_op = random.choice(['+', '-'])

        ans = 'Distributive'

        num_inserts = True

        for insert in inserts:
            try:
                int(insert)
            except:
                num_inserts = False
                break

        fillers = random.choice([['', f' {fill_op} {inserts[0]}'],
                                 [f'{inserts[0]}  {fill_op} ', ''],
                                 ['', '']])

        distribution = []

        if num_inserts is False:
            distribution = random.choice([[f'{inserts[1]}({inserts[2]} {inside_op} {inserts[3]})',
                                           f'{inserts[1]} \\times {inserts[2]} {inside_op} {inserts[1]} \\times {inserts[3]}'],
                                          [f'({inserts[1]} {inside_op} {inserts[2]}) \\times {inserts[3]}',
                                           f'{inserts[1]} \\times {inserts[3]} {inside_op} {inserts[2]} \\times {inserts[3]}']])
        else:
            distribution = random.choice([[f'{inserts[1]}({inserts[2]} {inside_op} {inserts[3]})',
                                           f'{eval("inserts[1]*inserts[2]")} {inside_op} {eval("inserts[1]*inserts[3]")}'],
                                          [f'({inserts[1]} {inside_op} {inserts[2]}) \\times {inserts[3]}',
                                           f'{eval("inserts[1]*inserts[3]")} {inside_op} {eval("inserts[2]*inserts[3]")}']])

        random.shuffle(distribution)

        sides = [f'{fillers[0]}{distribution[0]}{fillers[1]}',
                 f'{fillers[0]}{distribution[1]}{fillers[1]}']

        random.shuffle(sides)

        return f'\\mbox{{${sides[0]} =\\:$}} \\mbox{{${sides[1]}$}}', ans, 'v0'

    prob_ans_ver = []

    if mult_allowed:
        call_amounts = sm.constrained_weak_composition(10, 5, 1, 3)
    else:
        call_amounts = sm.constrained_weak_composition(10, 3, 1, 4)
        call_amounts += [0, 0]

    used_comm_versions = []

    used_ident_versions = []

    for i in range(call_amounts[0]):
        prob_ans_ver.append(create_comm(random.choice(ops),
                                        random.choice(fill_ops),
                                        gen_inserts(),
                                        used_versions=used_comm_versions))
        used_comm_versions.append(prob_ans_ver[i][2])

    for i in range(call_amounts[1]):
        prob_ans_ver.append(create_assoc(random.choice(ops),
                                         random.choice(fill_ops),
                                         gen_inserts()))

    for i in range(call_amounts[2]):
        prob_ans_ver.append(create_ident(random.choice(ops),
                                         random.choice(fill_ops),
                                         gen_inserts(excl_zero=True, excl_one=True),
                                         used_versions=used_ident_versions))
        used_ident_versions.append(prob_ans_ver[call_amounts[0] + call_amounts[1] + i][2])

    for i in range(call_amounts[3]):
        prob_ans_ver.append(create_zero_prod(random.choice(fill_ops),
                                             gen_inserts(excl_zero=True, excl_one=True)))

    for i in range(call_amounts[4]):
        prob_ans_ver.append(create_dist(gen_inserts(excl_zero=True, excl_one=True)))

    random.shuffle(prob_ans_ver)

    expl_choices = ['Commutative Property of Addition', 'Associative Property of Addition',
                    'Identity Property of Addition']

    if mult_allowed:
        expl_choices += ['Commutative Property of Multiplication', 'Identity Property of Multiplication',
                         'Distributive Property of Multiplication over Addition']

    expl_text = random.choice(expl_choices)

    return {
        'p1_prob': prob_ans_ver[0][0],
        'p1_ans': prob_ans_ver[0][1],
        'p1_ver': prob_ans_ver[0][2],
        'p2_prob': prob_ans_ver[1][0],
        'p2_ans': prob_ans_ver[1][1],
        'p2_ver': prob_ans_ver[1][2],
        'p3_prob': prob_ans_ver[2][0],
        'p3_ans': prob_ans_ver[2][1],
        'p3_ver': prob_ans_ver[2][2],
        'p4_prob': prob_ans_ver[3][0],
        'p4_ans': prob_ans_ver[3][1],
        'p4_ver': prob_ans_ver[3][2],
        'p5_prob': prob_ans_ver[4][0],
        'p5_ans': prob_ans_ver[4][1],
        'p5_ver': prob_ans_ver[4][2],
        'p6_prob': prob_ans_ver[5][0],
        'p6_ans': prob_ans_ver[5][1],
        'p6_ver': prob_ans_ver[5][2],
        'p7_prob': prob_ans_ver[6][0],
        'p7_ans': prob_ans_ver[6][1],
        'p7_ver': prob_ans_ver[6][2],
        'p8_prob': prob_ans_ver[7][0],
        'p8_ans': prob_ans_ver[7][1],
        'p8_ver': prob_ans_ver[7][2],
        'p9_prob': prob_ans_ver[8][0],
        'p9_ans': prob_ans_ver[8][1],
        'p9_ver': prob_ans_ver[8][2],
        'p10_prob': prob_ans_ver[9][0],
        'p10_ans': prob_ans_ver[9][1],
        'p10_ver': prob_ans_ver[9][2],
        'expl_text': expl_text
    }
