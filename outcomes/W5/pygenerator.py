import slye_math as sm
import random


def generate(**kwargs):
    base_ten_num1 = '0'
    base_ten_num2 = '0'
    base_b_num1 = '0'
    base_b_num2 = '0'
    base_ten_alg = 'Standard'
    base_b_alg = 'Standard'
    base_b_base = random.choice((4, 5, 6, 7, 8, 9))
    base_names = ['null', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    base_b_ss = base_names[base_b_base]
    bt_n1_wts = {'wt_0': 0.0, 'wt_1': 0.0}
    bt_n2_wts = {'wt_0': 0.0, 'wt_1': 0.0}
    bb_n1_wts = {'wt_0': 0.0, 'wt_1': 0.0, 'wt_2': 0.0, 'wt_3': 0.0, 'wt_4': 0.0,
                 'wt_5': 0.0, 'wt_6': 0.0, 'wt_7': 0.0, 'wt_8': 0.0, 'wt_9': 0.0}
    bb_n2_wts = {'wt_0': 0.0, 'wt_1': 0.0, 'wt_2': 0.0, 'wt_3': 0.0, 'wt_4': 0.0,
                 'wt_5': 0.0, 'wt_6': 0.0, 'wt_7': 0.0, 'wt_8': 0.0, 'wt_9': 0.0}

    lattice_pv1 = random.choice([3, 4])
    lattice_pv2 = random.choice(list(range(2, lattice_pv1)))

    partial_products_pv1 = random.choice([2, 3, 4])
    partial_products_pv2 = 2 if partial_products_pv1 == 4 else random.choice(list(range(2, max(3, partial_products_pv1))))

    mult_alg_vars = [('Lattice', lattice_pv1, lattice_pv2),
                     ('Partial Products', partial_products_pv1, partial_products_pv2)]

    random.shuffle(mult_alg_vars)

    for i, (n1_wt, n2_wt) in enumerate(zip(bb_n1_wts, bb_n2_wts)):
        if 1 < i < base_b_base:
            bb_n1_wts[n1_wt] = bb_n2_wts[n2_wt] = 1 / (base_b_base - 2)

    base_ten_num1 = sm.int_string(place_values=mult_alg_vars[0][1], **bt_n1_wts)
    base_ten_num2 = sm.int_string(place_values=mult_alg_vars[0][2], **bt_n2_wts)

    base_b_num1 = sm.int_string(place_values=mult_alg_vars[1][1], **bb_n1_wts)
    base_b_num2 = sm.int_string(place_values=mult_alg_vars[1][2], **bb_n2_wts)

    base_ten_prob = f'{base_ten_num1} \\times {base_ten_num2}'
    base_ten_alg = mult_alg_vars[0][0]
    base_ten_ans = f'{eval(base_ten_num1 + "*" + base_ten_num2)}'

    base_b_prob = f'{base_b_num1}_\\text{{{base_b_ss}}} \\times {base_b_num2}_\\text{{{base_b_ss}}}'
    base_b_alg = mult_alg_vars[1][0]
    base_b_ans = f'{sm.str_int_base_op(base_b_num1, base_b_num2, "*", base_b_base)}_\\text{{{base_b_ss}}}'

    return {
        'base_ten_prob': base_ten_prob,
        'base_ten_alg': base_ten_alg,
        'base_ten_ans': base_ten_ans,
        'base_b_prob': base_b_prob,
        'base_b_alg': base_b_alg,
        'base_b_ans': base_b_ans,
        'base_b_base': base_b_base
    }
