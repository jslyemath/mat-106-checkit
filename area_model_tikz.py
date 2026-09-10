"""TikZ sources for the fraction models F2 and F2-E ask for.

Lives at the bank root so both outcomes import one copy; it used to exist twice,
byte-identical, as an extension-less `area_model_tikz` file inside each outcome
folder -- which is why nothing could import it and it was only ever run by hand
to make images for print.

Each function returns TikZ *source*. CheckIt writes it to <seed>/<name>.tikz and
compiles it to a PNG, so one definition now serves the viewer and print alike.
"""

# area_model_tikz.py

from math import ceil, sqrt, cos, sin, radians

TIKZ_HEADER = r"""\begin{tikzpicture}[scale=1.5, every node/.style={inner sep=0,outer sep=0}, line width=1pt, line style/.style={line width=1pt}]
"""
TIKZ_FOOTER = r"\end{tikzpicture}"

def tikz_circles(numer, denom):
    n = ceil(numer/denom)
    filled = 0
    lines = [TIKZ_HEADER]
    for i in range(n):
        x = 2.2 * i
        for j in range(denom):
            start = j * 360/denom
            end   = (j+1) * 360/denom
            color = "blue!30" if filled < numer else "white"
            filled += 1
            lines.append(
                rf"    \filldraw[fill={color},draw=black] ({x},0) -- ++({start}:1) arc ({start}:{end}:1) -- cycle;")
    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)

def tikz_rectangles(numer, denom):
    n = ceil(numer/denom)
    filled = 0
    lines = [TIKZ_HEADER]
    for i in range(n):
        x = 2.6 * i
        w = 2/denom
        # base outline
        lines.append(rf"    \draw[thick] ({x},0) rectangle ({x+2},1);")
        for j in range(denom):
            color = "blue!30" if filled < numer else "white"
            filled += 1
            lines.append(
                rf"    \filldraw[fill={color},draw=black] ({x + j*w},0) rectangle ({x + (j+1)*w},1);")
    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)

def tikz_trapezoids(numer, denom):
    assert denom in (2,3,6)
    n = ceil(numer/denom)
    filled = 0
    lines = [TIKZ_HEADER]

    for i in range(n):
        x = 2.2*i
        # corner coords
        BL = f"({x-1:.3f},0)"; BR = f"({x+1:.3f},0)"
        TL = f"({x-0.5:.3f},1)"; TR = f"({x+0.5:.3f},1)"
        trap_path = f"{BL} -- {BR} -- {TR} -- {TL} -- cycle"

        # 1) draw outline
        lines.append(rf"    \draw[thick] {trap_path};")

        # 2) clip to trapezoid
        lines.append(r"    \begin{scope}")
        lines.append(rf"        \clip {trap_path};")

        # 3) fill parts inside the clip
        if denom==2:
            parts = [
              (BL, f"({x:.3f},0)", f"({x:.3f},1)", TL),
              (f"({x:.3f},0)", BR, TR, f"({x:.3f},1)")
            ]
        elif denom==3:
            MB = f"({x:.3f},0)"; MT = f"({x:.3f},1)"
            parts = [
              (BL, MB, TL),
              (TL, TR, MB),
              (MB, BR, TR)
            ]
        else:  # denom==6
            MB = f"({x:.3f},0)"; QL = f"({x-0.5:.3f},0)"
            QR = f"({x+0.5:.3f},0)"; MT = f"({x:.3f},1)"
            parts = [
              (BL, QL, TL),(QL, MB, TL),
              (MB, QR, TR),(QR, BR, TR),
              (TL, MT, MB),(MB, MT, TR)
            ]

        for pts in parts:
            color = "blue!30" if filled < numer else "white"
            filled += 1
            coord_str = " -- ".join(pts)
            lines.append(rf"        \filldraw[fill={color},draw=black] {coord_str} -- cycle;")

        # 4) end clipping
        lines.append(r"    \end{scope}")

    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)


def tikz_triangles(numer, denom):
    n = ceil(numer/denom)
    filled = 0
    h = sqrt(3)/2
    lines = [TIKZ_HEADER]
    for i in range(n):
        x = 1.2 * i
        BL = f"({x-0.5:.3f},0)"; BR = f"({x+0.5:.3f},0)"; T = f"({x:.3f},{h:.3f})"
        tri_path = f"{BL} -- {BR} -- {T} -- cycle"
        lines.append(rf"    \draw[thick] {tri_path};")
        # clip
        lines.append(r"    \begin{scope}")
        lines.append(rf"        \clip {tri_path};")
        # parts
        if denom == 2:
            parts = [
                (BL, f"({x:.3f},0)", T),
                (f"({x:.3f},0)", BR, T)
            ]
        else:
            C = f"({x:.3f},{(0+0+h)/3:.3f})"
            parts = [
                (BL, C, T),
                (BR, C, T),
                (BL, BR, C)
            ]
        for pts in parts:
            color = "blue!30" if filled < numer else "white"
            filled += 1
            coord_str = " -- ".join(pts)
            lines.append(rf"        \filldraw[fill={color},draw=black] {coord_str} -- cycle;")
        lines.append(r"    \end{scope}")
    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)


