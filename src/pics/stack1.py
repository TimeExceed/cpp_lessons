from fathom import Point, ORIGIN, centroid
import fathom.geometry as geo
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners

if __name__ == '__main__':
    canvas = tikz.Canvas()

    GRID_SIZE = Point(1, 0.8)
    F_OFFSET = Point(-0.6, 0)
    V_OFFSET = Point(0.6, 0)

    a = canvas.new_rectangle(
        lower_left = ORIGIN,
        upper_right = GRID_SIZE,
    ).get_skeleton()
    ret_g = canvas.new_rectangle(
        lower_left = a.vertices()[0],
        upper_right = a.vertices()[0] + GRID_SIZE,
    ).get_skeleton()
    x = canvas.new_rectangle(
        lower_left = ret_g.vertices()[0],
        upper_right = ret_g.vertices()[0] + GRID_SIZE,
    ).get_skeleton()

    canvas.new_arrow(
        src = F_OFFSET,
        dst = a.vertices()[3],
        line_style = line_styles.DASHED,
    )
    canvas.new_text(
        text = 'f',
        anchor = F_OFFSET,
        location = locations.WEST,
    )
    p = ret_g.vertices()[0] + F_OFFSET
    canvas.new_arrow(
        src = p,
        dst = ret_g.vertices()[0],
        line_style = line_styles.DASHED,
    )
    canvas.new_text(
        text = 'g',
        anchor = p,
        location = locations.WEST,
    )

    p = centroid([a.vertices()[1], a.vertices()[2]]) + V_OFFSET
    canvas.new_arrow(src = p, dst = a)
    canvas.new_text(
        text = 'a',
        anchor = p,
        location = locations.EAST,
    )
    p = centroid([ret_g.vertices()[1], ret_g.vertices()[2]]) + V_OFFSET + Point(0, -0.3)
    canvas.new_arrow(src = p, dst = ret_g)
    canvas.new_text(
        text = 'return of g',
        anchor = p,
        location = locations.EAST,
    )
    p = centroid([x.vertices()[1], x.vertices()[2]]) + V_OFFSET
    canvas.new_arrow(src = p, dst = x)
    canvas.new_text(
        text = 'x',
        anchor = p,
        location = locations.EAST,
    )
    p = centroid([ret_g.vertices()[1], ret_g.vertices()[2]]) + V_OFFSET + Point(0, 0.3)
    canvas.new_arrow(src = p, dst = ret_g)
    canvas.new_text(
        text = 'y',
        anchor = p,
        location = locations.EAST,
    )

    print(canvas.draw())
