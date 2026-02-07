import slye_math as sm
import random
import json
from pathlib import Path


def generate(**kwargs):
    course_progress = int(kwargs['course_progress'])
    mode = kwargs.get('mode', 'latex')

    # Lists of version keys, split up by course progress cutoff points.
    # These must be the same names as those in the versions dictionary, as well as the name of the png file.

    beginning_0 = ['add-coladd-1p', 'add-lattice-1p', 'add-mental-1p', 'add-standard-1p', 'add-standard-2p']
    sub_whole_1 = ['sub-standard-1p', 'sub-trades-1p']
    mult_div_whole_2 = ['mult-lattice-1p', 'mult-partial-1p', 'mult-standard-1p', 'div-scaffold-1p', 'div-standard-1p']
    int_pemdas_3 = ['pemdas-1p', 'pemdas-2p']
    add_sub_frac_4 = ['fraction-model-1p', 'fraction-model-2p', 'fraction-model-3p']
    mult_div_frac_5 = ['decimal-model-1p']

    versions_lists = [beginning_0, sub_whole_1, mult_div_whole_2, int_pemdas_3, add_sub_frac_4, mult_div_frac_5]

    def get_available_versions(n):
        return sum(versions_lists[:n+1], [])

    versions = {
        'add-coladd-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '4234 + 3592',
                'work_desc_2': " using the column addition algorithm.",
                'incorrect': "Instead of regrouping 10 from a place value to be 1 in the next column, the student was doing a 1-for-1 trade every time.",
                'thinking': "",
                'feedback': "",
            },
        'add-lattice-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '857 + 846',
                'work_desc_2': " using the lattice algorithm.",
                'incorrect': "The student flipped the positions of the ones and tens. Additionally, they added directly down, instead of adding diagonally.",
                'thinking': "",
                'feedback': "",
            },
        'add-mental-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '37 + 48',
                'work_desc_2': " using a mental math technique.",
                'incorrect': "The student attempted something akin to equal additions (a subtraction technique), and added 2 to both addends.",
                'thinking': "",
                'feedback': "Rounding 48 up to 50 is a great strategy, but we should subtract 2 from 37 instead. This will counteract the extra 2 added from the other addend.",
            },
        'add-standard-1p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '247 + 386',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "The student did not carry over the 1s for regrouping above the next column, instead leaving them as part of the final answer.",
                'thinking': "",
                'feedback': "",
            },
        'add-standard-2p':
            {
                'work_desc_1': "The student was trying to add ",
                'work_math': '574 + 891',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "The student added from left-to-right, including performing the regroupings to the next lesser place value.",
                'thinking': "",
                'feedback': "",
            },
        'sub-standard-1p':
            {
                'work_desc_1': "The student was trying to subtract ",
                'work_math': '9023 - 4586',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "The student regrouped directly from the thousands place to the tens place. They also stated that zero minus five is five.",
                'thinking': "",
                'feedback': "",
            },
        'sub-trades-1p':
            {
                'work_desc_1': "The student was trying to subtract ",
                'work_math': '3278 - 1352',
                'work_desc_2': " using the trades first algorithm.",
                'incorrect': "The student performed all trades, whether or not they were necessary. This resulted in more than 10 in two columns, and they simply placed all the digits next to each other in the final answer.",
                'thinking': "",
                'feedback': "",
            },
        'mult-lattice-1p':
            {
                'work_desc_1': "The student was trying to multiply ",
                'work_math': '82 \\times 97',
                'work_desc_2': " using the lattice algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'mult-partial-1p':
            {
                'work_desc_1': "The student was trying to multiply ",
                'work_math': '37 \\times 54',
                'work_desc_2': " using the partial products algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'mult-standard-1p':
            {
                'work_desc_1': "The student was trying to multiply ",
                'work_math': '1324 \\times 9',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'div-scaffold-1p':
            {
                'work_desc_1': "The student was trying to divide ",
                'work_math': '4251 \\div 12',
                'work_desc_2': " using the scaffold algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'div-standard-1p':
            {
                'work_desc_1': "The student was trying to divide ",
                'work_math': '642 \\div 6',
                'work_desc_2': " using the standard algorithm.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'pemdas-1p':
            {
                'work_desc_1': "The student was trying to compute ",
                'work_math': '23-(4+2)^2',
                'work_desc_2': " using the standard order of operations.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'pemdas-2p':
            {
                'work_desc_1': "The student was trying to compute ",
                'work_math': '1 - 32 \\div 4 \\times 2',
                'work_desc_2': " using the standard order of operations.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'fraction-model-1p':
            {
                'work_desc_1': "The student was trying to model the fraction ",
                'work_math': '\\dfrac{2}{3}',
                'work_desc_2': " using a hexagon as the whole.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'fraction-model-2p':
            {
                'work_desc_1': "The student was trying to determine the fraction of the rectangle represented by the ",
                'work_math': '\\text{red}',
                'work_desc_2': " shaded portion.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'fraction-model-3p':
            {
                'work_desc_1': "The student was trying to mark the locations of ",
                'work_math': '\\frac{1}{2} \\text{ and } \\frac{1}{3}',
                'work_desc_2': " on the number line.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
        'decimal-model-1p':
            {
                'work_desc_1': "The student was trying to mark the locations of ",
                'work_math': '0.11 \\text{ through } 0.19',
                'work_desc_2': " on the number line.",
                'incorrect': "",
                'thinking': "",
                'feedback': "",
            },
    }

    html_versions = {
        "add-coladd-1": {
            "work_desc_1": "The student was trying to add ",
            "work_math": "6475 + 2844",
            "work_desc_2": " using the column addition algorithm.",
            "incorrect": "Instead of regrouping from lower to higher place values, they regrouped from higher to lower. At the end, they allowed the 10 in the ones to stay, bumping the remaining place values one place value too high.",
            "thinking": "The student knew to regroup, but probably doesn't have a full grasp of why we regroup from right to left. The student may have gotten confused about what to do if they regrouped to the right and had nowhere to regroup the 10.",
            "feedback": "We should regroup from right to left, because a group of ten in base ten is one group of the next to the left. Consider the 11 from the 7 and the 4. That is 11 tens, which is 110. In other words, we have 1 group of one hundred and 1 group of ten left over. So we want to regroup that 1 over to the left and make 13 total hundreds. Likewise with the hundreds column. Finally, be sure that all your final values in each column are less than ten, and all regrouping is done, before writing your final answer."
        },
        "sub-standard-1": {
            "work_desc_1": "The student was trying to subtract ",
            "work_math": "6050 - 3764",
            "work_desc_2": " by using the standard algorithm.",
            "incorrect": "The student subtracted incorrectly in the ones column and the hundreds column. Additionally, they regrouped from the thousands directly to make 10 more groups of ten, which is not allowed.",
            "thinking": "When subtracting 0 - 4 or 0 - 7, the student may have been thinking of 4 - 0 and 7 - 0. They may have also thought that the zero in the hundreds column has no value, and can be skipped over to directly give regrouped values to the tens column.",
            "feedback": "Be careful with the order of subtraction! If we have 0-4, we don't have enough ones in the minuend to subtract, and must regroup from the tens first. When regrouping over a zero, we cannot just skip it. Bring the regrouped 1 from the thousands place over to the hundreds column. One group of one thousand is ten groups of one hundred. Now we can split apart those hundreds, take one away to leave us with 9 in the hundreds column, and give it as a ten (floating 1) in the tens column."
        },
        "add-partial-1": {
            "work_desc_1": "The student was trying to add ",
            "work_math": "325 + 297",
            "work_desc_2": " using the partial sums algorithm.",
            "incorrect": "The main error is that they placed each partial sum in its own column, rather than splitting each digit into it's proper place value. There was also a small error where they computed 3 + 2 = 6.",
            "thinking": "The student may have gotten the partial sums algorithm confused with the column-addition algorithm. Or, they may have not known what to do with each partial sum. The calculation error could have just been a counting error, or they may have accidentally multiplied.",
            "feedback": "In this algorithm, we need to pay attention to place values. If 5 + 7 = 12, that means we have one group of ten and 2 ones left over. We need that 1 to be aligned under the 2 and the 9, which are also in the tens column. Likewise, the 11 stands for 1 hundred and 1 ten, so the leftmost 1 needs to go in the hundreds column. Make sure to only place one digit in each column. Consider placing zeros where place values are empty, such as writing 110 instead of just 11 and an empty space. Also be careful to check your partial sums! Notice that 3 + 2 should be 5."
        },
        "add-lattice-1": {
            "work_desc_1": "The student was trying to add ",
            "work_math": "167 + 135",
            "work_desc_2": " by using the lattice algorithm.",
            "incorrect": "The student added each of the individual digits correctly. However, they swapped the placement of the tens and ones in each box. They also added directly down, instead of diagonally.",
            "thinking": "The student may have written down the ones digit first since it was the first triangle available, then regrouped underneath second. They may have added directly downward because that is how addition happens in other algorithms.",
            "feedback": "You did a good job adding each place value's digits together. However, we need to remember that in this algorithm, the ones go in the bottom triangle, then we regroup in the top triangle. This is true for each place value's rectangle. What this does for us is align the regrouped values and non-regrouped values diagonally, so that every pair of numbers in a diagonal chute belongs to the same place value. Add diagonally in this algorithm, along the chutes."
        },
        "mult-standard-1": {
            "work_desc_1": "The student was trying to multiply ",
            "work_math": "237 \\times 12",
            "work_desc_2": " by using the standard algorithm.",
            "incorrect": "The second partial product is in the incorrect place value. We should get 2370, so each of the digits should be moved one left in that second line.",
            "thinking": "The student may not have known to move the digits over another place value each time a new partial product is created in this algorithm.",
            "feedback": "When multiplying 1 by 237 in the second line, we are actually multiplying 10 by 237. This is because the 1 is in the tens place. What that means is that our product is 2370, and each of the 2, 3, and 7 should be one place value further over to the left."
        },
        "mult-dec-1": {
            "work_desc_1": "The student was trying to multiply ",
            "work_math": "3.2 \\times 1.6",
            "work_desc_2": " by using the standard algorithm.",
            "incorrect": "In the first partial product, the student multiplied 6 only by the 2, and not by 32. At the end, they brought the decimal straight down instead of moving it according to the total number of decimal places in the factors.",
            "thinking": "The student may have just forgotten the 3 in the first step, or they may have been unsure of what to do with the regrouped 1 from 2 times 6. They may have placed the decimal the way they did because that is how addition and subtraction of decimals works.",
            "feedback": "When multiplying, don't forget to place your regrouped values all the way above the problem's next digit, then keep multiplying each digit of the first factor. After getting 12, you should place the 1 above the 3 in 32. Then multiply 6  by 3 to get 18, add that regrouped 1 to get 19, and place that 19 to the left of the 2. Also remember that the decimal placement for multiplication works differently from addition and subtraction. We need to put back all the decimal places we ignored. Since we ignored 2 total places from the two factors, we should move in 2 places from the right of the last digit of the product."
        },
        "sub-trades-1": {
            "work_desc_1": "The student was trying to subtract ",
            "work_math": "464 - 325",
            "work_desc_2": " by using the trades-first algorithm.",
            "incorrect": "The student tried to regroup extra values from the hundreds column to the tens column, when we already have enough in that column to subtract 6-2. Then, instead of bringing 1 group of each column as ten of the next, they only brought it over as a 1.",
            "thinking": "The student may have thought that we must trade every single column in the trades-first algorithm. They may not have realized that we are regrouping according to place values, and not just moving around ones.",
            "feedback": "For this algorithm, we need to be sure only to trade if the minuend's digit in that column is less than the subtrahend's digit. Otherwise, we don't need to trade to it. Additionally, we are regrouping using the base ten place values. When we make the 7 one lower to create 6, that was one group of ten we split apart. That adds ten more ones to the next column, to give us 14 instead of just 5."
        },
        "mult-lattice-1": {
            "work_desc_1": "The student was trying to multiply ",
            "work_math": "45 \\times 67",
            "work_desc_2": " by using the lattice algorithm.",
            "incorrect": "The student added 4 + 6 instead of multiplying. They also seemed unsure of what to do with the 11 in the second chute, and simply smushed it together with the surrounding digits in the final product.",
            "thinking": "Since they multiplied every other partial product correctly, the student probably just lost track of what operation they were performing with 4 and 6. The student may not remember that this algorithm sometimes requires that we regroup after the adding step.",
            "feedback": "Be careful, 4 times 6 shoul be 24, not 10. After adding diagonally, check that we only have one digit at the end of each chute. If not, we need to regroup. Your 11 needs to have its first digit regrouped to the next chute. Like the standard algorithm, you could place this above the chute. Or, you could place it at the bottom. Either way, we need to add 3 + 0 + 2 + 1 to get 6 in the hundreds chute."
        },
        "div-fractions-2": {
            "work_desc_1": "The student was trying to divide ",
            "work_math": "\\frac{4}{3} \\div \\frac{2}{5}",
            "work_desc_2": " write their final answer as a fraction in simplest form.",
            "incorrect": "The student multiplied opposite, diagonal entries, but placed their products incorrectly in the resulting fraction. The result should be 20/6, not 6/20. Then, they subtracted 1 from numerator and denominator instead of removing a shared factor of 2.",
            "thinking": "They may have learned or invented a shortcut for turning division of fractions into multiplication. Or, they may have conflated the process with cross multiplication. They also may have thought that any operations (such as subtraction) are permitted when simplifying fractions, instead of only multiplication or division.",
            "feedback": "Remember that when we think of fraction division as you were here, we are thinking of multiplying the first fraction by the second fraction's reciprocal. I would encourage you to write out the extra step where we change the problem to 4/3 times 5/2, then multiply across horizontally as usual. Also, we can't subtract equal amounts from numerator and denominator and obtain an equivalent fraction. We can only multiply or divide both by the same amount. Consider if we were to do the same subtracting of 1 and 1 to the fraction 2/3. We would get 1/2, which is much smaller than 2/3."
        },
        "mult-dec-2": {
            "work_desc_1": "The student was trying to multiply ",
            "work_math": "2.7 \\times 1.3",
            "work_desc_2": " by using the standard algorithm.",
            "incorrect": "In the first partial product, the student multiplied 3 only by the 7, and not by 27. At the end, they brought the decimal straight down instead of moving it according to the total number of decimal places in the factors.",
            "thinking": "The student may have just forgotten the 2 in the first step, or they may have been unsure of what to do with the regrouped 2 from 3 times 7. They may have placed the decimal the way they did because that is how addition and subtraction of decimals works.",
            "feedback": "When multiplying, don't forget to place your regrouped values all the way above the problem's next digit, then keep multiplying each digit of the first factor. After getting 21, you should place the 2 above the 2 in 27. Then multiply 3  by 2 to get 6, add that regrouped 2 to get 8, and place that 8 to the left of the 1. Also remember that the decimal placement for multiplication works differently from addition and subtraction. We need to put back all the decimal places we ignored. Since we ignored 2 total places from the two factors, we should move in 2 places from the right of the last digit of the product."
        },
        "mult-partial-1": {
            "work_desc_1": "The student was trying to multiply ",
            "work_math": "92 \\times 14",
            "work_desc_2": " by using the partial products algorithm.",
            "incorrect": "The student did not correctly account for place values when writing the partial products.",
            "thinking": "The student may have been unaware that each partial product must be placed in the appropriate place value. Or, since there was an attempt to move over the final product from 9 to 90, they may not be sure how to place the partial products.",
            "feedback": "In this algorithm, we need to be aware of what numbers we are actually multiplying. For example, the 4 times the 9 is not actually just 4 times 9. The 9 of 92 is in the tens place value, so we are multiplying 4 by 90 to give us 360. Likewise, we will get 20 and 900 for the next two partial products."
        },
        "div-fractions-1": {
            "work_desc_1": "The student was trying to divide ",
            "work_math": "\\frac{2}{3} \\div \\frac{4}{5}",
            "work_desc_2": " write their final answer as a fraction in simplest form.",
            "incorrect": "The student multiplied opposite, diagonal entries, but placed their products incorrectly in the resulting fraction. The result should be 10/12, not 12/10. Then, they subtracted 9 from numerator and denominator instead of removing a shared factor of 2.",
            "thinking": "They may have learned or invented a shortcut for turning division of fractions into multiplication. Or, they may have conflated the process with cross multiplication. They also may have thought that any operations (such as subtraction) are permitted when simplifying fractions, instead of only multiplication or division.",
            "feedback": "Remember that when we think of fraction division as you were here, we are thinking of multiplying the first fraction by the second fraction's reciprocal. I would encourage you to write out the extra step where we change the problem to 2/3 times 5/4, then multiply across horizontally as usual. Also, we can't subtract equal amounts from numerator and denominator and obtain an equivalent fraction. We can only multiply or divide both by the same amount. Notice how your answer of 3 is much larger than 12/10."
        },
        "frac-equivalence-1": {
            "work_desc_1": "The student was trying to convert ",
            "work_math": "2 \\frac{3}{4}",
            "work_desc_2": " to a single, improper fraction by using an area model as their guide.",
            "incorrect": "The main issue is that their model does not have a consistent area to represent the whole (4/4). In the initial diagram for 2 3/4, the whole is both a square and a longer rectangle with four parts. In the second, it again changes to be longer, as they considered all the parts to be one larger whole split into 6 pieces. Furthermore, the pieces of the whole are not equal. In fraction models, the areas of the pieces of the whole must also all be equal.",
            "thinking": "The student may have been thinking that with fractions, we can always combine the numerator pieces, and count our numerator pieces over our total number of pieces. They may not have a robust understanding of how the parts of the whole must always be equal sizes.",
            "feedback": "When working with area models, beware that how big a part of the picture is is very important. Equal values should have equal area. Since the 2 is two wholes, and each whole is 4/4, we need to draw each of those left two boxes as rectangles just like your 3/4. Doing so will show us that we have 4 + 4 + 3 = 11 shaded pieces. Since each of the pieces is a fourth, we know 2 3/4 = 11/4. It is probably helpful to just keep the space in between the wholes, so we don't accidentally interpret the picture as meaning one whole giant whole with more than 4 parts."
        },
        "div-standard-1": {
            "work_desc_1": "The student was trying to divide ",
            "work_math": "632 \\div 15",
            "work_desc_2": " by using the standard algorithm, with remainder.",
            "incorrect": "First, the student did not align the digits of the quotient with the correct digits of the dividend. Since 15 does not divide 6, we move over to include the 3 to look at 63. The first digit of the quotient should be placed above the 3. Next, the student underestimated how many 15s are in 63, and said 3 instead of 4. Finally, the student tried to multiply 12 times 15 to account for how many times 15 goes into 182. However, we should not use more than one digit at a time in the quotients in the standard algorithm.",
            "thinking": "The student probably didn't realize that the partial remainder of 18 is larger than 15, or that such a result means we've made a mistake in the standard algorithm. They may also not have realized that the placement of the digits in the quotient hold meaning.",
            "feedback": "Always be careful where you place your digits in your quotient. Each should be placed above the rightmost digit of the number we are currently subtracting from. Also be careful to check partial remainders before bringing down another dividend digit. In your case, 18 is greater than 15, which means we need to go back, erase the 3, and figure out what higher amount of 15s can fit in 63."
        },
        "div-standard-2": {
            "work_desc_1": "The student was trying to divide ",
            "work_math": "683 \\div 21",
            "work_desc_2": " by using the standard algorithm, with remainder.",
            "incorrect": "First, the student did not align the digits of the quotient with the correct digits of the dividend. Since 21 does not divide 6, we move over to include the 8 to look at 68. The first digit of the quotient should be placed above the 8. Next, the student underestimated how many 21s are in 68, and said 2 instead of 3. Finally, the student tried to multiply 12 times 21 to account for how many times 21 goes into 263. However, we should not use more than one digit at a time in the quotients in the standard algorithm.",
            "thinking": "The student probably didn't realize that the partial remainder of 26 is larger than 21, or that such a result means we've made a mistake in the standard algorithm. They may also not have realized that the placement of the digits in the quotient hold meaning.",
            "feedback": "Always be careful where you place your digits in your quotient. Each should be placed above the rightmost digit of the number we are currently subtracting from. Also be careful to check partial remainders before bringing down another dividend digit. In your case, 26 is greater than 21, which means we need to go back, erase the 2, and figure out what higher amount of 21s can fit in 26."
        },
        "add-coladd-2": {
            "work_desc_1": "The student was trying to add ",
            "work_math": "5269 + 6383",
            "work_desc_2": " using the column addition algorithm.",
            "incorrect": "Instead of regrouping from lower to higher place values, they regrouped from higher to lower. At the end, they allowed the 13 in the ones to stay, bumping the remaining place values one place value too high.",
            "thinking": "The student knew to regroup, but probably doesn't have a full grasp of why we regroup from right to left. The student may have gotten confused about what to do if they regrouped to the right and had nowhere to regroup the 13.",
            "feedback": "We should regroup from right to left, because a group of ten in base ten is one group of the next to the left. Consider the 14 from the 6 and the 8. That is 14 tens, which is 140. In other words, we have 1 group of one hundred and 4 groups of ten left over. So we want to regroup that 1 over to the left and make 6 total hundreds. Likewise with the thousands column. Finally, be sure that all your final values in each column are less than ten, and all regrouping is done, before writing your final answer."
        },
        "frac-equivalence-2": {
            "work_desc_1": "The student was trying to convert ",
            "work_math": "3 \\frac{4}{5}",
            "work_desc_2": " to a single, improper fraction by using an area model as their guide.",
            "incorrect": "The main issue is that their model does not have a consistent area to represent the whole (5/5). In the initial diagram for 3 4/5, the whole is both a square and a longer rectangle with five parts. In the second, it again changes to be longer, as they considered all the parts to be one larger whole split into 8 pieces. Furthermore, the pieces of the whole are not equal. In fraction models, the areas of the pieces of the whole must also all be equal.",
            "thinking": "The student may have been thinking that with fractions, we can always combine the numerator pieces, and count our numerator pieces over our total number of pieces. They may not have a robust understanding of how the parts of the whole must always be equal sizes.",
            "feedback": "When working with area models, beware that how big a part of the picture is is very important. Equal values should have equal area. Since the 3 is three wholes, and each whole is 5/5, we need to draw each of those left three boxes as rectangles just like your 4/5. Doing so will show us that we have 5 + 5 + 5 + 4 = 19 shaded pieces. Since each of the pieces is a fifth, we know 3 4/5 = 19/5. It is probably helpful to just keep the space in between the wholes, so we don't accidentally interpret the picture as meaning one whole giant whole with more than 5 parts."
        },
        "div-dec-standard-1": {
            "work_desc_1": "The student was trying to divide ",
            "work_math": "378.5 \\div 0.25",
            "work_desc_2": " using the standard algorithm.",
            "incorrect": "The student did not move the decimal on both dividend and divisor far enough. They should move the decimal at least two places, so that the divisor is a whole number. The student also did not continue dividing until they arrived at zero or found a repeating decimal pattern. Instead, they treated the 10 as a sort of remainder after the decimal point.",
            "thinking": "The student may have been thinking that we only need to move the decimals until the dividend is a whole number. They may have also thought that remainders and amounts after the decimal point are interchangable.",
            "feedback": "Make sure to move the decimals on both numbers until the divisor is a whole number, not the dividend. Moving the decimal is actually just multiplying both numbers by 10, so there is no harm in continuing past the last digit of the dividend. We can place an extra zero at the end of the dividend. If we are dividing with decimal numbers, we don't usually have a concept of remainder. We need to bring down the next digits one at a time (all zeros from here on out) and continue the long division process until it stops or we find a repeating pattern."
        },

        "mult-lattice-2": {
            "work_desc_1": "The student was trying to multiply ",
            "work_math": "74 × 94",
            "work_desc_2": " by using the lattice algorithm.",
            "incorrect": "The student added 4 + 4 instead of multiplying. They also seemed unsure of what to do with the 14 in the second chute, and simply smushed it together with the surrounding digits in the final product.",
            "thinking": "Since they multiplied every other partial product correctly, the student probably just lost track of what operation they were performing with 4 and 4. The student may not remember that this algorithm sometimes requires that we regroup after the adding step.",
            "feedback": "Be careful, 4 times 4 should be 16, not 8. After adding diagonally, check that we only have one digit at the end of each chute. If not, we need to regroup. Your 14 needs to have its first digit regrouped to the next chute. Like the standard algorithm, you could place this above the chute. Or, you could place it at the bottom. Either way, we need to add 3 + 3 + 2 + 1 to get 9 in the hundreds chute."
        },

        "add-standard-1": {
            "work_desc_1": "The student was trying to add ",
            "work_math": "5286 + 1837",
            "work_desc_2": " using the standard algorithm.",
            "incorrect": "Each time they went to regroup to the next column, the student placed the ones instead of the tens. For instance, in 6 + 7 = 13, they placed the 3 above the tens column, instead of the 1.",
            "thinking": "This student may not have an understanding of why we regroup. They may have been thinking that one of the two digits needs to be placed above the next column, but not have an understanding of why this is so.",
            "feedback": "You've got the idea of the algorithm, but we need to be careful which number we are regrouping to the next column each time. For instance, with 6 + 7 = 13, the 13 represents 1 group of ten and 3 ones left over. That means the 3 is what needs to stay in our ones column, and the 1 is what needs to move over to the tens column. Each time we regroup a number, its left (higher place value) digit will be moved above the next column to the left (the next higher place value)."
        },
    }


    # Load the used versions from a JSON file
    def load_used_keys(filepath):
        if not Path(filepath).exists():  # Check if the file exists
            # Create the file if it doesn't exist
            with open(filepath, 'w') as file:
                json.dump([], file)  # Initialize with an empty list
        try:
            with open(filepath, 'r') as file:
                return json.load(file)  # Load the JSON data
        except json.JSONDecodeError:  # Handle any decoding errors
            return []  # If file exists but is empty or invalid, return empty list

    # Save the used version to a JSON file
    def save_used_keys(filepath, used_keys):
        with open(filepath, 'w') as file:
            json.dump(used_keys, file)

    if mode == 'html':
        available_versions = list(html_versions)
        version_name = random.choice(available_versions)
        version_data = html_versions[version_name]
    else:
        used_versions_file = Path('assets/R1/used_versions.json')

        used_versions = load_used_keys(used_versions_file)
        available_by_progress = get_available_versions(course_progress)
        available_versions = [x for x in available_by_progress if x not in used_versions]
        if available_versions:
            version_name = random.choice(available_versions)
        else:
            version_name = used_versions[0]
            used_versions = used_versions[1:]

        used_versions.append(version_name)
        save_used_keys(used_versions_file, used_versions)
        version_data = versions[version_name]

    version_data['version'] = version_name

    return version_data
