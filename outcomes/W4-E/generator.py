import bank_helpers as sm
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


# ---------------------------------------------------------------------------
# CheckIt entry point.
#
# Ported from generator.sage, which loaded this file with runpy and called:
#     pygenerate(mode='html', course_progress=6)
# Those arguments are reproduced exactly, so this port changes no output: the
# same seed yields the same data it did before. The shim existed only because
# SageMath could not reach a plain-Python file and the bank root was not
# importable; both gaps are closed, so the file extension now selects the
# plain-Python runtime directly.
class Generator(BaseGenerator):
    def data(self):
        return generate(mode='html', course_progress=6)
