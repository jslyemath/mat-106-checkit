import csv
import importlib
import importlib.util
import os
import random
import re
import shutil
import subprocess
import sys
import tkinter as tk
import xml.etree.ElementTree as ET

from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox

from jinja2 import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf
from latex.exc import LatexBuildError


def load_csv(filename: str | Path) -> list[list[str]]:
    """Load the CSV file into a list of rows (safe on Windows)."""
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
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
print(f"✅ Loaded CSV: '{Path(csv_data_path).name}' ({len(data)} total rows)")

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
course_progress_raw = get_named_value(data, 'R1, R2, W3, W4, F4:', 'below')
w7_allow_terminating_raw = get_named_value(data, 'W6:', 'below')
n3_n4_force_listing_method_raw = get_named_value(data, 'N3, N4:', 'below')
d2_allow_repeating_raw = get_named_value(data, 'D2:', 'below')
full_title = f'{title} {date}'

# Handle and create default directories/file paths
main_dir = Path(__file__).resolve().parent
default_pdf_dir = main_dir / 'PDF Outputs'
default_pdf_dir.mkdir(exist_ok=True)
tex_files_dir = main_dir / 'TeX Outputs'
tex_files_dir.mkdir(exist_ok=True)
main_template = main_dir / 'main_template.tex'
orig_sty_file = main_dir / 'skillcheckpoints.sty'
copied_sty_file = tex_files_dir / 'skillcheckpoints.sty'
bank_xml = main_dir / 'bank.xml'
skill_list_csv = main_dir / 'Skill List.csv'
skill_list_tex = tex_files_dir / 'Skill Descriptions.tex'
outcomes_dir = main_dir / 'outcomes'

if str(outcomes_dir) not in sys.path:
    sys.path.insert(0, str(outcomes_dir))

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

def update_skill_list_tex(skill_data: list[tuple[str, str, str]]) -> None:
    skill_list_tex.touch(exist_ok=True)
    with skill_list_tex.open(mode='w', encoding='utf-8') as file:
        for slug, desc, color in skill_data:
            # Writes \setskilldesc[ColorName]{Slug}{Description}
            file.write(f'\\setskilldesc[{color}]{{{slug}}}{{{desc}}}\n')

# XML default namespace for CheckIt bank.xml
NS = {'c': 'https://checkit.clontz.org'}

def _clean_text(node: ET.Element | None) -> str:
    """
    Return a cleaned, single-line string of all text inside `node`.
    - Uses itertext() to collect text even when the node has nested tags.
    - Collapses whitespace/newlines into single spaces.
    """
    if node is None:
        return ''
    raw = ''.join(node.itertext())
    return ' '.join(raw.split())

