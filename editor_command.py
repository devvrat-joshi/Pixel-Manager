#!/usr/bin/python3.8
import curses,time,os
import getpass,sys,signal
import shutil,re
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *
from create import *
from stats import *
from terminal_lib import *
from search import *
import editor
from deditor import start_editor
python_key = "import |from |for |while | or | and |def | in |range|if |else |elif"
def command_mode(stdscr,h,w,curpoint_row,curpoint_col,cursor_row,cursor_col,lene,row_current,col_current,x):
    # stdscr.addstr()
    curses.init_pair(55,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.init_pair(43,curses.COLOR_WHITE,curses.COLOR_BLACK)
    while 1:
        key = stdscr.getch()
        if key==ord("q"):
            return "quit"
        if key==ord("i"):
            return "insert"
        if key==ord("c"):
            while 1:
                key = stdscr.getch()
                if key==curses.KEY_RIGHT:
                    if cursor_col<w-(3+w//5+lene):
                        stdscr.addstr(cursor_row+1,3+w//5+lene+cursor_col,x[row_current][lene+2+cursor_col],curses.color_pair(55))
                        col_current +=1
                        if cursor_col<len(x[row_current])-lene-3:
                            cursor_col+=1
                        stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)
                if key==curses.KEY_LEFT:
                    if cursor_col>1:
                        cursor_col-=1
                        col_current-=1
                        stdscr.addstr(cursor_row+1,3+w//5+lene+cursor_col,x[row_current][lene+2+cursor_col],curses.color_pair(55))
                        stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)
                if key==curses.KEY_UP:
                    if cursor_col<1:
                        cursor_row-=1
                        row_current-=1
                        stdscr.addstr(cursor_row+1,3+w//5+lene+cursor_col,x[row_current][lene+2+cursor_col],curses.color_pair(55))
                        stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)
                if key==curses.KEY_DOWN:
                    if cursor_col<h-3:
                        cursor_row+=1
                        row_current+=1
                        stdscr.addstr(cursor_row,3+w//5+lene+cursor_col,x[row_current-1][lene+2+cursor_col:],curses.color_pair(55))     
                        stdscr.addstr(cursor_row+1,3+w//5+lene,x[row_current][lene+2:lene+2+cursor_col],curses.color_pair(55))
                        stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)
        