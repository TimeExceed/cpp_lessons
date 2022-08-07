from fathom import Point, ORIGIN, centroid
import fathom.geometry as geo
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners

def draw_store_buffer(canvas, center):
    sb = canvas.new_rectangle(
        center = center,
        width = 0.6,
        height = 0.6,
        pen_color = colors.BLUE,
    ).get_skeleton()
    for i in range(1, 3):
        l = sb.vertices()[3] + Point(0, sb.height() * i / 3)
        r = sb.vertices()[2] + Point(0, sb.height() * i / 3)
        canvas.new_line(
            src = l,
            dst = r,
            pen_color = colors.BLUE,
        )
    return sb

def draw_invalidate_queue(canvas, lower_left):
    iq = canvas.new_rectangle(
        lower_left = lower_left,
        upper_right = lower_left + Point(0.6, 0.6),
        pen_color = colors.RED,
    ).get_skeleton()
    iq0 = canvas.new_rectangle(
        lower_left = lower_left,
        upper_right = lower_left + Point(iq.width() / 3, iq.height()),
        pen_color = colors.INVISIBLE,
    ).get_skeleton()
    for i in range(1, 3):
        canvas.new_line(
            src = iq.vertices()[0] + Point(iq0.width() * i, 0),
            dst = iq.vertices()[3] + Point(iq0.width() * i, 0),
            pen_color = colors.RED,
        )

    return iq, iq0

def draw_cpu(canvas, ll, ur):
    frame = canvas.new_rectangle(
        lower_left = ll,
        upper_right = ur,
        corner_style = corners.DEFAULT_ROUNDED,
    ).get_skeleton()
    canvas.new_text(
        text = 'CPU core',
        anchor = centroid([frame.vertices()[0], frame.vertices()[1]]),
        location = locations.SOUTH,
    )

    alu = canvas.new_rectangle(
        center = centroid([frame.vertices()[0], frame.vertices()[1]]) + Point(0, -1),
        width = 2,
        height = 0.6,
    ).get_skeleton()
    canvas.new_text(
        text = 'ALU',
        anchor = alu.center(),
    )

    l1 = canvas.new_rectangle(
        center = centroid([frame.vertices()[0], frame.vertices()[1]]) + Point(0, -2),
        width = frame.width() * 4 / 5,
        height = 0.6,
    ).get_skeleton()
    canvas.new_text(
        text = 'L1 cache',
        anchor = l1.center(),
    )
    canvas.new_arrow(
        src = l1,
        dst = alu,
        pen_color = colors.ORANGE,
    )

    w_inv_ll = l1.vertices()[3] + Point(0.9, 0)
    w_inv_ur = l1.vertices()[0] + Point(1.1, 0)
    w_inv = canvas.new_rectangle(
        lower_left = w_inv_ll,
        upper_right = w_inv_ur,
        pen_color = colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_arrow(
        src = alu,
        dst = centroid([w_inv.vertices()[0], w_inv.vertices()[1]]),
        pen_color = colors.BLUE,
    )

    sb = draw_store_buffer(canvas, w_inv.center() + Point(0, -1.3))
    canvas.new_arrow(
        src = w_inv,
        dst = sb,
        pen_color = colors.BLUE,
    )

    iq_inv_ll = l1.vertices()[2] + Point(-1.1, 0)
    iq_inv_ur = l1.vertices()[1] + Point(-0.9, 0)
    iq_inv = canvas.new_rectangle(
        lower_left = iq_inv_ll,
        upper_right = iq_inv_ur,
        pen_color = colors.INVISIBLE,
    ).get_skeleton()
    iq, iq0 = draw_invalidate_queue(canvas, iq_inv.center() + Point(-0.1, -1.6))
    canvas.new_arrow(
        src = iq0,
        dst = iq_inv,
        pen_color = colors.RED,
    )

    return l1, sb, iq

if __name__ == '__main__':
    canvas = tikz.Canvas()

    bus = canvas.new_rectangle(
        lower_left = ORIGIN,
        upper_right = Point(15, 0.5),
    ).get_skeleton()
    canvas.new_text(
        text = '内存总线',
        anchor = bus.center(),
    )

    mem = canvas.new_rectangle(
        center = bus.center() + Point(0, -2),
        width = 2.4,
        height = 1.6,
    ).get_skeleton()
    canvas.new_text(
        text = '主存',
        anchor = mem.center(),
    )

    canvas.new_dblarrow(
        src = bus,
        dst = mem,
    )

    cpu1_l1, cpu1_sb, cpu1_iq = draw_cpu(canvas, Point(1, 1), Point(6, 5))
    cpu2_l1, cpu2_sb, cpu2_iq = draw_cpu(canvas, Point(9, 1), Point(14, 5))

    for sb in [cpu1_sb, cpu2_sb]:
        bus_upper = Point(sb.center().x, bus.vertices()[0].y)
        canvas.new_arrow(
            src = sb,
            dst = bus_upper,
            pen_color = colors.BLUE,
        )
    for l1 in [cpu1_l1, cpu2_l1]:
        bus_upper = Point(l1.center().x, bus.vertices()[0].y)
        canvas.new_arrow(
            src = bus_upper,
            dst = l1,
            pen_color = colors.ORANGE,
        )
    mesi = canvas.new_arrow(
        src = cpu2_sb,
        dst = cpu1_iq,
        pen_color = colors.RED,
    ).get_skeleton()
    canvas.new_text(
        text = 'MESI',
        anchor = mesi.center(),
        location = locations.NORTH,
    )

    illustrate_left = Point(11, -0.7)
    illustrate_right = Point(12, -0.7)
    illustrate_sep = Point(0, -0.5)
    illustrates = [
        (colors.BLUE, 'write'),
        (colors.ORANGE, 'read'),
        (colors.RED, 'invalidate'),
    ]
    for i, (c, t) in enumerate(illustrates):
        src = illustrate_left
        for _ in range(i):
            src = src + illustrate_sep
        dst = illustrate_right
        for _ in range(i):
            dst = dst + illustrate_sep
        a = canvas.new_arrow(
            src = src,
            dst = dst,
            pen_color = c,
        ).get_skeleton()
        canvas.new_text(
            text = t,
            anchor = a.vertices()[1],
            location = locations.EAST,
        )

    illustrate_sb = draw_store_buffer(canvas, Point(1, -0.7))
    canvas.new_text(
        text = 'store buffer',
        anchor = centroid([illustrate_sb.vertices()[1], illustrate_sb.vertices()[2]]),
        location = locations.EAST,
    )
    iq, _ = draw_invalidate_queue(canvas, illustrate_sb.vertices()[3] + Point(0, -1))
    canvas.new_text(
        text = 'invalidate queue',
        anchor = centroid([iq.vertices()[1], iq.vertices()[2]]),
        location = locations.EAST,
    )


    print(canvas.draw())
