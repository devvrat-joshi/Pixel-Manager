all = []
class Node:
    def __init__(self):
        self.children = [None]*300
        self.is_end = False
    
class Trie:
    def __init__(self):
        self.head = Node()
    def insert(self,pattern):
        temp = self.head
        for i in range(len(pattern)):
            ind = ord(pattern[i])
            # print(ind)
            if temp.children[ind] == None:
                temp.children[ind] = Node()
            temp = temp.children[ind]
        temp.is_end = True
    def search(self,pattern):
        temp = self.head
        for i in range(len(pattern)):
            ind = ord(pattern[i])
            if temp is None or temp.children[ind] is None:
                return False
            temp = temp.children[ind]
        return temp.is_end
    def prefix_all(self,head,pattern,results):
        temp = head
        for i in range(300):
            if temp.children[i]:
                if temp.children[i].is_end:
                    results.append(pattern+chr(i))
                results = self.prefix_all(temp.children[i],pattern+chr(i),results)
        return results
    def prefix_search(self,pattern):
        results = []
        temp = self.head
        for i in range(len(pattern)):
            ind = ord(pattern[i])
            if temp.children[ind] == None:
                return results
            temp=temp.children[ind]
        if(temp.is_end):
            key = pattern
            results.append(key)
        results = self.prefix_all(temp,pattern,results)
        return results
    
    def preprocess(self,path):
        try:
            for i in os.listdir(path):
                self.insert(i)
                if os.path.isdir(path+"/"+i):
                    old = path
                    path+="/"+i
                    self.preprocess(path)
                    path = old
        except:
            pass
import os,time
import curses
def prog(stdscr,h,w,kk):
    while not kk.values()[0]:
        curses.init_pair(100,1,10)
        curses.init_pair(200,2,25)
        for i in range(10):
            stdscr.addstr(0,0," "*w,curses.color_pair(1))
		# time.sleep(2)/
        stdscr.refresh()
        for i in range(0,w-1):
            if i==5:
                stdscr.addstr(0,i,"      ",curses.color_pair(200))
            elif i==4:
                stdscr.addstr(0,i,"     ",curses.color_pair(200))
            elif i==3:
                stdscr.addstr(0,i,"    ",curses.color_pair(200))
            elif i==2:
                stdscr.addstr(0,i,"   ",curses.color_pair(200))	
            elif i==1:
                stdscr.addstr(0,i,"  ",curses.color_pair(200))	
            elif i==0:
                stdscr.addstr(0,i," ",curses.color_pair(200))
            elif i<=w-6:
                stdscr.addstr(0,i,"      ",curses.color_pair(200))
            elif i==w-5:
                stdscr.addstr(0,i,"     ",curses.color_pair(200))
            elif i==w-4:
                stdscr.addstr(0,i,"    ",curses.color_pair(200))
            elif i==w-3:
                stdscr.addstr(0,i,"   ",curses.color_pair(200))	
            elif i==w-2:
                stdscr.addstr(0,i,"  ",curses.color_pair(200))	
            elif i==w-1:
                stdscr.addstr(0,i," ",curses.color_pair(200))
            stdscr.refresh()
            if kk.values()[0]:
                break
            time.sleep(0.03)
            if i==5:
                stdscr.addstr(0,i,"      ",curses.color_pair(100))
            elif i==4:
                stdscr.addstr(0,i,"     ",curses.color_pair(100))
            elif i==3:
                stdscr.addstr(0,i,"    ",curses.color_pair(100))
            elif i==2:
                stdscr.addstr(0,i,"   ",curses.color_pair(100))	
            elif i==1:
                stdscr.addstr(0,i,"  ",curses.color_pair(100))	
            elif i==0:
                stdscr.addstr(0,i," ",curses.color_pair(100))
            elif i<=w-6:
                stdscr.addstr(0,i,"      ",curses.color_pair(100))
            elif i==w-5:
                stdscr.addstr(0,i,"     ",curses.color_pair(100))
            elif i==w-4:
                stdscr.addstr(0,i,"    ",curses.color_pair(100))
            elif i==w-3:
                stdscr.addstr(0,i,"   ",curses.color_pair(100))	
            elif i==w-2:
                stdscr.addstr(0,i,"  ",curses.color_pair(100))	
            elif i==w-1:
                stdscr.addstr(0,i," ",curses.color_pair(100))
            stdscr.refresh()
    
