from fathom import Point, ORIGIN, centroid
import fathom.geometry as geo
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners

def draw_resource(canvas, center, text):
    r = canvas.new_rectangle(
        center = center,
        width = 1.2,
        height = 0.8,
    ).get_skeleton()
    canvas.new_text(
        text = text,
        anchor = center,
    )
    return r

if __name__ == '__main__':
    canvas = tikz.Canvas()

    SEP = Point(2, 0)
    o = draw_resource(canvas, ORIGIN, '.o')
    a = draw_resource(
        canvas,
        SEP,
        '.a')
    so = draw_resource(
        canvas,
        SEP + SEP,
        '.so')
    exe = draw_resource(
        canvas,
        SEP + SEP + SEP,
        'exe')

    lib = canvas.new_rectangle(
        center = centroid([a.center(), so.center()]) + Point(0, 2),
        width = 1,
        height = 0.8,
        pen_color = colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_text(
        text = 'library',
        anchor = lib.center(),
    )
    canvas.new_line(src = a, dst = lib)
    canvas.new_line(src = so, dst = lib)

    ar = canvas.new_rectangle(
        center = a.center() + Point(0, -2),
        width = 1,
        height = 0.8,
        pen_color = colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_text(
        text = 'ar',
        anchor = ar.center(),
    )
    canvas.new_line(src = a, dst = ar)

    elf = canvas.new_rectangle(
        center = so.center() + Point(0, -2),
        width = 1,
        height = 0.8,
        pen_color = colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_text(
        text = 'ELF',
        anchor = elf.center(),
    )
    canvas.new_line(src = o, dst = elf)
    canvas.new_line(src = so, dst = elf)
    canvas.new_line(src = exe, dst = elf)

    print(canvas.draw())
