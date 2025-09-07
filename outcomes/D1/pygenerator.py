import slye_math as sm
import random


def generate(**kwargs):
    # Begin place value task
    pv_amt = random.choice((9, 10, 11))
    dec_offset = random.choice((-4, -5, -6))

    pv_int_string = sm.int_string(pv_amt)
    pv_dec_string = sm.dec_string(dec_offset, custom_string=pv_int_string)

    # This code is specific to pv_amt and dec_offset remaining within the above bounds. If you change the above, you'll need to change this code.
    names_index_offset = -1 * (pv_amt + dec_offset) + 7
    pv_names = ('millions (1,000,000)', 'hundred-thousands (100,000)', 'ten-thousands (10,000)', 'thousands (1,000)',
                'hundreds (100)',
                'tens (10)', 'units (1)', 'tenths (1/10)', 'hundredths (1/100)', 'thousandths (1/1000)',
                'ten-thousandths (1/10,000)',
                'hundred-thousandths (1/100,000)', 'millionths (1/1,000,00)')

    pv_ans_text = ''
    for i, digit in enumerate(pv_int_string):
        pv_ans_text += f'{digit} is in the {pv_names[names_index_offset + i]} place.\n'

    # Begin blocks task
    # Did a hacky refactor to always include both the flats and large cubes versions

    units_block_choices = ['flats', 'large cubes']
    random.shuffle(units_block_choices)

    def blocks_prob_ans(units_block_choice = 'flats'):
        lcubes_amt = 0
        flats_amt = 0
        rods_amt = 0
        scubes_amt = 0

        blocks_digits = 3

        if units_block_choice == 'large cubes':
            blocks_digits = random.choices([3, 4], weights=[0.5, 0.5])[0]

        blocks_dec = sm.dec_string(-1 * blocks_digits + 1, blocks_digits, wt_7=0.0, wt_8=0.0, wt_9=0.0)
        int_blocks_dec = blocks_dec.replace(".", "")

        if units_block_choice == 'flats':
            units_block = 'flat'
            tenths_block = 'long'
            hundredths_block = 'small cube'
            lcubes_amt = 0
            flats_amt = int(int_blocks_dec[0])
            rods_amt = int(int_blocks_dec[1])
            scubes_amt = int(int_blocks_dec[2])
        else:
            units_block = 'large cube'
            tenths_block = 'flat'
            hundredths_block = 'long'
            lcubes_amt = int(int_blocks_dec[0])
            flats_amt = int(int_blocks_dec[1])
            rods_amt = int(int_blocks_dec[2])
            if blocks_digits == 4:
                scubes_amt = int(int_blocks_dec[3])

        blocks_ans_text = f'{lcubes_amt} large cubes, {flats_amt} flats, {rods_amt} longs, and {scubes_amt} small cubes'

        return blocks_dec, blocks_ans_text, units_block, tenths_block, hundredths_block
    

    blocks_dec = []
    units_block_choice = []
    blocks_ans_text = []
    units_block = []
    tenths_block = []
    hundredths_block = []
    
    for i, units_block_choice_i in enumerate(units_block_choices):
        blocks_dec_i, blocks_ans_text_i, units_block_i, tenths_block_i, hundredths_block_i = blocks_prob_ans(units_block_choice=units_block_choice_i)

        blocks_dec.append(blocks_dec_i)
        units_block_choice.append(units_block_choice_i)
        blocks_ans_text.append(blocks_ans_text_i)
        units_block.append(units_block_i)
        tenths_block.append(tenths_block_i)
        hundredths_block.append(hundredths_block_i)
        
        # lcubes_toggles = [True] * lcubes_amt + [False] * (9 - lcubes_amt)
        # flats_toggles = [True] * flats_amt + [False] * (9 - flats_amt)
        # rods_toggles = [True] * rods_amt + [False] * (9 - rods_amt)
        # scubes_toggles = [True] * scubes_amt + [False] * (9 - scubes_amt)

        # lcubes_dict = {'lcube' + str(i + 1): value for i, value in enumerate(lcubes_toggles)}
        # flats_dict = {'flat' + str(i + 1): value for i, value in enumerate(flats_toggles)}
        # rods_dict = {'rod' + str(i + 1): value for i, value in enumerate(rods_toggles)}
        # scubes_dict = {'scube' + str(i + 1): value for i, value in enumerate(scubes_toggles)}

    return {
        'pv_dec_string': pv_dec_string,
        'pv_ans_text': pv_ans_text,
        'blocks_dec_a': blocks_dec[0],
        'units_block_choice_a': units_block_choice[0],
        'blocks_ans_text_a': blocks_ans_text[0],
        'units_block_a': units_block[0],
        'tenths_block_a': tenths_block[0],
        'hundredths_block_a': hundredths_block[0],
        'blocks_dec_b': blocks_dec[1],
        'units_block_choice_b': units_block_choice[1],
        'blocks_ans_text_b': blocks_ans_text[1],
        'units_block_b': units_block[1],
        'tenths_block_b': tenths_block[1],
        'hundredths_block_b': hundredths_block[1],
    }