#!usr/bin/python3
import curses, time, os
import getpass, sys, signal
import shutil
from distutils.dir_util import copy_tree

# from datetime import datetime
from depend import *
from create import *


os.stat(".")

# print(time.ctime((os.stat(".").st_ctime)))


def show_stat(stdscr, file, dira):
    h, w = stdscr.getmaxyx()
    wn = 37
    if file == "Empty Folder":
        for i in range(2, 10):
            stdscr.addstr(i, w - wn, " " * wn, curses.color_pair(11))
        stdscr.addstr(1, w - wn + wn // 2 - 1, "Stats", curses.color_pair(11))
        stdscr.addstr(2, w - wn + wn // 2 - 7, "Nothing to show", curses.color_pair(11))
        return
    stdscr.addstr(h - 3, w - wn, " " * wn, curses.color_pair(11))
    try:
        st = os.stat(file)
    except:
        for i in range(2, 10):
            stdscr.addstr(i, w - wn, " " * wn, curses.color_pair(11))
        stdscr.addstr(1, w - wn + wn // 2 - 1, "Stats", curses.color_pair(11))
        stdscr.addstr(
            2, w - wn + wn // 2 - 7, "Permission Denied", curses.color_pair(11)
        )
        return
    if dira:
        dira = "Folder"
    else:
        dira = "File"
    kb = 2 ** 10

    stdscr.addstr(1, w - wn + wn // 2 - 1, "Stats", curses.color_pair(11))
    stdscr.addstr(
        2,
        w - wn + 1,
        "Created  : " + str(time.ctime(st.st_ctime)),
        curses.color_pair(11),
    )
    stdscr.addstr(
        3,
        w - wn + 1,
        "Modified : " + str(time.ctime(st.st_atime)),
        curses.color_pair(11),
    )
    stdscr.addstr(
        4,
        w - wn + 1,
        "Accessed : " + str(time.ctime(st.st_mtime)),
        curses.color_pair(11),
    )
    stdscr.addstr(5, w - wn, " " * wn, curses.color_pair(11))
    stdscr.addstr(
        5,
        w - wn + 1,
        "Size (KB): " + str(round(st.st_size / kb, 3)),
        curses.color_pair(11),
    )
    stdscr.addstr(6, w - wn, " " * wn, curses.color_pair(11))
    stdscr.addstr(6, w - wn + 1, "Type     : " + dira, curses.color_pair(11))
    stdscr.addstr(7, w - wn + 1, "User ID  : " + str(st.st_uid), curses.color_pair(11))
    stdscr.addstr(8, w - wn + 1, "Group ID : " + str(st.st_gid), curses.color_pair(11))
    stdscr.addstr(9, w - wn + 1, "Inode    : " + str(st.st_ino), curses.color_pair(11))


"""
atime ctime mtime size mode type 
"""
