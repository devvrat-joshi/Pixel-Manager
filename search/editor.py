import curses
import getpass,os
file = open("new.txt","r")
x = file.readlines()

def start_editor(stdscr,filename,cur_row):
    newfile = open("logging.txt","w")
    h,w = stdscr.getmaxyx()
    path = filename
    stdscr.addstr(0,0," "*w,curses.color_pair(5) + curses.A_BOLD)
    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
    curses.init_pair(3,curses.COLOR_WHITE,16)
    curses.init_pair(2, curses.COLOR_WHITE, 24)
    stdscr.refresh()
    for i in range(1,h-2):
        stdscr.addstr(i,w//5+1," "*(4*w//5-1),curses.color_pair(3))
    file = open(filename,"r")
    # file1 = open("temp"+filename,"w")
    x = file.readlines()
    l = len(x)
    lene = len(str(l))+1
    for i in range(max(len(x),h-2)):
        if i<l:
            st = x[i].find("\n")
            if st!=-1:
                x[i] = x[i][:st]
            x[i] = str(i+1)+"."+" "*(lene-len(str(i+1))+1)+x[i]
        else:
            x.append(str(i+1)+"."+" ")
    row_current = 0
    col_current = 0
    l = len(x)
    for i in range(1,h-2):
        if i<l:
            stdscr.addstr(i,w//5+1,x[i-1][:4*w//5],curses.color_pair(3))
            stdscr.addstr(i,w//5+1,x[i-1][:lene+1],curses.color_pair(5))
    curses.curs_set(1)
    cursor_row = 0
    cursor_col = 0
    curpoint_row = 1
    curpoint_col = 1
    stdscr.addstr(h-1,w-w//8," "*(w//8-1),curses.color_pair(5))
    stdscr.addstr(h-1,w-w//8,"{}, {}".format(curpoint_row,curpoint_col),curses.color_pair(5))
    stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)
    while 1:
        key = stdscr.getch()
        lll = len(x)
        if key==curses.KEY_END:
            ll = len(x[curpoint_row-1])
            curpoint_col = ll-lene-2
            cursor_col = ll-lene
        # newfile.write(str(len(x)))
        # ektrue = 0
        elif key==curses.KEY_DOWN and row_current<lll-h+3:
            curpoint_row+=1
            if cursor_row+1>=h-3:
                row_current+=1
            else:
                cursor_row+=1
            # cursor_col-=1
            if curpoint_col>=len(x[curpoint_row-1])-lene-1:
                curpoint_col = len(x[curpoint_row-1])-lene-1
                cursor_col = (len(x[curpoint_row-1])-lene-2)
                # exit()
            # if col_current>llen(x[curpoint_row-1])en(x[cur_row-1]):
            #     col_current = len(x[row_current-1])
            #     cursor_col = len(x[row_current-1])
        elif key==curses.KEY_UP and row_current>=0:
            if cursor_row+1<=1 and row_current>0:
                row_current-=1
                curpoint_row-=1
            else:
                if cursor_row>0:
                    curpoint_row-=1
                    cursor_row-=1
            if curpoint_col>=len(x[curpoint_row-1])-lene-1:
                curpoint_col = len(x[curpoint_row-1])-lene-1
                cursor_col = (len(x[curpoint_row-1])-lene-2)
        elif key==curses.KEY_ENTER or key==10 or key==13:
            temp = x[curpoint_row-1][curpoint_col-1:]
            x[curpoint_row-1] = x[curpoint_row-1][:curpoint_col+lene+1]
            x = x[:curpoint_row]+[temp]+x[curpoint_row:]
            l = len(x)
            for i in range(len(x)):
                if i<l:
                    x[i] = str(i+1)+"."+" "*(lene-len(str(i+1))+1)+x[i][lene+2:]
                else:
                    x.append(str(i+1)+"."+" ")
            curpoint_col = 1
            curpoint_row+=1
            if cursor_row+1>=h-3:
                row_current+=1
            lll = len(x)
            cursor_row+=1
            if cursor_row>=h-4:
                cursor_row = h-4
            cursor_col=0
        elif key==curses.KEY_RIGHT and curpoint_col<len(x[curpoint_row-1])-lene-1:
            curpoint_col+=1
            if 3+w//5+lene+cursor_col>=w-1:
                col_current+=1
            else:
                cursor_col+=1
        elif key==curses.KEY_LEFT and col_current>=0:
            curpoint_col-=1
            if cursor_col>0:
                cursor_col-=1
            else:
                if col_current>0:
                    col_current-=1
        elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE:
            # onboard = onboard[:-1]
            if curpoint_col==1 and curpoint_row>1:
                curlen = len(x[curpoint_row-2])
                x[curpoint_row-2] = x[curpoint_row-2]+x[curpoint_row-1][lene+2:]
                x = x[:curpoint_row-1]+x[curpoint_row:]
                curpoint_col = curlen-lene-1
                cursor_col = curlen-lene-2
                if curpoint_row<h-2:
                    cursor_row-=1
                curpoint_row-=1
                if cursor_row+1<=lll and row_current>0:
                    row_current-=1
                lll = l = len(x)
                for i in range(len(x)):
                    if i<l:
                        x[i] = str(i+1)+"."+" "*(lene-len(str(i+1))+1)+x[i][lene+2:]
                    else:
                        x.append(str(i+1)+"."+" ")
            elif curpoint_col>1:
                x[curpoint_row-1] = x[curpoint_row-1][:lene+1+curpoint_col-1]+x[curpoint_row-1][lene+1+curpoint_col:]
                curpoint_col-=1
                cursor_col-=1
        elif key!=263 and key!=258 and key!=259 and key!=261:
            x[curpoint_row-1] = x[curpoint_row-1][:lene+1+curpoint_col]+chr(key)+x[curpoint_row-1][lene+1+curpoint_col:]
            newfile.write(x[row_current])
            curpoint_col+=1
            cursor_col+=1
            
            
        stdscr.addstr(h-1,w-w//8," "*(w//8-1),curses.color_pair(5))
        stdscr.addstr(h-1,w-w//8,"{}, {}".format(curpoint_row,curpoint_col),curses.color_pair(5))
        for i in range(1,h-2):
            stdscr.addstr(i,w//5+1," "*(4*w//5),curses.color_pair(3))
        for i in range(1,h-2):
            if i<l:
                stdscr.addstr(i,w//5+1,x[row_current+i-1][col_current:col_current+4*w//5],curses.color_pair(3))
                stdscr.addstr(i,w//5+1,x[row_current+i-1][:lene+1],curses.color_pair(5))
        stdscr.refresh()
        if key==ord("e"):
            path = getpass.getuser()+":"+os.getcwd()+"/"+filename+"$"
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
            curses.init_pair(2, curses.COLOR_WHITE, 54)
            stdscr.refresh()
            return cur_row
        stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)
    # stdscr.getch()
    # stdscr.addstr()