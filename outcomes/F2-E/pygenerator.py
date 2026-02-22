import slye_math as sm
import random
import math
from fractions import Fraction


def generate(**kwargs):
    # We will only divide certain shapes certain ways in area models
    # 'shape' : [ways to divide]
    shapes_dict = {
        'circle': [2, 3, 4, 6, 8],
        'isosceles trapezoid': [2, 3, 6],
        'equilateral triangle': [2, 3],
        'regular hexagon': [2, 3, 4, 6],
        'rectangle': [2, 3, 4, 5, 6, 8],
        'semicircle': [2, 3, 4]
    }

    shapes_possibilities = [(shape, num) for shape, nums in shapes_dict.items() for num in nums]

    def gen_easy_line_prob():
        # Gives students a problem where the given is 1

        shape = 'line'
        # Choose from tick locations that have multiple divisors
        orig_loc = random.choice([6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28])
        orig_num = 1
        orig_denom = 1

        # Remove cases that are too easy for the requested denominator
        possible_requested_denoms = [x for x in sm.divisors(orig_loc) if x not in [1, 2, orig_loc]]
        requested_denom = random.choice(possible_requested_denoms)

        # Keep requested location within reasonable bounds
        possible_requested_nums = sm.rel_primes(requested_denom, stop=math.ceil(30 * requested_denom / orig_loc))
        requested_num = random.choice(possible_requested_nums)

        requested_loc = orig_loc * requested_num // requested_denom

        return shape, orig_loc, orig_num, orig_denom, requested_loc, requested_num, requested_denom

    def gen_easy_area_prob():
        shape = random.choice(list(shapes_dict.keys()))
        model_denom = int(random.choice(shapes_dict[shape]))
        model_num = int(random.choice(sm.rel_primes(model_denom, stop=3 * model_denom)))
        orig_denom = int(1)
        orig_num = int(1)
        requested_num, requested_denom = model_num, model_denom

        return shape, model_num, model_denom, orig_num, orig_denom, requested_num, requested_denom

    problem_type = random.choice(['number line', 'area model'])

    if problem_type == 'number line':
        p1_type, p1_orig_loc, p1_orig_num, p1_orig_denom, p1_requested_loc, p1_requested_num, p1_requested_denom = gen_easy_line_prob()
        p1_text = f'Given the number line below, mark the value '
        p1_math = f'\\dfrac{{{p1_requested_num}}}{{{p1_requested_denom}}}'
        p1_prob_text = f'Number line with 1 labeled {p1_orig_loc} spaces to the right of 0'
        p1_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p1_requested_num}/{p1_requested_denom} labeled {p1_requested_loc} '
                       f'spaces to the right of 0.')
        p1_model_num = None
        p1_model_denom = None
        p1_ticks = max(p1_orig_loc, p1_requested_loc) + random.randint(1, 4)
        p1_label_b = '1'
        p1_label_c = p1_math

    else:
        p1_type, p1_model_num, p1_model_denom, p1_orig_num, p1_orig_denom, p1_requested_num, p1_requested_denom = gen_easy_area_prob()
        p1_text = f'If one {p1_type} represents 1, draw an area model for '
        p1_math = f'\\dfrac{{{p1_requested_num}}}{{{p1_requested_denom}}}'
        p1_prob_text = ''
        p1_ans_text = (f'A model of {p1_type}(s) each split equally into {p1_model_denom} parts. A total of '
                       f'{p1_model_num}  of these parts are shaded to represent {p1_requested_num}/{p1_requested_denom}.')
        p1_orig_loc = None
        p1_requested_loc = None
        p1_ticks = None
        p1_label_b = None
        p1_label_c = None


#TODO: Bring area_model_tikz.py into the main script for latex generation, align textemplate to this.
#TODO: Generate standalone tikz pictures locally based on seeds.

    return {
        'p1_type': p1_type,
        'p1_orig_loc': p1_orig_loc,
        'p1_orig_num': p1_orig_num,
        'p1_orig_denom': p1_orig_denom,
        'p1_requested_loc': p1_requested_loc,
        'p1_requested_num': p1_requested_num,
        'p1_requested_denom': p1_requested_denom,
        'p1_model_num': p1_model_num,
        'p1_model_denom': p1_model_denom,
        'p1_text': p1_text,
        'p1_math': p1_math,
        'p1_prob_text': p1_prob_text,
        'p1_ans_text': p1_ans_text,
        'p1_ticks': p1_ticks,
        'p1_label_b': p1_label_b,
        'p1_label_c': p1_label_c,
    }