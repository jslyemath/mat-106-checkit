import random
import math
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, List
import re
from datetime import datetime, timedelta


def main():
    pass


def base_int_to_word(raw_int: int | str | float) -> str:
    try:
        clean_int = abs(int(float(raw_int))) 
    except (ValueError, TypeError):
        return TypeError(f'Input "{raw_int}" is not a valid number.')
    
    base_names = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thriteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty')

    return base_names[clean_int]


def add_sub_triad(op = '+', num_digits=4, base=10):
    leading_digits = []
    if op == '+':
        leading_digit_offset = 0
    else:
        leading_digit_offset = 1
        if base == 2:
            a = 0
            b = 0
        else:
            a = random.randint(1, base - 2)
            b = random.randint(0, base - a - 2)
        leading_digits = [[a, b, a+b]]

    forced_regroupings = random.randint(1, num_digits - leading_digit_offset)
    # print(f"{forced_regroupings=}")
    addends_sum = []
    for i in range(forced_regroupings):
        a = random.randint(1, base - 1)
        b = random.randint(base - a, base - 1)
        addends_sum.append([a, b, a+b])
    for i in range(num_digits - forced_regroupings - leading_digit_offset):
        if base == 2:
            a = random.randint(0, 1)
            b = random.randint(0, 1)
        else:
            a = random.randint(1, base - 1)
            b = random.randint(0, base - a - 1) if a != base-1 else 0
        addends_sum.append([a, b, a+b])

    random.shuffle(addends_sum)
    addends_sum += leading_digits
    # print(f"{addends_sum=}")

    num_a = 0
    num_b = 0
    num_c = 0
    for p, abc in enumerate(addends_sum):
        num_a += base ** p * abc[0]
        num_b += base ** p * abc[1]
        num_c += base ** p * abc[2]

    num_a = sm.base_conv(num_a, base=base, output='str')
    num_b = sm.base_conv(num_b, base=base, output='str')
    num_c = sm.str_int_base_op(num_a, num_b, '+', base)

    if op == '-':
        num_a, num_b, num_c = num_c, num_a, num_b

    return num_a, num_b, num_c


def normalize_time_str(time_str):
    """Normalize time string to a consistent format (e.g., 8:00 AM or 23:00 for 24-hour)."""
    try:
        int(time_str)
        time_str = f"{int(time_str):02}:00"
    except:
        pass
    time_str = time_str.strip().lower()

    # Check if the input is a 24-hour format like '23:00' or '09:30'
    if re.match(r'^\d{1,2}:\d{2}$', time_str):  # Matches '23:00', '09:30', etc.
        return time_str

    # Handle variations like '8p', '8pm' by inserting ':00'
    if re.match(r'^\d{1,2}[ap]m?$', time_str):  # Matches '8pm', '8p', '12am', etc.
        time_str = time_str[:-2] + ":00" + time_str[-2:]

    # Ensure there's a space between the time and 'am'/'pm'
    time_str = re.sub(r'(\d)(am|pm)', r'\1 \2', time_str)

    return time_str.upper()


def is_24_hour_format(time_str):
    """Check if the time string is in 24-hour format."""
    return re.match(r'^\d{1,2}:\d{2}$', time_str) is not None


def convert_to_24_hour(time_str):
    """Converts various time string formats (12-hour or 24-hour) to a 24-hour time."""
    time_str = str(time_str)
    normalized_time_str = normalize_time_str(time_str)

    # If already in 24-hour format, just parse it as is
    if is_24_hour_format(normalized_time_str):
        return datetime.strptime(normalized_time_str, '%H:%M')

    # Otherwise, it's a 12-hour format, so parse accordingly
    return datetime.strptime(normalized_time_str, '%I:%M %p')


def convert_to_12_hour(time_obj):
    """Converts a 24-hour datetime object, string, or int back to a 12-hour time string."""
    try:
        int(time_obj)
        time_obj = convert_to_24_hour(time_obj)
    except:
        pass

    return time_obj.strftime('%I:%M %p').lstrip('0')


def add_hours(time_str, hours):
    """Adds or subtracts hours from a given 12-hour or 24-hour formatted time string."""
    # Convert to datetime object in 24-hour format
    time_obj = convert_to_24_hour(time_str)

    # Add or subtract hours using timedelta
    new_time = time_obj + timedelta(hours=hours)

    # Convert back to 12-hour format and return
    return convert_to_12_hour(new_time)


