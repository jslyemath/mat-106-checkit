# Working in this bank

This is the live MAT 106 bank. The platform it runs on is a sibling repo, and
**the fuller guide lives there**: `../checkit/CLAUDE.md`. Read that too.

## This repo specifically

```bash
./venv/Scripts/python.exe -m checkit generate --remote https://jslyemath.github.io/mat-106-checkit
./venv/Scripts/python.exe -m checkit viewer        # rebuild docs/ from assets/
./venv/Scripts/python.exe -m checkit check         # structural checks
```

`--remote` is required: this bank has figures, and precomputed HTML needs
absolute image URLs. `generate` refuses without it rather than publishing
`<img>` tags that 404.

The venv has checkit installed **editable** against `../checkit/dashboard`, so
platform edits take effect here with no reinstall.

## Things that will bite

- **`-r` is what makes a generator fix real.** Without it, existing seeds are
  reused and your change reaches nothing. It also re-rolls every version, so
  not on a live skill mid-term.
- `outcomes/W1` and `W1-E` are marked `<frozen/>` — students are working
  through them. `--thaw W1` is the only way past, deliberately.
- **`TeX Outputs/` and `PDF Outputs/` hold real student names.** Gitignored.
  Never commit, never paste into chat.
- `printit/` holds the theme, installed by checkit-printit and declared in
  `bank.xml` under `<latex-support>`. `assets/*.sty` is a build copy and is
  gitignored; the source of truth is `printit/`.
- `pdfgenerator.py` and `main_template.tex` are the deprecated pre-printit
  path. They still work, but printit replaced them.
