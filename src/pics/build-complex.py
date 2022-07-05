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

def draw_processor(canvas, center, text):
    r = canvas.new_circle(
        center = center,
        radius = 0.6,
    ).get_skeleton()
    canvas.new_text(
        text = text,
        anchor = center,
    )
    return r

if __name__ == '__main__':
    canvas = tikz.Canvas()
    LEVEL1 = Point(0, -2)
    LEVEL2 = LEVEL1 + LEVEL1
    LEVEL3 = LEVEL2 + LEVEL1

    sep = Point(2, 0)
    a_c = draw_resource(
        canvas,
        ORIGIN,
        'a.c')
    b_h = draw_resource(
        canvas,
        a_c.center() + sep,
        'b.h')
    b_c = draw_resource(
        canvas,
        b_h.center() + sep,
        'b.c')
    c_in = draw_resource(
        canvas,
        b_c.center() + sep,
        'c.in')
    codegen = draw_processor(
        canvas,
        c_in.center() + sep,
        '\\small codegen')
    canvas.new_arrow(src = c_in, dst = codegen)
    c_c = draw_resource(
        canvas,
        codegen.center() + LEVEL1,
        'c.c')
    canvas.new_arrow(src = codegen, dst = c_c)

    gcc_to_a_o = draw_processor(
        canvas,
        centroid([a_c.center(), b_h.center()]) + LEVEL1,
        'gcc')
    canvas.new_arrow(src = a_c, dst = gcc_to_a_o)
    canvas.new_arrow(src = b_h, dst = gcc_to_a_o)
    gcc_to_b_o = draw_processor(
        canvas,
        centroid([b_h.center(), b_c.center()]) + LEVEL1,
        'gcc')
    canvas.new_arrow(src = b_h, dst = gcc_to_b_o)
    canvas.new_arrow(src = b_c, dst = gcc_to_b_o)

    a_o = draw_resource(
        canvas,
        gcc_to_a_o.center() + LEVEL1,
        'a.o')
    canvas.new_arrow(src = gcc_to_a_o, dst = a_o)
    b_o = draw_resource(
        canvas,
        gcc_to_b_o.center() + LEVEL1,
        'b.o')
    canvas.new_arrow(src = gcc_to_b_o, dst = b_o)

    gcc_to_c_o = draw_processor(
        canvas,
        c_c.center() - sep,
        'gcc')
    canvas.new_arrow(src = c_c, dst = gcc_to_c_o)

    c_o = draw_resource(
        canvas,
        b_o.center() + sep,
        'c.o')
    canvas.new_arrow(src = gcc_to_c_o, dst = c_o)

    ar = draw_processor(
        canvas,
        b_o.center() + LEVEL1,
        'ar')
    canvas.new_arrow(src = b_o, dst = ar)
    canvas.new_arrow(src = c_o, dst = ar)
    ld_so = draw_processor(
        canvas,
        c_o.center() + LEVEL1,
        'ld')
    canvas.new_arrow(src = b_o, dst = ld_so)
    canvas.new_arrow(src = c_o, dst = ld_so)

    libbc_a = draw_resource(
        canvas,
        ar.center() - sep - sep,
        '\\small libbc.a')
    canvas.new_arrow(src = ar, dst = libbc_a)
    libbc_so = draw_resource(
        canvas,
        ld_so.center() + LEVEL1,
        '\\small libbc.so')
    canvas.new_arrow(src = ld_so, dst = libbc_so)

    level_y = (libbc_a.center() + LEVEL1).y
    ld_to_exe1 = draw_processor(
        canvas,
        Point(a_o.center().x, level_y),
        'ld')
    canvas.new_arrow(src = a_o, dst = ld_to_exe1)
    canvas.new_arrow(src = libbc_a, dst = ld_to_exe1)
    ld_to_exe2 = draw_processor(
        canvas,
        Point(ar.center().x, level_y),
        'ld')
    canvas.new_arrow(src = a_o, dst = ld_to_exe2)
    canvas.new_arrow(src = libbc_so, dst = ld_to_exe2)

    exe1 = draw_resource(
        canvas,
        ld_to_exe1.center() + LEVEL1,
        'exe1')
    canvas.new_arrow(src = ld_to_exe1, dst = exe1)
    exe2 = draw_resource(
        canvas,
        ld_to_exe2.center() + LEVEL1,
        'exe2')
    canvas.new_arrow(src = ld_to_exe2, dst = exe2)

    print(canvas.draw())
