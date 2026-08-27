import bank_helpers as sm
import random


def generate(**kwargs):

    def bab_modern():
        modern = random.choice(range(3501, 162000))
        return (
            sm.glyphs(
                'babylonian',
                sm.to_simple_babylonian(modern, mode='html'),
                sm.to_simple_babylonian(modern, mode='latex'),
            ),
            modern,
            'ancient Babylonian',
        )

    def rom_modern():
        modern = int(sm.int_string(4, (0, 4, 5, 6, 7, 8, 9), wt_0=.03, wt_4=.2, wt_6=.2, wt_9=.2))
        rom = sm.to_roman(modern)
        # The slot this fills also receives glyphs() markup, so this has to be
        # markup too. Bare TeX renders as the literal "\text{MDCXLVIII}".
        return sm.as_math(f'\\text{{{rom}}}'), modern, 'Roman'
    
    def egy_modern():
        modern = random.choice(range(100000, 4000000))
        return (
            sm.glyphs(
                'egyptian',
                sm.to_egyptian(modern, mode='html'),
                '\\Large\\textpmhg{%s}' % sm.to_egyptian(modern, mode='latex'),
            ),
            modern,
            'ancient Egyptian',
        )

    non_bab_systems = [rom_modern, egy_modern]
    random.shuffle(non_bab_systems)
    other_system, expl_system_func = non_bab_systems
    chosen_systems = [bab_modern, other_system]
    random.shuffle(chosen_systems)
    to_ancient_func, to_modern_func = chosen_systems

    to_a_ancient, to_a_modern, to_a_system = to_ancient_func()
    to_m_ancient, to_m_modern, to_m_system = to_modern_func()

    # if expl_system_func == rom_modern:
    #     expl_system = 'Roman'
    #     expl_modern, expl_ancient = random.choice([(11, f'\\text{{{sm.to_roman(2)}}}'),
    #                                                (111, f'\\text{{{sm.to_roman(3)}}}'),
    #                                                (51, f'\\text{{{sm.to_roman(6)}}}'),
    #                                                (511, f'\\text{{{sm.to_roman(7)}}}'),
    #                                                (5111, f'\\text{{{sm.to_roman(8)}}}')])
    # else:
    #     expl_system = 'ancient Egyptian'
    #     expl_modern, expl_ancient = random.choice([(11, large_egy(sm.to_egyptian(2, mode=mode))),
    #                                                (111, large_egy(sm.to_egyptian(3, mode=mode))),
    #                                                (1111, large_egy(sm.to_egyptian(4, mode=mode))),
    #                                                (11111, large_egy(sm.to_egyptian(5, mode=mode))),
    #                                                (111111, large_egy(sm.to_egyptian(6, mode=mode)))])

    return {
        'to_a_modern': f'{int(to_a_modern):,}',
        'to_a_system': f'{to_a_system}',
        'to_a_ancient': f'{to_a_ancient}',
        'to_m_ancient': f'{to_m_ancient}',
        'to_m_system': f'{to_m_system}',
        'to_m_modern': f'{int(to_m_modern):,}',
    }


# ---------------------------------------------------------------------------
# CheckIt entry point.
#
# Ported from generator.sage, which loaded this file with runpy and called:
#     pygenerate(mode='html')
# Those arguments are reproduced exactly, so this port changes no output: the
# same seed yields the same data it did before. The shim existed only because
# SageMath could not reach a plain-Python file and the bank root was not
# importable; both gaps are closed, so the file extension now selects the
# plain-Python runtime directly.
class Generator(BaseGenerator):
    def data(self):
        return generate()
