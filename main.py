import pint
import re
import svgwrite


def q(quantity):
    """adapts a pint unit to svgwrite"""
    formatted_quantity = f"{quantity:~}"
    clean_quantity = re.sub(
        pattern=r"\s+",
        repl="",
        string=formatted_quantity,
    )
    return clean_quantity


ureg = pint.UnitRegistry()
mm = ureg.mm

## parameters

sheet_w = 210 * mm
body_h = 32 * mm
body_w = 12 * mm
body_r = 1.5 * mm
keyhole_h = 28 * mm
keyhole_d = 6 * mm
touchhole_h = 14 * mm
touchhole_d = 10.5 * mm
margin_kiss_to_die = 2 * mm


def main():
    summary = svgwrite.Drawing(
        filename="00_summary.svg",
        size=(
            q(210 * mm),
            # q(305 * mm),
            q(body_h + 3 * margin_kiss_to_die),
        ),
    )
    style_kiss_cut = {
        "fill": "none",
        "stroke": "black",
        "stroke_dasharray": "1",
        "stroke_width": 1,
    }
    style_die_cut = {
        "fill": "none",
        "stroke": "black",
        "stroke_width": 1,
    }
    delta = 3 * margin_kiss_to_die + 2 * body_w
    sierra = 0 * mm
    while sierra + delta <= sheet_w:
        summary.add(
            summary.circle(
                center=(
                    q(margin_kiss_to_die + body_w / 2 + sierra),
                    q(margin_kiss_to_die + touchhole_h),
                ),
                r=q(touchhole_d / 2),
                **style_kiss_cut,
            )
        )
        summary.add(
            summary.circle(
                center=(
                    q(margin_kiss_to_die + body_w / 2 + sierra),
                    q(margin_kiss_to_die + keyhole_h),
                ),
                r=q(keyhole_d / 2),
                **style_kiss_cut,
            )
        )
        summary.add(
            summary.rect(
                insert=(
                    q(margin_kiss_to_die + sierra),
                    q(margin_kiss_to_die),
                ),
                size=(q(body_w), q(body_h)),
                rx=q(body_r),
                ry=q(body_r),
                **style_kiss_cut,
            )
        )
        summary.add(
            summary.circle(
                center=(
                    q(2 * margin_kiss_to_die + 3 * body_w / 2 + sierra),
                    q(margin_kiss_to_die + keyhole_h),
                ),
                r=q(keyhole_d / 2),
                **style_kiss_cut,
            )
        )
        summary.add(
            summary.rect(
                insert=(
                    q(2 * margin_kiss_to_die + body_w + sierra),
                    q(margin_kiss_to_die),
                ),
                size=(q(body_w), q(body_h)),
                rx=q(body_r),
                ry=q(body_r),
                **style_kiss_cut,
            )
        )
        summary.add(
            summary.line(
                start=(
                    q(3 * margin_kiss_to_die + 2 * body_w + sierra),
                    q(2 * margin_kiss_to_die + body_h),
                ),
                end=(
                    q(3 * margin_kiss_to_die + 2 * body_w + sierra),
                    q(0 * mm),
                ),
                **style_die_cut,
            )
        )
        sierra += delta
    summary.add(
        summary.line(
            start=(
                q(0 * mm),
                q(2 * margin_kiss_to_die + body_h),
            ),
            end=(
                q(sheet_w),
                q(2 * margin_kiss_to_die + body_h),
            ),
            **style_die_cut,
        )
    )
    summary.save()


if __name__ == "__main__":
    main()
