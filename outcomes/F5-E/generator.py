"""F5-E: analysing an elementary student's proportional reasoning.

A missing-value word problem, a fictional student's work on it, and two
questions: describe the first step, the model and the numbers used first;
then judge whether the model was used accurately and the answer right.
Built from a colleague's hand-made version; the design and the reasons
behind it are in checkit/CODEBASE_NOTES.md, "F5-E: analysing a student's
proportional reasoning (2026-11-18)".

The numbers. A unit pair p : q (coprime, both 2..9), a given multiplier m
and an asked multiplier k (2..8, neither dividing the other):

    given  a = m*p  with  b = m*q        asked  c = k*q  ->  answer  x = k*p

so neither the ratio between the two quantities (p/q) nor the scale factor
within one (k/m) is a whole number -- the condition under which students
stop multiplying by "the obvious number" and show how they really reason.

Every problem has an irrelevant number (the colleague's "Exit 24"), which
one kind of incorrect work uses.
"""
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from math import gcd

import bank_helpers as sm


# --------------------------------------------------------------- contexts --

class Context:
    """One kind of situation. A is the quantity asked for; B is the one
    given in both situations. `text(a, b, c, D)` is the problem as TeX
    prose; the rest is vocabulary the answer key is written from."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


def _contexts(student):
    host = sm.random_person(avoid=[student])
    hs, hp = host.subj_pronoun(), host.poss_adjective()
    c1, c2 = random.sample(["red", "silver", "blue", "white", "green", "black"], 2)
    school = random.choice(["Maple Street", "Riverside", "Lincoln", "Hillcrest",
                            "Oak Grove", "Lakeview"])
    return [
        Context(
            key="cars", maxA=80, maxB=80, D=(10, 70),
            ratio_ok=lambda p, q: True,
            text=lambda a, b, c, D: (
                f"A {c1} car and a {c2} car are traveling at different but constant "
                f"speeds. They pass Exit {D} at the same time. When the {c1} car has "
                f"traveled {a} miles past Exit {D}, the {c2} car has traveled {b} "
                f"miles. How far will the {c1} car have traveled when the {c2} car "
                f"has traveled {c} miles past Exit {D}?"),
            A_short=f"{c1.capitalize()} (mi)", B_short=f"{c2.capitalize()} (mi)",
            A_amt=lambda n: f"{n} miles by the {c1} car",
            B_amt=lambda n: f"{n} miles by the {c2} car",
            pair=lambda nA, nB: f"the {c1} car travels {nA} miles while the {c2} car travels {nB} miles",
            A_name=f"the {c1} car's distance", B_name=f"the {c2} car's distance",
            B_two=f"the {c2} car's two distances",
            per_B=f"for each mile the {c2} car travels",
            distractor=lambda D: f"the exit number, {D}",
            answer=lambda x: f"the {c1} car will have traveled {x} miles",
        ),
        Context(
            key="punch", maxA=40, maxB=48, D=(12, 40),
            ratio_ok=lambda p, q: True,
            text=lambda a, b, c, D: (
                f"{host.name} is making punch for a party of {D} guests. "
                f"{hp.capitalize()} recipe mixes {a} cups of cranberry juice with {b} "
                f"cups of ginger ale. To make a batch that tastes the same, how many "
                f"cups of cranberry juice should {hs} mix with {c} cups of ginger ale?"),
            A_short="Juice (cups)", B_short="Ginger ale (cups)",
            A_amt=lambda n: f"{n} cups of juice", B_amt=lambda n: f"{n} cups of ginger ale",
            pair=lambda nA, nB: f"{nA} cups of juice go with {nB} cups of ginger ale",
            A_name="the amount of juice", B_name="the amount of ginger ale",
            B_two="the two amounts of ginger ale",
            per_B="for each cup of ginger ale",
            distractor=lambda D: f"the number of guests, {D}",
            answer=lambda x: f"{host.name} should use {x} cups of cranberry juice",
        ),
        Context(
            key="paint", maxA=64, maxB=64, D=(8, 30),
            ratio_ok=lambda p, q: True,
            text=lambda a, b, c, D: (
                f"An art class is painting a mural {D} feet long. To mix the shade "
                f"of green they want, they use {a} ounces of blue paint for every "
                f"{b} ounces of yellow paint. How many ounces of blue paint should "
                f"they mix with {c} ounces of yellow paint to get the same shade?"),
            A_short="Blue (oz)", B_short="Yellow (oz)",
            A_amt=lambda n: f"{n} ounces of blue", B_amt=lambda n: f"{n} ounces of yellow",
            pair=lambda nA, nB: f"{nA} ounces of blue go with {nB} ounces of yellow",
            A_name="the amount of blue paint", B_name="the amount of yellow paint",
            B_two="the two amounts of yellow paint",
            per_B="for each ounce of yellow",
            distractor=lambda D: f"the length of the mural, {D} feet",
            answer=lambda x: f"they need {x} ounces of blue paint",
        ),
        Context(
            key="map", maxA=40, maxB=72, D=(20, 60),
            ratio_ok=lambda p, q: True,
            text=lambda a, b, c, D: (
                f"On a map of a state park, {a} centimeters represent {b} kilometers "
                f"on the ground. The map is {D} centimeters wide. Two campsites are "
                f"{c} kilometers apart. How far apart are the campsites on the map?"),
            A_short="Map (cm)", B_short="Ground (km)",
            A_amt=lambda n: f"{n} centimeters on the map",
            B_amt=lambda n: f"{n} kilometers on the ground",
            pair=lambda nA, nB: f"{nA} centimeters on the map stand for {nB} kilometers",
            A_name="the distance on the map", B_name="the distance on the ground",
            B_two="the two distances on the ground",
            per_B="for each kilometer on the ground",
            distractor=lambda D: f"the width of the map, {D} centimeters",
            answer=lambda x: f"the campsites are {x} centimeters apart on the map",
        ),
        Context(
            key="price", maxA=40, maxB=72, D=(10, 40),
            # a pound of apples costs between $1 and $4.50
            ratio_ok=lambda p, q: 1 <= q / p <= 4.5,
            text=lambda a, b, c, D: (
                f"A farmers' market has {D} stalls. At one of them, {a} pounds of "
                f"apples cost \\${b}. At the same price per pound, how many pounds "
                f"of apples can you buy for \\${c}?"),
            A_short="Apples (lb)", B_short="Cost (\\$)",
            A_amt=lambda n: f"{n} pounds of apples", B_amt=lambda n: f"\\${n}",
            pair=lambda nA, nB: f"{nA} pounds of apples cost \\${nB}",
            A_name="the weight of apples", B_name="the cost",
            B_two="the two costs",
            per_B="for each dollar",
            distractor=lambda D: f"the number of stalls, {D}",
            answer=lambda x: f"you can buy {x} pounds of apples",
        ),
        Context(
            key="shadow", maxA=60, maxB=72, D=(15, 60),
            ratio_ok=lambda p, q: True,
            text=lambda a, b, c, D: (
                f"At the same time of day, a flagpole {a} feet tall casts a shadow "
                f"{b} feet long, and a tree standing {D} feet from the flagpole "
                f"casts a shadow {c} feet long. How tall is the tree?"),
            A_short="Height (ft)", B_short="Shadow (ft)",
            A_amt=lambda n: f"a height of {n} feet", B_amt=lambda n: f"a shadow of {n} feet",
            pair=lambda nA, nB: f"an object {nA} feet tall casts a shadow {nB} feet long",
            A_name="the height", B_name="the length of the shadow",
            B_two="the two shadows",
            per_B="for each foot of shadow",
            distractor=lambda D: f"the distance between the tree and the flagpole, {D} feet",
            answer=lambda x: f"the tree is {x} feet tall",
        ),
        Context(
            key="reading", maxA=72, maxB=72, D=(8, 30),
            ratio_ok=lambda p, q: 0.3 <= p / q <= 2,
            text=lambda a, b, c, D: (
                f"{host.name} is reading a book with {D} chapters at a steady pace. "
                f"{hs.capitalize()} {sm.verb_switch('reads', host.gender)} {a} pages in "
                f"{b} minutes. How many pages will {host.name} read in {c} minutes?"),
            A_short="Pages", B_short="Minutes",
            A_amt=lambda n: f"{n} pages", B_amt=lambda n: f"{n} minutes",
            pair=lambda nA, nB: f"{host.name} reads {nA} pages in {nB} minutes",
            A_name="the number of pages", B_name="the time",
            B_two="the two times",
            per_B="each minute",
            distractor=lambda D: f"the number of chapters, {D}",
            answer=lambda x: f"{host.name} will read {x} pages",
        ),
        Context(
            key="club", maxA=40, maxB=40, D=(12, 36),
            ratio_ok=lambda p, q: True,
            text=lambda a, b, c, D: (
                f"{school} Elementary has {D} classrooms. Its chess club has {a} "
                f"fifth graders and {b} fourth graders. The art club has fifth and "
                f"fourth graders in the same ratio, and it has {c} fourth graders. "
                f"How many fifth graders are in the art club?"),
            A_short="5th graders", B_short="4th graders",
            A_amt=lambda n: f"{n} fifth graders", B_amt=lambda n: f"{n} fourth graders",
            pair=lambda nA, nB: f"there are {nA} fifth graders for every {nB} fourth graders",
            A_name="the number of fifth graders", B_name="the number of fourth graders",
            B_two="the two numbers of fourth graders",
            per_B="for each fourth grader",
            distractor=lambda D: f"the number of classrooms, {D}",
            answer=lambda x: f"the art club has {x} fifth graders",
        ),
        Context(
            key="recipe", maxA=24, maxB=48, D=(25, 60),
            ratio_ok=lambda p, q: p < q,              # fewer eggs than servings
            text=lambda a, b, c, D: (
                f"A casserole recipe that serves {b} people uses {a} eggs and bakes "
                f"for {D} minutes. How many eggs are needed to make the same "
                f"casserole for {c} people?"),
            A_short="Eggs", B_short="Servings",
            A_amt=lambda n: f"{n} eggs", B_amt=lambda n: f"{n} servings",
            pair=lambda nA, nB: f"{nA} eggs make {nB} servings",
            A_name="the number of eggs", B_name="the number of servings",
            B_two="the two numbers of servings",
            per_B="for each serving",
            distractor=lambda D: f"the baking time, {D} minutes",
            answer=lambda x: f"{x} eggs are needed",
        ),
    ]


def _numbers(ctx):
    """p, q, m, k and the problem's numbers for one context, retried until
    every condition in the module docstring holds."""
    for _ in range(5000):
        p, q = random.randint(2, 9), random.randint(2, 9)
        if p == q or gcd(p, q) != 1 or not ctx.ratio_ok(p, q):
            continue
        m, k = random.randint(2, 8), random.randint(2, 8)
        if m == k or k % m == 0 or m % k == 0:
            continue
        a, b, c, x = m * p, m * q, k * q, k * p
        if max(a, x) > ctx.maxA or max(b, c) > ctx.maxB:
            continue
        if len({a, b, c, x}) < 4:
            continue
        lo, hi = ctx.D
        # The irrelevant number must still make sense: a map is wider
        # than any distance measured on it.
        floor = max(a, x) + 1 if ctx.key == "map" else lo
        choices = [d for d in range(max(lo, floor), hi + 1) if d not in {a, b, c, x}]
        if not choices:
            continue
        D = random.choice(choices)
        return dict(p=p, q=q, m=m, k=k, a=a, b=b, c=c, x=x, D=D)
    raise RuntimeError(f"no numbers found for {ctx.key}")


# ------------------------------------------------------- number writing --

def frac(f):
    f = Fraction(f)
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"


def ratio(f):
    """A fraction as a student would leave it: improper ones as mixed."""
    f = Fraction(f)
    return sm.mixed_number(f, format="latex") if f > 1 else frac(f)


def terminates(f):
    d = Fraction(f).denominator
    for prime in (2, 5):
        while d % prime == 0:
            d //= prime
    return d == 1


def num(f):
    """A result: a whole number, a short decimal, or else a mixed number."""
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    if terminates(f):
        text = format(Decimal(f.numerator) / Decimal(f.denominator), "f")
        if len(text.split(".")[1]) <= 3:
            return text
    return sm.mixed_number(f, format="latex")


def fraction_line(top, bottom):
    """`top/bottom`, simplified (and as a mixed number) when that changes it."""
    f = Fraction(top, bottom)
    line = f"\\frac{{{top}}}{{{bottom}}}"
    if (f.numerator, f.denominator) != (top, bottom):
        line += " = " + frac(f)
    if f > 1 and f.denominator != 1:
        line += " = " + sm.mixed_number(f, format="latex")
    return line


def times_line(f, n):
    """`f x n`, worked by parts when f is a mixed number, as in the
    colleague's sample: 1 1/4 x 36 = 36 + 9 = 45."""
    f = Fraction(f)
    if f > 1 and f.denominator != 1:
        whole = f.numerator // f.denominator
        part = f - whole
        return (f"{ratio(f)} \\times {n} = {num(whole * n)} + {num(part * n)} "
                f"= {num(f * n)}")
    return f"{ratio(f)} \\times {n} = {num(f * n)}"


