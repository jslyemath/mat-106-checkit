import slye_math as sm
import random
import json
from pathlib import Path


def generate(**kwargs):
    course_progress = int(kwargs['course_progress'])

    # Lists of version keys, split up by course progress cutoff points.
    # These must be the same names as those in the versions dictionary, as well as the name of the png file.

    beginning_0 = ['add-coladd-1p', 'add-lattice-1p', 'add-mental-1p', 'add-standard-1p', 'add-standard-2p']
    sub_whole_1 = ['sub-standard-1p', 'sub-trades-1p']
    mult_div_whole_2 = ['mult-lattice-1p', 'mult-partial-1p', 'mult-standard-1p', 'div-scaffold-1p', 'div-standard-1p']
    int_pemdas_3 = ['pemdas-1p', 'pemdas-2p']
    add_sub_frac_4 = ['fraction-model-1p', 'fraction-model-2p', 'fraction-model-3p']
    mult_div_frac_5 = ['decimal-model-1p']

    versions_lists = [beginning_0, sub_whole_1, mult_div_whole_2, int_pemdas_3, add_sub_frac_4, mult_div_frac_5]

    def get_available_versions(n):
        return sum(versions_lists[:n+1], [])

    versions = {
        'add-coladd-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '4234 + 3592',
                'work_desc_2': " using the column addition algorithm.",
                'incorrect': "Instead of regrouping 10 from a place value to be 1 in the next column, the student was doing a 1-for-1 trade every time.",
                'thinking': "",
                'feedback': "",
            },
        'add-lattice-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '857 + 846',
                'work_desc_2': " using the lattice algorithm.",
                'incorrect': "The student flipped the positions of the ones and tens. Additionally, they added directly down, instead of adding diagonally.",
                'thinking': "",
                'feedback': "",
            },
        'add-mental-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '37 + 48',
                'work_desc_2': " using a mental math technique.",
                'incorrect': "The student attempted something akin to equal additions (a subtraction technique), and added 2 to both addends.",
                'thinking': "",
                'feedback': "Rounding 48 up to 50 is a great strategy, but we should subtract 2 from 37 instead. This will counteract the extra 2 added from the other addend.",
            },
        'add-standard-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '247 + 386',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "The student did not carry over the 1s for regrouping above the next column, instead leaving them as part of the final answer.",
                'thinking': "",
                'feedback': "",
            },
        'add-standard-2p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '574 + 891',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "The student added from left-to-right, including performing the regroupings to the next lesser place value.",
                'thinking': "",
                'feedback': "",
            },
        'sub-standard-1p':
            {
                'work_desc_1': "The student was trying to subtract ",
                'work_math': '9023 - 4586',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "The student regrouped directly from the thousands place to the tens place. They also stated that zero minus five is five.",
                'thinking': "",
                'feedback': "",
            },
        'sub-trades-1p':
            {
                'work_desc_1': "The student was trying to subtract ",
                'work_math': '3278 - 1352',
                'work_desc_2': " using the trades first algorithm.",
                'incorrect': "The student performed all trades, whether or not they were necessary. This resulted in more than 10 in two columns, and they simply placed all the digits next to each other in the final answer.",
                'thinking': "",
                'feedback': "",
            },
        'mult-lattice-1p':
            {
                'work_desc_1': "The student was trying to multiply ",
                'work_math': '82 \\times 97',
                'work_desc_2': " using the lattice algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'mult-partial-1p':
            {
                'work_desc_1': "The student was trying to multiply ",
                'work_math': '37 \\times 54',
                'work_desc_2': " using the partial products algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'mult-standard-1p':
            {
                'work_desc_1': "The student was trying to multiply ",
                'work_math': '1324 \\times 9',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'div-scaffold-1p':
            {
                'work_desc_1': "The student was trying to divide ",
                'work_math': '4251 \\div 12',
                'work_desc_2': " using the scaffold algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'div-standard-1p':
            {
                'work_desc_1': "The student was trying to divide ",
                'work_math': '642 \\div 6',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'pemdas-1p':
            {
                'work_desc_1': "The student was trying to compute ",
                'work_math': '23-(4+2)^2',
                'work_desc_2': " using the standard order of operations.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'pemdas-2p':
            {
                'work_desc_1': "The student was trying to compute ",
                'work_math': '1 - 32 \\div 4 \\times 2',
                'work_desc_2': " using the standard order of operations.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'fraction-model-1p':
            {
                'work_desc_1': "The student was trying to model the fraction ",
                'work_math': '\\dfrac{2}{3}',
                'work_desc_2': " using a hexagon as the whole.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'fraction-model-2p':
            {
                'work_desc_1': "The student was trying to determine the fraction of the rectangle represented by the ",
                'work_math': '\\text{red}',
                'work_desc_2': " shaded portion.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'fraction-model-3p':
            {
                'work_desc_1': "The student was trying to mark the locations of ",
                'work_math': '\\frac{1}{2} \\text{ and } \\frac{1}{3}',
                'work_desc_2': " on the number line.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'decimal-model-1p':
            {
                'work_desc_1': "The student was trying to mark the locations of ",
                'work_math': '0.11 \\text{ through } 0.19',
                'work_desc_2': " on the number line.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
    }

    # Load the used versions from a JSON file
    def load_used_keys(filepath):
        if not Path(filepath).exists():  # Check if the file exists
            # Create the file if it doesn't exist
            with open(filepath, 'w') as file:
                json.dump([], file)  # Initialize with an empty list
        try:
            with open(filepath, 'r') as file:
                return json.load(file)  # Load the JSON data
        except json.JSONDecodeError:  # Handle any decoding errors
            return []  # If file exists but is empty or invalid, return empty list

    # Save the used version to a JSON file
    def save_used_keys(filepath, used_keys):
        with open(filepath, 'w') as file:
            json.dump(used_keys, file)

    used_versions_file = Path('assets/G1/used_versions.json')

    used_versions = load_used_keys(used_versions_file)
    available_by_progress = get_available_versions(course_progress)
    available_versions = [x for x in available_by_progress if x not in used_versions]
    if available_versions:
        version_name = random.choice(available_versions)
    else:
        version_name = used_versions[0]
        used_versions = used_versions[1:]

    used_versions.append(version_name)
    save_used_keys(used_versions_file, used_versions)

    version_data = versions[version_name]
    version_data['version'] = version_name

    return version_data
