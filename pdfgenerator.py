import csv
import importlib
import os
import random
import re
import subprocess
import sys
import tkinter as tk

from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox

from jinja2 import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf


def load_csv(filename):
    """Load the CSV file into a list of rows."""
    with open(filename, mode='r') as file:
        return list(csv.reader(file))


def get_named_value(array_data, name, direction):
    # Map direction to row and column index offsets
    direction_map = {
        'above': (-1, 0), 'up': (-1, 0),
        'below': (1, 0), 'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    row_offset, col_offset = direction_map.get(direction.lower(), (0, 0))

    for i, row in enumerate(array_data):
        for j, cell in enumerate(row):
            if cell == name:
                target_row = i + row_offset
                target_col = j + col_offset
                if 0 <= target_row < len(array_data) and 0 <= target_col < len(array_data[target_row]):
                    return array_data[target_row][target_col]
                else:
                    return None
    return None


def get_named_range(array_data, name, direction=None, height=None, width=None, filter_blanks=False):
    direction_map = {
        'below': (1, 0), 'down': (1, 0),
        'right': (0, 1)
    }

    start_row, start_col = None, None

    for i, row in enumerate(array_data):
        for j, cell in enumerate(row):
            if cell == name:
                row_offset, col_offset = direction_map.get(direction, (0, 0))
                start_row = i + row_offset
                start_col = j + col_offset
                break
        if start_row is not None:
            break

    if start_row is None or start_col is None:
        return []

    if width is None:
        width = 0
        while (start_col + width < len(array_data[start_row]) and
               array_data[start_row][start_col + width] != ''):
            width += 1

    if height is None:
        height = 0
        while (start_row + height < len(array_data) and
               array_data[start_row + height][start_col] != ''):
            height += 1

    range_2d = []
    for r in range(start_row, start_row + height):
        row_data = array_data[r][start_col:start_col + width]
        if filter_blanks:
            row_data = [x for x in row_data if x != '']
        range_2d.append(row_data)

    return range_2d


def count_2d(array, term):
    count = 0
    for row in array:
        for cell in row:
            if cell == term:
                count += 1
    return count


def sanitize_filename(filename):
    # Define a regex pattern that matches any character not allowed in Windows filenames
    banned_chars = r'[<>:"/\\|?*]'

    # Replace banned characters with '_'
    sanitized_filename = re.sub(banned_chars, '_', filename)

    # Remove leading/trailing spaces and dots, as they are also problematic
    sanitized_filename = sanitized_filename.strip().strip('.')

    return sanitized_filename


root = tk.Tk()
root.withdraw()

# Prompt user for CSV location and load the data
csv_data_path = filedialog.askopenfilename()
if not csv_data_path:
    root.destroy()
    sys.exit()
data = load_csv(csv_data_path)

# Get raw forms for relevant variables from data
title = get_named_value(data, 'Title:', 'right')
include_names_raw = get_named_value(data, 'Include Names:', 'right')
date = get_named_value(data, 'Date:', 'right')
submission_cutoff = get_named_value(data, 'Submission Cutoff:', 'right')
key_amount = get_named_value(data, 'Key Amount:', 'right')
seed_override_raw = get_named_value(data, 'Seed Override:', 'right')
pdf_location_raw = get_named_value(data, 'PDF Location:', 'right')
course = get_named_value(data, 'Course:', 'right')
semester = get_named_value(data, 'Semester:', 'right')
professor = get_named_value(data, 'Professor:', 'right')
course_progress_raw = get_named_value(data, 'G1, G2, W3, W4, F4:', 'below')
w6_allow_terminating_raw = get_named_value(data, 'W6:', 'below')
n3_n4_force_listing_method_raw = get_named_value(data, 'N3, N4:', 'below')
d2_allow_repeating_raw = get_named_value(data, 'D2:', 'below')
full_title = f'{title} {date}'

# Handle and create default directories/file paths
main_dir = Path(__file__).resolve().parent
default_pdf_dir = main_dir / 'PDF Files'
default_pdf_dir.mkdir(exist_ok=True)
tex_files_dir = main_dir / 'TeX Files'
tex_files_dir.mkdir(exist_ok=True)
main_template = main_dir / 'main_template.tex'
sty_file = tex_files_dir / 'skillcheckpoints.sty'
skill_list_csv = main_dir / 'Skill List.csv'
skill_list_tex = tex_files_dir / 'Skill Descriptions.tex'

full_title_filename = f'{sanitize_filename(full_title)}'
pdf_path = default_pdf_dir / f'{full_title_filename}.pdf'
main_tex_file_path = tex_files_dir / f'{full_title_filename}.tex'
pdf_location_choice = pdf_location_raw.split(' ')[0].casefold()
if pdf_location_choice == 'choose'.casefold():
    pdf_path = Path(filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=(("PDF file", "*.pdf"), ("All Files", "*.*"))))


