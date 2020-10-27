import curses,time,os
import getpass,sys,signal
import shutil
from distutils.dir_util import copy_tree
from datetime import datetime

os.chdir(".")
menu = os.listdir()

file = "It is a File"
copy = "Press c to copy the file: "
search = "Ctrl + S to search: "

def empty_right(stdscr):
    p,w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(3))
    for i in range(1,p-2):
        stdscr.addstr(i,w//5," "*(4*w//5-2))

def print_folder(stdscr,row):
    try:
        h = list(os.listdir(row))
        p,w = stdscr.getmaxyx()
        per10screen = w//5
        empty_right(stdscr)
        for i in range(p-3):
            stdscr.attron(curses.color_pair(3))
            if len(h[i])<per10screen:
                l = h[i]+" "*(per10screen-len(row))
            else:
                l = h[i][:per10screen]
            x = w//5+1
            y = i+1
            stdscr.addstr(y,x,l)
    except:
        pass


def print_menu(stdscr,listings,n,this,menu):
    # stdscr.clear()
    h,w = stdscr.getmaxyx()
    per10screen = w//5
    per = " "*(w//5)
    for i in range(1,h-2):
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(i,0,per)
    stdscr.attroff(curses.color_pair(2))
    curses.init_pair(4, curses.COLOR_WHITE, 2)
    curses.init_pair(5, 3,17)
    stdscr.attron(curses.color_pair(5))
    stdscr.addstr(0,0," "*w)
    if listings[0]:
        print_folder(stdscr,menu[0])
    else:
        empty_right(stdscr)
        stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(h-2,0," "*(w-1))
    stdscr.addstr(h-2,w//2-len(menu[0])//2,menu[0])
    for idx, row in enumerate(menu):
        if (idx==0 and n==0) or this==row:
            stdscr.attron(curses.color_pair(1))
            if len(row)<per10screen:
                i = row+" "*(per10screen-len(row))
            else:
                i = row[:per10screen]
            x = 0
            y = idx+1
            stdscr.addstr(y,x,i)
            stdscr.attroff(curses.color_pair(1))
        else:
            if idx>=h-3:
                break
            stdscr.attron(curses.color_pair(2))
            if len(row)<per10screen:
                i = row+" "*(per10screen-len(row))
            else:
                i = row[:per10screen]
            x = 0
            y = idx+1
            stdscr.addstr(y,x,i)
    stdscr.refresh()

def scrolldown(stdscr,cur_row,menu):
    # global menu
    h,w = stdscr.getmaxyx()
    per10screen = w//5
    maxi = 0
    per = " "*(w//5)
    stdscr.attron(curses.color_pair(2))
    for idx in range(cur_row-h+3,cur_row):
        if len(menu[idx])<per10screen:
            i = menu[idx]+" "*(per10screen-len(menu[idx]))
        else:
            i = menu[idx][:per10screen]
        if idx==cur_row-1:
            stdscr.attron(curses.color_pair(1))
            if len(menu[idx])<per10screen:
                i = menu[idx]+" "*(per10screen-len(menu[idx]))
            else:
                i = menu[idx][:per10screen]
            x = 0
            y = idx+1-cur_row+h-3
            stdscr.addstr(y,x,i)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(h-2,0," "*(w-1))
            stdscr.addstr(h-2,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
        else:
            x = 0
            y = idx+1-cur_row+h-3
            stdscr.addstr(y,x,i)
    stdscr.refresh()