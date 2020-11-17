#!/usr/bin/python3.8
import curses,time,os
import getpass,sys,signal
import preprocess_trie_hash
import shutil
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *
from create import *
from stats import *
from terminal_lib import *
import multiprocessing
se = "Search : "
seme = "Search Something To See Results Here"
def multi(m,kk):
    trie = preprocess_trie_hash.Trie()
    trie.preprocess(os.getcwd())
    m[0] = trie
    kk[0] = 1

def search_init(stdscr,h,w,path):
    mn = multiprocessing.Manager()
    m = mn.dict()
    kk = mn.dict()
    kk[0] = 0
    p1 = multiprocessing.Process(target=multi,args=(m,kk))
    p1.start()
    preprocess_trie_hash.prog(stdscr,h,w,kk)
    trie = m.values()[0]
    curses.init_pair(18,curses.COLOR_WHITE,18)
    curses.init_pair(19,curses.COLOR_WHITE,63)
    empty_right(stdscr)
    stdscr.addstr(0,0," "*w,curses.color_pair(18))
    stdscr.addstr(0,w//5+1,se+" "*(w-w//5-38-len(se)),curses.color_pair(19))
    k = 0
    curses.cbreak()
    curses.curs_set(1)
    # stdscr.addstr(h-2,len(pp)," ",curses.color_pair(6))
    stdscr.attron(curses.color_pair(19))
    
    onboard = ""
    while 1:
        key = stdscr.getch()
        i = 0
        if key==1:
            curses.curs_set(0)
            stdscr.addstr(0,0," "*w,curses.color_pair(5))
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
            return
        if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
            if k<0:
                continue
            k-=1
            onboard = onboard[:-1]
            stdscr.addstr("\b \b")
        elif key!=263 and key!=258 and key!=259 and key!=261:
            k+=1
            onboard+=chr(key)
            stdscr.attron(curses.color_pair(19))
            stdscr.move(0,w//5+len(se)+len(onboard))
            stdscr.addch(key)
            stdscr.attroff(curses.color_pair(19))
        empty_right(stdscr)
        ifit = 0
        if onboard:
            for files in trie.prefix_search(onboard):
                
                i+=1
                if i<=h-3:
                    stdscr.addstr(i,w//5+2,files[:w-w//5-38])
                ifit += 1
        if not ifit:
            if not onboard:
                stdscr.addstr(1,(w//5+w-36)//2-len(seme)//2,"Search Something To See Results Here")
            else:
                stdscr.addstr(1,w//5+2,"Not Found: "+onboard)
        stdscr.addstr(0,w-36,"Search Results :       ",curses.color_pair(18))        
        stdscr.addstr(0,w-36,"Search Results : "+str(ifit),curses.color_pair(18))
        stdscr.move(0,w//5+len(se)+len(onboard)+1)
        stdscr.attron(curses.color_pair(19))
