import curses

def main(stdscr):
    file = open("key.txt","w")
    key = stdscr.getch()
    file.write(str(key))
    file.close()

curses.wrapper(main)