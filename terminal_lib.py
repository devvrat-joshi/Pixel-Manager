#!/usr/bin/python3.8
# import dependencies
import curses,time,os                       # OS , curses, time     
import getpass,sys,signal                   # user info
import shutil                               
from distutils.dir_util import copy_tree
from datetime import datetime
from depend import *
from create import *
from stats import *
import multiprocessing

# Some strings
copy = " Selected File: "

# If required child
def child(onboard):
    os.system('({}) > /home/{}/output.txt 2>&1'.format(onboard,getpass.getuser()))

class Terminal:
    """
        Terminal class adds terminal to screen with control to terminal and its output
    """
    def __init__(self,stdscr,k,path,h,w,menu,listings,l,cur_row):
        # Making Room For Terminal
        self.path = path
        self.stdscr = stdscr
        self.h = h 
        self.w = w
        self.menu = menu
        self.listings = listings
        self.l = l
        self.cur_row = cur_row
        self.pp = "\U000025B8\U000025B8\U000025B8"
        self.stdscr.addstr(self.h-2,0,self.pp+" "*(w-len(self.pp)-1),curses.color_pair(6))
        curses.cbreak()
        curses.curs_set(1)
        self.stdscr.addstr(self.h-2,len(self.pp)," ",curses.color_pair(6))
        # Getting colors for Terminal
        curses.init_pair(20,curses.COLOR_WHITE,234)
        curses.init_pair(20,curses.COLOR_WHITE,236)
        curses.init_pair(21,curses.COLOR_WHITE,234)
        self.store_commands = []     # Stores history of commands

        # Making the Terminal Output Window
        for i in range(self.h-self.h//2,self.h-2):
            self.stdscr.addstr(i,self.w//5+1,(w-self.w//5-1)*" ",curses.color_pair(20))
        self.stdscr.attron(curses.color_pair(6))
        self.stdscr.addstr(self.h-self.h//2-1,self.w//5+1," "*(w-self.w//5-1),curses.color_pair(21))
        self.tring = "(esc) Terminal Output ({} Lines)".format(self.h//2-2)
        self.stdscr.addstr(self.h-self.h//2-1,(w+self.w//5+1)//2-len(self.tring)//2-1,self.tring,curses.color_pair(21))
        self.onboard = ""
        self.stdscr.move(self.h-2,len(self.pp)+len(self.onboard)+1)

    def start(self):
        """
            start terminal
        """
        self.o = 0
        self.cdied = 0
        self.done = 0
        k = 0
        while 1:
            self.old = os.getcwd()
            key = self.stdscr.getch()

            # if down key and no previous commands
            if key==curses.KEY_DOWN and not self.done:
                self.key_down_and_not_done()
                self.done = 0
                continue

            # if up key
            if key==curses.KEY_UP:
                if self.key_up():
                    continue

            # if down key
            elif key==curses.KEY_DOWN:
                if self.key_down():
                    continue
            
            # if back tab then exit
            elif key==curses.KEY_BTAB:
                return self.exit_to_main()

            # enter command, then run the command
            elif key==curses.KEY_ENTER or key==10 or key==13:
                if self.key_enter():
                    continue
            # print user input on screen
            elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
                if k<0:
                    continue
                k-=1
                self.onboard = self.onboard[:-1]
                # bar_single(self.stdscr,h,w)
                self.stdscr.move(self.h-2,len(self.pp)+len(self.onboard)+2)
                self.stdscr.addstr("\b \b")

            elif key!=263 and key!=258 and key!=259 and key!=261:
                k+=1
                self.onboard+=chr(key)
                self.stdscr.attron(curses.color_pair(6))
                # bar_single(self.stdscr,h,w)
                self.stdscr.move(self.h-2,len(self.pp)+len(self.onboard))
                self.stdscr.addch(key)
                
    def key_down_and_not_done(self):
        """
            if down key is pressed and no command had run previously, somewhat complex code
        """
        self.done = 1
        curses.curs_set(0)
        file = open('/home/{}/output.txt'.format(getpass.getuser()),"r")
        x =  file.readlines()
        self.l = len(x)
        self.curl = 0
        self.l = len(x)
        for i in range(self.h-self.h//2,self.h-2):
            if self.curl+i-self.h+self.h//2<self.l and self.curl>0:
                x[self.curl+i-self.h+self.h//2]=x[self.curl+i-self.h+self.h//2].replace("\n","")
                if len(x[i-self.h+self.h//2])>self.w-1-self.w//5:
                    self.stdscr.addstr(i,self.w//5+2,x[self.curl+i-self.h+self.h//2][:self.w-self.w//5-2],curses.color_pair(20))
                else:
                    self.stdscr.addstr(i,self.w//5+2,x[self.curl+i-self.h+self.h//2]+" ",curses.color_pair(20))
            self.stdscr.refresh()

        while 1:
            key = self.stdscr.getch()
            if key==curses.KEY_DOWN:
                self.curl+=1
            if key==curses.KEY_UP  and self.curl>0:
                self.curl-=1
            for i in range(self.h-self.h//2,self.h-2):
                self.stdscr.addstr(i,self.w//5+1,(self.w-self.w//5-1)*" ",curses.color_pair(20))
            self.stdscr.refresh()
            for i in range(self.h-self.h//2,self.h-2):
                if self.curl+i-self.h+self.h//2<self.l and self.curl>=0:
                    x[self.curl+i-self.h+self.h//2]=x[self.curl+i-self.h+self.h//2].replace("\n","")
                    if len(x[i-self.h+self.h//2])>self.w-1-self.w//5:
                        self.stdscr.addstr(i,self.w//5+2,x[self.curl+i-self.h+self.h//2][:self.w-self.w//5-3],curses.color_pair(20))
                    else:
                        self.stdscr.addstr(i,self.w//5+2,x[self.curl+i-self.h+self.h//2][:self.w-self.w//5-3]+" ",curses.color_pair(20))
                    self.stdscr.refresh()
                else:
                    if self.l==self.curl+i-self.h+self.h//2:
                        self.curl -= 1
            if key==27:
                break
        
        curses.curs_set(1)
        self.onboard = ""
        self.stdscr.addstr(self.h-1,0,copy,curses.color_pair(15))
        self.stdscr.move(self.h-2,len(self.pp)+len(self.onboard)+1)
        curses.init_pair(21,curses.COLOR_WHITE,234)
        self.stdscr.refresh()
        self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
        self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
    
    def key_up(self):
        """
            up key
        """
        if self.store_commands:
            if self.o>0:
                self.o -= 1
                self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
                self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
                self.stdscr.move(self.h-2,len(self.pp)+1)
                self.stdscr.attron(curses.color_pair(6))
                for i in range(len(self.store_commands[self.o])):
                    self.stdscr.addch(self.store_commands[self.o][i])
                    self.k+=1
                self.onboard = self.store_commands[self.o]
            return True

    def key_down(self):
        """
            if a previous command is executed, then scroll through the terminal output
        """
        if self.store_commands:
            if self.o<len(self.store_commands)-1:
                self.o += 1
                self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
                self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
                self.stdscr.move(self.h-2,len(self.pp)+1)
                for i in range(len(self.store_commands[self.o])):
                    self.stdscr.addch(self.store_commands[self.o][i])
                    k+=1
                self.onboard = self.store_commands[self.o]
            else:
                self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
                self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
                self.stdscr.move(self.h-2,len(self.pp)+1)
        return True
    
    def exit_to_main(self):
        """
            exit to main class
        """
        self.o = len(self.store_commands)
        self.onboard = ""
        self.stdscr.addstr(self.h-2,0," "*(self.w-1),curses.color_pair(4))
        self.stdscr.addstr(self.h-2,self.w//2-len(self.menu[0])//2,self.menu[0],curses.color_pair(4))
        curses.curs_set(0)
        curses.noecho()
        for i in range(self.h-self.h//2-1,self.h-2):
            self.stdscr.addstr(i,self.w//5+1,(self.w-self.w//5-1)*" ",curses.color_pair(3))
            self.stdscr.addstr(i,self.w-37," "*37,curses.color_pair(11))
        if self.cdied:
            self.cur_row = 1
        return self.menu,self.listings,self.l,self.path,self.cur_row
    
    def key_enter(self):
        """
            press enter to execute command, complex code and cd command handled in different fasion
        """
        self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
        curses.init_pair(21,curses.COLOR_WHITE,202)
        self.stdscr.refresh()
        if self.store_commands:
            if self.store_commands[-1]!=self.onboard:
                self.store_commands.append(self.onboard)
        else:
            self.store_commands.append(self.onboard)
        self.o+=1
        command = self.onboard
        if self.onboard.find("cd")!=-1:
            try:
                os.chdir('{}'.format(self.onboard[3:]))
                self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
                self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
            except:
                pass
        else:
            child(self.onboard)
            file = open('/home/{}/output.txt'.format(getpass.getuser()),"r")
            x =  file.readlines()
            self.l = len(x)
            for i in range(self.h-self.h//2,self.h-2):
                self.stdscr.addstr(i,self.w//5+1,(self.w-self.w//5-1)*" ",curses.color_pair(20))
            for i in range(self.h-self.h//2,self.h-2):
                if i-self.h+self.h//2<self.l:
                    x[i-self.h+self.h//2]=x[i-self.h+self.h//2].replace("\n","")
                    if len(x[i-self.h+self.h//2])>self.w-1-self.w//5:
                        self.stdscr.addstr(i,self.w//5+2,x[i-self.h+self.h//2][:self.w-self.w//5-2],curses.color_pair(20))
                    else:
                        self.stdscr.addstr(i,self.w//5+2,x[i-self.h+self.h//2]+" ",curses.color_pair(20))
            self.stdscr.addstr(self.h-self.h//2-1,self.w//5+1," "*(self.w-self.w//5-1),curses.color_pair(21))
            self.tring = "(esc) Terminal Output ({} Lines) : {}".format(self.h//2-2,command)
            self.stdscr.addstr(self.h-self.h//2-1,(self.w+self.w//5+1)//2-len(self.tring)//2-1,self.tring,curses.color_pair(21))
            self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
            self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
            option(self.stdscr,self.h,self.w)
        self.onboard = ""
        self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-5),curses.color_pair(6))
        
        if os.getcwd()!=self.old:
            # exit()
            self.cur_row = 0
            self.menu = os.listdir()
            self.l = len(self.menu)
            self.listings = []
            for i in self.menu:
                self.listings.append(os.path.isdir(i))
            self.menu.sort()
            print_menu(self.stdscr,self.listings,0,"",self.menu)
            self.cdied = 1
            for i in range(1,self.h-2):
                self.stdscr.addstr(i,0," ",curses.color_pair(14))
            self.pp = "\U000025B8\U000025B8\U000025B8"
            self.stdscr.addstr(self.h-2,0,self.pp+" "*(self.w-len(self.pp)-1),curses.color_pair(6))
            self.stdscr.addstr(self.h-2,len(self.pp)+1," ",curses.color_pair(6))
            self.path = getpass.getuser()+":"+os.getcwd()+"$"
            self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5) + curses.A_BOLD)
            for i in range(self.h-self.h//2,self.h-2):
                self.stdscr.addstr(i,self.w//5+1,(self.w-self.w//5-1)*" ",curses.color_pair(20))
            self.tring = "(esc) Terminal Output ({} Lines)".format(self.h//2-2)
            self.stdscr.addstr(self.h-self.h//2-1,self.w//5+1," "*(self.w-self.w//5-1),curses.color_pair(21))
            self.stdscr.addstr(self.h-self.h//2-1,(self.w+self.w//5+1)//2-len(self.tring)//2-1,self.tring,curses.color_pair(21))
        self.k = 0
        self.stdscr.addstr(self.h-1,0,copy,curses.color_pair(15))
        self.stdscr.move(self.h-2,len(self.pp)+len(self.onboard)+1)
        curses.init_pair(21,curses.COLOR_WHITE,234)
        self.stdscr.refresh()
        return True
    

        
