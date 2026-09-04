"""The Fundamentals Checkpoint: twenty problems across eleven fundamental skills.

Ported from the standalone FundCheck script. Three things changed in the move,
beyond the two bug fixes recorded in CODEBASE_NOTES.md:

* **No seeding here.** The old script reseeded before every draw, which made
  neighbouring versions overlap. CheckIt seeds once before calling `data()`, and
  every draw below simply carries on through that one stream.
* **No numpy.** CheckIt seeds `random` only, so a numpy draw would be different
  on every run and the same seed would stop meaning the same paper.
  `random.choices` covers the weighted digit draws.
* **Data, not LaTeX.** Each problem is returned as its parts, so `template.xml`
  and `textemplate.tex` can each lay them out their own way rather than having
  print formatting baked into the generator.
"""

import ast
import decimal
import fractions
import random
import re


# ---------------------------------------------------------------------------
# Whole-number and decimal arithmetic (problems 1-6)
# ---------------------------------------------------------------------------

MAIN_DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
LAST_DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#: Digit weights, tuned so the arithmetic is worth doing: middling digits appear
#: more often than 0 and 1, which would make a column trivial.
ADD_MAIN = [0.05, 0.05, 0.05, 0.05, 0.06, 0.17, 0.17, 0.17, 0.12, 0.11]
ADD_LAST = [0.09, 0.09, 0.09, 0.09, 0.13, 0.13, 0.13, 0.13, 0.12]


def _decimal_from(digits, power):
    return decimal.Decimal((0, digits, power))


def addition_problems():
    """Two additions, one on whole numbers and one on decimals."""
    first_offset = random.choice(range(-5, 0))
    second_offset = first_offset + random.choice(range(-2, 0))

    if random.choice([True, False]):
        powers = [0, 0, first_offset, second_offset]
    else:
        powers = [first_offset, second_offset, 0, 0]

    addends = []
    for power in powers:
        digits = [random.choice(range(1, 6))]
        digits.extend(random.choices(MAIN_DIGITS, weights=ADD_MAIN, k=4))
        digits.extend(random.choices(LAST_DIGITS, weights=ADD_LAST, k=1))
        addends.append(_decimal_from(digits, power))

    return [
        {'prob': f'{addends[0]} + {addends[1]}', 'ans': f'{addends[0] + addends[1]}'},
        {'prob': f'{addends[2]} + {addends[3]}', 'ans': f'{addends[2] + addends[3]}'},
    ]


def multiplication_problems():
    """Two multiplications: a long factor by a short one."""
    first_offset = random.choice(range(-2, 0))
    second_offset = first_offset + random.choice(range(-3, 0))

    if random.choice([True, False]):
        powers = [0, 0, first_offset, second_offset]
    else:
        powers = [first_offset, second_offset, 0, 0]

    factors = []
    for position, power in enumerate(powers):
        size = 4 if position % 2 == 0 else 2
        factors.append(_decimal_from(random.sample(LAST_DIGITS, size), power))

    return [
        {'prob': fr'{factors[0]} \times {factors[1]}',
         'ans': f'{factors[0] * factors[1]}'},
        {'prob': fr'{factors[2]} \times {factors[3]}',
         'ans': f'{factors[2] * factors[3]}'},
    ]


# -- subtraction, built backwards -------------------------------------------
#
# The difference and the subtrahend are chosen first and added to get the
# minuend, the same idea as bank_helpers.add_sub_triad, which builds an addition
# and hands it back reversed. A minuend that is the sum of two positive numbers
# cannot be the smaller of the pair, so a negative answer is impossible rather
# than merely unlikely -- the old script chose both numbers independently and
# tried to repair the cases where the subtrahend came out larger.
#
# A column whose two digits total ten or more carries when added, and that carry
# is exactly the borrow the student performs when subtracting, so the amount of
# regrouping is set directly instead of coaxed out of digit weights.

