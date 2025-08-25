import slye_math as sm
import random
from fractions import Fraction
import inflect
from datetime import datetime


def generate(**kwargs):
    course_progress = int(kwargs['course_progress'])
    mode = kwargs.get('mode', 'latex')

    def temperature_change():
        season = random.choice(['fall', 'winter'])
        start_time = random.randint(0, 2)
        time_1 = sm.add_hours(start_time, random.randint(2,7))
        time_2 = sm.add_hours(time_1, random.randint(2,7))
        time_3 = sm.add_hours(time_2, random.randint(2,7))

        start_temp = random.randint(-10, -1)
        fell_rose_2 = random.choice(['fell', 'rose'])
        if fell_rose_2 == 'fell':
            fell_rose_sign = -1
        else:
            fell_rose_sign = 1
        change_temp_1 = abs(start_temp) + random.randint(3,10)
        temp_2 = start_temp + change_temp_1
        change_temp_2 = random.randint(5, 12)

        doubled_tripled = random.choice(['doubled', 'tripled'])
        if doubled_tripled == 'doubled':
            multiplier = 2
        else:
            multiplier = 3
        mult_first = random.choice([True, False])

        if mult_first:
            operation_2 = doubled_tripled
            operation_3 = fell_rose_2
            phrase_2 = f"{doubled_tripled}"
            phrase_3 = f"{fell_rose_2} {change_temp_2} degrees"
            temp_3 = temp_2 * multiplier
            temp_4 = temp_3 + fell_rose_sign * change_temp_2
        else:
            operation_2 = fell_rose_2
            operation_3 = doubled_tripled
            if fell_rose_2 == 'fell':
                change_temp_2 = random.randint(1, temp_2)
            phrase_2 = f"{fell_rose_2} {change_temp_2} degrees"
            phrase_3 = f"{doubled_tripled}"
            temp_3 = temp_2 + fell_rose_sign * change_temp_2
            temp_4 = temp_3 * multiplier

        problem = (
            f"One {season} night, the temperature rose {change_temp_1} degrees between "
            f"{sm.convert_to_12_hour(start_time)} and {time_1}. By {time_2}, "
            f"the temperature {phrase_2} from what it was at {time_1}. By "
            f"{time_3}, it {phrase_3} from what it was at {time_2}. "
            f"If the temperature was ${temp_4}$ degrees at {time_3}, what was the original temperature at "
            f"{sm.convert_to_12_hour(start_time)}?"
        )

        #TODO: Make solution for temperature problem human readable.
        solution = (
            f"Start temp $= {start_temp}$\\newline "
            f"Temp2 $= {temp_2}$\\newline "
            f"Temp3 $= {temp_3}$\\newline "
            f"Temp4 $= {temp_4}$"
        )
        return problem, solution

    def travel_to_cabin():
        person = sm.random_person()
        rate = random.randint(50, 80)
        destination = random.choice(['cabin', 'lake house', 'beach house', 'villa', 'cottage'])
        start_time = random.randint(6, 18)
        start_time_military = datetime.strptime(f"{start_time}:00", "%H:%M")
        start_time_standard = sm.convert_to_12_hour(start_time_military)
        max_hours = 24 - start_time
        day_one_hours = random.randint(3, max_hours)
        day_one_distance = rate * day_one_hours
        end_time_standard = sm.add_hours(start_time_standard, day_one_hours)
        day_two_hours = random.randint(2, 10)

        # Create an inflect engine
        p = inflect.engine()

        # Function to convert integer to words
        def number_to_words(num):
            return p.number_to_words(num)

        problem = (
            f"{person.name}'s family is travelling to their {destination} for vacation. "
            f"Yesterday, they drove from {start_time_standard} to {end_time_standard}, with no stops until they made it to their hotel for the night. "
            f"In that time, they drove {day_one_distance} miles. Today {person.name}'s family continued driving at the same average speed for {number_to_words(day_two_hours)} more hours, after which they arrived at the {destination}. "
            f"During the past two days, how many miles did they travel to get to their {destination}?")

        solution = (
            f"First, we must determine their average speed. That is, we want to find how many miles they travel for each hour of driving. "
            f"Dividing the first day's distance of {day_one_distance} miles by {day_one_hours} hours gives us {rate} mph. "
            f"Now we can calculate the number of miles driven on the second day by multiplying {rate} mph by {day_two_hours} hours, "
            f"yielding {rate * day_two_hours} miles. Finally, adding together both distances gives a total of {day_one_distance + rate * day_two_hours} miles."
        )

        return problem, solution

    def contractor_selection():
        person = sm.random_person()
        contractor1_rate = random.randint(50, 80)
        rate_difference = random.randint(10, 20)
        contractor2_rate = contractor1_rate + rate_difference
        hours = random.randint(8, 24)
        contractor_1_better = random.choice([True, False])
        if contractor_1_better:
            discount = rate_difference * hours - random.randint(1, 100)
            higher_contractor = 'second'
            lower_contractor = 'first'
        else:
            discount = rate_difference * hours + random.randint(1, 100)
            higher_contractor = 'first'
            lower_contractor = 'second'

        contractor1_cost = contractor1_rate * hours
        contractor2_cost = (contractor2_rate * hours) - discount
        cost_difference = abs(contractor1_cost - contractor2_cost)

        problem = (
            f"{person.name}'s mom is trying to find a contractor to work on their house. The first contractor charges \\${contractor1_rate} per hour. "
            f"The second contractor charges \\${contractor2_rate} per hour, but {person.name}'s mom found a special deal online which will deduct \\${discount} from the total bill. "
            f"If {person.poss_adjective()} mom needs the chosen contractor to work for {hours} hours, how will the potential bills compare? Which contractor is the better deal?")

        solution = (
            f"To find the total cost for each contractor, we multiply the hourly rate by the number of hours needed. "
            f"The total cost for the first contractor is \\${contractor1_rate} per hour multiplied by {hours} hours, which equals \\${contractor1_cost}. "
            f"The total cost for the second contractor is \\${contractor2_rate} per hour multiplied by {hours} hours minus the \\${discount} discount, which equals \\${contractor2_cost}. "
            f"Therefore, the total bill will be \\${cost_difference} more if they choose the {higher_contractor} contractor. "
            f"{person.name} and {person.poss_adjective()} mom should higher the {lower_contractor} contractor.")

        return problem, solution

    def cookie_stand():
        person = sm.random_person()
        trays_initial = random.randint(15, 25)
        cookies_per_tray = random.randint(10, 15)

        initial_cookies = trays_initial * cookies_per_tray
        sold_friday = initial_cookies - random.randint(1, 20)
        extra_trays = random.randint(3, 6)

        extra_cookies = extra_trays * cookies_per_tray
        before_saturday = initial_cookies - sold_friday + extra_cookies
        remaining_cookies = random.randint(2, before_saturday // 2)
        sold_weekend = before_saturday - remaining_cookies
        sold_saturday = random.randint(20, 80) * sold_weekend // 100
        sold_sunday = sold_weekend - sold_saturday

        total_cookies = initial_cookies + extra_cookies

        problem = (
            f"{person.name} runs a small cookie stand every weekend. This weekend, {person.subj_pronoun()} started by baking {trays_initial} trays of cookies. "
            f"Each tray fits {cookies_per_tray} cookies at a time. On Friday, {person.subj_pronoun()} sold {sold_friday} cookies. So, {person.subj_pronoun()} decided to make {extra_trays} more trays of cookies on Saturday morning. "
            f"{person.subj_pronoun().capitalize()} then sold {sold_saturday} cookies on Saturday, and {sold_sunday} cookies on Sunday. {person.subj_pronoun().capitalize()} will bring the extra remaining cookies to school to share with {person.poss_adjective()} class on Monday. "
            f"How many cookies {sm.verb_switch('does', person.gender)} {person.subj_pronoun()} have to share with {person.poss_adjective()} class?")

        solution = (
            f"To find out how many cookies {person.name} has to share with {person.poss_adjective()} class, we could first calculate the total number of cookies baked. "
            f"So, {trays_initial} trays multiplied by {cookies_per_tray} cookies per tray equals {initial_cookies} cookies. "
            f"After that, {person.subj_pronoun()} baked {extra_trays} more trays of cookies, which adds another {extra_cookies} cookies. "
            f"The total number of cookies baked throughout the weekend was {total_cookies}. Adding together the cookies sold on Friday, Saturday, and Sunday, gives a total of  {sold_friday + sold_saturday + sold_sunday} cookies. "
            f"Subtracting this from the total {total_cookies} cookies cooked, there are {remaining_cookies} cookies left. Therefore, {person.name} {sm.verb_switch('has', person.gender)} {remaining_cookies} cookies to share with {person.poss_adjective()} class.")

        return problem, solution

    def christmas_decorations():
        person = sm.random_person()
        spool1 = int(random.randint(1, 6))
        spool2 = Fraction(int(random.randint(4, 15)), int(random.randint(2, 5)))
        text_spool2 = sm.mixed_number(spool2, format='plain')
        total_twine = spool1 + spool2
        denom1, denom2, denom3 = random.choices([int(2), int(3), int(4), int(5)], k=3)
        initial_percent1 = int(random.randint(10, 40))
        initial_percent2 = int(random.randint(10, 40))
        initial_percent3 = (int(100) - initial_percent1 - initial_percent2)
        roughly_enough = random.choice([True, False])
        percent_difference = int(random.randint(10, 40))
        if not roughly_enough:
            percent_difference *= int(-1)
        num1 = int(initial_percent1 * total_twine * denom1 * (percent_difference + int(100)) // int(10000))
        num2 = int(initial_percent2 * total_twine * denom2 * (percent_difference + int(100)) // int(10000) + int(1))
        num3 = int(initial_percent3 * total_twine * denom3 * (percent_difference + int(100)) // int(10000))
        project1 = Fraction(num1, denom1)
        project2 = Fraction(num2, denom2)
        project3 = Fraction(num3, denom3)
        text_project1 = sm.mixed_number(project1, format='plain')
        text_project2 = sm.mixed_number(project2, format='plain')
        text_project3 = sm.mixed_number(project3, format='plain')
        total_needed = project1 + project2 + project3
        text_total_needed = sm.mixed_number(total_needed, format='plain')
        text_total_twine = sm.mixed_number(total_twine, format='plain')
        has_enough = 'has' if total_twine >= total_needed else 'does not have'

        problem = (
            f"{person.name} is making some Christmas decorations with twine, but {person.subj_pronoun()} {sm.verb_switch('is', person.gender)} running out of twine to use! "
            f"{person.subj_pronoun().capitalize()} {sm.verb_switch('measures', person.gender)} {person.poss_adjective()} remaining twine before starting {person.poss_adjective()} projects. "
            f"{person.subj_pronoun().capitalize()} has {spool1} ft of twine on one spool, and {text_spool2} ft of twine on another spool. {person.poss_adjective().capitalize()} first project requires {text_project1} ft of twine, "
            f"{person.poss_adjective()} second project requires {text_project2} ft, and {person.poss_adjective()} third project requires {text_project3} ft. Will {person.name} have enough twine to make all three projects? Why or why not?")

        solution = (
            f"To find out if {person.name} has enough twine to complete all three projects, we first calculate the total amount of twine available. "
            f"Adding the two spools gives us {spool1} ft + {text_spool2} ft, which equals {text_total_twine} ft of twine. Then, we add up the amount of twine needed for each project. "
            f"Summing up {text_project1} ft + {text_project2} ft + {text_project3} ft gives us a total of {text_total_needed} ft of twine needed overall. "
            f"{person.name} {has_enough} enough twine to complete all three projects because {person.subj_pronoun()} needs {text_total_needed} ft and has {text_total_twine} ft on hand.")

        return problem, solution

    def walking_distance():
        person = sm.random_person()
        distance1 = Fraction(int(random.randint(1, 3)), int(random.randint(3, 5)))
        distance2 = Fraction(int(random.randint(2, 6)), int(random.randint(4, 6)))
        backtrack = Fraction(int(random.randint(1, 2)), int(random.randint(4, 8)))
        text_dist1 = sm.mixed_number(distance1, format='plain')
        text_dist2 = sm.mixed_number(distance2, format='plain')
        text_back = sm.mixed_number(backtrack, format='plain')
        total_distance = distance1 + distance2 - backtrack
        text_total = sm.mixed_number(total_distance, format='plain')

        problem = (f"{person.name} is walking down a straight road from {person.poss_adjective()} house to the market. "
                   f"{person.subj_pronoun().capitalize()} {sm.verb_switch('walks', person.gender)} {text_dist1} mi. before taking a rest. Then, {person.subj_pronoun()} {sm.verb_switch('keeps', person.gender)} walking another {text_dist2} mi. "
                   f"At that point, {person.subj_pronoun()} {sm.verb_switch('realizes', person.gender)} that {person.subj_pronoun()} already walked past the market, and {sm.verb_switch('backtracks', person.gender)} {text_back} mi. to get to the market. "
                   f"How far is it from {person.name}'s house to the market?")

        solution = (
            f"To find out the total distance from {person.name}'s house to the market, we add the distances {person.subj_pronoun()} walked and then subtract the distance {person.subj_pronoun()} backtracked. "
            f"{text_dist1} mi. plus {text_dist2} mi. equals {sm.mixed_number(distance1 + distance2, 'plain')} mi. Then, subtracting the {text_back} mi. backtracked, we get {text_total} mi. "
            f"Therefore, the total distance from {person.name}'s house to the market is {text_total} mi.")

        return problem, solution

    def can_production():
        person = sm.random_person()
        company = random.choice(['Bebsi', 'Dr. Salt', 'Koka Kora', 'Valley Dew'])
        cans_per_hour = random.randint(10000, 20000)
        cans_per_case = random.randint(20, 30)
        hours = random.randint(5, 12)
        total_cans = cans_per_hour * hours
        total_cases = total_cans // cans_per_case
        leftover_cans = total_cans % cans_per_case

        problem = (
            f"{person.name}'s family works at the {company} factory, where {cans_per_hour:,} cans of {company} are produced each hour. "
            f"The cans are packed in cases containing {cans_per_case:,} cans each. "
            f"How many cases could be filled with the cans produced in {hours} hours?")

        solution = (
            f"To find out how many cases could be filled, we first calculate the total number of cans produced in {hours} hours. "
            f"{cans_per_hour:,} cans per hour multiplied by {hours} hours equals {total_cans:,} cans. "
            f"Dividing this by {cans_per_case:,} cans per case, we get {total_cases:,} cases, with {leftover_cans:,} left over. "
            f"Therefore, {total_cases:,} cases could be filled with the cans produced in {hours} hours.")

        return problem, solution

    def buying_house():
        person = sm.random_person()
        house_price = random.randint(200000, 300000)
        down_payment = random.randint(20000, 40000)
        monthly_payments = random.randint(180, 300)

        remaining_amount = house_price - down_payment
        monthly_payment_amount = remaining_amount // monthly_payments
        final_payment = remaining_amount % monthly_payments

        problem = (
            f"{person.name}'s family is buying a new house. The agreed-upon price for the house at the time of closing is \\${house_price:,}. "
            f"The bank requires an immediate down payment of \\${down_payment:,}. The remaining amount will be paid over {monthly_payments:,} equal monthly payments, plus one more month for any remaining balance. "
            f"Assuming there is no interest involved, how much will {person.name}'s family be paying each month? Don't forget to mention the final month, in case there was a remaining balance.")

        solution = (
            f"To find out how much {person.name}'s family will need to pay each month, we first subtract the down payment from the house price to find the remaining amount. "
            f"\\${house_price:,} minus \\${down_payment:,} equals \\${remaining_amount:,}. Dividing this by {monthly_payments:,} monthly payments, we get \\${monthly_payment_amount:,} per month. "
            f"Therefore, {person.name}'s family will need to pay \\${monthly_payment_amount:,} each month for {monthly_payments} months, followed by a final payment of \\${final_payment:,}.")

        return problem, solution

    # Lists of problem generator functions, split up by course progress cutoff points.

    beginning_0 = [] #
    sub_whole_1 = []
    mult_div_whole_2 = [travel_to_cabin, contractor_selection, cookie_stand, can_production, buying_house]
    int_pemdas_3 = [temperature_change]
    add_sub_frac_4 = [christmas_decorations, walking_distance]
    mult_div_frac_5 = []

    versions_lists = [beginning_0, sub_whole_1, mult_div_whole_2, int_pemdas_3, add_sub_frac_4, mult_div_frac_5]

    def get_available_versions(n):
        return sum(versions_lists[:n + 1], [])

    available_versions = get_available_versions(course_progress)

    prob_sol_function = random.choice(available_versions)

    problem, solution = prob_sol_function()

    if mode == 'html':
        problem = problem.replace('\\', '')
        solution = solution.replace('\\', '')

    return {
        'problem': problem,
        'solution': solution,
    }
