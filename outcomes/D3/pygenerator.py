import slye_math as sm
import random
from fractions import Fraction
from decimal import Decimal, localcontext, ROUND_DOWN


def generate(**kwargs):
    def dec_list(l):
        return list(map(sm.dec, l))

    def min_dist(l, n):
        d_list = dec_list(l)
        n = sm.dec(n)
        distances = [abs(x - n) for x in d_list]
        return min(distances)

    def decimal_places(d):
        d = sm.dec(d).normalize()
        return -d.as_tuple().exponent

    def distribute_to_lists(candidates, primary, secondary, extras):
        if not sm.is_iterable(candidates):
            candidates = [candidates]
        if not candidates:
            return None
        filtered_candidates = []
        all_lists = primary + secondary + extras
        for x in candidates:
            if sm.dec(x) not in dec_list(filtered_candidates) + dec_list(all_lists):
                filtered_candidates.append(x)
        random.shuffle(filtered_candidates)

        if filtered_candidates:
            if len(filtered_candidates) > 0:
                primary.append(filtered_candidates[0])
            if len(filtered_candidates) > 1:
                secondary.append(filtered_candidates[1])
            extras.extend(filtered_candidates[2:])

    probs = []
    backup_probs = []
    extra_probs = []

    # (a) Original Fraction
    terminating = random.choices([True, False], [0.7, 0.3])[0]
    if terminating:
        denom_list = [4, 25, 8, 20, 50, 125]
    else:
        denom_list = [6, 11, 15, 21, 33]
    orig_frac_denom = int(random.choice(denom_list))
    orig_frac_num = int(random.choice(sm.rel_primes(orig_frac_denom)))
    orig_frac = Fraction(int(orig_frac_num), int(orig_frac_denom))

    # The number of spaces is specific to the denom_lists above
    orig_frac_dec = Decimal(orig_frac_num) / Decimal(orig_frac_denom)
    quantize_places = int(4)
    with localcontext() as ctx:
        ctx.rounding = ROUND_DOWN
        orig_frac_dec = orig_frac_dec.quantize(Decimal('0.' + quantize_places * '0'))
    orig_frac_dec_str = str(orig_frac_dec)
    probs.append(orig_frac)

    # (b) Easy Fraction
    easy_frac_denom = random.choice([3, 5, 9, 10])
    easy_frac_num = random.choice(sm.rel_primes(easy_frac_denom))
    easy_frac = Fraction(int(easy_frac_num), int(easy_frac_denom))
    probs.append(easy_frac)

    # (c) Truncate
    truncates = []
    for i in range(1, quantize_places):
        with localcontext() as ctx:
            ctx.rounding = ROUND_DOWN
            truncate = orig_frac_dec.quantize(Decimal('0.' + i * '0'))
        truncates.append(truncate)
    distribute_to_lists(truncates, probs, backup_probs, extra_probs)

    # (d) Insert Extra Digit
    inserteds = []
    digits = list(range(0, 10))
    for i in range(3, quantize_places + 1):
        available_digits = digits[:]
        next_digit = int(orig_frac_dec_str[i])
        available_digits.remove(next_digit)
        ins_digit = str(random.choice(available_digits))
        inserted = Decimal(orig_frac_dec_str[:i] + ins_digit + orig_frac_dec_str[i:])
        inserteds.append(inserted)
    distribute_to_lists(inserteds, probs, backup_probs, extra_probs)

    # (e) Transpose Digits
    transposeds = []
    for i in range(2, quantize_places + 1):
        swap_list = list(orig_frac_dec_str)
        swap_list[i], swap_list[i + 1] = swap_list[i + 1], swap_list[i]
        transposed = Decimal(''.join(swap_list))
        transposeds.append(transposed)
    distribute_to_lists(transposeds, probs, backup_probs, extra_probs)

    # (f) Small Nudge
    nudgeds = []
    for i in range(1, quantize_places + 1):
        sign = random.choice(['-', '+'])
        amount = random.choice([1, 2])
        offset = Decimal(f'{sign}{amount}') * Decimal(f'1e-{i}')
        nudged = orig_frac_dec + offset
        nudgeds.append(nudged)
    distribute_to_lists(nudgeds, probs, backup_probs, extra_probs)

    # (g) Percent
    min_places = 1000
    for extra_prob in extra_probs:
        current_places = decimal_places(extra_prob)
        if current_places < min_places:
            percent_prob = extra_prob
            min_places = current_places
            removal_list = extra_probs
    for backup_prob in backup_probs:
        current_places = decimal_places(backup_prob)
        if current_places < min_places:
            percent_prob = backup_prob
            min_places = current_places
            removal_list = backup_probs
    removal_list.remove(percent_prob)
    distribute_to_lists(percent_prob, probs, backup_probs, extra_probs)

    # (h) Benchmark Fraction
    bench_fracs = []
    for b in [Fraction(int(0), int(1)), Fraction(int(1), int(2)), Fraction(int(1), int(1))]:
        if b == Fraction(int(0), int(1)):
            sign = '+'
        elif b == Fraction(int(1), int(2)):
            sign = random.choice(['-', '+'])
        else:
            sign = '-'
        if min_dist(probs, b) > Decimal('0.1'):
            offset_denom = int(random.randint(12, 50))
            offset_num = int(random.randint(1, offset_denom // 10))
            offset_frac = Fraction(offset_num, offset_denom)
            bench_frac = b + offset_frac if sign == '+' else b - offset_frac
            bench_fracs.append(bench_frac)
    distribute_to_lists(bench_fracs, probs, backup_probs, extra_probs)

    # Add extra problems as necessary
    random.shuffle(backup_probs)
    random.shuffle(extra_probs)

    current_list = backup_probs
    while len(probs) < 8:
        if not current_list:
            current_list = extra_probs
        probs.append(current_list.pop())

    # Order from lowest to greatest
    ordered_probs = sorted(probs, key=float)
    prob_ans = list(enumerate(ordered_probs, start=1))
    random.shuffle(prob_ans)

    def ready_to_print(e):
        if type(e) == Fraction:
            return sm.frac_to_latex(e)
        elif e == percent_prob:
            e = e * Decimal('100')
            e = e.normalize()
            with localcontext() as ctx:
                ctx.rounding = ROUND_DOWN
                e = e.quantize(Decimal('0'))
            return str(e) + '\\%'
        elif type(e) == Decimal:
            return str(sm.dec(e).normalize())
        else:
            return str(e)

    prob_ans = [[ready_to_print(prob), ans] for ans, prob in prob_ans]

    return {
        'p1_prob': prob_ans[0][0],
        'p1_ans': prob_ans[0][1],
        'p2_prob': prob_ans[1][0],
        'p2_ans': prob_ans[1][1],
        'p3_prob': prob_ans[2][0],
        'p3_ans': prob_ans[2][1],
        'p4_prob': prob_ans[3][0],
        'p4_ans': prob_ans[3][1],
        'p5_prob': prob_ans[4][0],
        'p5_ans': prob_ans[4][1],
        'p6_prob': prob_ans[5][0],
        'p6_ans': prob_ans[5][1],
        'p7_prob': prob_ans[6][0],
        'p7_ans': prob_ans[6][1],
        'p8_prob': prob_ans[7][0],
        'p8_ans': prob_ans[7][1]
    }
