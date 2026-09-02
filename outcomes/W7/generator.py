import bank_helpers as sm
import random


def generate(**kwargs):
    # Repeating decimals come later in the semester, so this generator will not allow for repeating decimals
    decimals_allowed = False
    if kwargs['w7_allow_terminating']:
        decimals_allowed = True

    algorithm = 'Standard'
    directions = 'Directions go here.'
    remainder = None

    with_remainder = True
    if decimals_allowed:
        with_remainder = random.choice([True, False])

    quotient_pv = random.choice(list(range(4, 6)))
    divisor_pv = 2
    if quotient_pv == 4:
        divisor_pv = random.choice(list(range(2, 4)))
    quotient = sm.int_string(quotient_pv)
    divisor = sm.int_string(divisor_pv)

    if with_remainder:
        quotient = int(quotient)
        divisor = int(divisor)
        algorithm = random.choice(['Standard', 'Scaffold or Partial Quotients'])
        directions = f'Compute the following quotient and remainder using the {algorithm} algorithm.'
        dividend = divisor * quotient
        remainder = random.choice(list(range(0, divisor)))
        dividend += remainder
        quotient = sm.math_num(quotient)
        dividend = sm.math_num(dividend)
        answer = f'{quotient} remainder {remainder}'
    else:
        quotient_offset = random.choice(list(range(0, -1 * (quotient_pv + 1), -1)))
        divisor_offset = random.choice(list(range(1, -1 * (divisor_pv + 1), -1)))
        dividend_offset = quotient_offset + divisor_offset
        dividend = str(eval(quotient + '*' + divisor))
        dividend = sm.dec_string(dividend_offset, custom_string=dividend, separator=sm.MATH_COMMA)
        quotient = sm.dec_string(quotient_offset, custom_string=quotient, separator=sm.MATH_COMMA)
        divisor = sm.dec_string(divisor_offset, custom_string=divisor, separator=sm.MATH_COMMA)
        directions = 'Compute the following quotient. Give your final answer as a decimal. There should not be a remainder.'
        answer = f'{quotient}'

    div_prob = f'{dividend} \\div {divisor}'

    # TODO: Create logic for each of the division algorithms, and find a way to format their answers.

    return {
        'algorithm': algorithm,
        'answer': answer,
        'directions': directions,
        'div_prob': div_prob
    }


# ---------------------------------------------------------------------------
# CheckIt entry point.
#
# Ported from generator.sage, which loaded this file with runpy and called:
#     pygenerate(mode='html', course_progress=6, w7_allow_terminating=True)
# Those arguments are reproduced exactly, so this port changes no output: the
# same seed yields the same data it did before. The shim existed only because
# SageMath could not reach a plain-Python file and the bank root was not
# importable; both gaps are closed, so the file extension now selects the
# plain-Python runtime directly.
class Generator(BaseGenerator):
    # Terminating decimals arrive partway through the semester, so both
    # cases have to exist in the bank: a printed quiz set before that
    # point asks for "no_terminating", one set after asks for either.
    variants = ["no_terminating", "terminating"]

    def data(self):
        return generate(
            course_progress=6,
            w7_allow_terminating=self.variant == "terminating",
        )
