import slye_math as sm
import random


def generate(**kwargs):
    sub_allowed = False
    base_11_allowed = False
    base_12_allowed = False
    if int(kwargs['course_progress']) > 0:
        sub_allowed = True

    add_algs = ('Column Addition', 'Partial Sums', 'Lattice')
    sub_algs = ('Equal Additions', 'Trades First', 'Subtract from the Base')
    allowed_bases = [4, 5, 6, 7, 8, 9]
    if base_11_allowed:
        allowed_bases += [11]
    if base_12_allowed:
        allowed_bases += [12]
    base_b_base = random.choice(allowed_bases)
    base_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
    base_b_base_text = base_names[base_b_base]
    add_alg_choices = sm.samples(add_algs, k=2)
    if sub_allowed:
        ops_algs = [('+', add_alg_choices[0]), ('-', random.choice(sub_algs))]
        random.shuffle(ops_algs)
    else:
        ops_algs = [('+', add_alg_choices[0]), ('+', add_alg_choices[1])]

    def add_sub_triad(op = '+', num_digits=4, base=10):
        leading_digits = []
        if op == '+':
            leading_digit_offset = 0
        else:
            leading_digit_offset = 1
            if base == 2:
                a = 0
                b = 0
            else:
                a = random.randint(1, base - 2)
                b = random.randint(0, base - a - 2)
            leading_digits = [[a, b, a+b]]

        forced_regroupings = random.randint(1, num_digits - leading_digit_offset)
        # print(f"{forced_regroupings=}")
        addends_sum = []
        for i in range(forced_regroupings):
            a = random.randint(1, base - 1)
            b = random.randint(base - a, base - 1)
            addends_sum.append([a, b, a+b])
        for i in range(num_digits - forced_regroupings - leading_digit_offset):
            if base == 2:
                a = random.randint(0, 1)
                b = random.randint(0, 1)
            else:
                a = random.randint(1, base - 1)
                b = random.randint(0, base - a - 1) if a != base-1 else 0
            addends_sum.append([a, b, a+b])

        random.shuffle(addends_sum)
        addends_sum += leading_digits
        # print(f"{addends_sum=}")

        num_a = 0
        num_b = 0
        num_c = 0
        for p, abc in enumerate(addends_sum):
            num_a += base ** p * abc[0]
            num_b += base ** p * abc[1]
            num_c += base ** p * abc[2]

        num_a = sm.base_conv(num_a, base=base, output='str')
        num_b = sm.base_conv(num_b, base=base, output='str')
        num_c = sm.str_int_base_op(num_a, num_b, '+', base)

        if op == '-':
            num_a, num_b, num_c = num_c, num_a, num_b

        return num_a, num_b, num_c

    base_ten_op = ops_algs[0][0]
    base_ten_alg = ops_algs[0][1]
    base_ten_num_a, base_ten_num_b, base_ten_num_c = add_sub_triad(base_ten_op, num_digits=4, base = 10)
    base_ten_prob = f'{base_ten_num_a} {base_ten_op} {base_ten_num_b}'
    base_ten_ans = f'{base_ten_num_c}'

    base_b_op = ops_algs[1][0]
    base_b_alg = ops_algs[1][1]
    base_b_num_a, base_b_num_b, base_b_num_c = add_sub_triad(base_b_op, num_digits=4, base = base_b_base)
    base_b_prob = f'{base_b_num_a}_\\text{{{base_b_base_text}}} {base_b_op} {base_b_num_b}_\\text{{{base_b_base_text}}}'
    base_b_ans = f'{base_b_num_c}_\\text{{{base_b_base_text}}}'

    return {
        'base_ten_prob': base_ten_prob,
        'base_ten_alg': base_ten_alg,
        'base_ten_ans': base_ten_ans,
        'base_b_prob': base_b_prob,
        'base_b_alg': base_b_alg,
        'base_b_ans': base_b_ans
    }