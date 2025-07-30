import os
import shutil
import logging

logging.basicConfig(
    filename=os.getenv('GITHUB_WORKSPACE', '.') + '/sync_errors.log',
    filemode='w',
    format='%(levelname)s:%(message)s',
    level=logging.INFO
)

BANK_PATH = os.environ.get('BANK_PATH', '../mat-106-bank/outcomes')
LOCAL_BANK_PATH = os.environ.get('LOCAL_BANK_PATH', '../local-mat-106-bank')
CHECKIT_PATH = os.environ.get('CHECKIT_PATH', './outcomes')
DIRS = [f'D{i}' for i in range(1, 4)] + [f'W{i}' for i in range(1, 7)] + [f'F{i}' for i in range(1, 5)] + [f'G{i}' for i in range(1, 3)] + [f'N{i}' for i in range(1, 5)]

def safe_copy(src, dst):
    if not os.path.exists(src):
        logging.error(f"Missing source: {src}")
        return False
    if os.path.exists(dst):
        logging.warning(f"File exists, not overwriting: {dst}")
        return False
    shutil.copy(src, dst)
    return True

for d in DIRS:
    src_dir = os.path.join(BANK_PATH, d)
    dest_dir = os.path.join(CHECKIT_PATH, d)
    if not os.path.isdir(src_dir):
        logging.error(f"Source directory missing: {src_dir}")
        continue
    os.makedirs(dest_dir, exist_ok=True)

    # Copy template.xml
    xml_src = os.path.join(src_dir, 'template.xml')
    xml_dst = os.path.join(dest_dir, 'template.xml')
    safe_copy(xml_src, xml_dst)

    # Copy generator.py and template.tex from local-mat-106-bank
    pygen_src = os.path.join(LOCAL_BANK_PATH, f'{d}_generator.py')
    tex_src = os.path.join(LOCAL_BANK_PATH, f'{d}_template.tex')
    pygen_dst = os.path.join(dest_dir, 'pygenerator.py')
    tex_dst = os.path.join(dest_dir, 'textemplate.tex')
    safe_copy(pygen_src, pygen_dst)
    safe_copy(tex_src, tex_dst)