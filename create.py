#!/usr/bin/python3.8
import curses,time,os
import getpass,sys,signal
import shutil 
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *

# Define some strings
name = "File Name : "
fname = "Folder Name : "

"""
    Function : Get From
    Input : stdscr, menu, listings, q
    stdscr : standard screen
    menu : files in current path
    q : if q is False then this function makes file and q is True then Folder
"""
def getform(stdscr,menu,listings,q):
    h,w = stdscr.getmaxyx()
    
    # create a form for user
    curses.init_pair(10,curses.COLOR_WHITE,18)
    stdscr.attron(curses.color_pair(10))
    stdscr.addstr(h-3,w//5+1," "*(4*w//5),curses.color_pair(10))
    if not q:
        stdscr.addstr(h-3,w//5+1,name,curses.color_pair(10))
    else:
        stdscr.addstr(h-3,w//5+1,fname,curses.color_pair(10))

    key = stdscr.getch()
    k = 0
    # get user input
    onboard = ""

    # until enter is pressed, take input
    while key!=curses.KEY_ENTER and key!=10 and key!=13:
        if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
            if k<0:
                continue
            k-=1
            onboard = onboard[:-1]
            stdscr.addstr("\b \b")
        elif key!=263 and key!=258 and key!=259 and key!=261:
            k+=1
            onboard+=chr(key)
            if not q:
                stdscr.move(h-3,w//5+1+len(name)+len(onboard)-1)
            else:
                stdscr.move(h-3,w//5+1+len(fname)+len(onboard)-1)
            stdscr.addch(key)
        key = stdscr.getch()

    # if file, then create file
    if onboard!="" and not q:
        file = open(onboard,"w")
        file.close()
    elif onboard!="" and q:  # else folder
        os.mkdir(onboard)
    
    # update current directory
    menu = os.listdir()
    menu.sort()
    stdscr.addstr(h-3,w//5+1," "*(4*w//5),curses.color_pair(3))
    print_menu(stdscr,listings,0,"",menu)
    stdscr.refresh()
    listings = []
    for i in menu:
        listings.append(os.path.isdir(i))
    return menu,listings,1

# def create(name):
