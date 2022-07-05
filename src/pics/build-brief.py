from fathom import Point, ORIGIN, centroid
import fathom.geometry as geo
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners

def compile(src_text, dst_txt, compiler_text, y):
    c = canvas.new_rectangle(
        center = Point(0, y),
        width = 1,
        height = 0.8,
    ).get_skeleton()
    canvas.new_text(
        text = src_text,
        anchor = c.center(),
    )

    mid = canvas.new_circle(
        center = Point(2, y),
        radius = 0.5,
        pen_color = colors.BLUE,
    ).get_skeleton()
    canvas.new_text(
        text = compiler_text,
        anchor = mid.center(),
    )

    o = canvas.new_rectangle(
        center = Point(4, y),
        width = 1,
        height = 0.8,
    ).get_skeleton()
    canvas.new_text(
        text = dst_txt,
        anchor = o.center(),
    )

    canvas.new_arrow(
        src = c,
        dst = mid,
    ).get_skeleton()
    canvas.new_arrow(
        src = mid,
        dst = o,
    ).get_skeleton()

    return c, o

if __name__ == '__main__':
    canvas = tikz.Canvas()

    a_c, a_o = compile('a.c', 'a.o', 'gcc', 0)
    b_cpp, b_o = compile('b.cpp', 'b.o', 'g++', 2)

    backend_y = centroid([a_o.center(), b_o.center()]).y
    ld = canvas.new_circle(
        center = Point(6, backend_y),
        radius = 0.5,
        pen_color = colors.BLUE,
    ).get_skeleton()
    canvas.new_text(
        text = 'ld',
        anchor = ld.center(),
    )
    canvas.new_arrow(
        src = a_o,
        dst = ld,
    )
    canvas.new_arrow(
        src = b_o,
        dst = ld,
    )

    exe = canvas.new_rectangle(
        center = Point(8, backend_y),
        width = 1,
        height = 0.8,
    ).get_skeleton()
    canvas.new_text(
        text = 'exe',
        anchor = exe.center(),
    )
    canvas.new_arrow(
        src = ld,
        dst = exe,
    )

    compilation = canvas.new_rectangle(
        lower_left = a_c.vertices()[3] + Point(-0.5, -0.5),
        upper_right = b_o.vertices()[1] + Point(0.3, 0.5),
        line_style = line_styles.DASHED,
        pen_color = colors.BLUE,
    ).get_skeleton()
    canvas.new_text(
        text = 'Compilation',
        anchor = centroid(compilation.vertices()[:2]),
        location = locations.NORTH,
    )

    link = canvas.new_rectangle(
        lower_left = a_o.vertices()[3] + Point(-0.3, -0.6),
        upper_right = Point(exe.vertices()[1].x, b_o.vertices()[1].y) + Point(0.5, 0.6),
        line_style = line_styles.DASHED,
        pen_color = colors.MAGENTA,
    ).get_skeleton()
    canvas.new_text(
        text = 'Linking',
        anchor = centroid(link.vertices()[:2]),
        location = locations.NORTH,
    )

    print(canvas.draw())
