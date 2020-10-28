#!/usr/bin/python3.8
import curses,time,os
import getpass,sys,signal
import shutil
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *
from create import *
from stats import *
os.chdir(".")
menu = os.listdir()

permission = "Permission Denied"
file = "It is a File"
copy = "Selected File: "
options = " c : copy, m : move, k : create file, g : create folder"

def main(stdscr):
    global menu
    curses.curs_set(0)
    h,w = stdscr.getmaxyx()
    listings = []
    for i in menu:
        listings.append(os.path.isdir(i))
    per10screen = w//5
    curses.init_pair(1, curses.COLOR_WHITE, 34)
    curses.init_pair(2, curses.COLOR_WHITE, 18)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7,curses.COLOR_WHITE, 57)
    curses.init_pair(8,curses.COLOR_WHITE, 35)
    curses.init_pair(9,curses.COLOR_WHITE, 7)
    cur_row = 1
    maxi = 0
    for i in menu:
        maxi = max(maxi,len(i))
    l = len(menu)
    curses.init_pair(3, 3, 27)
    stdscr.bkgd(' ', curses.color_pair(3)|curses.A_BOLD)
    path = getpass.getuser()+":"+os.getcwd()+"$"
    print_menu(stdscr,listings,0,"",menu)
    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
    terminal = 0
    k = 0
    onboard = ""
    a,bb = 0,0
    night = 0
    # date = str(time.ctime())
    # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
    stdscr.addstr(h-1,0," "*(w-1),curses.color_pair(7))
    stdscr.addstr(h-1,2*w//5-1,options+" "*(3*w//5-len(options)+1),curses.color_pair(8))
    stdscr.addstr(h-1,0,copy,curses.color_pair(7))
    show_stat(stdscr,menu[0],listings[cur_row-1])
    curses.init_pair(11,curses.COLOR_WHITE,25)
    wn = 37
    for i in range(1,h-2):
        stdscr.addstr(i,w-wn," "*wn,curses.color_pair(11))
    curses.curs_set(0)
    while 1:
        show_stat(stdscr,menu[cur_row-1],listings[cur_row-1])
        if not terminal:
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
        enter = 0
        key = stdscr.getch()
        # date = time.ctime()
        if key==ord("k") and not terminal:
            menu,listings,cur_row = getform(stdscr,menu,listings,0)
            l = len(menu)
            continue
        if key==ord("g") and not terminal:
            menu,listings,cur_row = getform(stdscr,menu,listings,1)
            l = len(menu)
            continue
        if key==110 and not terminal:
            if night==0:
                curses.init_pair(2, curses.COLOR_WHITE, 161)
                curses.init_pair(3, curses.COLOR_WHITE, 1)
                night = 1
            else:
                curses.init_pair(2, curses.COLOR_WHITE, 18)
                curses.init_pair(3, curses.COLOR_WHITE, 27)
                night = 0
            stdscr.refresh()
            # time.sleep(2)
        if key==99 and not terminal:
            k = menu[cur_row-1]
            if len(k)>3*w//5-30:
                stdscr.addstr(h-1,len(copy),k[:3*w//5-30],curses.color_pair(7))
            else:
                stdscr.addstr(h-1,len(copy),k,curses.color_pair(7))
            folder_to_be_copied = os.getcwd()+"/"+menu[cur_row-1]
            folder = menu[cur_row-1]
            if listings[cur_row-1]==1:
                fold = True
            else:
                fold = False
            a = 1
            continue
        if key==118 and a==1 and not terminal:
            if not fold:
                shutil.copy(folder_to_be_copied, os.getcwd()+"/"+folder)
            else:
                copy_tree(folder_to_be_copied, os.getcwd()+"/"+folder)
            stdscr.addstr(h-1,0," "*(w-1),curses.color_pair(7))
            stdscr.addstr(h-1,2*w//5-1,options+" "*(3*w//5-len(options)+1),curses.color_pair(8))
            stdscr.addstr(h-1,0,copy,curses.color_pair(7))
            menu = os.listdir()
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            cur_row = menu.index(folder)+1
            print_menu(stdscr,listings,cur_row,folder,menu)
            l = len(menu)
            stdscr.addstr(0,0," "*w,curses.color_pair(5))
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
            a = 0
        if key==ord("m") and bb==0 and not terminal:
            k = menu[cur_row-1]
            if len(k)>3*w//5-30:
                stdscr.addstr(h-1,len(copy),k[:3*w//5-30],curses.color_pair(7))
            else:
                stdscr.addstr(h-1,len(copy),k,curses.color_pair(7))
            folder_to_be_copied = os.getcwd()+"/"+menu[cur_row-1]
            folder = menu[cur_row-1]
            if listings[cur_row-1]==1:
                fold = True
            else:
                fold = False
            bb = 1
            continue
        if key==118 and bb==1 and not terminal:
            shutil.move(folder_to_be_copied,os.getcwd()+"/")
            stdscr.addstr(h-1,0," "*(w-1),curses.color_pair(7))
            stdscr.addstr(h-1,2*w//5-1,options+" "*(3*w//5-len(options)+1),curses.color_pair(8))
            stdscr.addstr(h-1,0,copy,curses.color_pair(7))
            menu = os.listdir()
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            cur_row = menu.index(folder)+1
            print_menu(stdscr,listings,cur_row,folder,menu)
            l = len(menu)
            stdscr.addstr(0,0," "*w,curses.color_pair(5))
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
            bb = 0
        if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and terminal==1 and k>=0:
            if k<0:
                continue
            k-=1
            onboard = onboard[:-1]
            stdscr.addstr("\b \b")
        elif terminal==1 and key!=263 and key!=258 and key!=259 and key!=261:
            k+=1
            onboard+=chr(key)
            stdscr.move(0,len(path)+len(onboard)+1)
            # f = open("some.txt","w")
            # f.write(str(key))
            # f.close()
            if onboard=="cd ..":
                old_menu = path.split("/")[-1][:-1]
                if path==getpass.getuser()+":"+"/"+"$":
                    onboard = "cd .."
                    k = 4
                    # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                    continue
                os.chdir("..")
                path = getpass.getuser()+":"+os.getcwd()+"$"
                menu = os.listdir()
                cur_row = menu.index(old_menu)+1
                l = len(menu)
                listings = []
                for i in menu:
                    listings.append(os.path.isdir(i))
                print_menu(stdscr,listings,1,old_menu,menu)
                print_folder(stdscr,old_menu)
                if cur_row<=l:
                    stdscr.attron(curses.color_pair(4))
                    stdscr.addstr(h-2,0," "*(w-1))
                    stdscr.addstr(h-2,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
                if terminal==1:
                    stdscr.addstr(0,0,"Terminal: "+path+" "*(w-len(path)-10),curses.color_pair(6))
                    stdscr.attron(curses.color_pair(6))
                    stdscr.addstr(0,len("Terminal: "+path)+1,"")
                else:
                    stdscr.addstr(0,0," "*w,curses.color_pair(5))
                    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))    
                onboard=""
            else:
                stdscr.addch(key)
            
            
        if key==curses.KEY_BTAB:
            if terminal==0:
                pp = "Terminal: "+path
                stdscr.addstr(0,0,pp+" "*(w-len(path)-10),curses.color_pair(6))
                terminal = 1
                k = 0
                curses.cbreak()
                curses.curs_set(1)
                stdscr.addstr(0,len(pp)," ",curses.color_pair(6))
                stdscr.attron(curses.color_pair(6))
            else:
                onboard = ""
                stdscr.addstr(0,0," "*w,curses.color_pair(5))
                stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
                curses.curs_set(0)
                curses.noecho()
                terminal = 0
                continue
        
        if key==curses.KEY_DOWN and terminal==0:
            
            if cur_row==len(menu):
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            if cur_row>=l or cur_row>h-4:
                if listings[cur_row]:
                    print_folder(stdscr,menu[cur_row])
                else:
                    empty_right(stdscr)
                    stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
                cur_row+=1
                scrolldown(stdscr,cur_row,menu)
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(2))
            if listings[cur_row]:
                print_folder(stdscr,menu[cur_row])
            else:
                empty_right(stdscr)
                stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
            cur_row+=1
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(1))
            if cur_row<=l:
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(h-2,0," "*(w-1))
                stdscr.addstr(h-2,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
        elif key==curses.KEY_UP and terminal==0:
            
            if cur_row==1:
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            if cur_row>=h-2:
                cur_row-=1
                if listings[cur_row-1]:
                    print_folder(stdscr,menu[cur_row-1])
                else:
                    empty_right(stdscr)
                    stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
                scrolldown(stdscr,cur_row,menu)
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(2))
            cur_row-=1
            if listings[cur_row-1]:
                print_folder(stdscr,menu[cur_row-1])
            else:
                empty_right(stdscr)
                stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(h-2,0," "*(w-1))
            stdscr.addstr(h-2,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
        elif key==curses.KEY_LEFT:
            
            old_menu = path.split("/")[-1][:-1]
            if path==getpass.getuser()+":"+"/"+"$":
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            os.chdir("..")
            path = getpass.getuser()+":"+os.getcwd()+"$"
            menu = os.listdir()
            cur_row = menu.index(old_menu)+1
            l = len(menu)
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            print_menu(stdscr,listings,1,old_menu,menu)
            print_folder(stdscr,old_menu)
            if cur_row<=l:
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(h-2,0," "*(w-1))
                stdscr.addstr(h-2,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
            if terminal==1:
                stdscr.addstr(0,0,"Terminal: "+path+" "*(w-len(path)-10),curses.color_pair(6))
                stdscr.attron(curses.color_pair(6))
                stdscr.addstr(0,len("Terminal: "+path)+1,"")
            else:
                stdscr.addstr(0,0," "*w,curses.color_pair(5))
                stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
        elif key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT:
            try:
                if not os.path.isdir(menu[cur_row-1]):
                    os.system("gedit "+menu[cur_row-1])
                    # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                    continue
                old_row = cur_row
                os.chdir(menu[cur_row-1])
                cur_row=1
                menu = os.listdir()
                if len(menu)==0:
                    menu = ["Empty Folder"]
                path = getpass.getuser()+":"+os.getcwd()+"$"
                l = len(menu)
                listings = []
                for i in menu:
                    listings.append(os.path.isdir(i))
                print_menu(stdscr,listings,0,"",menu)
                if terminal==1:
                    stdscr.addstr(0,0,"Terminal: "+path+" "*(w-len(path)-10),curses.color_pair(6))
                    stdscr.attron(curses.color_pair(6))
                    stdscr.addstr(0,len("Terminal: "+path)+1,"")
                else:
                    stdscr.addstr(0,0," "*w,curses.color_pair(5))
                    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
            except:
                empty_right(stdscr)
                stdscr.addstr(h//2,w//2-len(permission)//2,permission,curses.color_pair(3))
                continue
                # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
        if terminal==1:
                stdscr.addstr(0,0,"Terminal: "+path+" "*(w-len(path)-10),curses.color_pair(6))
                stdscr.attron(curses.color_pair(6))
                stdscr.addstr(0,len("Terminal: "+path)+1,onboard)
        # stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
curses.wrapper(main)