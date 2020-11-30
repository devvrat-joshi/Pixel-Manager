#!/usr/bin/python3.8
import curses,time,os                    # Import some main dependencies
import getpass,sys,signal                # Used for getting user information and for passing system arguments
import shutil                            # Tree level copy, move, delete
from distutils.dir_util import copy_tree 
import preprocess_trie_hash              # Trie
from datetime import datetime            # Datetime
from depend import *                     # Custom created functions and dependencies
from create import *                     # Custom create file, self.folder 
from stats import *                      # Custom stats of files
from terminal_lib import Terminal        # Custom self.terminal
import pickle                            # For fast trie
import multiprocessing                   # Multiprocess Trie
import logging as log

# Some global variables
tries = {}
se = "Search : "
seme = "Search Something To See Results Here"

# Multiprocess Trie
def multi(m,kk):
    trie = preprocess_trie_hash.Trie()
    trie.preprocess(os.getcwd())
    m[0] = trie
    kk[0] = 1

# Multiprocess Update Trie
def multi_update(m,kk):
    trie = m.values()[0]
    trie.preprocess(os.getcwd())
    m[0] = trie
    kk[0] = 1

# Search Class
class Search:
    """
        init function :: stdscr : standard screen, h,w: screen size, path: current path, cur_row : current row in main menu, overall_path : pickle storage point
    """
    def __init__(self,stdscr,h,w,path,cur_row,overall_path):

        # make attributes for search instance so that passing variables between functions becomes simple
        self.stdscr = stdscr
        self.h = h
        self.w = w
        self.path = path
        self.cur_row = cur_row
        self.overall_path = overall_path
        self.path_right_now = os.getcwd().replace("/","-")+".pkl"
        self.curr_path = self.overall_path+"/"+self.path_right_now

        # If we have trie stored
        if self.path_right_now not in os.listdir(path=self.overall_path+"/"):
            mn = multiprocessing.Manager()
            m = mn.dict()
            kk = mn.dict()
            kk[0] = 0
            p1 = multiprocessing.Process(target=multi,args=(m,kk))
            p1.start()
            preprocess_trie_hash.prog(self.stdscr,h,w,kk)
            outfile = open(self.curr_path,'wb')
            pickle.dump(m.values()[0],outfile)
            outfile.close()
            self.trie = m.values()[0]
        else: # else load from pickle
            self.stdscr.addstr(0,2,"Please Wait...",curses.color_pair(5))
            self.stdscr.refresh()
            infile = open(self.curr_path,'rb')
            self.trie = pickle.load(infile)
            self.stdscr.addstr(0,2," "*14,curses.color_pair(5))
            self.stdscr.refresh()

        # get some colors for search
        curses.init_pair(18,curses.COLOR_WHITE,18)
        curses.init_pair(19,curses.COLOR_WHITE,63)
        curses.init_pair(100,curses.COLOR_WHITE,35)
        empty_right(self.stdscr) # empty the middle panel

        # make room for search
        self.stdscr.addstr(0,0," "*self.w,curses.color_pair(18))
        self.stdscr.addstr(0,self.w//5+1,se+" "*(w-w//5-38-len(se)),curses.color_pair(19))
        self.stdscr.addstr(1,(self.w//5+self.w-36)//2-len(seme)//2,"Search Something To See Results Here")
        self.stdscr.move(0,self.w//5+10)
        self.k = 0
        curses.cbreak()
        curses.curs_set(1)
        self.stdscr.attron(curses.color_pair(19))

        # global results
        self._results_ = []
        self.result_row = 0
        self.onboard = ""
        curses.cbreak()
        
    def start(self):
        """
            start search by taking input from user
        """
        while 1:
            key = self.stdscr.getch()

            # nothing to do with left key
            if key==curses.KEY_LEFT:
                continue
            
            # Down key
            if key==curses.KEY_DOWN:
                self.key_down()
                continue

            # if not up and enter key, then user is continuing the search input
            elif key!=curses.KEY_UP and key!=curses.KEY_ENTER and key!=13 and key!=10:
                self.result_row = 0

            # Up key for results
            if key==curses.KEY_UP:
                self.key_up()
                continue

            # enter key
            if (key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT) and self.result_row!=0:
                return_point = self.key_powerful_enter()
                if return_point!=None:
                    return return_point
                continue

            
            # below code does printing the search results on screen with printing the user typed keys
            curses.curs_set(1)
            self.stdscr.move(0,self.w//5+len(se)+len(self.onboard)+1)
            i = 0
            if key==1:
                curses.curs_set(0)
                self.stdscr.addstr(0,0," "*self.w,curses.color_pair(5))
                self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5))
                return False, "", "", "", ""

            if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and self.k>=0:
                if self.k<0:
                    continue
                self.k-=1
                self.onboard = self.onboard[:-1]
                self.stdscr.addstr("\b \b")

            elif key!=263 and key!=258 and key!=259 and key!=261:
                if self.w//5+10+self.k>self.w-42:
                    continue
                self.k+=1
                self.onboard+=chr(key)
                self.stdscr.attron(curses.color_pair(19))
                self.stdscr.move(0,self.w//5+len(se)+len(self.onboard))
                self.stdscr.addch(key)
                self.stdscr.attroff(curses.color_pair(19))
            empty_right(self.stdscr)

            self.ifit = 0
            if self.onboard:
                self._results_ = self.trie.prefix_search(self.onboard)
                for files in self._results_:
                    ff = len(files[1])
                    i+=1
                    if i<=self.h-3:
                        self.stdscr.addstr(i,self.w//5+2,files[0][:self.w-self.w//5-44]+" ("+str(ff)+")")
                    self.ifit += ff

            if not self.ifit:
                if not self.onboard:
                    self.stdscr.addstr(1,(self.w//5+self.w-36)//2-len(seme)//2,"Search Something To See Results Here")
                else:
                    self.stdscr.addstr(1,self.w//5+2,"Not Found: "+self.onboard)
                    
            self.stdscr.addstr(0,self.w-36,"Search Results :       ",curses.color_pair(18))        
            self.stdscr.addstr(0,self.w-36,"Search Results : "+str(self.ifit),curses.color_pair(18))
            bar_single(self.stdscr,self.h,self.w)
            self.stdscr.move(0,self.w//5+len(se)+len(self.onboard)+1)
            self.stdscr.attron(curses.color_pair(19))

    # key down
    def key_down(self):
        curses.curs_set(0)
        if self.result_row>len(self._results_)-1:
            return
        i = 0
        # # log.info(str(len(self._results_))+" "+str(self.h))
        if self.result_row>=self.h-3 and self.result_row<len(self._results_):
            if self.onboard:
                self.result_row+=1
                for i in range(self.result_row-self.h+3,self.result_row):
                    self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                    self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(3))
                self.stdscr.addstr(self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(100))
                self.stdscr.addstr(self.h-3,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(100))
                # result_row+=1
                # # log.info(self.result_row)
                return
        elif self.result_row>len(self._results_):
            return
        if self.result_row<self.h-3:
            if self.result_row!=0:
                self.stdscr.addstr(self.result_row,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                self.stdscr.addstr(self.result_row,self.w//5+2,self._results_[self.result_row-1][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[self.result_row-1][1]))+")",curses.color_pair(3))
            self.stdscr.addstr(self.result_row+1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(100))
            self.stdscr.addstr(self.result_row+1,self.w//5+2,self._results_[self.result_row][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[self.result_row][1]))+")",curses.color_pair(100))
        self.result_row+=1

    # key up
    def key_up(self):
        curses.curs_set(0)
        if self.result_row<1:
            return
        if self.result_row>self.h-3:
            if self.onboard:
                self.result_row-=1
                for i in range(self.result_row-self.h+3,self.result_row):
                    self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                    self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(3))
                self.stdscr.addstr(self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(100))
                self.stdscr.addstr(self.h-3,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(100))
                # result_row+=1
            return
        if self.result_row>1:
            self.result_row-=1
        if self.result_row<len(self._results_):
            self.stdscr.addstr(self.result_row+1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
            self.stdscr.addstr(self.result_row+1,self.w//5+2,self._results_[self.result_row][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[self.result_row][1]))+")",curses.color_pair(3))
        self.stdscr.addstr(self.result_row,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(100))
        self.stdscr.addstr(self.result_row,self.w//5+2,self._results_[self.result_row-1][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[self.result_row-1][1]))+")",curses.color_pair(100))

    # enter to the selected search results, quite complex code
    def key_powerful_enter(self):
        if self.onboard:
            self.ptrr = self.result_row
            self.store_res = self._results_[:]
            self._results_ = list(self._results_[self.result_row-1][1])
            empty_right(self.stdscr)
            for i in range(0,min(self.h-3,len(self._results_))):
                self.stdscr.addstr(i+1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                self.stdscr.addstr(i+1,self.w//5+2,self._results_[i][:self.w-self.w//5-44],curses.color_pair(3))
            self.stdscr.addstr(1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
            self.stdscr.addstr(1,self.w//5+2,self._results_[0][:self.w-self.w//5-44],curses.color_pair(1))
            self.result_row = 1
            while 1:
                key = self.stdscr.getch()
                if key==27:
                    self._results_ = self.store_res
                    self.result_row = self.ptrr
                    empty_right(self.stdscr)
                    if self.result_row>=self.h-3:
                        for i in range(self.result_row-self.h+3,self.result_row):
                            self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                            self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(3))
                        self.stdscr.addstr(self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
                        self.stdscr.addstr(self.h-3,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(1))
                    else:
                        for i in range(0,min(self.h-3,len(self._results_))):
                            self.stdscr.addstr(i+1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                            self.stdscr.addstr(i+1,self.w//5+2,self._results_[i][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[i][1]))+")",curses.color_pair(3))
                        self.stdscr.addstr(self.result_row,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
                        self.stdscr.addstr(self.result_row,self.w//5+2,self._results_[self.result_row-1][0][:self.w-self.w//5-44]+" ("+str(len(self._results_[self.result_row-1][1]))+")",curses.color_pair(1))
                    break
                if (key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT) and self.result_row!=0:
                    # log.info(self._results_[self.result_row-1])
                    os.chdir(self._results_[self.result_row-1])
                    self.cur_row=1
                    self.menu = os.listdir()
                    self.menu.sort()
                    if len(self.menu)==0:
                        self.menu = ["Empty Folder"]
                    self.path = getpass.getuser()+":"+os.getcwd()+"$"
                    self.l = len(menu)
                    self.listings = []
                    for i in self.menu:
                        self.listings.append(os.path.isdir(i))
                    print_menu(self.stdscr,self.listings,0,"",self.menu)
                    return True,self.listings,self.cur_row,self.l,self.menu,self.path
                    
                if key==curses.KEY_DOWN:
                    curses.curs_set(0)
                    if self.result_row>len(self._results_)-1:
                        continue
                    i = 0
                    if self.result_row>=self.h-3 and self.result_row<len(self._results_):
                        if self.onboard:
                            self.result_row+=1
                            for i in range(self.result_row-self.h+3,self.result_row):
                                self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                                self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2,self._results_[i][:self.w-self.w//5-44],curses.color_pair(3))
                            self.stdscr.addstr(self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
                            self.stdscr.addstr(self.h-3,self.w//5+2,self._results_[i][:self.w-self.w//5-44],curses.color_pair(1))
                            # result_row+=1
                            # # log.info(result_row)
                            continue
                    elif self.result_row>len(self._results_):
                        continue
                    if self.result_row<self.h-3:
                        if self.result_row!=0:
                            self.stdscr.addstr(self.result_row,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                            self.stdscr.addstr(self.result_row,self.w//5+2,self._results_[self.result_row-1][:self.w-self.w//5-44],curses.color_pair(3))
                        self.stdscr.addstr(self.result_row+1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
                        self.stdscr.addstr(self.result_row+1,self.w//5+2,self._results_[self.result_row][:self.w-self.w//5-44],curses.color_pair(1))
                    self.result_row+=1
                    continue
                elif key!=curses.KEY_UP and key!=curses.KEY_ENTER and key!=13 and key!=10:
                    self.result_row = 0

                if key==curses.KEY_UP:
                    curses.curs_set(0)
                    if self.result_row<1:
                        continue
                    if self.result_row>self.h-3:
                        if self.onboard:
                            self.result_row-=1
                            for i in range(self.result_row-self.h+3,self.result_row):
                                self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                                self.stdscr.addstr(i+1-self.result_row+self.h-3,self.w//5+2,self._results_[i][:self.w-self.w//5-44],curses.color_pair(3))
                            self.stdscr.addstr(self.h-3,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
                            self.stdscr.addstr(self.h-3,self.w//5+2,self._results_[i][:self.w-self.w//5-44],curses.color_pair(1))
                            # result_row+=1
                            # # log.info(result_row)
                        continue
                    if self.result_row>1:
                        self.result_row-=1
                    if self.result_row<len(self._results_):
                        self.stdscr.addstr(self.result_row+1,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(3))    
                        self.stdscr.addstr(self.result_row+1,self.w//5+2,self._results_[self.result_row][:self.w-self.w//5-44],curses.color_pair(3))
                    self.stdscr.addstr(self.result_row,self.w//5+2," "*(self.w-self.w//5-40),curses.color_pair(1))
                    self.stdscr.addstr(self.result_row,self.w//5+2,self._results_[self.result_row-1][:self.w-self.w//5-44],curses.color_pair(1))
                    continue
            