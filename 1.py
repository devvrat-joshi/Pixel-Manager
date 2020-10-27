#!/usr/bin/python3.8
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
    per10screen = w//5
    per = " "*(w//5)
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


def print_menu(stdscr,listings,n,this):
    global menu
    # stdscr.clear()
    h,w = stdscr.getmaxyx()
    per10screen = w//5
    maxi = 0
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

def scrolldown(stdscr,cur_row):
    global menu
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

def stat(stdscr,listings,menu,cur_row):
    pass

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
    curses.init_pair(8,curses.COLOR_WHITE, 105)
    curses.init_pair(9,curses.COLOR_WHITE, 7)
    cur_row = 1
    maxi = 0
    for i in menu:
        maxi = max(maxi,len(i))
    l = len(menu)
    curses.init_pair(3, 3, 27)
    stdscr.bkgd(' ', curses.color_pair(3)|curses.A_BOLD)
    path = getpass.getuser()+":"+os.getcwd()+"$"
    print_menu(stdscr,listings,0,"")
    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
    terminal = 0
    k = 0
    onboard = ""
    a = 0
    night = 0
    date = str(time.ctime())
    stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
    stdscr.addstr(h-1,0," "*(w-1),curses.color_pair(7))
    stdscr.addstr(h-1,3*w//5-1,search+" "*(2*w//5-len(search)+1),curses.color_pair(8))
    stdscr.addstr(h-1,0,copy,curses.color_pair(7))
    while 1:
        enter = 0
        key = stdscr.getch()
        date = time.ctime()
        if key==110 and not terminal:
            if night==0:
                curses.init_pair(2, curses.COLOR_WHITE, 161)
                curses.init_pair(3, curses.COLOR_WHITE, 1)
                night = 1
            else:
                curses.init_pair(2, curses.COLOR_WHITE, 18)
                curses.init_pair(3, curses.COLOR_WHITE, 27)
                night = 0
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
            stdscr.addstr(h-1,0,copy,curses.color_pair(7))
            stdscr.addstr(h-1,3*w//5-1,search+" "*(2*w//5-len(search)+1),curses.color_pair(8))
            menu = os.listdir()
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            print_menu(stdscr,listings,0,folder)
            l = len(menu)
            stdscr.addstr(0,0," "*w,curses.color_pair(5))
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
            a = 0
        if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and terminal==1 and k>=0:
            if k<0:
                continue
            k-=1
            onboard = onboard[:-1]
            stdscr.addstr("\b \b")
        elif terminal==1 and key!=263 and key!=258 and key!=259 and key!=261:
            k+=1
            onboard+=chr(key)
            # f = open("some.txt","w")
            # f.write(str(key))
            # f.close()
            if onboard=="cd ..":
                old_menu = path.split("/")[-1][:-1]
                if path==getpass.getuser()+":"+"/"+"$":
                    onboard = "cd .."
                    k = 4
                    stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                    continue
                os.chdir("..")
                path = getpass.getuser()+":"+os.getcwd()+"$"
                menu = os.listdir()
                for i in range(len(menu)):
                    menu[i] = menu[i].lower()
                cur_row = menu.index(old_menu.lower())+1
                l = len(menu)
                listings = []
                for i in menu:
                    listings.append(os.path.isdir(i))
                print_menu(stdscr,listings,1,old_menu)
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
                stdscr.addstr(0,len(pp)," ",curses.color_pair(6))
                curses.curs_set(1)
                stdscr.attron(curses.color_pair(6))
            else:
                onboard = ""
                stdscr.addstr(0,0," "*w,curses.color_pair(5))
                stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
                curses.curs_set(0)
                curses.noecho()
                terminal = 0
        elif key==curses.KEY_DOWN and terminal==0:
            
            if cur_row==len(menu):
                stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            if cur_row>=l or cur_row>h-4:
                if listings[cur_row]:
                    print_folder(stdscr,menu[cur_row])
                else:
                    empty_right(stdscr)
                    stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
                cur_row+=1
                scrolldown(stdscr,cur_row)
                stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
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
                stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            if cur_row>=h-2:
                cur_row-=1
                if listings[cur_row-1]:
                    print_folder(stdscr,menu[cur_row-1])
                else:
                    empty_right(stdscr)
                    stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
                scrolldown(stdscr,cur_row)
                stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
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
                stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            os.chdir("..")
            path = getpass.getuser()+":"+os.getcwd()+"$"
            menu = os.listdir()
            for i in range(len(menu)):
                menu[i] = menu[i].lower()
            cur_row = menu.index(old_menu.lower())+1
            l = len(menu)
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            print_menu(stdscr,listings,1,old_menu)
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
            
            if not os.path.isdir(menu[cur_row-1]):
                os.system("vim "+menu[cur_row-1])
                stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                continue
            old_row = cur_row
            os.chdir(menu[cur_row-1])
            cur_row=1
            menu = os.listdir()
            if len(menu)==0:
                os.chdir("..")
                cur_row=old_row
                menu = os.listdir()
                continue
            path = getpass.getuser()+":"+os.getcwd()+"$"
            l = len(menu)
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            print_menu(stdscr,listings,0,"")
            if terminal==1:
                stdscr.addstr(0,0,"Terminal: "+path+" "*(w-len(path)-10),curses.color_pair(6))
                stdscr.attron(curses.color_pair(6))
                stdscr.addstr(0,len("Terminal: "+path)+1,"")
            else:
                stdscr.addstr(0,0," "*w,curses.color_pair(5))
                stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
        stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
        if terminal==1:
                stdscr.addstr(0,0,"Terminal: "+path+" "*(w-len(path)-10),curses.color_pair(6))
                stdscr.attron(curses.color_pair(6))
                stdscr.addstr(0,len("Terminal: "+path)+1,onboard)
    curses.curs_set(0)
curses.wrapper(main)