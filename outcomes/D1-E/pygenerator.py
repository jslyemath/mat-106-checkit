import slye_math as sm
import random


def generate(**kwargs):

    units_block_choices = ['flats', 'large cubes']
    units_block_choice = random.choice(units_block_choices)

    def blocks_hierarchy(units_block_choice = 'flats'):
        if units_block_choice == 'flats':
            units_block = 'flat'
            tenths_block = 'long'
            hundredths_block = 'small cube'
        else:
            units_block = 'large cube'
            tenths_block = 'flat'
            hundredths_block = 'long'

        return units_block, tenths_block, hundredths_block
    

    units_block, tenths_block, hundredths_block = blocks_hierarchy(units_block_choice)

    return {
        'units_block_choice': units_block_choice,
        'units_block': units_block,
        'tenths_block': tenths_block,
        'hundredths_block': hundredths_block,
    }