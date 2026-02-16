import slye_math as sm
import random


def generate(**kwargs):
    mult_allowed = False
    if int(kwargs['course_progress']) > 1:
        mult_allowed = True

    expl_choices = ['Commutative Property of Addition', 'Associative Property of Addition']

    if mult_allowed:
        expl_choices += ['Commutative Property of Multiplication', 'Identity Property of Multiplication',
                         'Distributive Property of Multiplication over Addition']

    expl_text = random.choice(expl_choices)

    return {
        'expl_text': expl_text
    }
