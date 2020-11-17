#!/usr/bin/python3.8
import curses,time,os
import getpass,sys,signal
import shutil
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *
from create import *
from stats import *
from deditor import start_editor
import multiprocessing
copy = " Selected File: "

def child(onboard):
    os.system('{} > /home/{}/output.txt'.format(onboard,getpass.getuser()))

def terminal_shift_control(stdscr,k,path,h,w,menu,listings,l,cur_row):
    pp = "\U000025B8\U000025B8\U000025B8"
    stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
    k = 0
    curses.cbreak()
    curses.curs_set(1)
    stdscr.addstr(h-2,len(pp)," ",curses.color_pair(6))
    curses.init_pair(20,curses.COLOR_WHITE,234)
    curses.init_pair(20,curses.COLOR_WHITE,236)
    curses.init_pair(21,curses.COLOR_WHITE,234)
    store_commands = []
    for i in range(h-h//2,h-2):
        stdscr.addstr(i,w//5+1,(w-w//5-1)*" ",curses.color_pair(20))
    stdscr.attron(curses.color_pair(6))
    stdscr.addstr(h-h//2-1,w//5+1," "*(w-w//5-1),curses.color_pair(21))
    tring = "Terminal Output ({} Lines)".format(h//2-2)
    stdscr.addstr(h-h//2-1,(w+w//5+1)//2-len(tring)//2-1,tring,curses.color_pair(21))
    onboard = ""
    stdscr.move(h-2,len(pp)+len(onboard)+1)
    o = 0
    cdied = 0
    done = 0
    while 1:
        old = os.getcwd()
        key = stdscr.getch()
        if onboard=="out" and not done:
            done = 1
            curses.curs_set(0)
            file = open('/home/{}/output.txt'.format(getpass.getuser()),"r")
            x =  file.readlines()
            l = len(x)
            curl = 0
            l = len(x)
            for i in range(h-h//2,h-2):
                if curl+i-h+h//2<l and curl>0:
                    x[curl+i-h+h//2]=x[curl+i-h+h//2].replace("\n","")
                    if len(x[i-h+h//2])>w-1-w//5:
                        stdscr.addstr(i,w//5+2,x[curl+i-h+h//2][:w-w//5-2],curses.color_pair(20))
                    else:
                        stdscr.addstr(i,w//5+2,x[curl+i-h+h//2]+" ",curses.color_pair(20))
                stdscr.refresh()
            while 1:
                key = stdscr.getch()
                if key==curses.KEY_DOWN:
                    curl+=1
                if key==curses.KEY_UP  and curl>0:
                    curl-=1
                for i in range(h-h//2,h-2):
                    stdscr.addstr(i,w//5+1,(w-w//5-1)*" ",curses.color_pair(20))
                stdscr.refresh()
                for i in range(h-h//2,h-2):
                    if curl+i-h+h//2<l and curl>=0:
                        x[curl+i-h+h//2]=x[curl+i-h+h//2].replace("\n","")
                        if len(x[i-h+h//2])>w-1-w//5:
                            stdscr.addstr(i,w//5+2,x[curl+i-h+h//2][:w-w//5-2],curses.color_pair(20))
                        else:
                            stdscr.addstr(i,w//5+2,x[curl+i-h+h//2]+" ",curses.color_pair(20))
                        stdscr.refresh()
                    else:
                        if l==curl+i-h+h//2:
                            curl -= 1
                
                if key==ord("e"):
                    break
            
            curses.curs_set(1)
            onboard = ""
            stdscr.addstr(h-1,0,copy,curses.color_pair(15))
            stdscr.move(h-2,len(pp)+len(onboard)+1)
            curses.init_pair(21,curses.COLOR_WHITE,234)
            stdscr.refresh()
            stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
            stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
            # print_menu(stdscr, listings, 0, "", menu)
            # cur_row = 1
            # wn = 37
            # for i in range(1,h-2):
            #     stdscr.addstr(i,w-wn," "*wn,curses.color_pair(11))
            # curses.init_pair(3, 3, 55)
            done = 0
            continue
        if key==curses.KEY_UP:
            if store_commands:
                if o>0:
                    o -= 1
                    stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
                    stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
                    stdscr.move(h-2,len(pp)+1)
                    stdscr.attron(curses.color_pair(6))
                    for i in range(len(store_commands[o])):
                        stdscr.addch(store_commands[o][i])
                        k+=1
                    onboard = store_commands[o]
                continue
        elif key==curses.KEY_DOWN:
            if store_commands:
                if o<len(store_commands)-1:
                    o += 1
                    stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
                    stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
                    stdscr.move(h-2,len(pp)+1)
                    for i in range(len(store_commands[o])):
                        stdscr.addch(store_commands[o][i])
                        k+=1
                    onboard = store_commands[o]
                else:
                    stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
                    stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
                    stdscr.move(h-2,len(pp)+1)
            continue
        if key==curses.KEY_BTAB:
            o = len(store_commands)
            onboard = ""
            stdscr.addstr(h-2,0," "*(w-1),curses.color_pair(4))
            stdscr.addstr(h-2,w//2-len(menu[0])//2,menu[0],curses.color_pair(4))
            curses.curs_set(0)
            curses.noecho()
            for i in range(h-h//2-1,h-2):
                stdscr.addstr(i,w//5+1,(w-w//5-1)*" ",curses.color_pair(3))
                stdscr.addstr(i,w-37," "*37,curses.color_pair(11))
            if cdied:
                cur_row = 1
            return menu,listings,l,path,cur_row
        if key==curses.KEY_ENTER or key==10 or key==13:
            stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
            curses.init_pair(21,curses.COLOR_WHITE,202)
            stdscr.refresh()
            if store_commands:
                if store_commands[-1]!=onboard:
                    store_commands.append(onboard)
            else:
                store_commands.append(onboard)

            o+=1
            command = onboard
            if onboard.find("cd")!=-1:
                try:
                    os.chdir(onboard[3:])
                    stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
                    stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
                except:
                    pass
            else:
                # p = multiprocessing.Process(target=child, args=[onboard])
                # p.start()
                child(onboard)
                file = open('/home/{}/output.txt'.format(getpass.getuser()),"r")
                x =  file.readlines()
                l = len(x)
                for i in range(h-h//2,h-2):
                    stdscr.addstr(i,w//5+1,(w-w//5-1)*" ",curses.color_pair(20))
                for i in range(h-h//2,h-2):
                    if i-h+h//2<l:
                        x[i-h+h//2]=x[i-h+h//2].replace("\n","")
                        if len(x[i-h+h//2])>w-1-w//5:
                            stdscr.addstr(i,w//5+2,x[i-h+h//2][:w-w//5-2],curses.color_pair(20))
                        else:
                            stdscr.addstr(i,w//5+2,x[i-h+h//2]+" ",curses.color_pair(20))
                stdscr.addstr(h-h//2-1,w//5+1," "*(w-w//5-1),curses.color_pair(21))
                tring = "Terminal Output ({} Lines) : {}".format(h//2-2,command)
                stdscr.addstr(h-h//2-1,(w+w//5+1)//2-len(tring)//2-1,tring,curses.color_pair(21))
                stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
                stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
                option(stdscr,h,w)
            onboard = ""
            stdscr.addstr(h-2,0,pp+" "*(w-5),curses.color_pair(6))
            if os.getcwd()!=old:
                # exit()
                cur_row = 0
                menu = os.listdir()
                l = len(menu)
                listings = []
                for i in menu:
                    listings.append(os.path.isdir(i))
                menu.sort()
                print_menu(stdscr,listings,0,"",menu)
                cdied = 1
                for i in range(1,h-2):
                    stdscr.addstr(i,0," ",curses.color_pair(14))
                pp = "\U000025B8\U000025B8\U000025B8"
                stdscr.addstr(h-2,0,pp+" "*(w-len(pp)-1),curses.color_pair(6))
                stdscr.addstr(h-2,len(pp)+1," ",curses.color_pair(6))
                path = getpass.getuser()+":"+os.getcwd()+"$"
                stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
                for i in range(h-h//2,h-2):
                    stdscr.addstr(i,w//5+1,(w-w//5-1)*" ",curses.color_pair(20))
                tring = "Terminal Output ({} Lines)".format(h//2-2)
                stdscr.addstr(h-h//2-1,w//5+1," "*(w-w//5-1),curses.color_pair(21))
                stdscr.addstr(h-h//2-1,(w+w//5+1)//2-len(tring)//2-1,tring,curses.color_pair(21))
            k = 0
            stdscr.addstr(h-1,0,copy,curses.color_pair(15))
            stdscr.move(h-2,len(pp)+len(onboard)+1)
            curses.init_pair(21,curses.COLOR_WHITE,234)
            stdscr.refresh()
            continue
            # terminal = 0
        if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
            if k<0:
                continue
            k-=1
            onboard = onboard[:-1]
            stdscr.addstr("\b \b")
        elif key!=263 and key!=258 and key!=259 and key!=261:
            k+=1
            onboard+=chr(key)
            stdscr.attron(curses.color_pair(6))
            stdscr.move(h-2,len(pp)+len(onboard))
            stdscr.addch(key)