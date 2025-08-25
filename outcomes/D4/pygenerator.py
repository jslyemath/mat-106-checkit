import slye_math as sm
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
import inflect
from datetime import datetime

def generate(**kwargs):
    def stock_notification():
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
        person = sm.random_person()
        up_down = random.choice(['up', 'down'])
        percent_change = Decimal(random.choice(list(range(11, 999, 1)))) / 10

        original_value = Decimal(random.choice(list(range(10000, 100000, 1)))) / 100
        change_in_value = original_value * (percent_change / 100)

        if up_down == 'up':
            new_value = original_value + change_in_value
            more_less = 'more'
            add_subtract = 'add'
            from_to = 'to'
            increase_decrease = 'increase'
        else:
            new_value = original_value - change_in_value
            more_less = 'less'
            add_subtract = 'subtract'
            from_to = 'from'
            increase_decrease = 'decrease'

        original_value = sm.format_money(original_value, currency_symbol='\\$')
        new_value = sm.format_money(new_value, currency_symbol='\\$')
        change_in_value = sm.format_money(change_in_value, currency_symbol='\\$')

        problem = (
            f"{person.name} checks {person.poss_adjective()} phone notifications. One of {person.poss_adjective()} "
            f"notifications says that the value of {company} stock went {up_down} by {percent_change}\\%. "
            f"If {person.name} originally owned {original_value} in {company} stock before this {increase_decrease}, "
            f"how much is their investment worth now?"
        )

        solution = (
            f"First, we need to find how much {more_less} {person.poss_adjective()} stock is worth. Multiplying "
            f"{original_value} by {percent_change / 100} shows us that {person.poss_adjective()} investment is worth "
            f"{change_in_value} {more_less}. If we {add_subtract} this {from_to} the original value of {original_value}, "
            f"we see that {person.poss_adjective()} investment is now worth {new_value}."
        )
        return problem, solution

    available_versions = [stock_notification]

    prob_sol_function = random.choice(available_versions)

    problem, solution = prob_sol_function()
    return {
        'problem': problem,
        'solution': solution,
    }