def _sub_columns(num_digits, forced_borrows, zero_low):
    """Column digits for (difference, subtrahend), least significant first.

    `zero_low` forces the lowest columns of the minuend to zero, which is how
    the minuend ends up with fewer decimal places than the subtrahend: at the
    finer of the two scales its trailing digits are zeros. That mismatch is the
    alignment the problem is really testing.
    """
    difference, subtrahend = [], []
    carry = 0
    borrows_left = forced_borrows

    for column in range(num_digits):
        remaining = num_digits - column

        if column < zero_low:
            # The minuend digit must be zero, so the column has to total ten.
            s = random.randint(1, 9)
            d = (10 - s - carry) % 10
        elif column == num_digits - 1:
            # The leading column must not carry, or the minuend gains a digit
            # and stops matching the subtrahend in size.
            d = random.randint(1, max(1, 8 - carry))
            s = random.randint(1, max(1, 9 - carry - d))
        elif borrows_left >= remaining - 1 > 0 or (
                borrows_left > 0
                and random.random() < borrows_left / max(1, remaining - 1)):
            d = random.randint(1, 9)
            s = random.randint(10 - d, 9)
        else:
            d = random.randint(0, max(0, 9 - carry))
            s = random.randint(0, max(0, 9 - carry - d))

        total = d + s + carry
        if total >= 10:
            borrows_left = max(0, borrows_left - 1)
        carry = total // 10
        difference.append(d)
        subtrahend.append(s)

    return difference, subtrahend


def _digits_to_int(digits):
    return sum(digit * 10 ** place for place, digit in enumerate(digits))


def _one_subtraction(num_digits, forced_borrows, minuend_places, subtrahend_places):
    scale = max(minuend_places, subtrahend_places)
    zero_low = scale - minuend_places

    difference, subtrahend = _sub_columns(num_digits, forced_borrows, zero_low)
    sub_int = _digits_to_int(subtrahend)
    diff_int = _digits_to_int(difference)
    min_int = sub_int + diff_int

    # Built, not hoped for, so state the properties rather than test for them.
    assert min_int >= sub_int, 'minuend smaller than subtrahend'
    assert len(str(min_int)) <= num_digits, 'the sum grew an extra digit'
    assert min_int % (10 ** zero_low) == 0, 'minuend has too many decimal places'

    shift = decimal.Decimal(10) ** -scale
    minuend = (decimal.Decimal(min_int) * shift).quantize(
        decimal.Decimal(10) ** -minuend_places)
    return {
        'prob': f'{minuend} - {decimal.Decimal(sub_int) * shift}',
        'ans': f'{decimal.Decimal(diff_int) * shift}',
    }


def subtraction_problems():
    """Two subtractions, one on whole numbers and one on decimals."""
    minuend_places = -random.choice(range(-4, 0))
    subtrahend_places = minuend_places + random.choice(range(1, 3))

    pairs = [
        _one_subtraction(6, random.randint(2, 4), 0, 0),
        _one_subtraction(6, random.randint(2, 4), minuend_places, subtrahend_places),
    ]
    if random.choice([True, False]):
        pairs.reverse()
    return pairs


# ---------------------------------------------------------------------------
# Signed integer arithmetic (problems 7-10)
# ---------------------------------------------------------------------------

def _shuffled_parts(subproblems, answers):
    """Sub-problems in a random order, each labelled (a) to (d).

    The label travels in the data rather than being counted out by the
    template, so both templates agree on it and neither has to do arithmetic.
    """
    parts = list(zip(subproblems, answers))
    random.shuffle(parts)
    return [{'letter': 'abcdefgh'[index], 'prob': prob, 'ans': f'{ans}'}
            for index, (prob, ans) in enumerate(parts)]


def integer_addition_parts():
    """Four sums, covering every combination of signs."""
    values = random.sample(range(1, 13), 8)
    signs = random.sample([-1, 1, -1], k=2)
    values[6] *= signs[0]
    values[7] *= signs[1]

    return _shuffled_parts(
        [f'-{values[0]} + -{values[1]}',
         f'{values[2]} + -{values[3]}',
         f'-{values[4]} + {values[5]}',
         f'{values[6]} + {values[7]}'],
        [-values[0] - values[1],
         values[2] - values[3],
         -values[4] + values[5],
         values[6] + values[7]])


def integer_subtraction_parts():
    values = random.sample(range(1, 13), 8)
    # The last pair is deliberately ordered so the answer is negative: a student
    # who always subtracts smaller from larger should not be able to coast.
    values[7] = random.randint(1, 6) + values[6]

    return _shuffled_parts(
        [f'-{values[0]} - -{values[1]}',
         f'{values[2]} - -{values[3]}',
         f'-{values[4]} - {values[5]}',
         f'{values[6]} - {values[7]}'],
        [-values[0] + values[1],
         values[2] + values[3],
         -values[4] - values[5],
         values[6] - values[7]])