if not main_template.exists():
    messagebox.showerror('Missing Template', 'Main LaTeX template is missing. Aborting program.')
    root.destroy()
    sys.exit()

# Ask for skill list csv if it doesn't exist
if not skill_list_csv.exists():
    messagebox.showinfo('Skill List Needed', 'Please select the csv file containing the relevant skills descriptions. '
                                             'The skills and descriptions should be in a two-column format, '
                                             'with headers "Skill:" and "Description:".')
    skill_list_import = filedialog.askopenfilename()
    if not skill_list_import:
        root.destroy()
        sys.exit()
    skill_list_data = load_csv(skill_list_import)

    skill_list_tex.touch(exist_ok=False)

    skill_array_data = get_named_range(skill_list_data, 'Skill:', direction='below', height=None, width=2)
    skill_array_data = [row + 'm' for row in skill_array_data]
    assoc_skill_array_data = []
    if 'Associated Skill:' in skill_list_data[0]:
        assoc_skill_array_data = get_named_range(skill_list_data, 'Associated Skill:',
                                                 direction='below', height=len(skill_list_data)-1, width=2)
        assoc_skill_array_data = [x + ['a'] for x in assoc_skill_array_data if x[0]]
    with skill_list_csv.open(mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(skill_array_data)
        if assoc_skill_array_data:
            writer.writerows(assoc_skill_array_data)
    with skill_list_tex.open(mode='w') as file:
        for skill_row in skill_array_data:
            file.write(f'\\setskilldesc{{{skill_row[0]}}}{{{skill_row[1]}}}\n')
        for skill_row in assoc_skill_array_data:
            file.write(f'\\setskilldesc{{{skill_row[0]}}}{{{skill_row[1]}}}\n')

# Load skills for later, and create folders for future TeX file generation
skill_array = [row[:2] for row in load_csv(skill_list_csv) if row[2] == 'm']
skill_dict = {sk: {'dsc': de, 'gen': f'{sk}_generator', 'tpl': f'{sk}_template.tex'} for sk, de in skill_array}
skills = list(skill_dict)
for skill in skills:
    skill_tex_gen_dir = tex_files_dir / skill
    skill_tex_gen_dir.mkdir(exist_ok=True)
    # template_path = main_dir / f'{skill}_template.tex'
    # template_path.touch(exist_ok=True)
    # generator_path = main_dir / f'{skill}_generator.py'
    # generator_path.touch(exist_ok=True)

# Set remaining variables from raw data
include_names = True
if include_names_raw[0].casefold() in ('n'.casefold(), 'f'.casefold()):
    include_names = False

save_as_dialog = False
if 'default'.casefold() not in pdf_location_raw.casefold():
    save_as_dialog = True


# Save settings to settings dictionary, which will be passed to the generator functions
course_progress = int(course_progress_raw[0])
w6_allow_terminating = True if w6_allow_terminating_raw.casefold() == 'TRUE'.casefold() else False
d2_allow_repeating = True if d2_allow_repeating_raw.casefold() == 'TRUE'.casefold() else False
n3_n4_force_listing_method = True if n3_n4_force_listing_method_raw.casefold() == 'TRUE'.casefold() else False
settings = {k: v for k, v in locals().items() if k in ['course_progress',
                                                       'w6_allow_terminating',
                                                       'n3_n4_force_listing_method',
                                                       'd2_allow_repeating']}

full_choices_array = get_named_range(data, 'Full Name:')
sec_col_index = 3
var_col_index = 4
first_choice_col_index = 5
for col_index, item in enumerate(full_choices_array[0]):
    if item == 'Sec:':
        sec_col_index = col_index
    elif item == 'Var:':
        var_col_index = col_index
    elif item == '1:':
        first_choice_col_index = col_index
variants = list({x[var_col_index] for x in full_choices_array[1:]})
# Set seeds
seeds = []
variant_dict = {}
possible_seeds = list(range(10000, 100000))
if seed_override_raw == '':
    seeds = [0] * len(variants)
    for i, variant in enumerate(variants):
        seeds[i] = random.choice(possible_seeds)
        possible_seeds.remove(seeds[i])
        variant_dict[variant] = seeds[i]
else:
    seeds = [int(seed_override_raw)]
    for variant in variants:
        variant_dict[variant] = seeds[0]

chosen_skills_array = get_named_range(full_choices_array, '1:', direction='below', width=100, filter_blanks=True)
chosen_skills = list({sk for row in chosen_skills_array for sk in row})

# create a jinja2 environment with latex-compatible markup and instantiate a template
env = make_env(loader=FileSystemLoader('.'))

# Convert main_template to a relative path
relative_main_template_path = main_template.relative_to(main_dir)
loaded_main_template = env.get_template(str(relative_main_template_path))

main_var_dict = {k: v for k, v in locals().items() if k in ['course', 'semester', 'professor', 'full_title']}

# Build PDF
main_document = loaded_main_template.render(main_var_dict)
for skill in chosen_skills:
    if skill in skills:
        generator_name = skill_dict[skill]['gen']
        current_generator = importlib.import_module(generator_name)

        template_name = skill_dict[skill]['tpl']
        current_template = main_dir / template_name
        relative_template_path = current_template.relative_to(main_dir)
        loaded_current_template = env.get_template(str(relative_template_path))

        for current_seed in seeds:
            random.seed(current_seed)
            settings['seed'] = current_seed
            generated_skill_data = current_generator.generate(**settings)
            generated_skill_data['seed'] = current_seed
            variant_text = loaded_current_template.render(generated_skill_data)

            variant_path = tex_files_dir / f'{skill}' / f'{skill} v{current_seed}.tex'
            variant_path.write_text(variant_text, encoding='utf-8')

# Build student versions
student_text = ''
used_versions = set()
for row in full_choices_array[1:]:
    student_name = row[0]
    student_section = row[sec_col_index]
    if student_section == '':
        student_section = 'blank'
    student_variant = row[var_col_index]
    student_seed = variant_dict[student_variant]
    student_choices = [x for x in row[first_choice_col_index:] if len(str(x).strip(' ')) >= 1]

    student_text += (f'\\setname{{{student_name}}}\n'
                     f'\\setsect{{{student_section}}}\n')

    for student_choice in student_choices:
        choice_tex_path = f'{student_choice}/{student_choice} v{student_seed}'
        student_text += f'\\skillpage{{{choice_tex_path}}}\n'
        used_versions.add(choice_tex_path)

    student_text += '\n'

# Build answer key versions
sorted_used_versions = sorted(list(used_versions), key=lambda x: (skills.index(x[:2]), x))
key_name = 'Key'
key_section = 'Blank'
key_text = ('\\setboolean{anstoggle}{true}\n'
            f'\\setname{{{key_name}}}\n'
            f'\\setsect{{{key_section}}}\n')
if int(key_amount) > 0:
    for used_version in sorted_used_versions:
        key_text += f'\\skillpage{{{used_version}}}\n'
    key_text += key_text*(int(key_amount) - 1)


beginning, ending = main_document.split('% Student copies')
main_document = beginning + student_text + ending
beginning, ending = main_document.split('% Keys')
main_document = beginning + key_text + ending

pdf = build_pdf(main_document, texinputs=[str(tex_files_dir), str(main_dir), ''])
pdf.save_to(pdf_path)

main_document = main_document.replace(f'{tex_files_dir.stem}/', '')
main_tex_file_path.write_text(main_document, encoding='utf-8')

# Detect the OS and open the newly created PDF file accordingly
if os.name == 'nt':  # For Windows
    os.startfile(pdf_path)
elif os.name == 'posix':  # For Unix-based systems (Linux, macOS)
    subprocess.run(['open', pdf_path.resolve()], check=True)
else:
    raise OSError('Unsupported operating system')
