from fathom import Point, ORIGIN, centroid
import fathom.geometry as geo
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners

H_SEP = 4
THREAD_Y = 4
WIDTH = 1.6
HEIGHT = 0.9

def draw_thread(canvas, x, thread_txt, atomic_txt, color):
    atomic = canvas.new_rectangle(
        center = Point(x, 0),
        width = WIDTH,
        height = HEIGHT,
        brush_color = color,
    ).get_skeleton()
    canvas.new_text(
        text = atomic_txt,
        anchor = atomic.center(),
    )

    thread = canvas.new_rectangle(
        center = Point(x, THREAD_Y),
        width = WIDTH,
        height = HEIGHT,
        brush_color = color,
    ).get_skeleton()
    canvas.new_text(
        text = thread_txt,
        anchor = thread.center(),
    )

    return thread, atomic