def integer_multiplication_parts():
    values = random.sample(range(2, 13), 8)
    signs = random.sample([-1, 1, -1], k=2)
    values[6] *= signs[0]
    values[7] *= signs[1]

    return _shuffled_parts(
        [fr'-{values[0]} \times -{values[1]}',
         fr'{values[2]} \times -{values[3]}',
         fr'-{values[4]} \times {values[5]}',
         fr'{values[6]} \times {values[7]}'],
        [values[0] * values[1],
         -values[2] * values[3],
         -values[4] * values[5],
         values[6] * values[7]])


def integer_division_parts():
    values = random.sample(range(2, 11), 8)
    signs = random.sample([-1, 1, -1], k=2)
    # Each dividend is built as a product, so every quotient comes out whole.
    values[0] *= values[1]
    values[2] *= values[3]
    values[4] *= values[5]
    values[6] = signs[0] * values[6] * values[7]
    values[7] = signs[1] * values[7]

    return _shuffled_parts(
        [fr'-{values[0]} \div -{values[1]}',
         fr'{values[2]} \div -{values[3]}',
         fr'-{values[4]} \div {values[5]}',
         fr'{values[6]} \div {values[7]}'],
        [values[0] // values[1],
         -values[2] // values[3],
         -values[4] // values[5],
         int(values[6] / values[7])])


# ---------------------------------------------------------------------------
# Fractions (problems 11-14)
# ---------------------------------------------------------------------------

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _is_multiple(a, b):
    return a % b == 0 or b % a == 0


def _numerator_for(denominator):
    """A numerator that leaves the fraction already in lowest terms."""
    return random.choice([n for n in range(2, denominator)
                          if _gcd(n, denominator) == 1])


def _fraction_pair(numerator, denominator):
    return fr'\dfrac{{ {numerator} }}{{ {denominator} }}'


def fraction_multdiv_problems():
    denominators = random.sample(range(3, 12), 4)
    numerators = [_numerator_for(d) for d in denominators]

    product = (fractions.Fraction(numerators[0], denominators[0])
               * fractions.Fraction(numerators[1], denominators[1]))
    quotient = (fractions.Fraction(numerators[2], denominators[2])
                / fractions.Fraction(numerators[3], denominators[3]))

    return [
        {'prob': fr'{_fraction_pair(numerators[0], denominators[0])} \times '
                 fr'{_fraction_pair(numerators[1], denominators[1])}',
         'ans': _fraction_pair(product.numerator, product.denominator)},
        {'prob': fr'{_fraction_pair(numerators[2], denominators[2])} \div '
                 fr'{_fraction_pair(numerators[3], denominators[3])}',
         'ans': _fraction_pair(quotient.numerator, quotient.denominator)},
    ]


def fraction_addsub_problems():
    denominators = random.sample(range(3, 17), 4)
    # Unrelated denominators, so finding a common one is real work rather than
    # noticing that one divides the other.
    denominators[1] = random.choice(
        [d for d in range(3, 17) if not _is_multiple(d, denominators[0])])
    denominators[3] = random.choice(
        [d for d in range(3, 17)
         if not _is_multiple(d, denominators[2]) and d != denominators[1]])

    numerators = [_numerator_for(d) for d in denominators]

    # The subtraction is ordered so the answer stays positive.
    if (numerators[2] / denominators[2]) < (numerators[3] / denominators[3]):
        numerators[2], denominators[2], numerators[3], denominators[3] = (
            numerators[3], denominators[3], numerators[2], denominators[2])

    total = (fractions.Fraction(numerators[0], denominators[0])
             + fractions.Fraction(numerators[1], denominators[1]))
    difference = (fractions.Fraction(numerators[2], denominators[2])
                  - fractions.Fraction(numerators[3], denominators[3]))

    return [
        {'prob': fr'{_fraction_pair(numerators[0], denominators[0])} + '
                 fr'{_fraction_pair(numerators[1], denominators[1])}',
         'ans': _fraction_pair(total.numerator, total.denominator)},
        {'prob': fr'{_fraction_pair(numerators[2], denominators[2])} - '
                 fr'{_fraction_pair(numerators[3], denominators[3])}',
         'ans': _fraction_pair(difference.numerator, difference.denominator)},
    ]


# ---------------------------------------------------------------------------
# Order of operations (problems 15-16)
# ---------------------------------------------------------------------------

PEMDAS_TERMS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
PEMDAS_NAMES = ['a', 'b', 'c', 'd', 'e']