def tikz_hexagons(numer, denom):
    assert denom in (2,3,4,6)
    n = ceil(numer/denom)
    filled = 0
    lines = [TIKZ_HEADER]

    for i in range(n):
        x = 2*sqrt(3) * i
        center = (x, 0.0)
        # 1) compute outer vertices
        pts = [(x + cos(radians(60*j)), sin(radians(60*j))) for j in range(6)]
        hex_path = " -- ".join(f"({u:.3f},{v:.3f})" for u,v in pts) + " -- cycle"

        # draw the hexagon outline
        lines.append(rf"    \draw[thick] {hex_path};")
        # clip everything to inside that outline
        lines.append(r"    \begin{scope}")
        lines.append(rf"        \clip {hex_path};")

        # decide how to partition:
        if denom == 2:
            top = [pts[j] for j in (0,1,2,3)]
            bottom = [pts[j] for j in (3,4,5,0)]
            parts = [top, bottom]

        elif denom == 3:
            parts = [
            [center, pts[0], pts[1], pts[2]],
            [center, pts[2], pts[3], pts[4]],
            [center, pts[4], pts[5], pts[0]],
            ]

        elif denom == 4:
            mids = [
                ((pts[j][0] + pts[(j+1)%6][0]) / 2,
                (pts[j][1] + pts[(j+1)%6][1]) / 2)
                for j in range(6)
            ]
            parts = [
                [ center,
                pts[0],
                pts[1],
                mids[1]
                ],
                [ center,
                mids[1],
                pts[2],
                pts[3]
                ],
                [ center,
                pts[3],
                pts[4],
                mids[4]
                ],
                [ center,
                mids[4],
                pts[5],
                pts[0]
                ],
            ]

        else:  # denom == 6
            # six triangles from center out
            parts = []
            for j in range(6):
                parts.append([
                    (x,0),
                    pts[j],
                    pts[(j+1)%6]
                ])

        # now fill in order
        for poly in parts:
            color = "blue!30" if filled < numer else "white"
            filled += 1
            coord_str = " -- ".join(f"({u:.3f},{v:.3f})" for u,v in poly)
            lines.append(rf"        \filldraw[fill={color},draw=black] {coord_str} -- cycle;")

        # end clipping
        lines.append(r"    \end{scope}")

    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)



def tikz_semicircles(numer, denom):
    n = ceil(numer / denom)
    filled = 0
    lines = [TIKZ_HEADER]

    for i in range(n):
        x = 2.2 * i            # horizontal spacing
        step = 180 / denom     # degrees per slice
        # Define the half‐circle path: start at rightmost point, go CCW to leftmost
        half_path = rf"({x+1:.3f},0) arc (0:180:1) -- ({x-1:.3f},0) -- cycle"

        # 1) draw the outline
        lines.append(rf"    \draw[thick] {half_path};")
        # 2) clip to that half‐disk
        lines.append(r"    \begin{scope}")
        lines.append(rf"        \clip {half_path};")

        # 3) fill each wedge inside the clip
        for j in range(denom):
            start = j * step
            end   = (j+1) * step
            color = "blue!30" if filled < numer else "white"
            filled += 1
            lines.append(
                rf"        \filldraw[fill={color},draw=black] "
                rf"({x},0) -- ++({start}:1) arc ({start}:{end}:1) -- cycle;")

        # 4) end clipping
        lines.append(r"    \end{scope}")

    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)


    lines.append(TIKZ_FOOTER)
    return "\n".join(lines)


# dispatcher
shape_funcs = {
    'circle':          tikz_circles,
    'rectangle':       tikz_rectangles,
    'isosceles trapezoid': tikz_trapezoids,
    'equilateral triangle': tikz_triangles,
    'regular hexagon': tikz_hexagons,
    'semicircle':      tikz_semicircles
}

def generate_tikz(shape, numer, denom):
    assert shape in shape_funcs, f"Unknown shape {shape}"
    return shape_funcs[shape](numer, denom)


# Example usage:
# if __name__ == "__main__":
#     print(generate_tikz('semicircle', 4, 3))


# --------------------------------------------------------------------------
# Number lines.
#
# The shape functions above came from the print-only script; number lines did
# not, because that half was drawn with matplotlib in a graphics() method that
# is now commented out inside the generators. This replaces it, so both kinds
# of model come from one place and neither needs SageMath or matplotlib.

def tikz_number_line(ticks, labels, point=None):
    """A number line with `ticks` intervals and labelled positions.

    `labels` maps an integer position to LaTeX shown beneath it; `point` is an
    optional position to mark with a filled dot, which is what distinguishes an
    answer diagram from its problem.

    Drawn with the theme's `blank number line style`, which is what decides the
    double arrowheads, the tick length and the line weight. One source, two
    surfaces: CheckIt rasterizes this to PNG for the viewer, and a printed
    handout inputs the same .tikz.

    It used to be hand-drawn TikZ while the print template drew its own
    pgfplots axis -- two drawings of one picture, differing in every one of
    those properties. The visible symptom was a web number line with no
    left-hand arrowhead.
    """
    ordered = sorted(labels.items())
    positions = ",".join(str(p) for p, _ in ordered)
    texts = ",".join("$%s$" % t for _, t in ordered)
    out = [
        r"\setmyx{0}{%d}" % ticks,
        r"\begin{tikzpicture}[scale=2.3]",
        r"    \begin{axis}[blank number line style,",
        r"    extra x ticks={%s}," % positions,
        r"    extra x tick labels={%s}]" % texts,
    ]
    if point is not None:
        # scCOLOR is the theme's per-skill colour, so the answer dot matches
        # the skill box above it instead of being a hardcoded blue.
        out.append(
            r"        \node at (axis cs:%d,0) "
            r"{\tikz \fill[scCOLOR] (0,0) circle (2pt);};" % point
        )
    out += [r"    \end{axis}", r"\end{tikzpicture}"]
    return "\n".join(out)
