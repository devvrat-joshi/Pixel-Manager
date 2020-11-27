import curses
import time
import os,re
import logging as log
from depend import empty_right
from depend import option
from depend import copy
log.basicConfig(
    filename="logs.txt", filemode="a", level=log.INFO,
)

# scroll : when reaching bottom increase
# lines : exact location of typing
# cursor : cursor

class Editor:
    def __init__(self, stdscr, file_name=None):
        # log.info("starting editor")
        self.h,self.w = stdscr.getmaxyx()
        self.path = file_name
        self.stdscr = stdscr
        self.stdscr.addstr(0,0," "*self.w,curses.color_pair(5) + curses.A_BOLD)
        self.stdscr.addstr(0,self.w//2-len(self.path)//2,self.path,curses.color_pair(5) + curses.A_BOLD)
        curses.init_pair(3,curses.COLOR_WHITE,16)
        curses.init_pair(2, curses.COLOR_WHITE, 24)
        curses.init_pair(40,curses.COLOR_RED,16)
        curses.init_pair(60,curses.COLOR_YELLOW,24)
        self.global_pattern = ""
        self.clear_screen()
        self.stdscr.refresh()
        self.file = open(file_name,"r")
        self.temp_file = open(file_name+str(time.time())+".tmp","w")
        self.start()
        return 

    def clear_screen(self):
        # log.info("YES")
        for i in range(1,self.h-1):
            self.stdscr.addstr(i,0," "*(self.w),curses.color_pair(3))
    
    def print_screen(self,color,range_=None):
        curses.init_pair(44,curses.COLOR_WHITE,51)
        self.clear_screen()
        # [(m.start(0), m.end(0)) for m in re.finditer(self.global_pattern,self.lines[self.scroll_row+i-1][self.scroll_col:self.scroll_col+self.w-self.lenth_of_num-3])]
        for i in range(1,self.h-1):
            if self.scroll_row<max(self.number_of_lines,self.h-2):
                rrr = ""
                self.stdscr.addstr(i,0," "+str(self.scroll_row+i)+"."+" "*(self.lenth_of_num-len(str(self.scroll_row+i))),curses.color_pair(5))
                if range_ and range_[0]<=self.scroll_row+i and range_[1]>self.scroll_row+i:
                    self.stdscr.addstr(i,0," "+str(self.scroll_row+i)+"."+" "*(self.lenth_of_num-len(str(self.scroll_row+i))),curses.color_pair(60))

                if i<self.number_of_lines+1:
                    if self.global_pattern:
                        rrr = [(m.start(0), m.end(0)) for m in re.finditer(re.escape(self.global_pattern),self.lines[self.scroll_row+i-1][self.scroll_col:self.scroll_col+self.w-self.lenth_of_num-3])]
                    self.stdscr.addstr(i,self.lenth_of_num+3,self.lines[self.scroll_row+i-1][self.scroll_col:self.scroll_col+self.w-self.lenth_of_num-3],curses.color_pair(3))
                    log.info(rrr)
                    for j in rrr:
                        for k in range(j[0],j[1]):
                            self.stdscr.addstr(i,self.left_bound+k,self.lines[self.scroll_row+i-1][self.scroll_col+k],curses.color_pair(44))


    def tmp_saver(self):
        

    def background_saver(self):
        self.pid = os.fork()
        if pid==0:
            

    def move_cursor(self):
        self.stdscr.move(self.cursor_row,self.cursor_col)
        self.stdscr.refresh()

    def print_position(self):
        self.stdscr.addstr(self.h-1,self.w-self.w//8," "*(self.w//8-1),curses.color_pair(5))
        self.stdscr.addstr(self.h-1,self.w-self.w//8,"{}, {}".format(self.lines_row+1,self.lines_col+1),curses.color_pair(5))

    def replace(self):
        self.stdscr.addstr(0,0,"REPLACE :",curses.color_pair(60))
        self.stdscr.addstr(0,9," "*(self.w//5-8),curses.color_pair(13))
        replace_on = ""
        while 1:
            self.left_bound = len(str(self.number_of_lines))+3
            self.lenth_of_num = len(str(self.number_of_lines))
            self.print_screen(44)
            self.move_cursor()
            self.stdscr.refresh()
            k = 0
            self.global_patten = ""
            key = self.stdscr.getch()
            if key==curses.KEY_DOWN:
                self.key_down()
            elif key==curses.KEY_UP:
                self.key_up()
            elif key==curses.KEY_LEFT:
                self.key_left()
            elif key==curses.KEY_RIGHT:
                self.key_right()
            elif key==curses.KEY_ENTER or key==10 or key==13:
                for i in range(self.number_of_lines):
                    self.lines[i] = self.lines[i].replace(self.global_pattern,replace_on)
                self.stdscr.addstr(0,0," "*(self.w//5+1),curses.color_pair(5))
                return 

            if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
                    if k<0:
                        continue
                    k-=1
                    replace_on = replace_on[:-1]
                    self.stdscr.move(0,len(replace_on)+10)
                    self.stdscr.addstr("\b \b",curses.color_pair(13))
            elif key!=263 and key!=258 and key!=259 and key!=261:
                k+=1
                replace_on+=chr(key)
                self.stdscr.attron(curses.color_pair(6))
                self.stdscr.move(0,len(replace_on)+8)
                self.stdscr.addch(key,curses.color_pair(13))

    def find(self):
        self.stdscr.addstr(0,4*self.w//5,"FIND :",curses.color_pair(60))
        self.stdscr.addstr(0,4*self.w//5+6," "*(self.w//5-5),curses.color_pair(13))
        while 1:
            self.left_bound = len(str(self.number_of_lines))+3
            self.lenth_of_num = len(str(self.number_of_lines))
            self.print_screen(44)
            self.move_cursor()
            self.stdscr.refresh()
            k = 0
            self.global_patten = ""
            key = self.stdscr.getch()
            if key==curses.KEY_DOWN:
                self.key_down()
            elif key==curses.KEY_UP:
                self.key_up()
            elif key==curses.KEY_LEFT:
                self.key_left()
            elif key==curses.KEY_RIGHT:
                self.key_right()
            elif key==27:
                self.global_pattern = ""
                self.stdscr.addstr(0,4*self.w//5," "*(self.w//5+1),curses.color_pair(5))
                return
            if key==18:
                if self.global_pattern:
                    self.replace()
                    continue
            if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
                    if k<0:
                        continue
                    k-=1
                    self.global_pattern = self.global_pattern[:-1]
                    self.stdscr.move(0,4*self.w//5+len(self.global_pattern)+7)
                    self.stdscr.addstr("\b \b",curses.color_pair(13))
            elif key!=263 and key!=258 and key!=259 and key!=261:
                k+=1
                self.global_pattern+=chr(key)
                self.stdscr.attron(curses.color_pair(6))
                self.stdscr.move(0,4*self.w//5+len(self.global_pattern)+5)
                self.stdscr.addch(key,curses.color_pair(13))
        return

    def options(self,mode):
        if mode=="c":
            x = (self.w-43)//2
            self.stdscr.addstr(self.h-1,0," "*(self.w-1),curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x," esc ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+5,"Command Mode",curses.color_pair(13))
            self.stdscr.addstr(self.h-1,x+17," ctrl+f ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+25,"Find",curses.color_pair(13))
            self.stdscr.addstr(self.h-1,x+29," ctrl+r ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+37,"Replace",curses.color_pair(13))
        if mode=="nc":
            x = (self.w-24)//2
            self.stdscr.addstr(self.h-1,0," "*(self.w-1),curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x," q ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+3,"Exit",curses.color_pair(13))
            self.stdscr.addstr(self.h-1,x+7," i ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+10,"Insert",curses.color_pair(13))
            self.stdscr.addstr(self.h-1,x+16," s ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+19,"Visual",curses.color_pair(13))
        if mode=="v":
            x = (self.w-14)//2
            self.stdscr.addstr(self.h-1,0," "*(self.w-1),curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x," x ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+3,"Cut",curses.color_pair(13))
            self.stdscr.addstr(self.h-1,x+6," c ",curses.color_pair(15))
            self.stdscr.addstr(self.h-1,x+9,"Copy",curses.color_pair(13))

    def cur_copy_paste(self):
        curses.init_pair(44,curses.COLOR_WHITE,51)
        store_row = self.lines_row
        store_col = self.lines_col
        self.stdscr.addstr(0,self.w-self.w//6," "*(self.w//6-1),curses.color_pair(5))
        self.stdscr.addstr(0,self.w-self.w//6,"Select Start Pos : {}, {}".format(store_row+1,store_col+1),curses.color_pair(5))
        self.selector_col = store_col
        self.selector_row = store_row
        self.buffer = []
        no_range = False
        while 1:
            self.left_bound = len(str(self.number_of_lines))+3
            self.lenth_of_num = len(str(self.number_of_lines))
            if not no_range:
                range_ = [store_row+1,self.lines_row+2]
            self.print_screen(44,range_)
            self.stdscr.addstr(self.h-1,self.w-self.w//6," "*(self.w//6-1),curses.color_pair(5))
            self.stdscr.addstr(self.h-1,self.w-self.w//6,"Select End Pos : {}, {}".format(self.lines_row+1,self.lines_col+1),curses.color_pair(5))
            self.move_cursor()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            # exit, will not keep like this, just for now:
            # diff = self.lines_col-store_col
            if key==curses.KEY_DOWN:
                self.key_down()

            elif key==curses.KEY_UP:
                self.key_up()

            elif key==curses.KEY_LEFT:
                self.key_left()
            
            elif key==curses.KEY_RIGHT:
                self.key_right()
                
            elif key==27:
                self.buffer = []
                self.stdscr.addstr(0,self.w-self.w//5," "*(self.w//5-1),curses.color_pair(5))
                self.stdscr.addstr(self.h-1,self.w-self.w//6," "*(self.w//6-1),curses.color_pair(5))
                self.print_position()
                return

            elif key==ord("c"):
                no_range = True
                self.buffer = []
                # if self.lines_row<store_row:
                #     store_row,self.lines_row = self.lines_row,store_row
                # if store_col>self.lines_col:
                #     store_col,self.lines_col = self.lines_col,store_col
                    
                if self.lines_row!=store_row:
                    self.buffer.append(self.lines[store_row][store_col:])
                    for buff_lines in range(store_row+1,self.lines_row):
                        self.buffer.append(self.lines[buff_lines])
                    self.buffer.append(self.lines[self.lines_row][:self.lines_col])
                elif self.lines_col!=store_col:
                    self.buffer = [self.lines[store_row][store_col:]]
                log.info(self.buffer)
                self.stdscr.addstr(0,self.w-self.w//5," "*(self.w//5-1),curses.color_pair(5))
                self.print_position()
                self.stdscr.addstr(0,self.w-self.w//5,"Press v to paste at a position",curses.color_pair(5))
            elif key==ord("x"):
                no_range = True
                self.buffer = []
                store_lines = self.number_of_lines
                if self.lines_row!=store_row:
                    self.buffer.append(self.lines[store_row][store_col:])
                    for buff_lines in range(store_row+1,self.lines_row):
                        self.buffer.append(self.lines[buff_lines])
                    self.buffer.append(self.lines[self.lines_row][:self.lines_col])
                elif self.lines_col!=store_col:
                    self.buffer = [self.lines[store_row][store_col:]]
                if self.lines_row!=store_row:
                    self.lines[store_row] = self.lines[store_row][:store_col]
                    for buff_lines in range(store_row+1,self.lines_row):
                        self.lines.pop(store_row+1)
                        self.number_of_lines-=1
                        self.lines_row-=1
                    self.lines[self.lines_row] = self.lines[self.lines_row][self.lines_col:]
                    self.cursor_col = min(self.w,self.left_bound + len(self.lines[self.lines_row]))
                elif self.lines_col!=store_col:
                    self.lines[store_row] = self.lines[store_row][:store_col]+self.lines[store_row][self.lines_col:]
                    self.cursor_col = min(self.w,self.left_bound + store_col)
                if self.scroll_row>0:
                    self.scroll_row = max(self.scroll_row-(store_lines-self.number_of_lines),0)
                log.info(self.buffer)
                self.stdscr.addstr(0,self.w-self.w//5," "*(self.w//5-1),curses.color_pair(5))
                self.print_position
                self.stdscr.addstr(0,self.w-self.w//5,"Press v to paste at a position",curses.color_pair(5))
                self.lines_row = store_row
                self.lines_col = 0
                self.cursor_row = store_row+1
                self.cursor_col = self.left_bound
                if len(self.lines)==0:
                    self.lines = [""]

            elif key==ord("v") and self.buffer:
                if len(self.buffer)>1:
                    left = self.lines[self.lines_row][:self.lines_col]+self.buffer[0]
                    right = self.lines[self.lines_row][self.lines_col:]
                    self.lines[self.lines_row] = left
                    for buff_lines in range(1,len(self.buffer)):
                        self.number_of_lines+=1
                        self.lines = self.lines[:self.lines_row+buff_lines]+[self.buffer[buff_lines]]+self.lines[self.lines_row+buff_lines:]
                    if right:
                        self.lines = self.lines[:self.lines_row+buff_lines+1]+[right]+self.lines[self.lines_row+buff_lines+1:]
                else:
                     self.lines[self.lines_row] = self.lines[self.lines_row][:self.lines_col]+self.buffer[0]+self.lines[self.lines_row][self.lines_col:]


    def key_down(self):
        if self.cursor_row<min(self.h-2,self.number_of_lines):
            self.cursor_row+=1
        elif self.number_of_lines-self.h+2>self.scroll_row:
            self.scroll_row+=1
        if self.lines_row<self.number_of_lines-1:
            self.lines_row+=1
        if self.cursor_col<len(self.lines[self.lines_row]) and not self.scrolled_right:
            return
        if self.lines_col>self.w or self.scrolled_right:
            self.cursor_col = self.left_bound
            self.lines_col = 0
            self.scroll_col = 0
            self.scrolled_right = False
        elif self.cursor_col>len(self.lines[self.lines_row])+self.left_bound:
            self.cursor_col = len(self.lines[self.lines_row])+self.left_bound
            self.lines_col = len(self.lines[self.lines_row])

    def key_up(self):
        if self.cursor_row>1:
            self.cursor_row-=1
        elif self.scroll_row>0:
            self.scroll_row-=1
        if self.lines_row>0:
            self.lines_row-=1
        if self.cursor_col<len(self.lines[self.lines_row]) and not self.scrolled_right:
            return
        if self.lines_col>self.w or self.scrolled_right:
            self.cursor_col = self.left_bound
            self.lines_col = 0
            self.scroll_col = 0
            self.scrolled_right = False
        elif self.cursor_col>len(self.lines[self.lines_row])+self.left_bound:
            self.cursor_col = len(self.lines[self.lines_row])+self.left_bound
            self.lines_col = len(self.lines[self.lines_row])

    def key_right(self):
        if self.cursor_col<self.w-1 and self.cursor_col<self.left_bound+len(self.lines[self.lines_row]):
            self.cursor_col+=1
        elif self.scroll_col<len(self.lines[self.lines_row])-self.w+self.left_bound+1:
            # log.info(str(len(self.lines[self.lines_row])-2)+" "+str(self.scroll_col))
            self.scrolled_right = True
            self.scroll_col+=1
        if self.lines_col<len(self.lines[self.lines_row]):
            self.lines_col+=1
    def key_left(self):
        if self.cursor_col>self.left_bound:
            self.cursor_col-=1
        elif self.scroll_col>0:
            self.scroll_col-=1
        if self.lines_col>0:
            self.lines_col-=1

    def key_enter(self):
        if self.lines_row<self.number_of_lines:
            if self.lines_col==len(self.lines[self.lines_row]):
                left = self.lines[self.lines_row][:self.lines_col]    
                right = ""
            else:
                left = self.lines[self.lines_row][:self.lines_col]
                right = self.lines[self.lines_row][self.lines_col:]
            self.lines[self.lines_row] = left
            self.lines = self.lines[:self.lines_row+1]+[right]+self.lines[self.lines_row+1:]
            self.number_of_lines+=1
            if self.cursor_row<self.h-2:
                self.cursor_row+=1
            else:
                self.scroll_row+=1
            if self.lines_row<self.number_of_lines:
                self.lines_row+=1
            self.cursor_col = self.left_bound
            self.lines_col = 0
            self.scroll_col = 0

    def key_back(self):
        if self.lines_col==0:
            if self.lines_row!=0:
                store_len = len(self.lines[self.lines_row-1])
                self.lines[self.lines_row-1] = self.lines[self.lines_row-1]+self.lines[self.lines_row]
                self.lines.pop(self.lines_row)
                self.number_of_lines-=1
                self.lines_row-=1
                self.lines_col=store_len
                if self.cursor_col>0:
                    if store_len>self.w:
                        self.scroll_col=store_len-self.w+self.left_bound+1
                        self.cursor_col=self.w-1
                    else:
                        self.cursor_col=store_len+self.left_bound
                if self.scroll_row>0:
                    self.scroll_row-=1
                elif self.cursor_row>1:
                    self.cursor_row-=1

            return
        if self.lines_col>0 and self.lines_col<len(self.lines[self.lines_row])-1:
            self.lines[self.lines_row] = self.lines[self.lines_row][:self.lines_col-1]+self.lines[self.lines_row][self.lines_col:]
        elif self.lines_col>0:
            self.lines[self.lines_row] = self.lines[self.lines_row][:self.lines_col-1]
        if self.cursor_col>self.left_bound:
            self.cursor_col-=1
        elif self.scroll_col>0:
            self.scroll_col-=1
        if self.lines_col>0:
            self.lines_col-=1

    def key_print(self,key):
        self.lines[self.lines_row] = self.lines[self.lines_row][:self.lines_col]+chr(key)+self.lines[self.lines_row][self.lines_col:]
        if self.cursor_col<self.w-1:
            self.cursor_col+=1
        else:
            self.scroll_col+=1
        self.lines_col+=1

    def start(self):
        self.lines = self.file.readlines()
        if len(self.lines)==0:
            self.lines = [""]
        self.number_of_lines = len(self.lines)
        for line in range(self.number_of_lines):
            self.lines[line] = self.lines[line].replace("\n","")
        # self.lines[-1] = self.lines[-1]+" "
        self.lenth_of_num = len(str(self.number_of_lines))
        self.scroll_row = 0
        self.scrolled_right = False
        self.scroll_col = 0
        self.cursor_row = 1
        self.lines_row = 0
        self.lines_col = 0
        self.cursor_col = len(str(self.number_of_lines))+3
        self.left_bound = len(str(self.number_of_lines))+3
        curses.curs_set(1)
        self.options("c")
        self.print_screen(3)
        self.move_cursor()
        self.stdscr.refresh()
        while 1:
            self.left_bound = len(str(self.number_of_lines))+3
            self.lenth_of_num = len(str(self.number_of_lines))
            self.print_screen(3)
            self.print_position()
            self.move_cursor()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            # exit, will not keep like this, just for now:
            if key==27:
                self.options("nc")
                self.move_cursor()
                self.print_position()
                while 1:
                    key = self.stdscr.getch()
                    if key==ord("q"):
                        option(self.stdscr,self.h,self.w)
                        self.stdscr.refresh()
                        self.stdscr.addstr(self.h-1,0,copy,curses.color_pair(15))
                        curses.curs_set(0)
                        return 
                    elif key==ord("s"):
                        self.options("v")
                        self.move_cursor()
                        self.print_position()
                        self.cur_copy_paste()
                        break
                    elif key==ord("i"):
                        break
                self.options("c")
                self.move_cursor()
                self.print_position()
                continue

            if key==6:
                self.find()
                continue

            if key==curses.KEY_DOWN:
                self.key_down()

            elif key==curses.KEY_UP:
                self.key_up()

            elif key==curses.KEY_LEFT:
                self.key_left()
            
            elif key==curses.KEY_RIGHT:
                self.key_right()

            elif key==curses.KEY_ENTER or key==10 or key==13:
                self.key_enter()


            elif key==curses.KEY_BACKSPACE:
                self.key_back()

            else:
                self.key_print(key)



# else:
#     if self.lines_col==0:
#         self.lines[self.lines_row] = self.lines[self.lines_row][:self.lines_col]+chr(key)+" "
#     else:
#         self.lines[self.lines_row] = self.lines[self.lines_row][:self.lines_col-1]+chr(key)+" "
# DOWN
# if store_row<self.lines_row:
                #     self.stdscr.addstr(self.cursor_row-1,
                #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-2][self.scroll_col+self.cursor_col-self.left_bound:min(self.w,len(self.lines[self.scroll_row+self.lines_row-1]))],
                #                         curses.color_pair(44))
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][:self.scroll_col+self.cursor_col-self.left_bound],
                #                         curses.color_pair(44))
                # else:
                #     self.stdscr.addstr(self.cursor_row-1,
                #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-2][self.scroll_col+self.cursor_col-self.left_bound:min(self.w,len(self.lines[self.scroll_row+self.lines_row-1]))],
                #                         curses.color_pair(3))
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][:self.scroll_col+self.cursor_col-self.left_bound],
                #                         curses.color_pair(3))
# UP
                # if store_row>self.lines_row:
                #     self.stdscr.addstr(self.cursor_row+1,
                #                         self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row][:self.scroll_col+self.cursor_col-self.left_bound],
                #                         curses.color_pair(44))
                #     self.stdscr.addstr(self.cursor_row, 
                #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound:min(self.w,len(self.lines[self.scroll_row+self.lines_row]))],
                #                         curses.color_pair(44))
                # else:
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound:min(self.w,len(self.lines[self.scroll_row+self.lines_row]))],
                #                         curses.color_pair(3))
                #     self.stdscr.addstr(self.cursor_row+1,
                #                         self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row][:self.scroll_col+self.cursor_col-self.left_bound],
                #                         curses.color_pair(3))
#Right
# if self.lines_col>store_col:
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.lenth_of_num+2+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound-1],
                #                         curses.color_pair(44))
                # else:
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.lenth_of_num+2+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound-1],
                #                         curses.color_pair(3))
            
            
            # elif self.lines_col<store_col:
            #     self.stdscr.addstr(self.cursor_row,
            #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
            #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound],
            #                         curses.color_pair(44))
#LEFT
# if self.lines_col<store_col:
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound],
                #                         curses.color_pair(44))
                # else:
                #     self.stdscr.addstr(self.cursor_row,
                #                         self.lenth_of_num+3+self.cursor_col-self.left_bound,
                #                         self.lines[self.scroll_row+self.cursor_row-1][self.scroll_col+self.cursor_col-self.left_bound],
                #                         curses.color_pair(3))