class Person:
    def __init__(self, name, gender):
        self.name = str(name)
        self.gender = str(gender).lower()

    def info(self):
        return self.name, self.gender

    def name_cap(self):
        name = self.name
        return name.capitalize()

    def subj_pronoun(self):
        if self.gender == 'm':
            return 'he'
        elif self.gender == 'f':
            return 'she'
        elif self.gender == 'n':
            return 'they'

    def obj_pronoun(self):
        if self.gender == 'm':
            return 'him'
        elif self.gender == 'f':
            return 'her'
        elif self.gender == 'n':
            return 'them'

    def poss_adjective(self):
        if self.gender == 'm':
            return 'his'
        elif self.gender == 'f':
            return 'her'
        elif self.gender == 'n':
            return 'their'

    def poss_pronoun(self):
        if self.gender == 'm':
            return 'his'
        elif self.gender == 'f':
            return 'hers'
        elif self.gender == 'n':
            return 'theirs'

    def refl_pronoun(self):
        if self.gender == 'm':
            return 'himself'
        elif self.gender == 'f':
            return 'herself'
        elif self.gender == 'n':
            return 'themselves'


def sign(x):
    if Fraction(x).numerator == 0:
        return 0
    else:
        return int(Fraction(x) / abs(Fraction(x)))


def frac_to_latex(f, dfrac=True):
    f = Fraction(f)
    frac_type = 'dfrac' if dfrac else 'frac'
    return f'\\{frac_type}{{{f.numerator}}}{{{f.denominator}}}'


def mixed_number(f, format=None):
    sign_x = sign(f)
    f = abs(Fraction(f))
    d = f.denominator
    i = f.numerator
    w = i // d
    n = i % d
    final_whole = sign_x * w
    final_numerator = Fraction(n, d).numerator
    final_denominator = Fraction(n, d).denominator
    if f == Fraction(0, 1):
        text_final_whole = '0'
    elif final_whole == 0:
        text_final_whole = ''
    else:
        text_final_whole = f'{final_whole}'
    space = '' if text_final_whole == '' else ' '

    match format:
        case 'latex':
            if final_numerator == 0:
                final_formatted = f'{text_final_whole}'
            else:
                final_formatted = f'{text_final_whole}{space}{frac_to_latex(Fraction(n, d), dfrac=False)}'
        case 'plain':
            if final_numerator == 0:
                final_formatted = f'{text_final_whole}'
            else:
                final_formatted = f'{text_final_whole}{space}{final_numerator}/{final_denominator}'
        case _:
            final_formatted = (final_whole, final_numerator, final_denominator)
    return final_formatted


def dec(x):
    if isinstance(x, Decimal):
        return x
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    else:
        return Decimal(str(x))


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def int_string(place_values=1, excl_first=[0], excl_last=[], wt_0=None, wt_1=None, wt_2=None, wt_3=None, wt_4=None,
                wt_5=None, wt_6=None, wt_7=None, wt_8=None, wt_9=None):
    the_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    wt_list = [wt_0, wt_1, wt_2, wt_3, wt_4, wt_5, wt_6, wt_7, wt_8, wt_9]
    non_wtd = sum(1 for wt in wt_list if wt is None)
    if non_wtd == 10:
        for i in range(len(wt_list)):
            wt_list[i] = 0.1
    elif non_wtd > 0:
        wt_rem = 1 - sum(wt for wt in wt_list if wt is not None)
        wt_rem_split = wt_rem / non_wtd

        for i in range(len(wt_list)):
            if wt_list[i] is None:
                wt_list[i] = wt_rem_split

    if excl_first is None:
        excl_first = []

    if excl_last is None:
        excl_last = []

    def exclude_digits(excluded):
        if is_iterable(excluded) is False:
            excluded = [excluded]
        return list(filter(lambda w: w not in excluded, the_digits))

    first_digits = exclude_digits(excl_first)
    fd_wt_list = []
    for digit in first_digits:
        fd_wt_list.append(wt_list[digit])

    last_digits = exclude_digits(excl_last)
    ld_wt_list = []
    for digit in last_digits:
        ld_wt_list.append(wt_list[digit])

    first_digit = random.choices(first_digits, weights=fd_wt_list, k=1)
    middle_digits = random.choices(the_digits, weights=wt_list, k=place_values - 2)
    if place_values == 1:
        last_digit = []
    else:
        last_digit = random.choices(last_digits, weights=ld_wt_list, k=1)
    all_digits = first_digit + middle_digits + last_digit
    all_digits_strings = [str(digit) for digit in all_digits]

    our_int_string = ''.join(all_digits_strings)

    return our_int_string


