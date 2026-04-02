import svgwrite
import sympy
from sympy.physics.units import convert_to, inch, mm

pt = inch / 72


## parameters

sheet_h = (
    12 * inch - inch / 2
)  # cricut claims that they would sell you 12 inches of workspace and material. but they never let you plot inside a qaurter margin border on both sides.
sheet_w = (
    12 * inch - inch / 2
)  # cricut claims that they would sell you 12 inches of workspace and material. but they never let you plot inside a qaurter margin border on both sides.
body_h = 31 * mm
body_w = 16 * mm
body_r = 1 * mm
keyhole_h = 27 * mm
keyhole_d = sympy.Rational("5.5") * mm
touchhole_h = 13 * mm
touchhole_d = sympy.Rational("10.5") * mm
margin_kiss_to_die = sympy.Rational("1.5") * mm
ε = mm / 100


sheet_w = convert_to(
    sheet_w, mm
)  # optimizes calculation speed when we force that up front
sheet_h = convert_to(
    sheet_h, mm
)  # optimizes calculation speed when we force that up front


def q(quantity):
    """adapts a sympy thingy to svgwrite"""
    return convert_to(quantity / pt, 1).evalf()


def body(X, Y):
    return [
        "M",
        q(X + body_w / 2),
        q(Y),
        "l",
        q(body_w / 2 - body_r),
        0,
        "a",
        q(+body_r),
        q(+body_r),
        0,
        0,
        1,
        q(body_r),
        q(body_r),
        "l",
        0,
        q(body_h - 2 * body_r),
        "a",
        q(body_r),
        q(body_r),
        0,
        0,
        1,
        q(-body_r),
        q(+body_r),
        "l",
        q(-(body_w - 2 * body_r)),
        0,
        "a",
        q(body_r),
        q(body_r),
        0,
        0,
        1,
        q(-body_r),
        q(-body_r),
        "l",
        0,
        q(-(body_h - 2 * body_r)),
        "a",
        q(body_r),
        q(body_r),
        0,
        0,
        1,
        q(+body_r),
        q(-body_r),
        "z",
    ]


def keyhole(X, Y):
    keyhole_r = keyhole_d / 2
    return [
        "M",
        q(X + keyhole_r),
        q(Y),
        "a",
        q(keyhole_r),
        q(keyhole_r),
        0,
        0,
        0,
        q(-keyhole_d),
        0,
        "a",
        q(keyhole_r),
        q(keyhole_r),
        0,
        0,
        0,
        q(keyhole_d),
        0,
        "z",
    ]


def touchhole(X, Y):
    touchhole_r = touchhole_d / 2
    return [
        "M",
        q(X + touchhole_r),
        q(Y),
        "a",
        q(touchhole_r),
        q(touchhole_r),
        0,
        0,
        0,
        q(-touchhole_d),
        0,
        "a",
        q(touchhole_r),
        q(touchhole_r),
        0,
        0,
        0,
        q(touchhole_d),
        0,
        "z",
    ]


def die_cut_half(X, Y):
    W = 2 * body_w + 3 * margin_kiss_to_die
    H = body_h + 2 * margin_kiss_to_die
    return [
        "M",
        q(W + X),
        q(H),
        "l",
        q(-W),
        0,
        "l",
        0,
        q(-ε),
        "l",
        q(W - ε),
        0,
        "l",
        0,
        q(-H + ε),
        "l",
        q(ε),
        0,
        "z",
    ]


def die_cut_horizontal(X, Y):
    return [
        "M",
        q(X),
        q(Y + 0 * ε),
        "L",
        q(X + sheet_w),
        q(Y + 0 * ε),
        "L",
        q(X + sheet_w),
        q(Y + 1 * ε),
        "L",
        q(X),
        q(Y + 1 * ε),
        "z",
        "M",
        q(X),
        q(Y + 2 * ε),
        "L",
        q(X + sheet_w),
        q(Y + 2 * ε),
        "L",
        q(X + sheet_w),
        q(Y + 3 * ε),
        "L",
        q(X),
        q(Y + 3 * ε),
        "z",
    ]


def die_cut_vertical(X, Y):
    H = body_h + 2 * margin_kiss_to_die
    return [
        "M",
        q(X + 0 * ε),
        q(Y + 5 * ε),
        "L",
        q(X + 0 * ε),
        q(Y + H),
        "L",
        q(X + 1 * ε),
        q(Y + H),
        "L",
        q(X + 1 * ε),
        q(Y + 5 * ε),
        "z",
        "M",
        q(X + 2 * ε),
        q(Y + 5 * ε),
        "L",
        q(X + 2 * ε),
        q(Y + H),
        "L",
        q(X + 3 * ε),
        q(Y + H),
        "L",
        q(X + 3 * ε),
        q(Y + 5 * ε),
        "z",
    ]


def main():
    step_x = 3 * margin_kiss_to_die + 2 * body_w
    step_y = body_h + 2 * margin_kiss_to_die

    path = list()
    iterator_y = 0 * mm
    while iterator_y + step_y <= sheet_h:
        iterator_x = 0 * mm
        path += die_cut_horizontal(X=iterator_x, Y=iterator_y)
        while iterator_x + step_x <= sheet_w:
            path += (
                body(
                    X=margin_kiss_to_die + iterator_x,
                    Y=margin_kiss_to_die + iterator_y,
                )
                + keyhole(
                    X=margin_kiss_to_die + body_w / 2 + iterator_x,
                    Y=margin_kiss_to_die + keyhole_h + iterator_y,
                )
                + touchhole(
                    X=margin_kiss_to_die + body_w / 2 + iterator_x,
                    Y=margin_kiss_to_die + touchhole_h + iterator_y,
                )
                + body(
                    X=body_w + 2 * margin_kiss_to_die + iterator_x,
                    Y=margin_kiss_to_die + iterator_y,
                )
                + keyhole(
                    X=2 * margin_kiss_to_die + 3 * body_w / 2 + iterator_x,
                    Y=margin_kiss_to_die + keyhole_h + iterator_y,
                )
                + die_cut_vertical(X=iterator_x, Y=iterator_y)
            )
            iterator_x += step_x
        path += die_cut_vertical(X=iterator_x, Y=iterator_y)
        iterator_y += step_y
    path += die_cut_horizontal(X=0, Y=iterator_y)

    plot = svgwrite.Drawing(
        filename="upload_this_to_cricut_maker.svg",
        size=(
            f"{convert_to(sheet_w / mm, 1).evalf()}mm",
            f"{convert_to(sheet_h / mm, 1).evalf()}mm",
        ),
    )
    plot.add(
        plot.path(
            d=path,
            fill="#808080",
            fill_opacity=0.5,
            stroke="black",
            stroke_width=0.1,
        )
    )
    plot.save()
    print(f"expected plot size {iterator_x.evalf()} × {iterator_y.evalf()}")
    print(f"on a sheet of {sheet_w.evalf()} × {sheet_h.evalf()}")


if __name__ == "__main__":
    main()
