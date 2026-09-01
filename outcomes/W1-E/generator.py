import bank_helpers as sm
import random


def generate(**kwargs):

    def rom_modern():
        modern = int(sm.int_string(4, (0, 4, 5, 6, 7, 8, 9), wt_0=.03, wt_4=.2, wt_6=.2, wt_9=.2))
        rom = sm.to_roman(modern)
        # Markup, not bare TeX: the slot also carries glyphs() output.
        return sm.as_math(f'\\text{{{rom}}}'), modern, 'Roman'
    
    def egy_glyphs(n):
        return sm.glyphs(
            'egyptian',
            sm.to_egyptian(n, mode='html'),
            r'\Large\textpmhg{%s}' % sm.to_egyptian(n, mode='latex'),
        )

    def egy_modern():
        modern = random.choice(range(100000, 4000000))
        return (
            sm.glyphs(
                'egyptian',
                sm.to_egyptian(modern, mode='html'),
                r'\Large\textpmhg{%s}' % sm.to_egyptian(modern, mode='latex'),
            ),
            modern,
            'ancient Egyptian',
        )

    non_bab_systems = [rom_modern, egy_modern]
    expl_system_func = random.choice(non_bab_systems)

    if expl_system_func == rom_modern:
        expl_system = 'Roman'
        # sm.math, not a bare f-string: {{{expl_ancient}}} is a markup slot,
        # and its other branch below fills it with glyphs() output.
        def rom(n):
            return sm.as_math(f'\\text{{{sm.to_roman(n)}}}')

        expl_modern, expl_ancient = random.choice([(11, rom(2)),
                                                   (111, rom(3)),
                                                   (51, rom(6)),
                                                   (511, rom(7)),
                                                   (5111, rom(8))])
    else:
        expl_system = 'ancient Egyptian'
        expl_modern, expl_ancient = random.choice([(11, egy_glyphs(2)),
                                                   (111, egy_glyphs(3)),
                                                   (1111, egy_glyphs(4)),
                                                   (11111, egy_glyphs(5)),
                                                   (111111, egy_glyphs(6))])

    # TODO: Add logic for explanation.

    return {
        'expl_modern': f'{expl_modern}',
        'expl_ancient': f'{expl_ancient}',
        'expl_system': f'{expl_system}',
    }


# ---------------------------------------------------------------------------
# CheckIt entry point.
#
# Ported from generator.sage, which loaded this file with runpy and called:
#     pygenerate(mode='html')
# The dead arguments among those were dropped on 2026-08-31 -- no generate()
# ever read `mode`, and only R1, R2, W4, W4-E and W5 read `course_progress`.
# Verified output-identical across 350 samples before and after.
#
# The shim existed only because
# SageMath could not reach a plain-Python file and the bank root was not
# importable; both gaps are closed, so the file extension now selects the
# plain-Python runtime directly.
class Generator(BaseGenerator):
    def data(self):
        return generate()
