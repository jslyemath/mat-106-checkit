class Generator(BaseGenerator):
    def data(self):
        return pygenerate()

# ────────────────────────────────────────────────────────────────────────────

from pathlib import Path
import sys, runpy

# Find the real paths to the current generator and the outcomes directory
generator_path = Path(sys.argv[1])
generator_dir = generator_path.parent
outcomes_dir = generator_dir.parent

# The slye_math python file is in the outcomes. Place outcomes in sys path.
outcomes_str = str(outcomes_dir.resolve())
if outcomes_str not in sys.path:
    sys.path.insert(0, outcomes_str)

# Load pygenerator.py and add its generate function as pygenerate to globals
pygenerator_path = generator_dir / "pygenerator.py"
module_globals = runpy.run_path(str(pygenerator_path))
try:
    pygenerate = module_globals["generate"]
except KeyError:
    raise ImportError("pygenerator.py must define a top‑level generate() function")