def _pemdas_template():
    """One expression shape, with a, b, c, d, e as holes.

    Each of the four operations appears exactly once, so every version exercises
    the whole of the order rather than whichever operations happened to be drawn.
    """
    exponent = '3' if random.uniform(0, 1) < 0.2 else '2'

    operators = [' + ', ' - ', ' * ', ' / ']
    random.shuffle(operators)
    operators.append('')
    text = ''.join(''.join(pair) for pair in zip(PEMDAS_NAMES, operators))

    if random.uniform(0, 1) < 0.85:
        opening, closing = sorted(random.sample(PEMDAS_NAMES, 2))
        if opening == 'a' and closing == 'e':
            closing = random.choice(['b', 'c', 'd'])
        text = text.replace(opening, '(' + opening)
        text = text.replace(closing, closing + ')')
        exponent_spot = random.choice(PEMDAS_NAMES + [')'])
    else:
        exponent_spot = random.choice(PEMDAS_NAMES)

    return text.replace(exponent_spot, exponent_spot + f'**{exponent}')


def _exact(node, environment):
    """One node's value as an exact Fraction.

    Fraction, not float and not Decimal: 7/2 has to stay 7/2, or a later
    multiplication by 4 quietly turns a fractional step back into a whole answer
    and hides the fraction the student would have had to write down.
    """
    if isinstance(node, ast.Expression):
        return _exact(node.body, environment)
    if isinstance(node, ast.Name):
        return fractions.Fraction(environment[node.id])
    if isinstance(node, ast.Constant):
        return fractions.Fraction(node.value)
    left = _exact(node.left, environment)
    right = _exact(node.right, environment)
    operator = node.op
    if isinstance(operator, ast.Add):
        return left + right
    if isinstance(operator, ast.Sub):
        return left - right
    if isinstance(operator, ast.Mult):
        return left * right
    if isinstance(operator, ast.Div):
        if right == 0:
            raise ZeroDivisionError
        return left / right
    if isinstance(operator, ast.Pow):
        return left ** int(right)
    raise ValueError(f'unexpected operator {operator!r}')


def _variables_of(node, found=None):
    found = set() if found is None else found
    if isinstance(node, ast.Expression):
        _variables_of(node.body, found)
    elif isinstance(node, ast.Name):
        found.add(node.id)
    elif isinstance(node, ast.BinOp):
        _variables_of(node.left, found)
        _variables_of(node.right, found)
    return found


def _divisions_of(node, found=None):
    """Every division, with the variables it depends on.

    Those variable sets are what make the search cheap: once a division's
    variables are all assigned its result is decided, so a branch that has
    already gone fractional can be abandoned rather than finished.
    """
    found = [] if found is None else found
    if isinstance(node, ast.Expression):
        _divisions_of(node.body, found)
    elif isinstance(node, ast.BinOp):
        _divisions_of(node.left, found)
        _divisions_of(node.right, found)
        if isinstance(node.op, ast.Div):
            found.append((node, _variables_of(node)))
    return found


def _solve_pemdas(template, wanted=120, low=-60, high=70):
    """Assignments where no step anywhere is fractional.

    Backtracking, not sampling. Sampling five values and keeping the draw when
    the *final* answer is whole allows a fraction in the middle so long as a
    later step clears it, which for some shapes is most of what it produces --
    and it cannot tell a rare shape from an impossible one, so it burns a
    million draws either way. Filling the variables in one at a time and
    dropping a branch as soon as a decided division comes out fractional
    settles every shape in milliseconds, the impossible ones included.
    """
    tree = ast.parse(template, mode='eval')
    divisions = _divisions_of(tree)
    found = []

    def recurse(index, environment, unused):
        if len(found) >= wanted:
            return
        if index == len(PEMDAS_NAMES):
            try:
                result = _exact(tree, environment)
            except ZeroDivisionError:
                return
            if result.denominator == 1 and low < result < high:
                found.append((dict(environment), int(result)))
            return

        name = PEMDAS_NAMES[index]
        pool = unused[:]
        random.shuffle(pool)
        for value in pool:
            environment[name] = value
            assigned = set(environment)
            usable = True
            for division, needs in divisions:
                if needs <= assigned:
                    try:
                        if _exact(division, environment).denominator != 1:
                            usable = False
                            break
                    except ZeroDivisionError:
                        usable = False
                        break
            if usable:
                recurse(index + 1, environment,
                        [v for v in unused if v != value])
            del environment[name]
            if len(found) >= wanted:
                return

    recurse(0, {}, list(PEMDAS_TERMS))
    return found