# ------------------------------------------------------------- the work --
#
# Each kind returns (lines, figure, answer to question 1, answer to question
# 2, the student's answer). `lines` is display maths, or [] when the work is
# a picture. The answers are TeX prose, with $...$ for maths.

def _kinds(N, ctx, n):
    """Every kind of work these numbers allow: name -> (weight, builder)."""
    p, q, m, k, a, b, c, x, D = (n[v] for v in "p q m k a b c x D".split())
    S = N.subj_pronoun()
    pq = frac(Fraction(p, q))
    right = f"The correct answer is {x}: {ctx.answer(x)}."
    check = f"$\\frac{{{a}}}{{{b}}} = {pq}$, and ${pq} \\times {c} = {x}$"
    top_max = max(m, k)
    kinds = {}

    # --------------------------------------------------------- correct --

    def between():
        lines = [fraction_line(a, b), times_line(Fraction(p, q), c)]
        q1 = (f"{N.name} first compared the two quantities from the same moment in "
              f"the problem, dividing {a} ({ctx.A_amt(a)}) by {b} ({ctx.B_amt(b)}) and "
              f"simplifying to ${pq}$. That fraction is a ratio between the two "
              f"quantities: {ctx.pair(p, q)}. So {N.name} used a ratio (multiplicative "
              f"comparison) model, starting with {a} and {b}.")
        q2 = (f"Yes. The ratio between {ctx.A_name} and {ctx.B_name} stays ${pq}$ the "
              f"whole time, so multiplying the new amount, {c}, by ${pq}$ gives the "
              f"matching amount. {N.name}'s answer is correct. {right}")
        return lines, None, q1, q2, x
    kinds["between"] = (1.25, between)

    def within():
        sf = Fraction(c, b)
        lines = [fraction_line(c, b), times_line(sf, a)]
        q1 = (f"{N.name} first compared {ctx.B_two}, the new {c} against the original "
              f"{b}, and found the scale factor ${ratio(sf)}$: the new situation is "
              f"${ratio(sf)}$ times the size of the first. {N.name} used a scale-factor "
              f"model, starting with {b} and {c}.")
        q2 = (f"Yes. Because the two quantities are proportional, {ctx.A_name} changes "
              f"by the same factor, so ${ratio(sf)} \\times {a} = {x}$. {N.name}'s "
              f"answer is correct. {right}")
        return lines, None, q1, q2, x
    kinds["within"] = (1.25, within)

    def chunk():
        lines = [f"{a} \\div {m} = {p}", f"{b} \\div {m} = {q}",
                 f"{c} \\div {q} = {k}", f"{k} \\times {p} = {x}"]
        q1 = (f"{N.name} first divided both {a} and {b} by {m} to find the smallest "
              f"matching amounts: {ctx.pair(p, q)}. That pair is a unit, or "
              f"\"chunk\", that can be repeated. {S.capitalize()} then counted how many "
              f"chunks of {q} make {c} ({k} of them) and built {k} chunks of {p}. This "
              f"is a building-up (composed unit) model, starting with {a} and {b}.")
        q2 = (f"Yes. Every chunk keeps {p} and {q} together, so {k} chunks give "
              f"${k} \\times {p} = {x}$ matched with ${k} \\times {q} = {c}$. "
              f"{N.name}'s answer is correct. {right}")
        return lines, None, q1, q2, x
    kinds["chunk"] = (1.25, chunk)

    def proportion():
        lines = [f"\\frac{{{a}}}{{{b}}} = \\frac{{x}}{{{c}}}",
                 f"{b} \\cdot x = {a} \\cdot {c}", f"{b}x = {a * c}",
                 f"x = {a * c} \\div {b} = {x}"]
        q1 = (f"{N.name} set up a proportion, with {ctx.A_name} in both numerators and "
              f"{ctx.B_name} in both denominators and $x$ for the unknown. The first "
              f"numbers {S} placed were {a} over {b}, which belong to the same moment "
              f"in the problem, and then {c}, with $x$ above it.")
        q2 = (f"Yes. Both fractions compare {ctx.A_name} to {ctx.B_name} in the same "
              f"order, so the proportion is set up correctly, and cross-multiplying and "
              f"dividing by {b} gives $x = {x}$. {N.name}'s answer is correct. {right}")
        return lines, None, q1, q2, x
    kinds["proportion"] = (1.25, proportion)

    def number_line():
        fig = dict(kind="line", top_label=ctx.A_short, bottom_label=ctx.B_short,
                   top=[str(j * p) for j in range(top_max + 1)],
                   bottom=[str(j * q) for j in range(top_max + 1)], circle=k)
        q1 = (f"{N.name} drew a double number line, with {ctx.A_name} on the top line "
              f"and {ctx.B_name} on the bottom, both starting at 0. {S.capitalize()} "
              f"placed {a} above {b} first, split that into {m} equal jumps of {p} and "
              f"{q}, and skip counted by those jumps until the bottom line reached {c}.")
        q2 = (f"Yes. Each jump adds {p} on the top line and {q} on the bottom, so every "
              f"pair of matching marks is in the same ratio, {p} to {q}. Reading the top "
              f"line above {c} gives {x}. {N.name}'s answer is correct. {right}")
        return [], fig, q1, q2, x
    kinds["number line"] = (1.75, number_line)

    # A tape is drawn to scale, so it has to fit: the narrower box wide
    # enough for its number, the longest tape at most about 12 cm.
    unit = 0.5 / min(p, q)
    if top_max * max(p, q) * unit <= 12:
        def tape():
            fig = dict(kind="tape", top_label=ctx.A_short, bottom_label=ctx.B_short,
                       p=p, q=q, m=m, k=k, a=a, b=b, c=c, answer=str(x), unit=unit)
            q1 = (f"{N.name} drew tape diagrams. {S.capitalize()} first split {a} and "
                  f"{b} into {m} equal parts, so each part of the top tape is {p} and "
                  f"each part of the bottom tape is {q}. Then {S} drew {k} parts of {q} "
                  f"to make {c}, with {k} matching parts of {p} above them.")
            q2 = (f"Yes. The parts stay matched, {p} with {q}, so {k} parts on the top "
                  f"tape make ${k} \\times {p} = {x}$. {N.name}'s answer is correct. "
                  f"{right}")
            return [], fig, q1, q2, x
        kinds["tape"] = (1.75, tape)

    # ------------------------------------------------------- incorrect --

    wrong = c - b + a
    if wrong > 0:
        def additive():
            if b > a:
                gap, rel = b - a, "less than"
                lines = [f"{b} - {a} = {gap}", f"{c} - {gap} = {wrong}"]
            else:
                gap, rel = a - b, "more than"
                lines = [f"{a} - {b} = {gap}", f"{c} + {gap} = {wrong}"]
            q1 = (f"{N.name} first found the difference between {a} and {b}, which is "
                  f"{gap}. {S.capitalize()} used an additive model: {S} assumed "
                  f"{ctx.A_name} is always {gap} {rel} {ctx.B_name}, and applied the "
                  f"same difference to {c}.")
            q2 = (f"No. The relationship is multiplicative, not additive: "
                  f"{ctx.pair(p, q)}, so as the quantities grow, the gap between them "
                  f"grows too. Doubling the first situation, for example, gives {2 * a} "
                  f"and {2 * b}, which differ by {2 * gap}, not {gap}. Comparing "
                  f"multiplicatively instead, {check}. {N.name}'s answer of {wrong} is "
                  f"incorrect. {right}")
            return lines, None, q1, q2, wrong
        kinds["additive"] = (2.0, additive)

    off = Fraction(a, D) * c
    if off != x:
        def distractor():
            lines = [fraction_line(a, D), times_line(Fraction(a, D), c)]
            q1 = (f"{N.name} started by dividing {a} by {D}, which is "
                  f"{ctx.distractor(D)}. As in a ratio model, {S} compared two numbers "
                  f"and used the comparison to multiply {c}, but the two numbers {S} "
                  f"chose first do not describe the same moment in the problem.")
            q2 = (f"No. {D} is not part of the relationship between {ctx.A_name} and "
                  f"{ctx.B_name}; it is extra information. The ratio has to come from "
                  f"{a} and {b}, which happen together: {check}. Using a ratio was a "
                  f"good idea, but {N.name} put the wrong numbers in it, so the answer "
                  f"of ${num(off)}$ is incorrect. {right}")
            return lines, None, q1, q2, off
        kinds["distractor"] = (1.5, distractor)

    upside = Fraction(b, a) * c
    side = "smaller" if a < b else "larger"

    def inverted():
        lines = [fraction_line(b, a), times_line(Fraction(b, a), c)]
        q1 = (f"{N.name} compared the two quantities from the same moment, dividing {b} "
              f"by {a} to get ${ratio(Fraction(b, a))}$, and then multiplied {c} by it. "
              f"That is a ratio model, starting with {b} and {a}.")
        q2 = (f"No. Dividing {b} by {a} compares {ctx.B_name} to {ctx.A_name}, so "
              f"multiplying by it finds {ctx.B_name} from {ctx.A_name}, not the reverse. "
              f"To find {ctx.A_name}, {N.name} needed $\\frac{{{a}}}{{{b}}}$ instead. "
              f"A quick check catches it: in the first "
              f"situation {a} is {side} "
              f"than {b}, so the answer should be {side} than {c}, and ${num(upside)}$ "
              f"is not. Instead, {check}. {right}")
        return lines, None, q1, q2, upside
    kinds["inverted ratio"] = (1.0, inverted)

    def mismatched():
        lines = [f"\\frac{{{a}}}{{{b}}} = \\frac{{{c}}}{{x}}",
                 f"{a} \\cdot x = {b} \\cdot {c}", f"{a}x = {b * c}",
                 f"x = {b * c} \\div {a} = {num(upside)}"]
        q1 = (f"{N.name} set up a proportion. {S.capitalize()} placed {a} over {b} "
              f"first, then put {c} in the numerator of the second fraction with $x$ "
              f"below it.")
        q2 = (f"No. The first fraction compares {ctx.A_name} to {ctx.B_name}, but the "
              f"second compares them the other way round: {c} goes with "
              f"{ctx.B_name}, yet it sits in the numerator, where the first fraction "
              f"has {ctx.A_name}. "
              f"Keeping the order the same, $\\frac{{{a}}}{{{b}}} = \\frac{{x}}{{{c}}}$, "
              f"so $x = {x}$. {N.name}'s answer of ${num(upside)}$ is incorrect. {right}")
        return lines, None, q1, q2, upside
    kinds["mismatched proportion"] = (1.0, mismatched)

    steps = [s for s in (2, 3, 4) if c > b and (c - b) % s == 0]
    if steps:
        def additive_line():
            s = random.choice(steps)
            t = (c - b) // s
            fig = dict(kind="line", top_label=ctx.A_short, bottom_label=ctx.B_short,
                       top=[str(a + i * t) for i in range(s + 1)],
                       bottom=[str(b + i * t) for i in range(s + 1)], circle=s)
            q1 = (f"{N.name} drew a double number line with {ctx.A_name} on top and "
                  f"{ctx.B_name} on the bottom. {S.capitalize()} placed {a} above {b} "
                  f"first, then added {t} to both lines at every jump until the bottom "
                  f"line reached {c}.")
            q2 = (f"No. Adding the same amount to both lines is additive reasoning: it "
                  f"keeps the difference between the quantities the same, when it is "
                  f"the ratio that has to stay the same. On a double number line both "
                  f"lines start at 0, and each jump adds amounts in the ratio {p} to "
                  f"{q}: {p} on top for every {q} on the bottom. Done that way, {c} on "
                  f"the bottom lines up with {x} on top, so {N.name}'s answer of "
                  f"{a + c - b} is incorrect. {right}")
            return [], fig, q1, q2, a + c - b
        kinds["additive number line"] = (1.5, additive_line)

    def slipped_line():
        e = random.randint(2, k)
        delta = random.choice([-2, -1, 1, 2])
        top = [str(j * p + (delta if j >= e else 0)) for j in range(top_max + 1)]
        fig = dict(kind="line", top_label=ctx.A_short, bottom_label=ctx.B_short,
                   top=top, bottom=[str(j * q) for j in range(top_max + 1)], circle=k)
        before = int(top[e - 1])
        q1 = (f"{N.name} drew a double number line, with {ctx.A_name} on the top line "
              f"and {ctx.B_name} on the bottom, both starting at 0. {S.capitalize()} "
              f"placed 0 with 0 first, then made jumps of {p} on the top line and {q} "
              f"on the bottom until the bottom line reached {c}.")
        q2 = (f"Partly. The model is set up accurately: both lines start at 0, and "
              f"every jump should add {p} on top and {q} on the bottom. But {N.name} "
              f"made a skip-counting mistake, ${before} + {p} = {before + p}$, not "
              f"{top[e]}, and every mark after it is off by {abs(delta)}. So the "
              f"answer of {top[k]} is incorrect. {right}")
        return [], fig, q1, q2, int(top[k])
    kinds["skip-count slip"] = (1.0, slipped_line)

    for f, mult, first in ((Fraction(p, q), c, (a, b)), (Fraction(c, b), a, (c, b))):
        if f > 1 and f.denominator != 1:
            def mixed_slip(f=f, mult=mult, first=first):
                whole = f.numerator // f.denominator
                part = f - whole
                said = whole * mult + part
                lines = [fraction_line(*first),
                         f"{ratio(f)} \\times {mult} = {sm.mixed_number(said, format='latex')}"]
                model = ("a ratio model, comparing the two quantities from the same "
                         "moment" if first == (a, b) else
                         f"a scale-factor model, comparing {ctx.B_two}")
                q1 = (f"{N.name} first divided {first[0]} by {first[1]} and wrote the "
                      f"result as the mixed number ${ratio(f)}$, then multiplied it by "
                      f"{mult}. That is {model}.")
                q2 = (f"Partly. The model is used accurately: ${ratio(f)}$ is the right "
                      f"number to multiply {mult} by. But multiplying a mixed number "
                      f"means multiplying both of its parts: ${whole} \\times {mult} + "
                      f"{frac(part)} \\times {mult} = {num(whole * mult)} + "
                      f"{num(part * mult)} = {x}$. {N.name} multiplied only the whole "
                      f"number and kept the fraction, so the answer of "
                      f"${sm.mixed_number(said, format='latex')}$ is incorrect. {right}")
                return lines, None, q1, q2, said
            kinds["mixed-number slip"] = (0.75, mixed_slip)
            break

    if not terminates(Fraction(p, q)):
        rate = (Decimal(a) / Decimal(b)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        approx = rate * c
        if Fraction(str(approx)) != x:
            def rounded():
                lines = [f"{a} \\div {b} \\approx {rate}", f"{rate} \\times {c} = {approx}"]
                q1 = (f"{N.name} found a unit rate, dividing {a} by {b} to get "
                      f"{ctx.A_name} {ctx.per_B}. The division does not end, so {S} "
                      f"rounded it to {rate}, and then multiplied by {c}.")
                q2 = (f"Partly. The unit-rate model is accurate, but rounding the "
                      f"repeating decimal changed the answer: {N.name} got {approx} "
                      f"instead of exactly {x}. Keeping the rate as a fraction avoids "
                      f"that: {check}. {right}")
                return lines, None, q1, q2, Fraction(str(approx))
            kinds["rounded unit rate"] = (0.75, rounded)

    return kinds


CORRECT = {"between", "within", "chunk", "proportion", "number line", "tape"}


# -------------------------------------------------------------- generate --

def _describe(N, fig):
    """Alt text for the picture: what a sighted reader sees, in words."""
    if fig["kind"] == "line":
        text = (f"{N}'s double number line: the top line, {fig['top_label']}, is marked "
                f"{', '.join(fig['top'])}; the bottom line, {fig['bottom_label']}, is "
                f"marked {', '.join(fig['bottom'])}; {fig['top'][fig['circle']]} on the "
                f"top line is circled.")
    else:
        text = (f"{N}'s tape diagrams. First, {fig['top_label']}: {fig['m']} parts of "
                f"{fig['p']}, totaling {fig['a']}, over {fig['bottom_label']}: "
                f"{fig['m']} parts of {fig['q']}, totaling {fig['b']}. Then "
                f"{fig['k']} parts of {fig['p']}, totaling {fig['answer']} (circled), "
                f"over {fig['k']} parts of {fig['q']}, totaling {fig['c']}.")
    return text.replace("\\$", "$")


def generate(**kwargs):
    student = sm.random_person()
    ctx = random.choice(_contexts(student))
    n = _numbers(ctx)
    kinds = _kinds(student, ctx, n)
    names = list(kinds)
    kind = random.choices(names, weights=[kinds[k][0] for k in names])[0]
    lines, figure, a1, a2, said = kinds[kind][1]()

    N = student.name
    problem_tex = ctx.text(n["a"], n["b"], n["c"], n["D"])
    q1_tex = (f"Describe the first step that {N} took to solve the problem. What model "
              f"or strategy did {N} use? "
              + (f"What numbers do you think {N} placed first?" if figure else
                 f"Which numbers from the problem did {N} work with first?"))
    q2_tex = (f"Analyze {N}'s work. Was the model or strategy used accurately? Did {N} "
              f"get the correct answer? Explain how you made your decision about the "
              f"accuracy.")

    return {
        "context": ctx.key,
        "kind": kind,
        "correct": kind in CORRECT,
        "answer": n["x"],
        "student_answer": str(said),
        "student": N,
        "verb": "drew" if figure else "wrote",
        "problem": sm.spatext_math(problem_tex),
        "problem_tex": problem_tex,
        "has_figure": bool(figure),
        "figure": figure or {},
        "figure_desc": _describe(N, figure) if figure else "",
        # One string of display maths, empty for a picture: `checkit check`
        # reads a field inside a {{#list}} section as a top-level one.
        "work": "".join(sm.spatext_math(f"\\[{t}\\]") for t in lines),
        "work_lines_tex": lines,
        "q1": sm.spatext_math(q1_tex),
        "q1_tex": q1_tex,
        "q2": sm.spatext_math(q2_tex),
        "q2_tex": q2_tex,
        "a1": sm.spatext_math(a1),
        "a1_tex": a1,
        "a2": sm.spatext_math(a2),
        "a2_tex": a2,
    }


# ----------------------------------------------------------------- figures --

def draw_number_line(fig):
    """A double number line as a student draws one: two arrows, matching
    ticks joined by a faint line, labels above and below, the answer
    circled. Jumps are evenly spaced -- on the additive-error line too,
    since there it is the labels that are wrong, not the drawing."""
    n = len(fig["top"]) - 1
    out = [r"\begin{tikzpicture}[x=1.15cm, y=1cm, font=\small]",
           rf"    \draw[thick, ->] (0,1.2) -- ({n + 0.7},1.2);",
           rf"    \draw[thick, ->] (0,0) -- ({n + 0.7},0);",
           rf"    \node[left] at (-0.2,1.2) {{{fig['top_label']}}};",
           rf"    \node[left] at (-0.2,0) {{{fig['bottom_label']}}};"]
    for j, (t, b) in enumerate(zip(fig["top"], fig["bottom"])):
        ring = ", draw, circle, inner sep=1.5pt" if j == fig["circle"] else ""
        out += [rf"    \draw[gray!60] ({j},0.12) -- ({j},1.08);",
                rf"    \draw ({j},1.32) -- ({j},1.08);",
                rf"    \node[above{ring}] at ({j},1.32) {{{t}}};",
                rf"    \draw ({j},0.12) -- ({j},-0.12);",
                rf"    \node[below] at ({j},-0.12) {{{b}}};"]
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def draw_tapes(fig):
    """Two pairs of tape diagrams, the given situation above the asked one,
    to scale: a box of the top tape is p units wide and one of the bottom
    tape q, so the picture shows the ratio as well as stating it. The
    colleague's braces need decorations.pathreplacing, which the figure
    preamble does not load, so each tape's total is written beside it."""
    p, q, u = fig["p"], fig["q"], fig["unit"]
    out = [r"\begin{tikzpicture}[font=\small]"]

    def pair(y, count, top_total, bottom_total):
        rows = ((y + 0.75, p, top_total, fig["top_label"], top_total == fig["answer"]),
                (y, q, bottom_total, fig["bottom_label"], False))
        for base, size, total, label, circled in rows:
            w = size * u
            out.append(rf"    \node[left] at (-0.2,{base + 0.3:.2f}) {{{label}}};")
            for i in range(count):
                out.append(rf"    \draw[thick] ({i * w:.3f},{base:.2f}) rectangle "
                           rf"({(i + 1) * w:.3f},{base + 0.6:.2f});")
                out.append(rf"    \node[font=\footnotesize] at ({(i + 0.5) * w:.3f},"
                           rf"{base + 0.3:.2f}) {{{size}}};")
            style = "right, draw, circle, inner sep=1.5pt" if circled else "right"
            out.append(rf"    \node[{style}] at ({count * w + 0.2:.3f},{base + 0.3:.2f}) "
                       rf"{{{total}}};")

    pair(0, fig["m"], str(fig["a"]), str(fig["b"]))
    pair(-2.0, fig["k"], fig["answer"], str(fig["c"]))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# CheckIt entry point. A picture is written as TikZ, rasterized for the
# website and \input by print, so the two show the same drawing.
class Generator(BaseGenerator):
    @provide_data
    def tikz_graphics(data):
        if not data["has_figure"]:
            return {}
        fig = data["figure"]
        if fig["kind"] == "line":
            return {"work": draw_number_line(fig)}
        return {"work": draw_tapes(fig)}

    def data(self):
        return generate()
