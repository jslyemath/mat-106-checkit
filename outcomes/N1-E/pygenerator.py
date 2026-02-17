import slye_math as sm
import random
import re


def generate(**kwargs):
    mode = kwargs.get('mode', 'latex')

    def mathify_sentence(s: str):
        """
        Turn a sentence with inline $...$ math into one big math-mode string
        where non-math text is wrapped in \\text{...} and $ delimiters are dropped.
        """
        # Split on any $...$ (non-greedy), keeping the delimiters in the result list
        parts = re.split(r'(\$.*?\$)', s)
        
        all_math_version = []
        for part in parts:
            if not part:
                # Skip over empty strings.
                continue
            if part.startswith('$') and part.endswith('$'):
                # math segment: drop the delimiters
                all_math_version.append(part[1:-1])
            else:
                # text segment: wrap exactly, preserving spaces
                all_math_version.append(r'\text{' + part + '}')
        return ''.join(all_math_version)

    def check_and_cast_to_int(value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def flex_mult(a, b):
        a, a_is_int = check_and_cast_to_int(a)
        b, b_is_int = check_and_cast_to_int(b)

        if a_is_int and b_is_int:
            ab = a * b
        elif a_is_int:
            if len(b) > 1:
                b = f'({b})'
            ab = str(a) + b
        elif b_is_int:
            if len(a) > 1:
                a = f'({a})'
            ab = str(b) + a
        else:
            if len(b) > 1:
                b = f'({b})'
            if len(a) > 1:
                a = f'({a})'
            ab = a + b
        return ab

    def div_statement(a=None, b=None, vocab_mode='e', default_order=True, use_not=False):
        # When a and b are integers, they will be ordered automatically for a true statement
        # Else, they will be ordered as entered
        # Use default_order=False to reverse the order in either case
        # Vocab types: 'e' - dividEs, 'o' - divisOr of, 'f' - Factor of, 'm' - Multiple of
        # use_not converts to not statement

        if a is None or b is None:
            a = int(random.randint(2, 12))
            b = a * int(random.randint(2, 12))

        else:
            a, a_is_int = check_and_cast_to_int(a)
            b, b_is_int = check_and_cast_to_int(b)
            if a_is_int and b_is_int:
                a, b = sorted([a, b])

        match vocab_mode:
            case 'e':
                connecting_string = ' does not divide ' if use_not else ' divides '
            case 'o':
                connecting_string = ' is not a divisor of ' if use_not else ' is a divisor of '
            case 'f':
                connecting_string = ' is not a factor of ' if use_not else ' is a factor of '
            case 'm':
                connecting_string = ' is not a multiple of ' if use_not else ' is a multiple of '
                a, b = b, a

        if not default_order:
            a, b = b, a

        prob = f'${a}$ {connecting_string} ${b}$'
        return prob

    vars = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n',
            'p', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def sum_statement(ans=True, last_used=[]):
        op = '+'
        available_versions_list = ['does divide', 'does not divide']
        available_versions_list = [x for x in available_versions_list if x not in last_used]
        ver = random.choice(available_versions_list)

        vocab = random.choice(['e', 'o', 'f', 'm'])
        a = random.choice(vars)
        b = random.choice([3, 4, 6, 7, 8, 9])

        int_first = random.choice([True, False])
        if int_first:
            a, b = b, a
            second_variable = random.choices([False, True], [0.7, 0.3])[0]
        else:
            second_variable = True

        if second_variable:
            if int_first:
                vars.remove(b)
                op = random.choice(['+', '-'])
            else:
                vars.remove(a)
            c = random.choice(vars)

        match ver:
            case 'does divide':
                if second_variable:
                    extra_statement = f' and {div_statement(a, c, vocab_mode=vocab)} '
                else:
                    c = int(random.randint(1, 9)) * a
                    extra_statement = ''

                prob = (f'If {div_statement(a, b, vocab_mode=vocab)}{extra_statement}, then  '
                        f'{div_statement(a, f"{b} {op} {c}", vocab_mode=vocab, use_not=not ans)}.')

            case 'does not divide':
                use_nots_hypothesis = [True, False]
                random.shuffle(use_nots_hypothesis)
                if second_variable:
                    extra_statement = (' and '
                                       f'{div_statement(a, c, vocab_mode=vocab, use_not=use_nots_hypothesis[1])}')
                else:
                    if use_nots_hypothesis[0] is True:
                        c = int(random.randint(1, 9)) * a
                    else:
                        c = random.randint(0, 8) * a + random.randint(1, a - 1)
                    extra_statement = ''
                prob = (f'If {div_statement(a, b, vocab_mode=vocab, use_not=use_nots_hypothesis[0])}'
                        f'{extra_statement}, then '
                        f'{div_statement(a, f"{b} {op} {c}", vocab_mode=vocab, use_not=ans)}.')

        return prob, ver

    def mult_statement(ans=True, already_used=[]):
        available_versions_dict = {'larger multiple': 0.4, 'smaller factor': 0.4, 'every-is': 0.2}
        if set(already_used) == set(available_versions_dict.keys()):
            available_versions_list = list(available_versions_dict.keys())
            available_versions_weights = list(available_versions_dict.values())
        if set(already_used) != set(available_versions_dict.keys()):
            available_versions_list = [x for x in available_versions_dict.keys() if x not in already_used]
            available_versions_weights = [v for k, v in available_versions_dict.items()
                                          if k in available_versions_list]
        ver = random.choices(available_versions_list, available_versions_weights)[0]

        vocab = random.choice(['e', 'o', 'f', 'm'])
        a = random.choice(vars)
        second_variable = random.choices([False, True], [0.8, 0.2])[0]

        if second_variable:
            vars.remove(a)
            b = random.choice(vars)
        else:
            b = random.choice([3, 4, 6, 7, 8, 9])

        swap = random.choice([True, False])
        if swap:
            a, b = b, a

        # By other properties dealing with prime divisors, the usual way of handling construction may
        # break in the following cases. We account for this by changing the setup slightly in these cases.
        special_case_1 = ver == 'smaller factor' and ans is False and second_variable is False and swap is True
        special_case_2 = ver == 'smaller factor' and ans is True and second_variable is False and swap is True
        special_case_3 = ver == 'larger multiple' and ans is False and second_variable is False and swap is True

        if special_case_1 or special_case_2 or special_case_3:
            if special_case_1:
                lots_of_factors = [6, 8, 12, 16, 18, 20]
            else:
                lots_of_factors = [16, 18, 20, 24, 28, 30, 32, 36, 40, 48]
            a = random.choice(lots_of_factors)
            multipliers = sm.divisors(a)
            multipliers.remove(1)
            multipliers.remove(a)
            multiplier = random.choice(multipliers)
        else:
            multiplier = int(random.randint(2, 9))

        b_mult = flex_mult(b, multiplier)

        match ver:
            case 'larger multiple':
                prob = (f'If {div_statement(a, b, vocab_mode=vocab, default_order=ans)}, then '
                        f'{div_statement(a, b_mult, vocab_mode=vocab, default_order=ans)}.')
            case 'smaller factor':
                prob = (
                    f'If {div_statement(b_mult, a, vocab_mode=vocab, default_order=ans)}, then '
                    f'{div_statement(b, a, vocab_mode=vocab, default_order=ans)}.')
            case 'every-is':
                if ans is False:
                    b, b_mult = b_mult, b
                match vocab:
                    case 'o':
                        vocab_statement = 'divisor of'
                    case 'e':
                        vocab_statement = random.choice(['divisor of', 'factor of'])
                    case 'f':
                        vocab_statement = 'factor of'
                    case 'm':
                        vocab_statement = 'multiple of'
                        prob = f'Every {vocab_statement} ${b_mult}$ is a {vocab_statement} ${b}$.'

                if vocab in ['o', 'e', 'f']:
                    prob = f'Every {vocab_statement} ${b}$ is a {vocab_statement} ${b_mult}$.'
        return prob, ver

    def sum_false():
        vocab = random.choice(['e', 'o', 'f', 'm'])
        not_ver = random.choice([True, False])
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.choice(vars)
        vars.remove(c)
        d = random.choice(vars)

        prob = (f'If {div_statement(a, c, vocab_mode=vocab, use_not=not_ver)}'
                f' and {div_statement(b, d, vocab_mode=vocab, use_not=not_ver)},'
                f' then {div_statement(f"{a + b}", f"{c} + {d}", vocab_mode=vocab, use_not=not_ver)}.')

        return prob

    def mult_false():
        vocab = random.choice(['e', 'o', 'f', 'm'])
        a = int(random.randint(2, 9))
        a_mult = int(random.randint(2, 6)) * a
        b = random.choice(vars)
        prob = (f'If {div_statement(a, b, vocab_mode=vocab)} '
                f' and {div_statement(a_mult, b, vocab_mode=vocab)}, '
                f' then {div_statement(a * a_mult, b, vocab_mode=vocab)}.')
        return prob

    already_used_mult = []
    last_used_sum = ''

    problems =[]

    if_then_answers = [False, True] + random.choices([True, False], [0.5, 0.5], k=2)
    if_then_versions = ['sum', 'mult', 'sum', 'mult']
    random.shuffle(if_then_versions)
    functype_answers = list(zip(if_then_versions, if_then_answers))
    remaining_functype_answers = functype_answers[:]

    use_an_always_false = True  # random.choices([True, False], [0.6, 0.4])[0]
    if use_an_always_false:
        if functype_answers[0][0] == 'sum':
            problems.append(sum_false())
        else:
            problems.append(mult_false())
        remaining_functype_answers = functype_answers[1:]
    for functype, ans in remaining_functype_answers:
        if functype == 'sum':
            prob, ver = sum_statement(ans=ans, last_used=last_used_sum)
            last_used_sum = ver
        else:
            prob, ver = mult_statement(ans=ans, already_used=already_used_mult)
            already_used_mult.append(ver)
        problems.append(prob)

    answers = list(map(lambda x: str(x), if_then_answers))

    prob_ans = list(zip(problems, answers))

    if mode == 'html':
        for i, entry in enumerate(prob_ans):
            entry = list(entry)
            entry[0] = mathify_sentence(entry[0])
            prob_ans[i] = tuple(entry)

    explain_prob_ans = prob_ans[0:3]

    random.shuffle(explain_prob_ans)

    return {
        'explain_prob_1': explain_prob_ans[0][0],
        'explain_ans_1': explain_prob_ans[0][1],
        'explain_prob_2': explain_prob_ans[1][0],
        'explain_ans_2': explain_prob_ans[1][1],
        'explain_prob_3': explain_prob_ans[2][0],
        'explain_ans_3': explain_prob_ans[2][1],
    }
