import curses,time,os
import getpass,sys,signal
import shutil
from distutils.dir_util import copy_tree
from datetime import datetime

def main(stdscr):
    curses.curs_set(0)
    h,w = stdscr.getmaxyx()
    row = 0
    curses.init_pair(1, curses.COLOR_WHITE, 34)
    stdscr.addstr(row,1,">>>",curses.color_pair(1))
    curses.cbreak()
    while True:
        input_cmd = ""
        cursor_pos = 5
        while cursor_pos <w:
            key_pressed = stdscr.getch()
            if key_pressed == 10:
                stdscr.move(row+1,1)
                output = os.system(input_cmd)
                # stdscr.addstr(row+1,1,(output),curses.color_pair(1))
                row+=1
                cursor_pos = 5
                break
            input_cmd = input_cmd + chr(key_pressed)
            # print(input_cmd)
            stdscr.addstr(row,cursor_pos,chr(key_pressed),curses.color_pair(1))
            cursor_pos+=1
        

        # if key_pressed == ord('a'):
            # stdscr.attron(curses.color_pair(1))
        
        # stdscr.refresh()
        # time.sleep(2)
            # break
        if key_pressed == 27:
            break



curses.wrapper(main)

