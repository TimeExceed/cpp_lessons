from clh import *

if __name__ == '__main__':
    canvas = tikz.Canvas()

    mtx, default_atomics = draw_thread(canvas, 0, 'mtx', 'false', colors.GREEN)
    canvas.new_arrow(
        src = mtx,
        dst = default_atomics,
        pen_color = colors.GREEN,
    )

    print(canvas.draw())
