import curses
import getpass,os
file = open("new.txt","r")
x = file.readlines()

def start_editor(stdscr,filename,cur_row):
    h,w = stdscr.getmaxyx()
    path = filename
    stdscr.addstr(0,0," "*w,curses.color_pair(5) + curses.A_BOLD)
    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
    curses.init_pair(3,curses.COLOR_WHITE,16)
    curses.init_pair(2, curses.COLOR_WHITE, 24)
    stdscr.refresh()
    for i in range(1,h-1):
        stdscr.addstr(i,w//5+1," "*(4*w//5-1),curses.color_pair(3))
    file = open(filename,"r")
    # file1 = open("temp"+filename,"w")
    x = file.readlines()
    l = len(x)
    lene = len(str(l))+1
    for i in range(max(len(x),h-1)):
        if i<l:
            x[i] = str(i+1)+"."+" "*(lene-len(str(i+1))+1)+x[i]
        else:
            x.append(str(i+1)+"."+" ")
    curline = 0
    l = len(x)
    for i in range(1,h-1):
        if i<l:
            stdscr.addstr(i,w//5+1,x[i-1][:4*w//5],curses.color_pair(3))
            stdscr.addstr(i,w//5+1,x[i-1][:lene+1],curses.color_pair(5))
    curses.curs_set(0)
    while 1:
        key = stdscr.getch()
        if key==curses.KEY_DOWN and curline<-h+1+l:
            curline+=1
        if key==curses.KEY_UP and curline!=0:
            curline-=1
        for i in range(1,h-1):
            if i<l:
                stdscr.addstr(i,w//5+1,x[curline+i-1][:4*w//5],curses.color_pair(3))
                stdscr.addstr(i,w//5+1,x[curline+i-1][:lene+1],curses.color_pair(5))
        if key==ord("e"):
            path = getpass.getuser()+":"+os.getcwd()+"/"+filename+"$"
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
            curses.init_pair(2, curses.COLOR_WHITE, 54)
            stdscr.refresh()
            return cur_row
    # stdscr.getch()
    # stdscr.addstr()