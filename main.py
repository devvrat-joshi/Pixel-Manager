# There are total __ number of files with 2000 lines of code.

import curses  # Import some main dependencies
import getpass  # Used for getting user information and for passing system arguments
import os
import shutil  # Tree level copy, move, delete
import signal
import sys
import time
from datetime import datetime  # Datetime
from distutils.dir_util import copy_tree
from datetime import datetime            # Datetime
import depend                     # Custom created functions and dependencies
from create import getform                     # Custom create file, self.folder 
from stats import bar, bar_single, show_stat, start                      # Custom stats of files
from terminal_lib import terminal_shift_control            # Custom self.terminal
from search import search_init                     # Custom recusive search
from powerful_editor import Editor       # Custom Editor
from deditor import start_editor         #CHECK

# Get Current Directory Details
os.chdir(".")
menu = os.listdir()
menu.sort()

# Some string definitions
permission = "Permission Denied"
file = "It is a File"
copy = " Selected File: "
options = " c : copy, m : move, k : create file, g : create self.folder, v : paste"
search_files_path = os.getcwd()+"/search_files"


class FileManager:
    
    """ 
    Starting of the File Manager
    Takes Input as standard screen : self.stdscr, list of files and folders in current directory
    """
    def __init__(self,stdscr,menu):
        self.menu = menu
        self.stdscr = stdscr
        self.h, self.w = self.stdscr.getmaxyx()      # Get current screen dimensions
        curses.curs_set(0)                           # Set cursor to not visible form
        self.listings = []                                # Prepare a boolean list of self.folder and files
        for i in self.menu:                          
            self.listings.append(os.path.isdir(i))       # Cheking if the self.path is a directory or not
        self.per10screen = self.w//5                          # Dividing screen into 20% - 80%

        # ------------Getting colors for everything on screen-------------
        curses.init_pair(1, curses.COLOR_WHITE, 34) 
        curses.init_pair(2, curses.COLOR_WHITE, 54)
        curses.init_pair(3, 3, 55)
        curses.init_pair(6, curses.COLOR_WHITE, 16)
        curses.init_pair(7,curses.COLOR_WHITE, 57)
        curses.init_pair(15,curses.COLOR_WHITE, 17)
        curses.init_pair(8,curses.COLOR_WHITE, 35)
        curses.init_pair(9,curses.COLOR_WHITE, 7)
        curses.init_pair(13,curses.COLOR_WHITE, 24)
        curses.init_pair(11,curses.COLOR_WHITE,25)
        curses.init_pair(14,curses.COLOR_WHITE,34)
        # ---------///Getting colors for everything on screen///----------

        self.stdscr.bkgd(' ', curses.color_pair(3)|curses.A_BOLD) # Creating background
        self.path = getpass.getuser()+":"+os.getcwd()+"$"         # Making self.path
        self.cur_row = 1
        self.terminal = 0
        self.k = 0
        self.onboard = ""
        self.a,self.bb = 0,0
        self.l = len(self.menu)
        depend.print_menu(self.stdscr,self.listings,0,"",self.menu)
        self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5) + curses.A_BOLD)
        depend.option(self.stdscr,self.h, self.w)
        self.stdscr.addstr(self.h-1,0,copy,curses.color_pair(15))
        show_stat(self.stdscr,self.menu[0],self.listings[self.cur_row-1])
        self.wn = 37
        for i in range(1,self.h-2):
            self.stdscr.addstr(i,self.w-self.wn," "*self.wn,curses.color_pair(11))
        start(self.stdscr)
        curses.curs_set(0)
        self.folder = ""
        self.folder_to_be_copied = ""
        self.startManager()

    def startManager(self):
        """
        Starts File Manager and has all the key bindings.
        Most of the key bindings is added to the bottom of screen.  

        Also, README.md has all bindings listed 
        """
        while 1:
            self.init_new_iteration()
            key = self.stdscr.getch()

            # end key to exit the program
            if key==curses.KEY_END:
                exit(0)

            # Control +A to start searching
            if key==1:
                self.init_search()

            if key==curses.KEY_BTAB: # Open self.terminal
                self.menu,self.listings,self.l,self.path,self.cur_row = terminal_shift_control(self.stdscr,self.k,self.path,self.h, self.w,self.menu,self.listings,self.l,self.cur_row)
                           
            # e to open editor
            if key == ord("e"):
                # editor
                self.init_editor()

            # d to delete the selected file
            if key==ord("d"):
                # Delete file
                self.delete_selection()

            # escape to remove any selected file. (selected for cut/copy/delete)
            if key==27:
                self.delesect_selection()
                continue

            # k to create a new folder
            if key==ord("k") and not self.terminal:
                self.menu,self.listings,self.cur_row = getform(self.stdscr,self.menu,self.listings,0)
                self.l = len(self.menu)
                continue

            # g to create new file
            if key==ord("g") and not self.terminal: 
                self.menu,self.listings,self.cur_row = getform(self.stdscr,self.menu,self.listings,1)
                self.l = len(self.menu)
                continue

            # select current file/folder for copy
            if key==ord('c') and not self.terminal:
                self.copy_selection()
                continue

            if key==ord('v') and self.a==1 and not self.terminal:
                # copy the file/self.folder in buffer to current directory
                self.menu,self.listings,self.l,self.cur_row,_ = depend.copy_cur(self.stdscr,self.fold,self.folder,self.folder_to_be_copied,self.h, self.w,self.path)

            # select current file/folder for moving
            if key==ord("m") and self.bb==0 and not self.terminal:
                # Move
                self.move_selection()
                continue

            # v to paste the selected files
            if key==ord('v') and self.bb==1 and not self.terminal:
                self.moved()
            
            # Down key calling function given terminal is not open
            if key==curses.KEY_DOWN and self.terminal==0:
                if self.key_down():
                    continue
                
            # up key calling function given terminal is not open
            elif key==curses.KEY_UP and self.terminal==0:
                if self.key_up():
                    continue
            
            # left key calling function
            elif key==curses.KEY_LEFT:
                if self.key_left():
                    continue

            # enter key binding, key=10 and 13 are ascii code for enter only.
            # Function for right key is same as enter
            elif key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT:
                if self.key_enter():
                    continue

            # 
            if self.terminal==1:
                self.stdscr.addstr(0,0,"terminal: "+self.path+" "*(self.w-len(self.path)-10),curses.color_pair(6))
                self.stdscr.attron(curses.color_pair(6))
                self.stdscr.addstr(0,len("terminal: "+self.path)+1,self.onboard)

    def key_left(self):
        """
        Browses to the parent directory
        """

        old_menu = self.path.split("/")[-1][:-1]
        if self.path==getpass.getuser()+":"+"/"+"$":
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
            return True
        os.chdir("..")
        self.path = getpass.getuser()+":"+os.getcwd()+"$"
        self.menu = os.listdir()
        self.menu.sort()
        self.cur_row = self.menu.index(old_menu)+1
        l = len(self.menu)
        self.listings = []
        for i in self.menu:
            self.listings.append(os.path.isdir(i))
        depend.print_menu(self.stdscr,self.listings,1,old_menu,self.menu)
        depend.print_folder(self.stdscr,old_menu)
        if self.cur_row<=l:
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.h-2,0," "*(self.w-1))
            self.stdscr.addstr(self.h-2,self.w//2-len(self.menu[self.cur_row-1])//2,self.menu[self.cur_row-1])
        if self.terminal==1:
            self.stdscr.addstr(0,0,"self.terminal: "+self.path+" "*(self.w-len(self.path)-10),curses.color_pair(6))
            self.stdscr.attron(curses.color_pair(6))
            self.stdscr.addstr(0,len("self.terminal: "+self.path)+1,"")
        else:
            self.stdscr.addstr(0,0," "*self.w,curses.color_pair(5))
            self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5))

    def key_enter(self):
        """
        1. browse into the directory if it is a directory
        2. Checks whether it can be opened in the editor (has particular extensions) and opens if possible
        """
        try:
            if not os.path.isdir(self.menu[self.cur_row-1]):
                if self.menu[self.cur_row-1].split(".")[-1] in ["txt","py","cpp","c"]:
                    self.init_editor()
                # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
                return True
            # old_row = self.cur_row
            os.chdir(self.menu[self.cur_row-1])
            self.cur_row=1
            self.menu = os.listdir()
            self.menu.sort()
            if len(self.menu)==0:
                self.menu = ["Empty folder"]
            self.path = getpass.getuser()+":"+os.getcwd()+"$"
            self.l = len(self.menu)
            self.listings = []
            for i in self.menu:
                self.listings.append(os.path.isdir(i))
            depend.print_menu(self.stdscr,self.listings,0,"",self.menu)
            if self.terminal==1:
                self.stdscr.addstr(0,0,"terminal: "+self.path+" "*(self.w-len(self.path)-10),curses.color_pair(6))
                self.stdscr.attron(curses.color_pair(6))
                self.stdscr.addstr(0,len("terminal: "+self.path)+1,"")
            else:
                self.stdscr.addstr(0,0," "*self.w,curses.color_pair(5))
                self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5))
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
        except:
            depend.empty_right(self.stdscr)
            self.stdscr.addstr(self.h//2,self.w//2-len(permission)//2,permission,curses.color_pair(3))
            return True
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
    
    def key_down(self):
        """
        naviagate in a directory
        """

        # last item of directory
        if self.cur_row==len(self.menu):
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
            return True
        
        # to enable scrolling
        if self.cur_row>=self.l or self.cur_row>self.h-4:
            if self.listings[self.cur_row]:
                depend.print_folder(self.stdscr,self.menu[self.cur_row])
            else:
                depend.empty_right(self.stdscr)
                self.stdscr.addstr(self.h//2,self.w//2-len(file)//2,file,curses.color_pair(3))
            self.cur_row+=1
            depend.scrolldown(self.stdscr,self.cur_row,self.menu)
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
            return True
        if len(self.menu[self.cur_row-1])<self.per10screen:
            x = self.menu[self.cur_row-1]+" "*((self.per10screen-len(self.menu[self.cur_row-1])))
        else:
            x = self.menu[self.cur_row-1][:self.per10screen]
        self.stdscr.addstr(self.cur_row,1,x,curses.color_pair(2))
        if self.listings[self.cur_row]:
            depend.print_folder(self.stdscr,self.menu[self.cur_row])
        else:
            depend.empty_right(self.stdscr)
            self.stdscr.addstr(self.h//2,self.w//2-len(file)//2,file,curses.color_pair(3))
        self.cur_row+=1
        if len(self.menu[self.cur_row-1])<self.per10screen:
            x = self.menu[self.cur_row-1]+" "*((self.per10screen-len(self.menu[self.cur_row-1])))
        else:
            x = self.menu[self.cur_row-1][:self.per10screen]
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(self.cur_row,1,x)
        self.stdscr.attroff(curses.color_pair(1))
        if self.cur_row<=self.l:
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.h-2,0," "*(self.w-1))
            self.stdscr.addstr(self.h-2,self.w//2-len(self.menu[self.cur_row-1])//2,self.menu[self.cur_row-1])

    def key_up(self):
        """
        Navigate up in a directory with scrolling
        """
        
        # reached first item
        if self.cur_row==1:
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
            return True

        # scrolling 
        if self.cur_row>=self.h-2:
            self.cur_row-=1

            # printing insides of folder if it is a folder 
            if self.listings[self.cur_row-1]:
                depend.print_folder(self.stdscr,self.menu[self.cur_row-1])
            
            # to print ("this is a file")
            else:
                depend.empty_right(self.stdscr)
                self.stdscr.addstr(self.h//2,self.w//2-len(file)//2,file,curses.color_pair(3))
            depend.scrolldown(self.stdscr,self.cur_row,self.menu)
            # self.stdscr.addstr(1,w-len(date),date,curses.color_pair(5))
            return True

        if len(self.menu[self.cur_row-1])<self.per10screen:
            x = self.menu[self.cur_row-1]+" "*((self.per10screen-len(self.menu[self.cur_row-1])))
        else:
            x = self.menu[self.cur_row-1][:self.per10screen]
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(self.cur_row,1,x)
        self.stdscr.attroff(curses.color_pair(2))
        self.cur_row-=1
        if self.listings[self.cur_row-1]:
            depend.print_folder(self.stdscr,self.menu[self.cur_row-1])
        else:
            depend.empty_right(self.stdscr)
            self.stdscr.addstr(self.h//2,self.w//2-len(file)//2,file,curses.color_pair(3))
        if len(self.menu[self.cur_row-1])<self.per10screen:
            x = self.menu[self.cur_row-1]+" "*((self.per10screen-len(self.menu[self.cur_row-1])))
        else:
            x = self.menu[self.cur_row-1][:self.per10screen]
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(self.cur_row,1,x)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(self.h-2,0," "*(self.w-1))
        self.stdscr.addstr(self.h-2,self.w//2-len(self.menu[self.cur_row-1])//2,self.menu[self.cur_row-1])

    def init_new_iteration(self):
        """
        This function updates state of stdscr when starting each iteration
        """
        show_stat(self.stdscr,self.menu[self.cur_row-1],self.listings[self.cur_row-1])
        for i in range(1,self.h-1):
            self.stdscr.addstr(i,0," ",curses.color_pair(5))
        for i in range(1,self.h-1):
            self.stdscr.addstr(i,self.w-1," ",curses.color_pair(5))
        if not self.terminal:
            self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5) + curses.A_BOLD)

    def init_search(self):
        """
        This function is function used to show the search bar to
        search all files of the current folder (recursive) 
        """
        truth = search_init(self.stdscr,self.h, self.w,self.path,self.cur_row,search_files_path)
        if truth[0]:
            self.listings,self.cur_row,self.l,self.menu,self.path = truth[1],truth[2],truth[3],truth[4],truth[5]
        depend.empty_right(self.stdscr)
        depend.print_folder(self.stdscr,self.menu[self.cur_row-1])

    def init_editor(self):
        """
        Starting out editor. This function restores the state after exiting from the editor
        """
        Editor(self.stdscr,self.menu[self.cur_row-1])
        depend.print_menu(self.stdscr, self.listings, self.cur_row-1, self.menu[self.cur_row-1], self.menu)
        for i in range(1,self.h-2):
            self.stdscr.addstr(i,self.w-self.wn," "*self.wn,curses.color_pair(11))
        curses.init_pair(3, 3, 55)
        curses.init_pair(2, curses.COLOR_WHITE, 54)
        self.stdscr.refresh()

    def delete_selection(self):
        """
        delete the selected file/folder. Need to press r for confirmation
        """
        curses.init_pair(1, curses.COLOR_WHITE, 1)
        curses.init_pair(14, curses.COLOR_WHITE, 1)
        curses.init_pair(4,curses.COLOR_WHITE,1)
        self.stdscr.refresh()
        key = self.stdscr.getch()
        if(key==ord("r")):
            if(os.path.isdir(self.menu[self.cur_row-1])):
                shutil.rmtree(self.menu[self.cur_row-1])
            else:
                os.remove(self.menu[self.cur_row-1])
            self.cur_row = 1
            self.menu = os.listdir()
            self.menu.sort()
            self.listings = []
            for i in self.menu:
                self.listings.append(os.path.isdir(i))
            depend.print_menu(self.stdscr,self.listings,0,"",self.menu)
        curses.init_pair(1, curses.COLOR_WHITE, 34)
        curses.init_pair(14, curses.COLOR_WHITE, 34)
        curses.init_pair(4,curses.COLOR_WHITE,34)
        self.stdscr.refresh()

    def delesect_selection(self):
        """
        Discards the selected file
        """

        depend.option(self.stdscr,self.h, self.w)
        self.stdscr.addstr(self.h-1,0,copy,curses.color_pair(15))
        self.bb = 0
        self.folder = ""
        self.folder_to_be_copied = ""
    
    def move_selection(self):
        """
        This function is used to select the file that is to be moved
        """

        k = self.menu[self.cur_row-1]
        if len(k)>3*self.w//5-30:
            self.stdscr.addstr(self.h-1,len(copy),k[:3*self.w//5-30],curses.color_pair(15))
        else:
            self.stdscr.addstr(self.h-1,len(copy),k,curses.color_pair(15))
        self.folder_to_be_copied = os.getcwd()+"/"+self.menu[self.cur_row-1]
        self.folder = self.menu[self.cur_row-1]
        if self.listings[self.cur_row-1]==1:
            self.fold = True
        else:
            self.fold = False
        self.bb = 1

    def moved(self):
        """
        This function is used to paste the moved selected folder
        """
        try:
            shutil.move(self.folder_to_be_copied,os.getcwd()+"/")
        except:
            pass
        depend.option(self.stdscr,self.h, self.w)
        self.stdscr.addstr(self.h-1,0,copy,curses.color_pair(15))
        self.menu = os.listdir()
        self.menu.sort()
        self.listings = []
        for i in self.menu:
            self.listings.append(os.path.isdir(i))
        self.cur_row = self.menu.index(self.folder)+1
        depend.print_menu(self.stdscr,self.listings,self.cur_row,self.folder,self.menu)
        self.l = len(self.menu)
        self.stdscr.addstr(0,0," "*self.w,curses.color_pair(5))
        self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5))
        self.bb = 0

    def copy_selection(self):
        """
        This function is used to select the file that is to be copied. 
        
        The code to paste the copied structure is in depend.py
        """
        
        k = self.menu[self.cur_row-1]
        if len(k)>3*self.w//5-30:
            self.stdscr.addstr(self.h-1,len(copy),k[:3*self.w//5-30],curses.color_pair(15))
        else:
            self.stdscr.addstr(self.h-1,len(copy),k,curses.color_pair(15))
        self.folder_to_be_copied = os.getcwd()+"/"+self.menu[self.cur_row-1]
        self.folder = self.menu[self.cur_row-1]
        if self.listings[self.cur_row-1]==1:
            self.fold = True
        else:
            self.fold = False
        self.a = 1

def main(stdscr):
    FileManager(stdscr,menu)

curses.wrapper(main)
    
# Previewer
# if key == ord("p"):
#                 self.cur_row = start_editor(self.stdscr,self.menu[self.cur_row-1],self.cur_row)
#                 print_menu(self.stdscr, self.listings, self.cur_row-1, "", self.menu)
#                 for i in range(1,self.h-2):
#                     self.stdscr.addstr(i,self.w-self.wn," "*self.wn,curses.color_pair(11))
#                 curses.init_pair(3, 3, 55)

# Night Mode
#CHECKfile
            # if key==110 and not self.terminal: # Night Mode
            #     if night==0:
            #         curses.init_pair(2, curses.COLOR_WHITE, 161)
            #         curses.init_pair(3, curses.COLOR_WHITE, 1)
            #         night = 1
            #     else:
            #         curses.init_pair(2, curses.COLOR_WHITE, 18)
            #         curses.init_pair(3, curses.COLOR_WHITE, 27)
            #         night = 0
            #     self.stdscr.refresh()
