import slye_math as sm
import random
from fractions import Fraction
from decimal import Decimal


def generate(**kwargs):
    # (a) Convert fraction to decimal
    allow_repeating_dec = False
    if kwargs['d2_allow_repeating']:
        allow_repeating_dec = True

    def frac_to_repeating_dec():
        period = random.randint(1, 2)
        for i in range(0, 50000):
            repetend_denom = int('9' * period)
            repetend_num = random.choice(sm.rel_primes(repetend_denom))
            repetend_frac = Fraction(repetend_num, repetend_denom)

            place_val_offset = int(random.randint(0, 2))
            non_repeating_digits = int(sm.int_string(place_values=place_val_offset + 1,
                                                     excl_first=[],
                                                     excl_last=[],
                                                     wt_0=0.13, wt_1=0.13, wt_2=0.13, wt_3=0.13, wt_4=0.13))
            shifter = Fraction(int(1), int(Decimal('10') ** Decimal(place_val_offset)))

            our_fraction = (Fraction(non_repeating_digits) + repetend_frac) * shifter
            fraction_num, fraction_denom = our_fraction.as_integer_ratio()
            non_repeating_dec_part = sm.dec_string(-1 * place_val_offset,
                                                   custom_string=non_repeating_digits,
                                                   remove_trails=False)
            if place_val_offset == 0:
                non_repeating_dec_part += '.'

            our_fraction_latex = f'\\dfrac{{{fraction_num}}}{{{fraction_denom}}}'
            our_decimal_latex = non_repeating_dec_part + f'\\overline{{{repetend_num}}}'

            output = (our_fraction_latex, our_decimal_latex)

            if fraction_denom == 9 and fraction_denom > 9:
                return output

            if fraction_denom != repetend_denom and fraction_num < 1000 and fraction_denom < 1000:
                return output

        return output

    def frac_to_terminating_decimal():
        denom = int(random.choice([16, 32, 80, 125, 250, 625]))
        num = int(random.choice(sm.rel_primes(denom, stop= 3 *denom)))

        our_fraction_latex = f'\\dfrac{{{num}}}{{{denom}}}'
        our_decimal_latex = f'{Decimal(num) / Decimal(denom)}'

        return our_fraction_latex, our_decimal_latex

    # (b) and (c) Convert decimals to percents (or vice-versa)
    def dec_percent(reverse=False):
        # Does not guarantee number of digits due to trailing zeros, but we don't need to be that precise
        digits = random.randint(1, 2)
        our_integer = int(random.randint(101, 999) if digits == 3 else random.randint(11, 99))
        offset = int(random.randint(-5, 0))
        dec = Decimal(our_integer) * Decimal(int(10)) ** Decimal(offset)
        percent = str(dec * Decimal(int(10)) ** Decimal(int(2)))
        percent = sm.dec_string(2, custom_string=str(dec))

        prob = f'{dec}'
        ans = f'{percent}\\%'
        ans_type = 'percent'

        if reverse is True:
            prob, ans = ans, prob
            ans_type = 'decimal'

        return prob, ans, ans_type

    if allow_repeating_dec is True:
        p1_prob, p1_ans = random.choices([frac_to_repeating_dec, frac_to_terminating_decimal], [0.8, 0.2], k=1)[0]()
    else:
        p1_prob, p1_ans = frac_to_terminating_decimal()

    reverse_ans_types = [True, False]
    random.shuffle(reverse_ans_types)

    p2_prob, p2_ans, p2_ans_type = dec_percent(reverse_ans_types[0])

    p3_prob, p3_ans, p3_ans_type = dec_percent(reverse_ans_types[1])

    return {
        'p1_prob': p1_prob,
        'p1_ans': p1_ans,
        'p2_prob': p2_prob,
        'p2_ans': p2_ans,
        'p2_ans_type': p2_ans_type,
        'p3_prob': p3_prob,
        'p3_ans': p3_ans,
        'p3_ans_type': p3_ans_type,
    }
