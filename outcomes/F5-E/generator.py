import bank_helpers as sm
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
import inflect
from datetime import datetime
import re


# TODO: Finish F5-E

def generate(**kwargs):
    dummy = 0

    return {
        'dummy': dummy,
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
