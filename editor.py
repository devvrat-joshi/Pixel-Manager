import curses,re                                                                    #a,sdjflksdjfl;kajsdlkfjalksdfj;laksjdfklajsd;lfjalksdfjaklsdjfalksjdfklajsdflkajsdlfkjasdlkfjasldkfjl;
from editor_command import command_mode
import getpass,os
python_key = "import |from |for |while | or | and |def | in |range|if |else |elif"
import curses,re                                                                    #a,sdjflksdjfl;kajsdlkfjalksdfj;laksjdfklajsd;lfjalksdfjaklsdjfalksjdfklajsdflkajsdlfkjasdlkfjasldkfjl;
def start_editor(stdscr,filename,cur_row):
    curses.init_pair(55,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.init_pair(43,curses.COLOR_WHITE,curses.COLOR_BLACK)
    newfile = open("logging.txt","w")
    h,w = stdscr.getmaxyx()
    path = filename
    stdscr.addstr(0,0," "*w,curses.color_pair(5) + curses.A_BOLD)
    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
    curses.init_pair(3,curses.COLOR_WHITE,16)
    curses.init_pair(2, curses.COLOR_WHITE, 24)
    curses.init_pair(40,curses.COLOR_RED,16)
    stdscr.refresh()
    for i in range(1,h-2):
        stdscr.addstr(i,w//5+1," "*(4*w//5),curses.color_pair(3))
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
        rrr = [(m.start(0), m.end(0)) for m in re.finditer(python_key,x[row_current+i-1]+"\n")]
        for j in rrr:
            if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                # exit()
                for k in range(j[0],j[1]):
                    stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(40))
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
        if key==6:
            stdscr.addstr(0,4*w//5,"find :"+" "*(w//5-5),curses.color_pair(13))
            k = 0
            onboard = ""
            pp = 4*w//5+5
            while 1:
                row_current = curpoint_row-1
                key = stdscr.getch()
                if key==27:
                    stdscr.addstr(0,4*w//5," "*(w//5+1),curses.color_pair(15))
                    row_current = curpoint_row-1
                    cursor_row = 0
                    cursor_col = 0
                    col_current = 0
                    curpoint_col = 1
                    break
                if key==18:
                    kk = 0
                    stdscr.addstr(0,0,"Replace :"+" "*(w//5-8),curses.color_pair(11))
                    stdscr.move(0,9)
                    onb = ""
                    while 1:
                        key = stdscr.getch()
                        if key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT:
                            for i in range(len(x)):
                                x[i] = x[i].replace(onboard,onb)
                            for i in range(1,h-2):
                                if i<len(x):
                                    stdscr.addstr(i,w//5+1,x[row_current+i-1][:4*w//5],curses.color_pair(3))
                                    stdscr.addstr(i,w//5+1,x[row_current+i-1][:lene+1],curses.color_pair(5))
                                rrr = [(m.start(0), m.end(0)) for m in re.finditer(python_key,x[row_current+i-1]+"\n")]
                                for j in rrr:
                                    if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                                        # exit()
                                        for k in range(j[0],j[1]):
                                            stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(40))
                                rrr = [(m.start(0), m.end(0)) for m in re.finditer(onb,x[row_current+i-1]+"\n")]
                                for j in rrr:
                                    if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                                        # exit()
                                        for k in range(j[0],j[1]):
                                            stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(43)) 
                                stdscr.addstr(0,0," "*(w//5+1),curses.color_pair(15))
                            break
                        elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE and kk>=0:
                            if kk<0:
                                continue
                            kk-=1
                            onb = onb[:-1]
                            stdscr.move(0,10+len(onb))
                            stdscr.addstr("\b \b",curses.color_pair(13))
                        elif key!=263 and key!=258 and key!=259 and key!=261:
                            kk+=1
                            onb+=chr(key)
                            stdscr.attron(curses.color_pair(6))
                            stdscr.move(0,8+len(onb))
                            stdscr.addch(key,curses.color_pair(13))
                    continue
                        # stdscr.m                        if key==27:ove(0,9+len(onb))
                if key==curses.KEY_DOWN or key==10 or key==13:
                    row_current+=1
                    curpoint_row+=1
                    for i in range(1,h-2):
                        stdscr.addstr(i,w//5+1," "*(4*w//5),curses.color_pair(3))
                    for i in range(1,h-2):
                        if i<len(x):
                            stdscr.addstr(i,w//5+1,x[row_current+i-1][:4*w//5],curses.color_pair(3))
                            stdscr.addstr(i,w//5+1,x[row_current+i-1][:lene+1],curses.color_pair(5))
                        rrr = [(m.start(0), m.end(0)) for m in re.finditer(python_key,x[row_current+i-1]+"\n")]
                        for j in rrr:
                            if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                                # exit()
                                for k in range(j[0],j[1]):
                                    stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(40))
                        rrr = [(m.start(0), m.end(0)) for m in re.finditer(onboard,x[row_current+i-1]+"\n")]
                        for j in rrr:
                            if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                                # exit()
                                for k in range(j[0],j[1]):
                                    stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(43))
                    stdscr.addstr(h-1,w-w//8," "*(w//8-1),curses.color_pair(5))
                    stdscr.addstr(h-1,w-w//8,"{}, {}".format(curpoint_row,curpoint_col),curses.color_pair(5))
                    continue
                if key==curses.KEY_UP:
                    curpoint_row-=1
                    row_current-=1
                    for i in range(1,h-2):
                        stdscr.addstr(i,w//5+1," "*(4*w//5),curses.color_pair(3))
                    for i in range(1,h-2):
                        if i<len(x):
                            stdscr.addstr(i,w//5+1,x[row_current+i-1][:4*w//5],curses.color_pair(3))
                            stdscr.addstr(i,w//5+1,x[row_current+i-1][:lene+1],curses.color_pair(5))
                        rrr = [(m.start(0), m.end(0)) for m in re.finditer(python_key,x[row_current+i-1]+"\n")]
                        for j in rrr:
                            if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                                # exit()
                                for k in range(j[0],j[1]):
                                    stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(40))
                        rrr = [(m.start(0), m.end(0)) for m in re.finditer(onboard,x[row_current+i-1]+"\n")]
                        for j in rrr:
                            if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                                # exit()
                                for k in range(j[0],j[1]):
                                    stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(43))
                    stdscr.addstr(h-1,w-w//8," "*(w//8-1),curses.color_pair(5))
                    stdscr.addstr(h-1,w-w//8,"{}, {}".format(curpoint_row,curpoint_col),curses.color_pair(5))
                    continue    
                if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k>=0:
                    if k<0:
                        continue
                    k-=1
                    onboard = onboard[:-1]
                    stdscr.move(0,pp+len(onboard)+2)
                    stdscr.addstr("\b \b",curses.color_pair(13))
                elif key!=263 and key!=258 and key!=259 and key!=261:
                    k+=1
                    onboard+=chr(key)
                    stdscr.attron(curses.color_pair(6))
                    stdscr.move(0,pp+len(onboard))
                    stdscr.addch(key,curses.color_pair(13))
                for i in range(1,h-2):
                    if i<len(x):
                        stdscr.addstr(i,w//5+1,x[row_current+i-1][:4*w//5],curses.color_pair(3))
                        stdscr.addstr(i,w//5+1,x[row_current+i-1][:lene+1],curses.color_pair(5))
                    rrr = [(m.start(0), m.end(0)) for m in re.finditer(python_key,x[row_current+i-1]+"\n")]
                    for j in rrr:
                        if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                            # exit()
                            for k in range(j[0],j[1]):
                                stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(40))
                    rrr = [(m.start(0), m.end(0)) for m in re.finditer(onboard,x[row_current+i-1]+"\n")]
                    for j in rrr:
                        if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                            # exit()
                            for k in range(j[0],j[1]):
                                stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(43))
                
            stdscr.move(1,w//5+3+lene)
            continue
        if key==27:
            store = command_mode(stdscr,h,w,curpoint_row,curpoint_col,cursor_row,cursor_col,lene,row_current,col_current,x)
            if store=="quit":
                path = getpass.getuser()+":"+os.getcwd()+"/"+filename+"$"
                stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
                curses.init_pair(2, curses.COLOR_WHITE, 54)
                stdscr.refresh()
                return cur_row
        if key==curses.KEY_END:
            ll = len(x[curpoint_row-1])
            curpoint_col = ll-lene-2
            cursor_col = ll-lene
        elif key==curses.KEY_DOWN:
            if curpoint_row<lll-1:
                curpoint_row+=1
            if cursor_row+1>h-4 and row_current<lll-h+2:
                row_current+=1
            else:
                if cursor_row<h-4:
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
        elif key==curses.KEY_LEFT and col_current>=0 and curpoint_col>1:
            curpoint_col-=1
            if cursor_col>0:
                cursor_col-=1
            else:
                if col_current>0:
                    col_current-=1
        elif key==curses.KEY_LEFT:
            continue
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
            rrr = [(m.start(0), m.end(0)) for m in re.finditer(python_key,x[row_current+i-1]+"\n")]
            for j in rrr:
                if j[0]>=col_current and j[1]<=col_current+4*w//5-1:
                    # exit()
                    for k in range(j[0],j[1]):
                        stdscr.addstr(i,w//5+1+k-col_current,x[row_current+i-1][k],curses.color_pair(40))
        stdscr.refresh()
        # if key==27:
            # path = getpass.getuser()+":"+os.getcwd()+"/"+filename+"$"
            # stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
            # curses.init_pair(2, curses.COLOR_WHITE, 54)
            # stdscr.refresh()
            # return cur_row
        stdscr.move(1+cursor_row,3+w//5+lene+cursor_col)