# The MAT 106 bank

@../checkit/WORKING_RULES.md

The line above loads the house rules shared by all three repos; they start
with checking that student names are masked. The whole-project map is
`../checkit/CLAUDE.md`, and what is left to do is `../checkit/ROADMAP.md`.

This is the live bank: 29 outcomes, published to `docs/`.

```bash
./venv/Scripts/python.exe -m checkit generate --remote https://jslyemath.github.io/mat-106-checkit
./venv/Scripts/python.exe -m checkit viewer        # rebuild docs/ from assets/
./venv/Scripts/python.exe -m checkit check         # structural checks, every version
```

The venv has checkit installed **editable** against `../checkit/dashboard`,
so platform edits take effect here with no reinstall. The installed label
reads 0.2.8.1 while the source says 0.2.9.1; the code that runs is current,
and `pip install -e ../checkit/dashboard` refreshes the label.

## Things that will bite

- **`--remote` is required**: this bank has figures, and precomputed HTML
  needs absolute image URLs. Images to 400 with `-i --image-seeds 400`.
- **`-r` is what makes a generator fix real**, and it re-rolls every
  version -- not on a live skill mid-term. **Republish the same day**: R1
  was regenerated on 2026-10-12 and not deployed for five weeks, so
  students browsed old versions while printit printed new ones.
- **`W1` and `W1-E` are `<frozen/>`** -- students are working through them.
  `--thaw W1` is the only way past, deliberately.
- **`TeX Outputs/` and `PDF Outputs/` hold real student names.** Gitignored.
  Never commit, never read into chat.
- **`printit/` holds the theme**, installed by checkit-printit and declared
  in `bank.xml` under `<latex-support>`. `assets/*.sty` is a build copy.
  A theme change reaches this bank only by `checkit-printit install --force`.
- Nine skills declare variants (R1, R2, W4, W4-E, W5, W7, N3, N4, D2), so a
  print run needs a `[variants]` line for them.
- `pdfgenerator.py` and `main_template.tex` are the deprecated pre-printit
  path. They still work; printit replaced them.
- The course state for this bank -- roster, seating, form, print record --
  is `~/CheckItPrintIt/courses/MAT 106/`, deliberately outside this repo.
