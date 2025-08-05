import slye_math as sm
import random


def generate(**kwargs):
    mult_allowed = False
    if int(kwargs['course_progress']) > 1:
        mult_allowed = True
    item_data = (
        {
            'category': 'fruit',
            'items': ('apples', 'oranges', 'bananas'),
            'container': 'bags',
            'layout': 'a fruit stand',
            'many_cat': 'much',
            'many_it': 'many'
        },
        {
            'category': 'coins',
            'items': ('pennies', 'nickels', 'dimes', 'quarters'),
            'container': 'piles',
            'layout': 'a coin display board',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'chairs',
            'items': ('folding chairs', 'stacking chairs', 'theater chairs'),
            'container': 'stacks',
            'layout': 'an auditorium',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'building blocks',
            'items': ('LEGO', 'Duplos', 'Mega Bloks'),
            'container': 'sets',
            'layout': 'a flat starting grid',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'art supplies',
            'items': ('crayons', 'colored pencils', 'markers'),
            'container': 'boxes',
            'layout': 'an art studio',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'toy cars',
            'items': ('Matchbox cars', 'Hot Wheels cars', 'diecast cars'),
            'container': 'garages',
            'layout': 'a toy car display',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'puzzle pieces',
            'items': ('jigsaw puzzle pieces', '3D puzzle pieces', 'alphabet puzzle pieces'),
            'container': 'boxes',
            'layout': 'a puzzle table',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'cards',
            'items': ('playing cards', 'Pokémon cards', 'Uno cards'),
            'container': 'decks',
            'layout': 'a card table',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'stuffed animals',
            'items': ('teddy bears', 'plush dogs', 'toy bunnies'),
            'container': 'baskets',
            'layout': 'a toy store',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'action figures',
            'items': ('superheroes', 'soldiers', 'robots'),
            'container': 'boxes',
            'layout': 'a toy display case',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'craft materials',
            'items': ('beads', 'buttons', 'pipe cleaners'),
            'container': 'jars',
            'layout': 'a craft table',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'toy animals',
            'items': ('farm animals', 'zoo animals', 'marine animals'),
            'container': 'bins',
            'layout': 'a toy farm set',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'kitchen utensils',
            'items': ('spoons', 'forks', 'knives'),
            'container': 'drawers',
            'layout': 'a kitchen counter',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'books',
            'items': ('novels', 'notebooks', 'magazines'),
            'container': 'shelves',
            'layout': 'a library',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'office supplies',
            'items': ('staplers', 'paper clips', 'sticky notes'),
            'container': 'drawers',
            'layout': 'an office desk',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'kitchenware',
            'items': ('plates', 'cups', 'bowls'),
            'container': 'cabinets',
            'layout': 'a kitchen shelf',
            'many_cat': 'much',
            'many_it': 'many'
        },
        {
            'category': 'clothing',
            'items': ('shirts', 'pants', 'jackets'),
            'container': 'closets',
            'layout': 'a clothing rack',
            'many_cat': 'much',
            'many_it': 'many'
        },
        {
            'category': 'cleaning supplies',
            'items': ('sponges', 'cleaning cloths', 'scrub brushes'),
            'container': 'buckets',
            'layout': 'a cleaning closet',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'tools',
            'items': ('hammers', 'screwdrivers', 'wrenches'),
            'container': 'toolboxes',
            'layout': 'a workbench',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'shoes',
            'items': ('sneakers', 'boots', 'sandals'),
            'container': 'shoe racks',
            'layout': 'a shoe store display',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'pillows',
            'items': ('bed pillows', 'throw pillows', 'couch cushions'),
            'container': 'piles',
            'layout': 'a living room',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'jewelry',
            'items': ('necklaces', 'bracelets', 'rings'),
            'container': 'jewelry boxes',
            'layout': 'a jewelry display case',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'stationery',
            'items': ('pencils', 'pens', 'erasers'),
            'container': 'pencil cases',
            'layout': 'a desk',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'toys',
            'items': ('dolls', 'action figures', 'stuffed animals'),
            'container': 'toy bins',
            'layout': 'a playroom',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'sports balls',
            'items': ('basketballs', 'footballs', 'tennis balls'),
            'container': 'storage racks',
            'layout': 'a sports equipment room',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'musical instruments',
            'items': ('guitars', 'drums', 'flutes'),
            'container': 'music room storage closets',
            'layout': 'a music store display',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'garden tools',
            'items': ('rakes', 'shovels', 'pruning shears'),
            'container': 'garden sheds',
            'layout': 'a gardening area',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'drinks',
            'items': ('soda cans', 'juice boxes', 'water bottles'),
            'container': 'fridges',
            'layout': 'a kitchen counter',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'umbrellas',
            'items': ('folding umbrellas', 'golf umbrellas', 'beach umbrellas'),
            'container': 'stands',
            'layout': 'an entryway',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'batteries',
            'items': ('AA batteries', 'AAA batteries', '9-volt batteries'),
            'container': 'battery cases',
            'layout': 'a utility drawer',
            'many_cat': 'many',
            'many_it': 'many'
        },
        {
            'category': 'keys',
            'items': ('house keys', 'car keys', 'locker keys'),
            'container': 'keyrings',
            'layout': 'a key holder',
            'many_cat': 'many',
            'many_it': 'many'
        }
    )

    def addition_subtraction_prob(op=None, last_type=None):
        if op is None:
            op = random.choice(['addition', 'subtraction'])

        a = int(random.randint(2, 15))
        b = random.choice([x for x in range(2, 15) if x != a])
        c = a + b

        person_1 = sm.random_person()
        person_2 = sm.random_person(avoid=person_1)

        item_dict = random.choice(item_data)
        category = item_dict['category']
        item_1 = random.choice(item_dict['items'])
        item_2 = random.choice([x for x in item_dict['items'] if x != item_1])
        many_cat = item_dict['many_cat']
        many_it = item_dict['many_it']

        match op:
            case 'addition':
                add_probs = (('Join', 'Result Unknown'), ('Separate', 'Start Unknown'),
                             ('Part-Part-Whole', 'Whole Unknown'), ('Compare', 'Larger Quantity Unknown'))
                prob_tuple = random.choice([x for x in add_probs if x[0] != last_type])

                match prob_tuple:
                    case ('Join', 'Result Unknown'):
                        ans_text = (f'{person_1.name_cap()} had {a} {item_1}. {person_2.name_cap()} '
                                    f'gave {person_1.obj_pronoun()} {b} more. How {many_it} {item_1} does {person_1.name}'
                                    f' have now?')
                        ans_math = f'{a} + {b} = \\Box'

                    case ('Separate', 'Start Unknown'):
                        ans_text = (f'{person_1.name_cap()} had some {item_1}. '
                                    f'{person_1.subj_pronoun().capitalize()} gave {b} to {person_2.name}. '
                                    f'Now {person_1.name} has {a} {item_1} left. How {many_it} {item_1} did '
                                    f'{person_1.name} have to begin with?')
                        ans_math = f'\\Box - {b} = {a}'

                    case ('Part-Part-Whole', 'Whole Unknown'):
                        ans_text = f'{person_1.name_cap()} has {b} {item_1} and {a} {item_2}. How {many_cat} {category} {"do" if person_1.gender == "n" else "does"} {person_1.subj_pronoun()} have overall?'
                        ans_math = f'{b} + {a} = \\Box'

                    case ('Compare', 'Larger Quantity Unknown'):
                        ans_text = f'{person_2.name_cap()} has {b} more {item_1} than {person_1.name}. {person_1.name_cap()} has {a} {item_1}. How {many_it} {item_1} does {person_2.name} have?'
                        ans_math = f'{a} + {b} = \\Box'

            case 'subtraction':
                sub_probs = (('Join', 'Change Unknown'), ('Join', 'Start Unknown'), ('Separate', 'Result Unknown'),
                             ('Separate', 'Change Unknown'), ('Part-Part-Whole', 'One Part Unknown'),
                             ('Compare', 'Difference Unknown'), ('Compare', 'Smaller Quantity Unknown'))
                prob_tuple = random.choice([x for x in sub_probs if x[0] != last_type])

                match prob_tuple:
                    case ('Join', 'Change Unknown'):
                        ans_text = f'{person_1.name_cap()} had {a} {item_1}. {person_2.name_cap()} gave {person_1.obj_pronoun()} some more. Now {person_1.name} has {c} {item_1}. How {many_it} did {person_2.name} give {person_1.obj_pronoun()}?'
                        ans_math = f'{a} + \\Box = {c}'

                    case ('Join', 'Start Unknown'):
                        ans_text = f'{person_1.name_cap()} had some {item_1}. {person_2.name_cap()} gave {person_1.obj_pronoun()} {b} more. Now {person_1.name} has {c} {item_1}. How {many_it} {item_1} did {person_1.name} have to begin with?'
                        ans_math = f'\\Box + {b} = {c}'

                    case ('Separate', 'Result Unknown'):
                        ans_text = f'{person_1.name_cap()} had {c} {item_1}. {person_1.subj_pronoun().capitalize()} gave {b} {item_1} to {person_2.name}. How {many_it} {item_1} does {person_1.name} have now?'
                        ans_math = f'{c} - {b} = \\Box'

                    case ('Separate', 'Change Unknown'):
                        ans_text = f'{person_1.name_cap()} had {c} {item_1}. {person_1.subj_pronoun().capitalize()} gave some to {person_2.name}. Now {person_1.subj_pronoun()} {"have" if person_1.gender == "n" else "has"} {a} {item_1}. How {many_it} did {person_1.subj_pronoun()} give to {person_2.name}?'
                        ans_math = f'{c} - \\Box = {a}'

                    case ('Part-Part-Whole', 'One Part Unknown'):
                        ans_text = f'{person_2.name_cap()} has {c} {category}. Of those {category}, {a} are {item_1} and the rest are {item_2}. How {many_it} {item_2} does {person_2.name} have?'
                        ans_math = f'{b} + \\Box = {c}'

                    case ('Compare', 'Difference Unknown'):
                        ans_text = f'{person_2.name_cap()} has {c} {item_1}, and {person_1.name} has {a} {item_1}. How {many_it} more {item_1} does {person_2.name} have than {person_1.name}?'
                        ans_math = f'{a} + \\Box = {c}'

                    case ('Compare', 'Smaller Quantity Unknown'):
                        ans_text = f'{person_2.name_cap()} has {b} more {item_1} than {person_1.name}. If {person_2.name_cap()} has {c} {item_1}, how {many_it} {item_1} does {person_1.name} have?'
                        ans_math = f'\\Box + {b} = {c}'

        prob = f'{prob_tuple[0]} - {prob_tuple[1]}'
        return prob, ans_text, ans_math, prob_tuple[0]

    def multiplication_division_prob(op=None, last_type=None):
        if op is None:
            op = random.choice(['multiplication', 'division'])

        a = int(random.randint(3, 12))
        b = random.choice([x for x in range(3, 12) if x != a])
        c = a * b

        person_1 = sm.random_person()
        person_2 = sm.random_person(avoid=person_1)

        item_dict = random.choice(item_data)
        item = random.choice(item_dict['items'])
        container = item_dict['container']
        layout = item_dict['layout']
        many_it = item_dict['many_it']

        match op:
            case 'multiplication':
                mult_probs = (('Equal Groups', 'Product Unknown'), ('Multiplicative Comparison', 'Product Unknown'),
                              ('Array', 'Product Unknown'))
                prob_tuple = random.choice([x for x in mult_probs if x[0] != last_type])

                match prob_tuple:
                    case ('Equal Groups', 'Product Unknown'):
                        ans_text = f'{person_1.name_cap()} had {a} {container} of {item}. There are {b} {item} in each of the {container}. How {many_it} {item} does {person_1.name} have altogether?'
                        ans_math = f'{a} \\times {b} = \\Box'

                    case ('Multiplicative Comparison', 'Product Unknown'):
                        ans_text = f'{person_2.name_cap()} {"have" if person_2.gender == "n" else "has"} {b} {item}. {person_1.name_cap()} has {a} times as {many_it} {item} as {person_2.name}. How {many_it} {item} does {person_1.name} have?'
                        ans_math = f'{b} \\times {a} = \\Box'

                    case ('Array', 'Product Unknown'):
                        ans_text = f'{layout.capitalize()} has {a} rows of {item} with {b} {item} in each row. How {many_it} {item} are there?'
                        ans_math = f'{a} \\times {b} = \\Box'

            case 'division':
                div_probs = (('Equal Groups', 'Group Size Unknown'), ('Equal Groups', 'Number of Groups Unknown'),
                             ('Multiplicative Comparison', 'Group Size Unknown'), ('Multiplicative Comparison', 'Multiplier Unknown'),
                             ('Array', 'Group Size Unknown'), ('Array', 'Number of Groups Unknown'))
                prob_tuple = random.choice([x for x in div_probs if x[0] != last_type])

                match prob_tuple:
                    case ('Equal Groups', 'Group Size Unknown'):
                        ans_text = f'{person_1.name_cap()} has {c} {item}. {person_1.subj_pronoun().capitalize()} wants to distribute them evenly into {a} {container}. How {many_it} {item} should {person_1.subj_pronoun()} place in each of the {container}?'
                        ans_math = f'{c} \\div {a} = \\Box'

                    case ('Equal Groups', 'Number of Groups Unknown'):
                        ans_text = f'{person_1.name_cap()} has {c} {item}. {person_1.subj_pronoun().capitalize()} put them into {container} with {b} {item} in each. How many {container} does {person_1.name} use?'
                        ans_math = f'{b} \\times \\Box = {c}'

                    case ('Multiplicative Comparison', 'Group Size Unknown'):
                        ans_text = f'{person_1.name_cap()} has {c} {item}. {person_1.subj_pronoun().capitalize()} {"have" if person_1.gender == "n" else "has"} {a} times as {many_it} {item} as {person_2.name}. How {many_it} {item} {"do" if person_2.gender == "n" else "does"} {person_2.name} have?'
                        ans_math = f'\\Box \\times {a} = {c}'

                    case ('Multiplicative Comparison', 'Multiplier Unknown'):
                        ans_text = f'{person_1.name_cap()} has {c} {item}. {person_2.name_cap()} has only {b}. How many times as {many_it} {item} does {person_1.name} have compared to {person_2.name}?'
                        ans_math = f'{b} \\times \\Box = {c}'

                    case ('Array', 'Group Size Unknown'):
                        ans_text = f'There are {c} {item} placed in {layout} in {a} equal rows. How {many_it} {item} are in each row?'
                        ans_math = f'{c} \\div {a} = \\Box'

                    case ('Array', 'Number of Groups Unknown'):
                        ans_text = f'There are {c} {item} placed in {layout} in equal rows of {b} {item} each. How many rows are there?'
                        ans_math = f'{b} \\times \\Box = {c}'

        prob = f'{prob_tuple[0]} - {prob_tuple[1]}'
        return prob, ans_text, ans_math, prob_tuple[0]

    add_tuple = addition_subtraction_prob(op='addition')
    sub_tuple = addition_subtraction_prob(op='subtraction', last_type=add_tuple[3])

    expl_tuple_1 = random.choice([add_tuple, sub_tuple])

    if mult_allowed:
        mult_tuple = multiplication_division_prob(op='multiplication')
        div_tuple = multiplication_division_prob(op='division', last_type=mult_tuple[3])
        expl_tuple_2 = random.choice([mult_tuple, div_tuple])
        prob_tuples = [add_tuple, sub_tuple, mult_tuple, div_tuple]
    else:
        add_tuple_2 = addition_subtraction_prob(op='addition', last_type=add_tuple[3])
        sub_tuple_2 = addition_subtraction_prob(op='subtraction', last_type=sub_tuple[3])
        expl_tuple_2 = random.choice([add_tuple_2, sub_tuple_2])
        prob_tuples = [add_tuple, sub_tuple, add_tuple_2, sub_tuple_2]

    random.shuffle(prob_tuples)

    return {
        'prob_1': prob_tuples[0][0],
        'ans_text_1': prob_tuples[0][1],
        'ans_math_1': prob_tuples[0][2],
        'prob_2': prob_tuples[1][0],
        'ans_text_2': prob_tuples[1][1],
        'ans_math_2': prob_tuples[1][2],
        'prob_3': prob_tuples[2][0],
        'ans_text_3': prob_tuples[2][1],
        'ans_math_3': prob_tuples[2][2],
        'prob_4': prob_tuples[3][0],
        'ans_text_4': prob_tuples[3][1],
        'ans_math_4': prob_tuples[3][2],
        'expl_prob_1': expl_tuple_1[0],
        'expl_ans_math_1': expl_tuple_1[2],
        'expl_prob_context_1': expl_tuple_1[3],
        'expl_prob_2': expl_tuple_2[0],
        'expl_ans_math_2': expl_tuple_2[2],
        'expl_prob_context_2': expl_tuple_2[3],
    }
