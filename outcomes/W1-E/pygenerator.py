import slye_math as sm
import random


def generate(**kwargs):
    mode = kwargs.get('mode', 'latex')

    def rom_modern():
        modern = int(sm.int_string(4, (0, 4, 5, 6, 7, 8, 9), wt_0=.03, wt_4=.2, wt_6=.2, wt_9=.2))
        rom = sm.to_roman(modern)
        return f'\\text{{{rom}}}', modern, 'Roman'
    
    def large_egy(org_egy):
        if mode == 'html':
            return f'\\Huge {org_egy}'
        else:
            return f'\\Large\\textpmhg{{{org_egy}}}'

    def egy_modern():
        modern = random.choice(range(100000, 4000000))
        egy = sm.to_egyptian(modern, mode=mode)
        return large_egy(egy), modern, 'ancient Egyptian'

    non_bab_systems = [rom_modern, egy_modern]
    expl_system_func = random.choice(non_bab_systems)

    if expl_system_func == rom_modern:
        expl_system = 'Roman'
        expl_modern, expl_ancient = random.choice([(11, f'\\text{{{sm.to_roman(2)}}}'),
                                                   (111, f'\\text{{{sm.to_roman(3)}}}'),
                                                   (51, f'\\text{{{sm.to_roman(6)}}}'),
                                                   (511, f'\\text{{{sm.to_roman(7)}}}'),
                                                   (5111, f'\\text{{{sm.to_roman(8)}}}')])
    else:
        expl_system = 'ancient Egyptian'
        expl_modern, expl_ancient = random.choice([(11, large_egy(sm.to_egyptian(2, mode=mode))),
                                                   (111, large_egy(sm.to_egyptian(3, mode=mode))),
                                                   (1111, large_egy(sm.to_egyptian(4, mode=mode))),
                                                   (11111, large_egy(sm.to_egyptian(5, mode=mode))),
                                                   (111111, large_egy(sm.to_egyptian(6, mode=mode)))])

    # TODO: Add logic for explanation.

    return {
        'expl_modern': f'{expl_modern}',
        'expl_ancient': f'{expl_ancient}',
        'expl_system': f'{expl_system}',
    }
