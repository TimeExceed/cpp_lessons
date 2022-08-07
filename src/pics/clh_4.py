from clh import *

if __name__ == '__main__':
    canvas = tikz.Canvas()

    mtx, default_atomics = draw_thread(canvas, 0, 'mtx', 'false', colors.GREEN)
    thread1, atomic1 = draw_thread(canvas, H_SEP, '线程1', 'true', colors.CYAN)
    thread2, atomic2 = draw_thread(canvas, H_SEP * 2, '线程2', 'true', colors.ORANGE)
    canvas.new_arrow(
        src = mtx,
        dst = atomic2,
        pen_color = colors.GREEN,
    )
    canvas.new_arrow(
        src = thread1,
        dst = default_atomics,
        pen_color = colors.CYAN,
    )
    canvas.new_arrow(
        src = thread2,
        dst = atomic1,
        pen_color = colors.ORANGE,
    )

    print(canvas.draw())
