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
    # course_progress is read for exactly one thing here:
    #     mult_allowed = int(kwargs['course_progress']) > 1
    # so the generator has two behaviours, not seven. As a variant both are
    # pregenerated across the bank and the print tool filters to the one the
    # course has reached, instead of the value being frozen in a shim and the
    # whole bank being regenerated to advance the semester.
    variants = ["no_multiplication", "multiplication"]

    def data(self):
        progress = 2 if self.variant == "multiplication" else 1
        return generate(course_progress=progress)
