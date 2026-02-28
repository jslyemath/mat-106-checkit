import slye_math as sm
import random


def generate(**kwargs):
    two_base_ten = kwargs.get('two_base_ten', False)
    base_11_allowed = False
    base_12_allowed = False

    sub_algs = ('Equal Additions', 'Trades First', 'Subtract from the Base')
    
    sub_alg_choices = sm.samples(sub_algs, k=3)

    allowed_bases = [4, 5, 6, 7, 8, 9]
    if base_11_allowed:
        allowed_bases += [11]
    if base_12_allowed:
        allowed_bases += [12]
    base_b_base, base_b2_base = sm.samples(allowed_bases, k=2)

    base_list = [10, base_b_base]

    if two_base_ten:
        base_list.append(10)
    else:
        base_list.append(base_b2_base)
    
    random.shuffle(base_list)
    
    prob_ans = []

    for current_base in base_list:
        base_word = sm.base_int_to_word(current_base)
        base_suffix = f"_\\text{{{base_word}}}" if current_base != 10 else ""
        num_a, num_b, num_c = sm.add_sub_triad('-', num_digits=4, base = current_base)
        prob = f'{num_a}{base_suffix} - {num_b}{base_suffix}'
        ans = f'{num_c}{base_suffix}'
        prob_ans.append([prob, ans])

    # TODO: Create logic for each of the addition algorithms, and find a way to format their answers.

    return {
        'prob_1': prob_ans[0][0],
        'alg_1': sub_alg_choices[0],
        'ans_1': prob_ans[0][1],
        'prob_2': prob_ans[1][0],
        'alg_2': sub_alg_choices[1],
        'ans_2': prob_ans[1][1],
        'prob_3': prob_ans[2][0],
        'alg_3': sub_alg_choices[2],
        'ans_3': prob_ans[2][1],
    }