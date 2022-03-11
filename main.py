import cv2 as cv
import curses

win = None
min_color, max_color = 0, 255
h, w = 0, 0
color_dict = dict()

colors = dict()

def draw(frame):
    win.erase()
    for i in range(h):
        for j in range(w):
            b, g, r = frame[i, j]
            color = colors[(r, g, b)]
            win.attron(curses.color_pair(color))
            win.addstr(i+1, j+1, ' ')
            win.attroff(curses.color_pair(color))
    win.refresh()

def init_colors():
    ci = 0
    step = 43
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                curses.init_color(ci, r*4, g*4, b*4)
                ci += 1
                for ar in range(step):
                    for ag in range(step):
                        for ab in range(step):
                            colors[(r + ar, g + ag, b + ab)] = ci
    curses.flash()


def main(stdscr):
    global win, h, w
    win = stdscr
    init_colors()
    win.nodelay(1)
    win.timeout(20)
    h, w = win.getmaxyx()
    h -= 2
    w -= 2
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    for i in range(min_color, max_color+1):
        curses.init_pair(i, -1, i)
    
    capture = cv.VideoCapture(0)
    while True:
        istrue, frame = capture.read()
        frame = cv.resize(frame, (w, h))
        draw(frame)
        cv.waitKey(20)
        key = win.getch()
        if key == 113:
            break

curses.wrapper(main)