def dec_string(dec_offset=-1, place_values=1, excl_first=[0], excl_last=[0], wt_0=None, wt_1=None, wt_2=None, wt_3=None, wt_4=None,
                wt_5=None, wt_6=None, wt_7=None, wt_8=None, wt_9=None, custom_string=None, separator=',', remove_trails=True):

    dec_offset = int(dec_offset)

    if separator is None:
        separator = ''

    if custom_string is None:
        our_int_string = int_string(place_values, excl_first, excl_last, wt_0, wt_1, wt_2, wt_3, wt_4, wt_5, wt_6, wt_7, wt_8, wt_9)
    else:
        our_int_string = str(custom_string)

    our_int_string = str(our_int_string).replace(',', '')

    # if dec_offset == 0:
    #     our_dec_string = f'{int(our_int_string):,}'
    if dec_offset < 0:
        whole_part = our_int_string
        dec_part = ''
        if '.' in our_int_string:
            whole_part, dec_part = our_int_string.split('.', 1)
        if abs(dec_offset) >= len(whole_part):
            num_extra_zeros = 1 + abs(dec_offset) - len(whole_part)
            whole_part = '0' * num_extra_zeros + whole_part
        new_dec_part = whole_part[dec_offset:] + dec_part
        if remove_trails:
            new_dec_part = new_dec_part.rstrip('0')
        new_whole_part = f'{int(whole_part[:dec_offset]):,}' if whole_part[:dec_offset] != '' else ''
        our_dec_string = new_whole_part + '.' + new_dec_part
    elif dec_offset >= 0:
        if dec_offset == 0 and remove_trails is False:
            our_dec_string = our_int_string
        elif '.' in our_int_string:
            whole_part, dec_part = our_int_string.split('.', 1)
            if dec_offset >= len(dec_part):
                num_extra_zeros = dec_offset - len(dec_part)
                our_dec_string = f'{int(whole_part + dec_part + "0" * num_extra_zeros):,}'
            else:
                our_dec_string = f'{int(whole_part + dec_part[0:dec_offset]):,}' + '.' + dec_part[dec_offset:]
        else:
            our_dec_string = f'{int(our_int_string + "0" * dec_offset):,}'

    if remove_trails:
        our_dec_string = our_dec_string.rstrip('.').replace(',', separator)
    else:
        our_dec_string = our_dec_string.replace(',', separator)

    return our_dec_string


def base_conv(original_int, base=10, output='list'):
    # https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    if original_int == 0:
        return [0]
    digits = []
    while original_int:
        digits.append(int(original_int % base))
        original_int //= base
    if output == 'str':
        if 11 <= base <= 36:
            digits = [chr(x + 55) if 10 <= x <= 35 else x for x in digits]
        elif base > 36:
            digits = [f"[{x}]" for x in digits]
        return ''.join(map(str, digits[::-1]))
    else:
        return digits[::-1]


def str_int_base_op(num1, num2, op, base):
    base = int(base)
    num1 = str(num1)
    num2 = str(num2)
    op = str(op)
    return base_conv(eval(str(int(num1, base=base)) + op + str(int(num2, base=base))), base, output='str')


def to_egyptian(num, mode='latex'):
    egy_html = ('\U000133FA', '\U00013386', '\U00013362', '\U000131BC', '\U000130AD', '\U00013190', '\U00013068')
    egy_latex = ('\\Hone', '\\Hten', '\\Hhundred', '\\Hthousand', '\\HXthousand', '\\HCthousand', '\\Hmillion')
    egy_powers = []

    if mode == 'html':
        egy_powers = egy_html
    else:
        egy_powers = egy_latex

    egyptian_list = []

    rev_digits = str(num)[::-1]
    for ten_power, digit in enumerate(rev_digits):
        digit = int(digit)
        for i in range(0, digit):
            egyptian_list += [egy_powers[ten_power]]

    return ''.join(egyptian_list)