def parse_bank(xml_path: str | Path) -> list[tuple[str, str, str, str, str]]:
    """
    Parse bank.xml and return a list of tuples:
        (slug, description, path, kind, color)
    """
    xml_path = str(xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # --- 1. Build the dynamic color map from the XML ---
    dynamic_color_map = {}
    for elem in root.iter():
        if elem.tag.endswith('category'):
            prefix = elem.get('prefix')
            color_attr = elem.get('color')
            if prefix and color_attr:
                dynamic_color_map[prefix] = color_attr

    items = []

    # --- 2. Helper to find color or default based on slug ---
    def get_color(element, slug):
        # First check if the outcome has a specific color tag overriding the map
        color_el = element.find('c:color', NS)
        if color_el is not None and color_el.text:
            return color_el.text.strip()
        
        # Fallback to mapping based on the first letter of the slug
        first_letter = slug[0].upper() if slug else ''
        # We now use the local dictionary we just built!
        return dynamic_color_map.get(first_letter, 'scCOLOR')

    # --- 3. Process outcomes (m) and associates (a) ---
    for tag, kind in [('.//c:outcome', 'm'), ('.//c:associate', 'a')]:
        for entry in root.findall(tag, NS):
            slug_el = entry.find('c:slug', NS)
            desc_el = entry.find('c:description', NS)
            path_el = entry.find('c:path', NS)

            slug = (slug_el.text or '').strip() if slug_el is not None else ''
            desc = _clean_text(desc_el)
            path = (path_el.text or '').strip() if path_el is not None and path_el.text else ''
            color = get_color(entry, slug)

            items.append((slug, desc, path, kind, color))

    return items


skill_array = parse_bank(bank_xml)
print(f"✅ Parsed XML Bank: Found {len(skill_array)} total skills.")

main_skill_dict = {
    slug: {
        'dsc': desc,
        'gen': main_dir / path / 'pygenerator.py',
        'tpl': main_dir / path / 'textemplate.tex'
    }
    for slug, desc, path, kind, color in skill_array
    if kind == "m"
}

main_skills = list(main_skill_dict)
skill_desc_list = [(row[0], row[1], row[4]) for row in skill_array]

for skill in main_skills:
    skill_tex_gen_dir = tex_files_dir / skill
    skill_tex_gen_dir.mkdir(exist_ok=True)

shutil.copyfile(orig_sty_file, copied_sty_file)

update_skill_list_tex(skill_desc_list)

# Set remaining variables from raw data
include_names = True
if include_names_raw[0].casefold() in ('n'.casefold(), 'f'.casefold()):
    include_names = False

save_as_dialog = False
if 'default'.casefold() not in pdf_location_raw.casefold():
    save_as_dialog = True


# Save settings to settings dictionary, which will be passed to the generator functions
course_progress = int(course_progress_raw[0])
w7_allow_terminating = True if w7_allow_terminating_raw.casefold() == 'TRUE'.casefold() else False
d2_allow_repeating = True if d2_allow_repeating_raw.casefold() == 'TRUE'.casefold() else False
n3_n4_force_listing_method = True if n3_n4_force_listing_method_raw.casefold() == 'TRUE'.casefold() else False
settings = {k: v for k, v in locals().items() if k in ['course_progress',
                                                       'w7_allow_terminating',
                                                       'n3_n4_force_listing_method',
                                                       'd2_allow_repeating']}

# Trying to make full_choices_array non empty if a row is empty
# full_choices_array = get_named_range(data, 'Full Name:')
# Find the header row manually and grab everything below it
full_choices_array = []
for i, row in enumerate(data):
    if 'Full Name:' in row:
        start_col = row.index('Full Name:')
        # Grab the header row
        full_choices_array.append(row[start_col:])
        # Grab all subsequent rows where the Full Name isn't blank
        for student_row in data[i+1:]:
            if student_row[start_col].strip() != '':
                full_choices_array.append(student_row[start_col:])
        break
student_count = len(full_choices_array) - 1 if len(full_choices_array) > 0 else 0
print(f"✅ Roster Loaded: {student_count} students found.")
if student_count == 0:
    print("⚠️ WARNING: 0 students found.")

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

chosen_main_skills_array = get_named_range(full_choices_array, '1:', direction='below', width=100, filter_blanks=True)
chosen_main_skills = list({sk for row in chosen_main_skills_array for sk in row})

# create a jinja2 environment with latex-compatible markup and instantiate a template
env = make_env(loader=FileSystemLoader('.'))

# Convert main_template to a relative path
relative_main_template_path = main_template.relative_to(main_dir)
loaded_main_template = env.get_template(relative_main_template_path.as_posix())

main_var_dict = {k: v for k, v in locals().items() if k in ['course', 'semester', 'professor', 'full_title']}

# Build PDF
print(f"⚙️ Generating TeX files for {len(chosen_main_skills)} unique skills...")
main_document = loaded_main_template.render(main_var_dict)
for skill in chosen_main_skills:
    if skill in main_skills:
        generator_path = main_skill_dict[skill]['gen']
        spec = importlib.util.spec_from_file_location('pygenerator', generator_path)
        current_generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(current_generator)

        current_template = main_skill_dict[skill]['tpl']
        relative_template_path = current_template.relative_to(main_dir)
        loaded_current_template = env.get_template(relative_template_path.as_posix())

        for current_seed in seeds:
            print(f"   -> Creating {skill} (Seed: {current_seed})")
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

    student_text += "\\preparefornextstudent\n\n"

# Build answer key versions
sorted_used_versions = sorted(
    used_versions,
    key=lambda x: (main_skills.index(x.split('/', 1)[0]), x)
)

key_name = 'Key'
key_section = 'Blank'
key_text = ('\\setboolean{anstoggle}{true}\n'
            f'\\setname{{{key_name}}}\n'
            f'\\setsect{{{key_section}}}\n')
if int(key_amount) > 0:
    # Create a single complete key first
    single_key = ""
    for used_version in sorted_used_versions:
        single_key += f'\\skillpage{{{used_version}}}\n'
    
    # Add the buffer to the end of the key
    single_key += "\\preparefornextstudent\n"
    
    # Now multiply the entire "packet" (Key + Buffer)
    key_text += single_key * int(key_amount)


beginning, ending = main_document.split('% Student copies')
main_document = beginning + student_text + ending
beginning, ending = main_document.split('% Keys')
main_document = beginning + key_text + ending

main_document = main_document.replace(f'{tex_files_dir.stem}/', '')
main_tex_file_path.write_text(main_document, encoding='utf-8')

print("📝 Compiling final PDF (this may take a moment)...")

try:
    pdf = build_pdf(main_document, texinputs=[str(tex_files_dir), str(main_dir), ''])
    pdf.save_to(pdf_path)
    print(f"📄✨ Success! PDF saved to: {pdf_path.name}")
except LatexBuildError as e:
    print("\n❌ LaTeX Compilation Failed...")
    
    # Save the massive error log to a file instead of the terminal
    error_log_path = main_dir / "latex_error_log.txt"
    with open(error_log_path, "w", encoding="utf-8") as f:
        f.write(str(e))
        
    print(f"⚠️ The terminal was saved from a LaTeX log avalanche.")
    print(f"⚠️ Please open '{error_log_path.name}' to see the exact LaTeX error.")
    
    # Stop the script safely
    sys.exit(1)

# Detect the OS and open the newly created PDF file accordingly
if os.name == 'nt':  # For Windows
    os.startfile(pdf_path)
elif os.name == 'posix':  # For Unix-based systems (Linux, macOS)
    subprocess.run(['open', pdf_path.resolve()], check=True)
else:
    raise OSError('Unsupported operating system')
