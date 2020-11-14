import curses
def main(stdscr):
    i = 0
    curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLACK)
    while 1:
        key = stdscr.getch()
        if key==curses.KEY_RIGHT:
            i+=1
        elif key==curses.KEY_LEFT:
            i-=1
        stdscr.addstr(0,0,str(i),curses.color_pair(2))
        curses.init_pair(1,1,i)
        stdscr.bkgd(' ', curses.color_pair(1)|curses.A_BOLD)
curses.wrapper(main)