# -- is the problem worth asking? -------------------------------------------
#
# An expression only tests the order of operations if getting the order WRONG
# gives a different answer. One a student can work through left to right and
# still land on the right number is a free mark. About a third of otherwise
# valid expressions are like that, so they are filtered out.

_PEMDAS_TOKEN = re.compile(r'\d+|\*\*|[-+*/()]')


def _nest(tokens):
    stack = [[]]
    for token in tokens:
        if token == '(':
            stack.append([])
        elif token == ')':
            inner = stack.pop()
            stack[-1].append(inner)
        else:
            stack[-1].append(token)
    return stack[0]


def _as_fraction(item):
    return item if isinstance(item, fractions.Fraction) else fractions.Fraction(int(item))


def _sweep(items, operators):
    """One left-to-right pass applying only these operators."""
    out = [items[0]]
    index = 1
    while index < len(items):
        operator, right = items[index], items[index + 1]
        if operator in operators:
            left, right = _as_fraction(out[-1]), _as_fraction(right)
            if operator == '+':
                out[-1] = left + right
            elif operator == '-':
                out[-1] = left - right
            elif operator == '*':
                out[-1] = left * right
            elif operator == '/':
                out[-1] = left / right
            else:
                out[-1] = left ** int(right)
        else:
            out.extend((operator, right))
        index += 2
    return out


def _evaluate(sequence, tiers):
    """Value of one bracket level, applying the given tiers in order."""
    items = []
    for item in sequence:
        items.append(_evaluate(item, tiers) if isinstance(item, list) else item)
    for tier in tiers:
        items = _sweep(items, tier)
    return _as_fraction(items[0])


#: Exponents bind tightest under every reading -- students reliably do those
#: first. It is the two middle tiers they run together.
BY_THE_RULES = [['**'], ['*', '/'], ['+', '-']]
LEFT_TO_RIGHT = [['**'], ['*', '/', '+', '-']]
#: "PEMDAS" read as an order rather than two tiers: every multiplication before
#: every division, every addition before every subtraction.
BY_THE_MNEMONIC = [['**'], ['*'], ['/'], ['+'], ['-']]


def _answer(expression, tiers=BY_THE_RULES):
    return _evaluate(_nest(_PEMDAS_TOKEN.findall(expression.replace(' ', ''))), tiers)


def _fill_in(template, environment):
    text = template
    for name in PEMDAS_NAMES:
        text = text.replace(name, str(environment[name]))
    return text


def _discriminates(expression, catch_mnemonic=False):
    """Does a wrong order give a wrong answer?

    Always required: a left-to-right reading must land somewhere else, and the
    brackets must earn their place -- `(3^2 / 9 * 7) - 4 + 5` is the same with
    them or without, so it quietly teaches that brackets are decoration.

    `catch_mnemonic` additionally demands that the multiplication-before-
    division misreading show up. That one is a property of the SHAPE, not the
    numbers: it only surfaces when two same-tier operators share an operand, so
    only about a third of shapes can express it. Asked of one of the two
    problems, so every student meets the trap once without the shapes becoming
    repetitive.
    """
    try:
        correct = _answer(expression)
        if _answer(expression, LEFT_TO_RIGHT) == correct:
            return False
        if catch_mnemonic and _answer(expression, BY_THE_MNEMONIC) == correct:
            return False
    except ZeroDivisionError:
        return False

    if '(' not in expression:
        return True
    if ')**' in expression:
        # An exponent on a bracketed group cannot be redundant: without the
        # brackets it would land on the last term instead.
        return True
    try:
        return _answer(expression.replace('(', '').replace(')', '')) != correct
    except ZeroDivisionError:
        return True


def _one_pemdas(catch_mnemonic, attempts=60):
    for _ in range(attempts):
        template = _pemdas_template()
        usable = [(environment, result)
                  for environment, result in _solve_pemdas(template)
                  if _discriminates(_fill_in(template, environment), catch_mnemonic)]
        if not usable:
            continue
        environment, result = random.choice(usable)
        rendered = _fill_in(template, environment)
        for python, latex in (('**', '^'), ('*', r'\times'), ('/', r'\div')):
            rendered = rendered.replace(python, latex)
        return {'prob': rendered, 'ans': f'{result}'}
    raise RuntimeError(
        f'no order-of-operations problem found in {attempts} shapes '
        f'(catch_mnemonic={catch_mnemonic}); the constraints have been '
        'tightened past what the term pool can satisfy')