def to_simple_babylonian(num, mode='latex'):
    base_60 = base_conv(num, 60)

    bab_html_zero = '\U000120F5'
    bab_html = ('\U00012079', '\U0001230B')

    bab_latex_zero = '\\babz'
    bab_latex = ('\\babo', '\\babt')

    bab_zero = '0'
    bab_powers = []

    if mode == 'html':
        bab_zero = bab_html_zero
        bab_powers = bab_html
    else:
        bab_zero = bab_latex_zero
        bab_powers = bab_latex

    babylonian_list = []

    for index, value in enumerate(base_60):
        if index != 0:
            babylonian_list += ['\\hspace{30pt}']
        if value == 0 and index != 0:
            babylonian_list += [bab_zero]
        else:
            current_numeral = []
            rev_digits = str(value)[::-1]
            for ten_power, digit in enumerate(rev_digits):
                digit = int(digit)
                for i in range(0, digit):
                    current_numeral += [bab_powers[ten_power]]
            babylonian_list += ''.join(current_numeral[::-1])

    return ''.join(babylonian_list)


def to_roman(num):
    # https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
    num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
               (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    roman = ''
    while num > 0:
        for i, r in num_map:
            while num >= i:
                roman += r
                num -= i
    return roman


def samples(population, weights=None, k=1, rng=random):
    # https://maxhalford.github.io/blog/weighted-sampling-without-replacement/
    # https://stackoverflow.com/questions/26785354/normalizing-a-list-of-numbers-in-python
    if weights is None:
        weights = []
        weights += len(population) * [1]
    normed_weights = [float(i)/sum(weights) for i in weights]
    v = [rng.random() ** (1 / w) for w in normed_weights]
    order = sorted(range(len(population)), key=lambda i: v[i])
    return [population[i] for i in order[-k:]]


def constrained_weak_composition(n, k, min_elem, max_elem):
    # https://stackoverflow.com/questions/58915599/generate-restricted-weak-integer-compositions-or-partitions-of-an-integer-n-in
    allowed = range(max_elem, min_elem-1, -1)

    def helper(n, k, t):
        if k == 0:
            if n == 0:
                yield t
        elif k == 1:
            if n in allowed:
                yield t + [n]
        elif min_elem * k <= n <= max_elem * k:
            for v in allowed:
                yield from helper(n - v, k - 1, t + [v])

    full_list = list(helper(n, k, []))

    return random.choice(full_list)


def list_intersect(list_a, list_b):
    # https://stackoverflow.com/a/45313655
    set_intersection = set(list_a).intersection(set(list_b))
    list_intersection = []
    for i in set_intersection:
        num = min(list_a.count(i), list_b.count(i))
        for j in range(num):
            list_intersection.append(i)
    return sorted(list_intersection)


def readable_list(seq: List[Any]) -> str:
    # https://stackoverflow.com/a/53981846
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return ' and '.join(seq)
    return ', '.join(seq[:-1]) + ', and ' + seq[-1]


def rel_primes(n, start=None, stop=None, include_1=True):
    n = abs(int(n))
    if start is None:
        start = 1
    if stop is None:
        stop = n
    if start > stop:
        raise ValueError("Parameter 'start' must be less than or equal to parameter 'stop'.")
    if n == 0:
        return None
    rel_primes_list = []
    if n == 1 and stop == 1:
        if include_1:
            return [1]
        else:
            return None
    for i in range(start, stop + 1):
        if math.gcd(n, i) == 1:
            rel_primes_list.append(i)
    if not include_1 and 1 in rel_primes_list:
        rel_primes_list.remove(1)
    return rel_primes_list


def divisors(n):
    n = abs(int(n))
    if n == 0:
        return None
    divisors_list = []
    if n == 1:
        return [1]
    for i in range(1, n//2 + 1):
        if n % i == 0:
            divisors_list.append(i)
    divisors_list.append(n)
    return divisors_list


def random_person(gender=None, avoid=[]):
    if not is_iterable(avoid):
        avoid = [avoid]
    avoid_names = []
    for x in avoid:
        if isinstance(x, Person):
            avoid_names.append(x.name)
        else:
            avoid_names.append(str(x))
    names_and_genders = (('Noah', 'm'), ('Liam', 'm'), ('Jacob', 'm'), ('William', 'm'), ('Mason', 'm'), ('Ethan', 'm'), ('Michael', 'm'), ('Alexander', 'm'), ('James', 'm'), ('Elijah', 'm'), ('Benjamin', 'm'), ('Daniel', 'm'), ('Aiden', 'm'), ('Logan', 'm'), ('Jayden', 'm'), ('Matthew', 'm'), ('Lucas', 'm'), ('David', 'm'), ('Jackson', 'm'), ('Joseph', 'm'), ('Anthony', 'm'), ('Samuel', 'm'), ('Joshua', 'm'), ('Gabriel', 'm'), ('Andrew', 'm'), ('John', 'm'), ('Christopher', 'm'), ('Oliver', 'm'), ('Dylan', 'm'), ('Carter', 'm'), ('Isaac', 'm'), ('Luke', 'm'), ('Henry', 'm'), ('Owen', 'm'), ('Ryan', 'm'), ('Nathan', 'm'), ('Wyatt', 'm'), ('Caleb', 'm'), ('Sebastian', 'm'), ('Jack', 'm'), ('Christian', 'm'), ('Jonathan', 'm'), ('Julian', 'm'), ('Landon', 'm'), ('Levi', 'm'), ('Isaiah', 'm'), ('Hunter', 'm'), ('Aaron', 'm'), ('Thomas', 'm'), ('Charles', 'm'), ('Eli', 'm'), ('Jaxon', 'm'), ('Connor', 'm'), ('Nicholas', 'm'), ('Jeremiah', 'm'), ('Grayson', 'm'), ('Cameron', 'm'), ('Brayden', 'm'), ('Adrian', 'n'), ('Evan', 'm'), ('Jordan', 'n'), ('Josiah', 'm'), ('Angel', 'm'), ('Robert', 'm'), ('Gavin', 'm'), ('Tyler', 'm'), ('Austin', 'm'), ('Colton', 'm'), ('Jose', 'm'), ('Dominic', 'm'), ('Brandon', 'm'), ('Ian', 'm'), ('Lincoln', 'm'), ('Hudson', 'm'), ('Kevin', 'm'), ('Zachary', 'm'), ('Adam', 'm'), ('Mateo', 'm'), ('Jason', 'm'), ('Chase', 'm'), ('Nolan', 'm'), ('Ayden', 'm'), ('Cooper', 'm'), ('Parker', 'n'), ('Xavier', 'm'), ('Asher', 'm'), ('Carson', 'm'), ('Jace', 'm'), ('Easton', 'm'), ('Justin', 'm'), ('Leo', 'm'), ('Bentley', 'm'), ('Jaxson', 'm'), ('Nathaniel', 'm'), ('Blake', 'm'), ('Elias', 'm'), ('Theodore', 'm'), ('Kayden', 'm'), ('Luis', 'm'), ('Tristan', 'm'), ('Ezra', 'm'), ('Bryson', 'm'), ('Juan', 'm'), ('Brody', 'm'), ('Vincent', 'm'), ('Micah', 'm'), ('Miles', 'm'), ('Santiago', 'm'), ('Cole', 'm'), ('Ryder', 'm'), ('Carlos', 'm'), ('Damian', 'm'), ('Leonardo', 'm'), ('Roman', 'm'), ('Max', 'm'), ('Sawyer', 'm'), ('Jesus', 'm'), ('Diego', 'm'), ('Greyson', 'm'), ('Alex', 'm'), ('Maxwell', 'm'), ('Axel', 'm'), ('Eric', 'm'), ('Wesley', 'm'), ('Declan', 'm'), ('Giovanni', 'm'), ('Ezekiel', 'm'), ('Braxton', 'm'), ('Ashton', 'm'), ('Ivan', 'm'), ('Hayden', 'n'), ('Camden', 'm'), ('Silas', 'm'), ('Bryce', 'm'), ('Weston', 'm'), ('Harrison', 'm'), ('Jameson', 'm'), ('George', 'm'), ('Antonio', 'm'), ('Timothy', 'm'), ('Kaiden', 'm'), ('Jonah', 'm'), ('Everett', 'm'), ('Miguel', 'm'), ('Steven', 'm'), ('Richard', 'm'), ('Emmett', 'm'), ('Victor', 'm'), ('Kaleb', 'm'), ('Kai', 'm'), ('Maverick', 'm'), ('Joel', 'm'), ('Bryan', 'm'), ('Maddox', 'm'), ('Kingston', 'm'), ('Aidan', 'm'), ('Patrick', 'm'), ('Edward', 'm'), ('Emmanuel', 'm'), ('Jude', 'm'), ('Preston', 'm'), ('Alejandro', 'm'), ('Luca', 'm'), ('Bennett', 'm'), ('Jesse', 'm'), ('Jaden', 'm'), ('Colin', 'm'), ('Malachi', 'm'), ('Kaden', 'm'), ('Jayce', 'm'), ('Alan', 'm'), ('Marcus', 'm'), ('Kyle', 'm'), ('Brian', 'm'), ('Ryker', 'm'), ('Grant', 'm'), ('Abel', 'm'), ('Jeremy', 'm'), ('Riley', 'n'), ('Calvin', 'm'), ('Brantley', 'm'), ('Caden', 'm'), ('Oscar', 'm'), ('Abraham', 'm'), ('Brady', 'm'), ('Sean', 'm'), ('Jake', 'm'), ('Tucker', 'm'), ('Nicolas', 'm'), ('Mark', 'm'), ('Amir', 'm'), ('Avery', 'n'), ('King', 'm'), ('Gael', 'm'), ('Kenneth', 'm'), ('Bradley', 'm'), ('Cayden', 'm'), ('Xander', 'm'), ('Graham', 'm'), ('Paul', 'm'), ('Emma', 'f'), ('Olivia', 'f'), ('Sophia', 'f'), ('Isabella', 'f'), ('Ava', 'f'), ('Mia', 'f'), ('Abigail', 'f'), ('Emily', 'f'), ('Charlotte', 'f'), ('Madison', 'f'), ('Elizabeth', 'f'), ('Amelia', 'f'), ('Evelyn', 'f'), ('Ella', 'f'), ('Chloe', 'f'), ('Harper', 'f'), ('Sofia', 'f'), ('Grace', 'f'), ('Addison', 'f'), ('Victoria', 'f'), ('Lily', 'f'), ('Natalie', 'f'), ('Aubrey', 'f'), ('Zoey', 'f'), ('Lillian', 'f'), ('Hannah', 'f'), ('Layla', 'f'), ('Brooklyn', 'f'), ('Scarlett', 'f'), ('Zoe', 'f'), ('Camila', 'f'), ('Samantha', 'f'), ('Leah', 'f'), ('Aria', 'f'), ('Savannah', 'f'), ('Audrey', 'f'), ('Anna', 'f'), ('Allison', 'f'), ('Gabriella', 'f'), ('Hailey', 'f'), ('Claire', 'f'), ('Penelope', 'f'), ('Aaliyah', 'f'), ('Sarah', 'f'), ('Nevaeh', 'f'), ('Kaylee', 'f'), ('Stella', 'f'), ('Mila', 'f'), ('Nora', 'f'), ('Ellie', 'f'), ('Bella', 'f'), ('Lucy', 'f'), ('Alexa', 'f'), ('Arianna', 'f'), ('Violet', 'f'), ('Ariana', 'f'), ('Genesis', 'f'), ('Alexis', 'f'), ('Eleanor', 'f'), ('Maya', 'f'), ('Caroline', 'f'), ('Peyton', 'f'), ('Skylar', 'f'), ('Madelyn', 'f'), ('Serenity', 'f'), ('Kennedy', 'f'), ('Taylor', 'f'), ('Alyssa', 'f'), ('Autumn', 'f'), ('Paisley', 'f'), ('Ashley', 'f'), ('Brianna', 'f'), ('Sadie', 'f'), ('Naomi', 'f'), ('Kylie', 'f'), ('Julia', 'f'), ('Sophie', 'f'), ('Mackenzie', 'f'), ('Eva', 'f'), ('Gianna', 'f'), ('Luna', 'f'), ('Katherine', 'f'), ('Hazel', 'f'), ('Khloe', 'f'), ('Ruby', 'f'), ('Piper', 'f'), ('Melanie', 'f'), ('Lydia', 'f'), ('Aubree', 'f'), ('Madeline', 'f'), ('Aurora', 'f'), ('Faith', 'f'), ('Alexandra', 'f'), ('Alice', 'f'), ('Kayla', 'f'), ('Jasmine', 'f'), ('Maria', 'f'), ('Annabelle', 'f'), ('Lauren', 'f'), ('Reagan', 'f'), ('Elena', 'f'), ('Rylee', 'f'), ('Isabelle', 'f'), ('Bailey', 'f'), ('Eliana', 'f'), ('Sydney', 'f'), ('Makayla', 'f'), ('Cora', 'f'), ('Morgan', 'f'), ('Natalia', 'f'), ('Kimberly', 'f'), ('Vivian', 'f'), ('Quinn', 'f'), ('Valentina', 'f'), ('Andrea', 'f'), ('Willow', 'f'), ('Clara', 'f'), ('London', 'f'), ('Jade', 'f'), ('Liliana', 'f'), ('Jocelyn', 'f'), ('Trinity', 'f'), ('Kinsley', 'f'), ('Brielle', 'f'), ('Mary', 'f'), ('Molly', 'f'), ('Hadley', 'f'), ('Delilah', 'f'), ('Emilia', 'f'), ('Josephine', 'f'), ('Brooke', 'f'), ('Lilly', 'f'), ('Ivy', 'f'), ('Adeline', 'f'), ('Payton', 'f'), ('Lyla', 'f'), ('Isla', 'f'), ('Jordyn', 'f'), ('Paige', 'f'), ('Isabel', 'f'), ('Mariah', 'f'), ('Mya', 'f'), ('Nicole', 'f'), ('Valeria', 'f'), ('Destiny', 'f'), ('Rachel', 'f'), ('Ximena', 'f'), ('Emery', 'f'), ('Everly', 'f'), ('Sara', 'f'), ('Angelina', 'f'), ('Adalynn', 'f'), ('Kendall', 'f'), ('Reese', 'f'), ('Aliyah', 'f'), ('Margaret', 'f'), ('Juliana', 'f'), ('Melody', 'f'), ('Amy', 'f'), ('Eden', 'f'), ('Mckenzie', 'f'), ('Laila', 'f'), ('Vanessa', 'f'), ('Ariel', 'f'), ('Gracie', 'f'), ('Valerie', 'f'), ('Adalyn', 'f'), ('Brooklynn', 'f'), ('Gabrielle', 'f'), ('Kaitlyn', 'f'), ('Athena', 'f'), ('Elise', 'f'), ('Jessica', 'f'), ('Adriana', 'f'), ('Leilani', 'f'), ('Ryleigh', 'f'), ('Daisy', 'f'), ('Nova', 'f'), ('Norah', 'f'), ('Eliza', 'f'), ('Rose', 'f'), ('Rebecca', 'f'), ('Michelle', 'f'), ('Alaina', 'f'), ('Catherine', 'f'), ('Londyn', 'f'), ('Summer', 'f'), ('Lila', 'f'), ('Jayla', 'f'), ('Katelyn', 'f'), ('Daniela', 'f'), ('Harmony', 'f'), ('Amaya', 'f'), ('Alana', 'f'), ('Emerson', 'f'), ('Julianna', 'f'), ('Cecilia', 'f'), ('Izabella', 'f'))
    name, gender = random.choice([x for x in names_and_genders if (gender is None or x[1] == gender) and x[0] not in avoid_names])
    person = Person(name, gender)
    return person


def format_money(amount, currency_symbol='$'):
    amount = Decimal(amount)
    if amount == amount.to_integral_value():
        return f"{currency_symbol}{int(amount)}"
    else:
        return f"{currency_symbol}{amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"


def verb_switch(v, g):
    singular = False if g == 'n' or g == 'p' else True
    # Looks for pairs (tuples, lists, etc.). Returns left if singular, right if plural.
    if len(v) == 2 and not isinstance(v, str):
        return v[0] if singular else v[1]

    # Allowable non-pair special verbs
    special_verb_singular_plural = (('is', 'are'), ('does', 'do'), ('has', 'have'))
    for vs, vp in special_verb_singular_plural:
        if v == vs or v == vp:
            if singular:
                return vs
            else:
                return vp

    # Other non-pairs will have 's' shaved off/added on
    if singular:
        common_verb = v + 's' if v[-1] != 's' else v
    else:
        common_verb = v[:-1] if v[-1] == 's' else v
    return common_verb


if __name__ == "__main__":
    main()