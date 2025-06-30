import slye_math as sm
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime


def generate(**kwargs):
    def flag_dimensions():
        locations_with_adjectives = [
            ('Hyrule', 'Hylian'),
            ('Labrynna', 'Labrynnian'),
            ('Holodrum', 'Holodrumian'),
            ('Ylisse', 'Ylissean'),
            ('Altea', 'Altean'),
            ('Isle Delfino', 'Delfinian'),
            ('Tortimer Island', 'Tortimerian'),
            ('Gallia', 'Gallian'),
            ('Daein', 'Daein'),
            ('Neo Arcadia', 'Neo Arcadian'),
            ('Archanea', 'Archanean'),
            ('Magvel', 'Magvelian'),
            ('Aionios', 'Aionian'),
            ('Tethe\'alla', 'Tethe\'allan'),
            ('Sylvarant', 'Sylvaranti'),
            ('Dream Land', 'Dreamlandian'),
            ('Popstar', 'Popstarian'),
            ('Aeos Island', 'Aeosian'),
            ('New Donk City', 'New Donk City'),
            ('Inkopolis', 'Inkopolissean'),
            ('Splatsville', 'Splatlandian'),
            ('Gusty Gulch', 'Gusty Gulchian'),
            ('Zora\'s Domain', 'Zoran'),
            ('Lorule', 'Lorulian'),
            ('Termina', 'Terminian'),
            ('Valla', 'Vallite'),
            ('Norfair', 'Norfairian'),
            ('Kanto', 'Kantonian'),
            ('Johto', 'Johtonian'),
            ('Hoenn', 'Hoennian'),
            ('Sinnoh', 'Sinnohan'),
            ('Unova', 'Unovan'),
            ('Kalos', 'Kalosian'),
            ('Alola', 'Alolan'),
            ('Galar', 'Galarian'),
            ('Paldea', 'Paldean')
        ]
        
        location, proper_adjective = random.choice(locations_with_adjectives)

        ratio_width = random.randint(5, 20)
        possible_ratio_lengths = sm.rel_primes(ratio_width, start=ratio_width, stop=ratio_width*3)
        ratio_length = random.choice(possible_ratio_lengths)

        swap_length_width = random.choice([True, False])

        if swap_length_width:
            ratio_length, ratio_width = ratio_width, ratio_length

        ratio_part_and_value = [('length', ratio_length), ('width', ratio_width)]
        random.shuffle(ratio_part_and_value)

        fractional_part_denom = random.randint(1,5)

        if fractional_part_denom == 1:
            fractional_part_num = 0
        else:
            fractional_part_num = random.choice(sm.rel_primes(fractional_part_denom))

        start_dim_whole = random.randint(5, 25)
        start_dim_frac = Fraction(fractional_part_num, fractional_part_denom)
        starting_dimension = start_dim_whole + start_dim_frac

        find_given_length_width = ['length', 'width']
        random.shuffle(find_given_length_width)

        dimension_to_find, given_dimension = find_given_length_width

        to_find_num, to_find_denom = 'x', sm.mixed_number(starting_dimension, format='latex')

        answer = starting_dimension * ratio_part_and_value[0][1] / ratio_part_and_value[1][1]

        if given_dimension == ratio_part_and_value[0][0]:
            to_find_num, to_find_denom = to_find_denom, to_find_num
            answer = starting_dimension * ratio_part_and_value[1][1] / ratio_part_and_value[0][1]

        problem = (
            f"For every flag of {location}, the ratio of its {ratio_part_and_value[0][0]} to its "
            f"{ratio_part_and_value[1][0]} must be ${ratio_part_and_value[0][1]}:{ratio_part_and_value[1][1]}$. "
            f"If a {proper_adjective} flag is to be produced with a \\textbf{{{given_dimension}}} of "
            f"${sm.mixed_number(starting_dimension, format='latex')}$ ft, what should its "
            f"\\textbf{{{dimension_to_find}}} be? "
            f"Give your final answer as a mixed number, if necessary."
        )

        solution = (
            f"If we place the given ratio in a proportion with our known {given_dimension} and "
            f"unknown {dimension_to_find} (being careful to "
            f"attend to matching the order of length and width the numerators and denominators), we get "
            f"\\[ \\dfrac{{{ratio_part_and_value[0][1]}}}{{{ratio_part_and_value[1][1]}}} = "
            f"\\dfrac{{{to_find_num}}}{{{to_find_denom}}}, \\] "
            f"where $x$ is the unknown {dimension_to_find}. Solving this proportion, we get "
            f"\\[ x = {sm.mixed_number(answer, format='latex')}\\]"
        )
        return problem, solution

    def split_work():
        companies = parody_companies = [
            "Mindendo",
            "Somy",
            "Boba Cola",
            "Burger Queen",
            "Snapplegram",
            "Bizney Studios",
            "Mocrosoft",
            "Netflips",
            "QuickDonalds",
            "Gloogle",
            "Starmugs",
            "Amazoom",
            "Red Sky",
            "Blockify",
            "Twiddle",
            "Chick-fil-B",
            "Slapchat",
            "TickyTocky",
            "Faceplant",
            "Walmurt",
            "ReadIt",
            "Towny Bank",
            "Hula",
            "LinkedOut",
            "Zamzung",
            "Instagramble",
            "FedWhy",
        ]

        company = random.choice(companies)

        person_a = sm.random_person()
        person_b = sm.random_person()

        hourly_wage = Decimal(random.choice(list(range(2000, 5001, 25)))) / 100
        hourly_wage_cents = hourly_wage - int(hourly_wage)
        hourly_wage_num, hourly_wage_denom = Fraction(hourly_wage).as_integer_ratio()

        total_hours_list = list(range(40, 161))
        total_hours_list = [x for x in total_hours_list if x % hourly_wage_denom == 0]
        total_hours = random.choice(total_hours_list)
        hours_a = random.choice(list(range(15, total_hours // 2)))
        hours_b = total_hours - hours_a
        shuffle_hours = random.choice([True, False])
        if shuffle_hours:
            hours_a, hours_b = hours_b, hours_a

        total_wages = sm.format_money(total_hours * hourly_wage, currency_symbol='\\$')
        wages_a = sm.format_money(hours_a * hourly_wage, currency_symbol='\\$')
        wages_b = sm.format_money(hours_b * hourly_wage, currency_symbol='\\$')
        hourly_wage = sm.format_money(hourly_wage, currency_symbol='\\$')

        problem = (
            f"{person_a.name} and {person_b.name} just completed their contract work for the "
            f"{company} company. {person_a.name} worked a total of {hours_a} hours, while {person_b.name} worked "
            f"{hours_b} hours. For their combined work, {company} sent them {total_wages}. If they decide "
            f"that the fairest way to split the money in a way that reflects the amount of time each of them worked, "
            f"how much money will each person receive?"
        )
        solution = (
            f"One way to solve this is by finding the hourly rate for their work. Since they made a total of "
            f"{total_wages} over a collective {total_hours} hours of work, we can divide to find that they were making {hourly_wage} "
            f"per hour. Now, we can multiply this unit rate by each person's hours worked. Doing so shows us that "
            f"{person_a.name} should receive {wages_a}, and {person_b.name} should receive {wages_b}."
        )
        return problem, solution

    available_versions = [split_work] # [flag_dimensions]

    prob_sol_function = random.choice(available_versions)

    problem, solution = prob_sol_function()
    return {
        'problem': problem,
        'solution': solution,
    }