#!/usr/bin/python3.8
import curses,time,os
import getpass,sys,signal
import preprocess_trie_hash
import shutil, pickle
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *
from create import *
from stats import *
from terminal_lib import *
import multiprocessing
import logging as log
# from depend import empty_right

log.basicConfig(
    filename="logs.txt", filemode="a", level=log.INFO,
)
tries = {}
se = "Search : "
seme = "Search Something To See Results Here"
def multi(m,kk):
    trie = preprocess_trie_hash.Trie()
    trie.preprocess(os.getcwd())
    m[0] = trie
    kk[0] = 1

# def printer(stdscr, paths, ptr):
#     for i in range(ptr,min(ptr+h-2,len())):
#         stdscr.addstr(i+1-result_row+h-3,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
#         stdscr.addstr(i+1-result_row+h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(3))
#     stdscr.addstr(h-3,w//5+2," "*(w-w//5-40),curses.color_pair(1))
#     stdscr.addstr(h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(1))
    # result_row+=1

def search_init(stdscr,h,w,path,cur_row,overall_path):
    path_right_now = os.getcwd().replace("/","-")+".pkl"
    curr_path = overall_path+"/"+path_right_now
    if path_right_now not in os.listdir(path=overall_path+"/"):
        log.info(path_right_now)
        log.info(os.listdir(overall_path))
        mn = multiprocessing.Manager()
        m = mn.dict()
        kk = mn.dict()
        kk[0] = 0
        p1 = multiprocessing.Process(target=multi,args=(m,kk))
        p1.start()
        preprocess_trie_hash.prog(stdscr,h,w,kk)
        outfile = open(curr_path,'wb')
        pickle.dump(m.values()[0],outfile)
        outfile.close()
        trie = m.values()[0]
    else:
        stdscr.addstr(0,2,"Please Wait...",curses.color_pair(5))
        stdscr.refresh()
        infile = open(curr_path,'rb')
        trie = pickle.load(infile)
        stdscr.addstr(0,2," "*14,curses.color_pair(5))
        stdscr.refresh()
    # trie = tries[os.getcwd()]
    curses.init_pair(18,curses.COLOR_WHITE,18)
    curses.init_pair(19,curses.COLOR_WHITE,63)
    curses.init_pair(100,curses.COLOR_WHITE,35)
    empty_right(stdscr)
    stdscr.addstr(0,0," "*w,curses.color_pair(18))
    stdscr.addstr(0,w//5+1,se+" "*(w-w//5-38-len(se)),curses.color_pair(19))
    stdscr.addstr(1,(w//5+w-36)//2-len(seme)//2,"Search Something To See Results Here")
    stdscr.move(0,w//5+10)
    k = 0
    curses.cbreak()
    curses.curs_set(1)
    # stdscr.addstr(h-2,len(pp)," ",curses.color_pair(6))
    stdscr.attron(curses.color_pair(19))
    _results_ = []
    result_row = 0
    onboard = ""
    curses.cbreak()
    while 1:
        key = stdscr.getch()
        if key==curses.KEY_LEFT:
            continue
        if key==curses.KEY_DOWN:
            curses.curs_set(0)
            # if _results_:
            if result_row>len(_results_)-1:
                continue
            i = 0
            log.info(str(len(_results_))+" "+str(h))
            if result_row>=h-3 and result_row<len(_results_):
                if onboard:
                    result_row+=1
                    for i in range(result_row-h+3,result_row):
                        stdscr.addstr(i+1-result_row+h-3,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                        stdscr.addstr(i+1-result_row+h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(3))
                    stdscr.addstr(h-3,w//5+2," "*(w-w//5-40),curses.color_pair(100))
                    stdscr.addstr(h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(100))
                    # result_row+=1
                    log.info(result_row)
                    continue
            elif result_row>len(_results_):
                continue
            if result_row<h-3:
                if result_row!=0:
                    stdscr.addstr(result_row,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                    stdscr.addstr(result_row,w//5+2,_results_[result_row-1][0][:w-w//5-44]+" ("+str(len(_results_[result_row-1][1]))+")",curses.color_pair(3))
                stdscr.addstr(result_row+1,w//5+2," "*(w-w//5-40),curses.color_pair(100))
                stdscr.addstr(result_row+1,w//5+2,_results_[result_row][0][:w-w//5-44]+" ("+str(len(_results_[result_row][1]))+")",curses.color_pair(100))
            result_row+=1
            continue
        elif key!=curses.KEY_UP and key!=curses.KEY_ENTER and key!=13 and key!=10:
            result_row = 0

        if key==curses.KEY_UP:
            curses.curs_set(0)
            if result_row<1:
                continue
            if result_row>h-3:
                if onboard:
                    result_row-=1
                    for i in range(result_row-h+3,result_row):
                        stdscr.addstr(i+1-result_row+h-3,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                        stdscr.addstr(i+1-result_row+h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(3))
                    stdscr.addstr(h-3,w//5+2," "*(w-w//5-40),curses.color_pair(100))
                    stdscr.addstr(h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(100))
                    # result_row+=1
                    log.info(result_row)
                continue
            if result_row>1:
                result_row-=1
            if result_row<len(_results_):
                stdscr.addstr(result_row+1,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                stdscr.addstr(result_row+1,w//5+2,_results_[result_row][0][:w-w//5-44]+" ("+str(len(_results_[result_row][1]))+")",curses.color_pair(3))
            stdscr.addstr(result_row,w//5+2," "*(w-w//5-40),curses.color_pair(100))
            stdscr.addstr(result_row,w//5+2,_results_[result_row-1][0][:w-w//5-44]+" ("+str(len(_results_[result_row-1][1]))+")",curses.color_pair(100))
            continue
        if (key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT) and result_row!=0:
            if onboard:
                ptrr = result_row
                store_res = _results_[:]
                
                _results_ = _results_[result_row-1][1]
                empty_right(stdscr)
                for i in range(0,min(h-3,len(_results_))):
                    stdscr.addstr(i+1,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                    stdscr.addstr(i+1,w//5+2,_results_[i][:w-w//5-44],curses.color_pair(3))
                stdscr.addstr(1,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                stdscr.addstr(1,w//5+2,_results_[0][:w-w//5-44],curses.color_pair(1))
                result_row = 1
                while 1:
                    key = stdscr.getch()
                    if key==27:
                        _results_ = store_res
                        result_row = ptrr
                        empty_right(stdscr)
                        if result_row>=h-3:
                            for i in range(result_row-h+3,result_row):
                                stdscr.addstr(i+1-result_row+h-3,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                                stdscr.addstr(i+1-result_row+h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(3))
                            stdscr.addstr(h-3,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                            stdscr.addstr(h-3,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(1))
                        else:
                            for i in range(0,min(h-3,len(_results_))):
                                stdscr.addstr(i+1,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                                stdscr.addstr(i+1,w//5+2,_results_[i][0][:w-w//5-44]+" ("+str(len(_results_[i][1]))+")",curses.color_pair(3))
                            stdscr.addstr(result_row,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                            stdscr.addstr(result_row,w//5+2,_results_[result_row-1][0][:w-w//5-44]+" ("+str(len(_results_[result_row-1][1]))+")",curses.color_pair(1))
                        log.info(result_row)
                        break
                    if (key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT) and result_row!=0:
                        log.info(_results_[result_row-1])
                        os.chdir(_results_[result_row-1])
                        log.info(os.getcwd())
                        cur_row=1
                        menu = os.listdir()
                        menu.sort()
                        if len(menu)==0:
                            menu = ["Empty Folder"]
                        path = getpass.getuser()+":"+os.getcwd()+"$"
                        l = len(menu)
                        listings = []
                        for i in menu:
                            listings.append(os.path.isdir(i))
                        print_menu(stdscr,listings,0,"",menu)
                        return True,listings,cur_row,l,menu,path
                        
                    if key==curses.KEY_DOWN:
                        curses.curs_set(0)
                        if result_row>len(_results_)-1:
                            continue
                        i = 0
                        log.info(str(len(_results_))+" "+str(h))
                        if result_row>=h-3 and result_row<len(_results_):
                            if onboard:
                                result_row+=1
                                for i in range(result_row-h+3,result_row):
                                    stdscr.addstr(i+1-result_row+h-3,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                                    stdscr.addstr(i+1-result_row+h-3,w//5+2,_results_[i][:w-w//5-44],curses.color_pair(3))
                                stdscr.addstr(h-3,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                                stdscr.addstr(h-3,w//5+2,_results_[i][:w-w//5-44],curses.color_pair(1))
                                # result_row+=1
                                log.info(result_row)
                                continue
                        elif result_row>len(_results_):
                            continue
                        if result_row<h-3:
                            if result_row!=0:
                                stdscr.addstr(result_row,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                                stdscr.addstr(result_row,w//5+2,_results_[result_row-1][:w-w//5-44],curses.color_pair(3))
                            stdscr.addstr(result_row+1,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                            stdscr.addstr(result_row+1,w//5+2,_results_[result_row][:w-w//5-44],curses.color_pair(1))
                        result_row+=1
                        continue
                    elif key!=curses.KEY_UP and key!=curses.KEY_ENTER and key!=13 and key!=10:
                        result_row = 0

                    if key==curses.KEY_UP:
                        curses.curs_set(0)
                        if result_row<1:
                            continue
                        if result_row>h-3:
                            if onboard:
                                result_row-=1
                                for i in range(result_row-h+3,result_row):
                                    stdscr.addstr(i+1-result_row+h-3,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                                    stdscr.addstr(i+1-result_row+h-3,w//5+2,_results_[i][:w-w//5-44],curses.color_pair(3))
                                stdscr.addstr(h-3,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                                stdscr.addstr(h-3,w//5+2,_results_[i][:w-w//5-44],curses.color_pair(1))
                                # result_row+=1
                                log.info(result_row)
                            continue
                        if result_row>1:
                            result_row-=1
                        if result_row<len(_results_):
                            stdscr.addstr(result_row+1,w//5+2," "*(w-w//5-40),curses.color_pair(3))    
                            stdscr.addstr(result_row+1,w//5+2,_results_[result_row][:w-w//5-44],curses.color_pair(3))
                        stdscr.addstr(result_row,w//5+2," "*(w-w//5-40),curses.color_pair(1))
                        stdscr.addstr(result_row,w//5+2,_results_[result_row-1][:w-w//5-44],curses.color_pair(1))
                        continue
                continue


        curses.curs_set(1)
        stdscr.move(0,w//5+len(se)+len(onboard)+1)
        i = 0
        if key==1:
            curses.curs_set(0)
            stdscr.addstr(0,0," "*w,curses.color_pair(5))
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
            return False, "", "", "", ""
        if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
            if k<0:
                continue
            k-=1
            onboard = onboard[:-1]
            stdscr.addstr("\b \b")
        elif key!=263 and key!=258 and key!=259 and key!=261:
            if w//5+10+k>w-42:
                continue
            k+=1
            onboard+=chr(key)
            stdscr.attron(curses.color_pair(19))
            stdscr.move(0,w//5+len(se)+len(onboard))
            stdscr.addch(key)
            stdscr.attroff(curses.color_pair(19))
        empty_right(stdscr)
        ifit = 0
        if onboard:
            _results_ = trie.prefix_search(onboard)
            for files in _results_:
                ff = len(files[1])
                i+=1
                if i<=h-3:
                    stdscr.addstr(i,w//5+2,files[0][:w-w//5-44]+" ("+str(ff)+")")
                ifit += ff
        if not ifit:
            if not onboard:
                stdscr.addstr(1,(w//5+w-36)//2-len(seme)//2,"Search Something To See Results Here")
            else:
                stdscr.addstr(1,w//5+2,"Not Found: "+onboard)
        stdscr.addstr(0,w-36,"Search Results :       ",curses.color_pair(18))        
        stdscr.addstr(0,w-36,"Search Results : "+str(ifit),curses.color_pair(18))
        bar_single(stdscr,h,w)
        stdscr.move(0,w//5+len(se)+len(onboard)+1)
        stdscr.attron(curses.color_pair(19))