def pemdas_problems():
    """Two order-of-operations problems, both fraction-free at every step.

    One of the two also has to catch the mnemonic misreading, and which one is
    chosen at random so its position is not a tell.
    """
    strict_first = random.choice([True, False])
    return [_one_pemdas(catch_mnemonic=strict_first),
            _one_pemdas(catch_mnemonic=not strict_first)]


# ---------------------------------------------------------------------------
# Ordering and rounding (problems 17-20)
# ---------------------------------------------------------------------------

def ordering_problems():
    """Two lists of integers to put in order, one mixed and one all negative."""
    mixed = random.sample(range(-19, 1), 4)
    mixed[3] *= (-1) ** random.choice([0, 1])
    # `sample` draws distinct values only within a single call. The flip above
    # can turn mixed[3] positive, so the two positives are drawn from a pool
    # that leaves it out; otherwise the list asks for the same number twice.
    mixed.extend(random.sample([n for n in range(1, 20) if n != mixed[3]], 2))
    random.shuffle(mixed)

    negatives = random.sample(range(-19, 1), 6)
    random.shuffle(negatives)

    lists = [mixed, negatives]
    if random.choice([True, False]):
        lists.reverse()

    for values in lists:
        assert len(set(values)) == len(values), f'repeated value in {values}'

    return [{'prob': ', '.join(str(n) for n in values),
             'ans': ', '.join(str(n) for n in sorted(values))}
            for values in lists]


PLACE_NAMES = {-3: 'thousandths', -2: 'hundredths', -1: 'tenths',
               1: 'tens', 2: 'hundreds', 3: 'thousands'}

ROUND_MAIN = [0.1, 0.06, 0.06, 0.18, 0.18, 0.18, 0.06, 0.06, 0.06, 0.06]
ROUND_LAST = [0.07, 0.07, 0.193, 0.194, 0.193, 0.07, 0.07, 0.07, 0.07]


def rounding_parts():
    """Four numbers to round, in two groups of two.

    The digit weights lean on 3, 4 and 5 in the deciding place, so the problem
    turns on knowing the rule rather than on the digit being obviously far from
    the halfway point.
    """
    powers = random.sample(list(PLACE_NAMES), 4)
    parts = []

    for power in powers:
        extra = random.choice(range(0, 3))
        total_digits = abs(power * 2) + 3 + extra
        placement = -(abs(power) + 2) - (1 if extra == 2 else 0)

        digits = [random.choice(range(1, 9))]
        digits.extend(random.choices(MAIN_DIGITS, weights=ROUND_MAIN,
                                     k=total_digits - 2))
        digits.extend(random.choices(LAST_DIGITS, weights=ROUND_LAST, k=1))

        number = _decimal_from(digits, placement)
        if power < 0:
            answer = number.quantize(decimal.Decimal(10) ** power)
        else:
            shifted = number * (decimal.Decimal(10) ** -power)
            answer = round(shifted) * 10 ** power

        parts.append({'prob': f'{number}', 'place': PLACE_NAMES[power],
                      'ans': f'{answer}'})

    groups = [parts[:2], parts[2:]]
    for group in groups:
        for index, part in enumerate(group):
            part['letter'] = 'ab'[index]
    return groups


# ---------------------------------------------------------------------------
# CheckIt entry point
# ---------------------------------------------------------------------------

def generate():
    """All twenty problems, as the parts each template needs.

    Numbered to match the printed sheet, because the layout is fixed and the
    numbering is what an instructor and a student both refer to.
    """
    p1, p2 = addition_problems()
    p3, p6 = multiplication_problems()
    p4, p5 = subtraction_problems()
    p11, p12 = fraction_multdiv_problems()
    p13, p14 = fraction_addsub_problems()
    p15, p16 = pemdas_problems()
    p17, p18 = ordering_problems()
    p19, p20 = rounding_parts()

    data = {
        'p7_parts': integer_addition_parts(),
        'p8_parts': integer_subtraction_parts(),
        'p9_parts': integer_multiplication_parts(),
        'p10_parts': integer_division_parts(),
        'p19_parts': p19,
        'p20_parts': p20,
    }
    for number, problem in enumerate(
            [p1, p2, p3, p4, p5, p6, None, None, None, None, p11, p12,
             p13, p14, p15, p16, p17, p18], start=1):
        if problem is None:
            continue
        data[f'p{number}_prob'] = problem['prob']
        data[f'p{number}_ans'] = problem['ans']
    return data


class Generator(BaseGenerator):
    def data(self):
        return generate()
