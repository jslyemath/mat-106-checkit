class Generator(BaseGenerator):
    def data(self):
        return generate()

# ────────────────────────────────────────────────────────────────────────────

import os, sys, runpy

# 1) The real path to YOUR generator.sage in your workspace:
real_sage = sys.argv[1]                  # e.g. "/workspaces/.../outcomes/EX1/generator.sage"
gen_dir   = os.path.dirname(real_sage)   # e.g. "/workspaces/.../outcomes/EX1"

# 2) The parent of that is exactly the "outcomes" folder where slye_math.py lives:
outcomes_dir = os.path.abspath(os.path.join(gen_dir, os.pardir))

# 3) Stick it at the front of sys.path so import slye_math will work inside pygenerator.py
if outcomes_dir not in sys.path:
    sys.path.insert(0, outcomes_dir)

# 4) Now load your local pygenerator.py by full path
module_globals = runpy.run_path(os.path.join(gen_dir, "pygenerator.py"))

# 5) Pull its generate() into this .sage’s globals
try:
    generate = module_globals["generate"]
except KeyError:
    raise ImportError("pygenerator.py must define a top‑level generate() function")
