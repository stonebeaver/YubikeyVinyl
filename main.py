import svgwrite
import sympy
from sympy.physics.units import convert_to, inch, mm

pt = inch / 72


## parameters

sheet_w = (
    12 * inch - inch / 2
)  # they claim that they would sell you 12 inches but never let you plot inside a qaurter margin border on both sides
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


def die_cut(X, Y):
    W = 2 * body_w + 3 * margin_kiss_to_die
    H = body_h + 2 * margin_kiss_to_die
    return [
        "M",  ################
        q(X + 0 * ε),
        q(Y + 0 * ε),
        "L",
        q(X + 0 * ε),
        q(Y + H - 0 * ε),
        "L",
        q(X + W - 0 * ε),
        q(Y + H - 0 * ε),
        "L",
        q(X + W - 0 * ε),
        q(Y + 0 * ε),
        "z",
        "M",  ################
        q(X + 1 * ε),
        q(Y + 1 * ε),
        "L",
        q(X + W - 1 * ε),
        q(Y + 1 * ε),
        "L",
        q(X + W - 1 * ε),
        q(Y + H - 1 * ε),
        "L",
        q(X + 1 * ε),
        q(Y + H - 1 * ε),
        "z",
        "M",  ################
        q(X + 2 * ε),
        q(Y + 2 * ε),
        "L",
        q(X + 2 * ε),
        q(Y + H - 2 * ε),
        "L",
        q(X + W - 2 * ε),
        q(Y + H - 2 * ε),
        "L",
        q(X + W - 2 * ε),
        q(Y + 2 * ε),
        "z",
        "M",  ################
        q(X + 3 * ε),
        q(Y + 3 * ε),
        "L",
        q(X + W - 3 * ε),
        q(Y + 3 * ε),
        "L",
        q(X + W - 3 * ε),
        q(Y + H - 3 * ε),
        "L",
        q(X + 3 * ε),
        q(Y + H - 3 * ε),
        "z",
    ]


def main():
    W = sheet_w
    H = body_h + 3 * margin_kiss_to_die
    plot = svgwrite.Drawing(
        filename="upload_this_to_cricut_maker.svg",
        size=(
            f"{convert_to(W / mm, 1).evalf()}mm",
            f"{convert_to(H / mm, 1).evalf()}mm",
        ),
    )
    delta = 3 * margin_kiss_to_die + 2 * body_w
    sierra = 0 * mm
    path = list()
    while sierra + delta <= sheet_w:
        path += (
            body(
                X=margin_kiss_to_die + sierra,
                Y=margin_kiss_to_die,
            )
            + keyhole(
                X=margin_kiss_to_die + body_w / 2 + sierra,
                Y=margin_kiss_to_die + keyhole_h,
            )
            + touchhole(
                X=margin_kiss_to_die + body_w / 2 + sierra,
                Y=margin_kiss_to_die + touchhole_h,
            )
            + body(
                X=body_w + 2 * margin_kiss_to_die + sierra,
                Y=margin_kiss_to_die,
            )
            + keyhole(
                X=2 * margin_kiss_to_die + 3 * body_w / 2 + sierra,
                Y=margin_kiss_to_die + keyhole_h,
            )
            + die_cut(X=sierra, Y=0)
        )
        sierra += delta
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
    print(f"expected import size: {sierra.evalf()} × {H.evalf()}")
    return


if __name__ == "__main__":
    main()
