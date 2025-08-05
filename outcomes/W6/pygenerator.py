import slye_math as sm
import random


def generate(**kwargs):
    # Repeating decimals come later in the semester, so this generator will not allow for repeating decimals
    decimals_allowed = False
    if kwargs['w6_allow_terminating']:
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
        quotient = f'{quotient:,}'.replace(",", "{,}")
        dividend = f'{dividend:,}'.replace(",", "{,}")
        answer = f'{quotient} remainder {remainder}'
    else:
        quotient_offset = random.choice(list(range(0, -1 * (quotient_pv + 1), -1)))
        divisor_offset = random.choice(list(range(1, -1 * (divisor_pv + 1), -1)))
        dividend_offset = quotient_offset + divisor_offset
        dividend = str(eval(quotient + '*' + divisor))
        dividend = sm.dec_string(dividend_offset, custom_string=dividend)
        quotient = sm.dec_string(quotient_offset, custom_string=quotient)
        divisor = sm.dec_string(divisor_offset, custom_string=divisor)
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
