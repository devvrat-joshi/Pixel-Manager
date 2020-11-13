import curses
import time
import os
import re

import logging as log
from depend import empty_right, print_menu

log.basicConfig(
    filename="logs.txt", filemode="a", level=log.INFO,
)


class Editor:
    def __init__(self, stdscr, file_name=None):
        log.info("starting editor")
        # if file_name is None:
        #     self.new = 1
        #     self.file_name = f"temp{time.time()}.txt"
        # else:
        na, ex = file_name.split(".")
        self.file_name = f"{na}-temp{time.time()}.{ex}"
        self.stdscr = stdscr
        self.mode = "insert"
        self.column_no = 1
        self.line_number = 1
        self.writeable = 1
        os.system(f"cp {file_name} {self.file_name}")
        try:
            # if not self.new:
            self.curr_file = open(self.file_name, "r+")
        except PermissionError:
            self.curr_file = open(self.file_name, "r")
            self.writeable = 0
            log.info("the file is not writable")
        except Exception as e:
            log.error(f"error in __init__ fn - {e}")
            self.file_name = f"temp{time.time()}.txt"
            self.curr_file = open(self.file_name, "r+")
        self.content = self.curr_file.readlines()
        self.height, self.swidth = self.stdscr.getmaxyx()
        empty_right(self.stdscr, True)
        self.show_editor()

    def show_editor(self):
        try:
            curses.cbreak()
            curses.echo()
            curses.curs_set(1)
            self.stdscr.attron(curses.color_pair(2))
            log.info("turned off cbreak")
            self.print_content()
            self.loop()
        except Exception as e:
            log.error(f"exception occured in show_editor function - {e}")
        finally:
            self.curr_file.close()
            curses.curs_set(0)
            curses.noecho()
            empty_right(self.stdscr, True)
            # print_menu(self.stdscr, )  # bas devvrat ko hi pata kaise kaam kar rha yeh function
            return 1

    def loop(self):
        log.info(self.content)
        quit_editor = 0
        while 1:
            key_pressed = self.stdscr.getch()
            if self.mode == "insert":
                _ = self.insert(key_pressed)
            else:
                quit_editor, save_file = self.command(key_pressed)
            if quit_editor:
                break
        if save_file:
            self.save()
        else:
            self.curr_file.close()
            os.system(f"rm {self.file_name}")
        return

    def insert(self, key_pressed):
        # TODO
        if key_pressed == 27:
            self.mode = "command"
            return 0
        elif key_pressed == curses.KEY_UP:
            self.line_number = max(1, self.line_number - 1)
            self.column_no = min(
                self.column_no, len(self.content[self.line_number - 1])
            )
            self.stdscr.move(self.line_number, self.column_no)
        elif key_pressed == curses.KEY_DOWN:
            self.line_number = min(len(self.content), self.line_number + 1)
            self.column_no = min(
                self.column_no, len(self.content[self.line_number - 1])
            )
            self.stdscr.move(self.line_number, self.column_no)
        elif key_pressed == curses.KEY_LEFT:
            self.column_no = max(1, self.column_no - 1)
            self.stdscr.move(self.line_number, self.column_no)
        elif key_pressed == curses.KEY_RIGHT:
            self.column_no = min(
                len(self.content[self.line_number - 1]), self.column_no + 1
            )
            self.stdscr.move(self.line_number, self.column_no)
        elif key_pressed == curses.KEY_BACKSPACE or key_pressed == 8:
            if self.column_no == 1:
                self.stdscr.move(self.line_number, 1)
                return 0
            self.column_no -= 1
            self.content[self.line_number - 1] = (
                self.content[self.line_number - 1][: self.column_no - 1]
                + self.content[self.line_number - 1][self.column_no :]
            )
            # self.stdscr.delch(self.line_number, self.column_no + self.swidth // 5)
            self.stdscr.addstr(
                self.line_number,
                1,
                self.content[self.line_number - 1],
            )
            self.stdscr.move(self.line_number, self.column_no)
        elif key_pressed == curses.KEY_ENTER or key_pressed == 10:
            self.line_number += 1
            self.content = (
                self.content[: self.line_number - 1]
                + ["\n"]
                + self.content[self.line_number - 1 :]
            )
            self.column_no = 1
            self.print_content()
            self.stdscr.move(self.line_number, self.column_no)

        else:
            self.content[self.line_number - 1] = (
                self.content[self.line_number - 1][: self.column_no - 1]
                + chr(key_pressed)
                + self.content[self.line_number - 1][self.column_no - 1 :]
            )
            self.stdscr.addstr(
                self.line_number,
                1,
                self.content[self.line_number - 1],
            )
            self.column_no += 1
            self.stdscr.move(self.line_number, self.column_no)

        return 0

    def command(self, key_pressed):
        # TODO
        if key_pressed == ord("i"):
            self.mode = "insert"
            return 0, True
        elif key_pressed == ord("s"):
            return 1, True
        elif key_pressed == ord("d"):
            return 1, False

        return 0, True

    def save(self):
        log.info(self.content)
        self.curr_file.close()
        self.curr_file = open(self.file_name, "w")
        self.curr_file.writelines(self.content)
        if not self.writeable:
            log.warning("The file is not writable, the data is deleted")
            return
        # if self.new:
        #     fname = self.create_newfile(self.stdscr)
        # else:
        li = self.file_name.split("-")
        fname = li[0]
        ext = li[-1].split(".")[-1]
        fname = f"{fname}.{ext}"

        os.system(f"mv {self.file_name} {fname}")
        return

    def print_content(self):
        for lno in range(len(self.content)):
            x = 1
            y = lno + 1

            # TODO - wrap text when line size is more than a particular length
            self.stdscr.addstr(y, x, self.content[lno])
        self.stdscr.move(1, 1)
        self.stdscr.refresh()
        return


"""
    @staticmethod
    def create_newfile(stdscr):
        name_str = "File Name : "
        h, w = stdscr.getmaxyx()
        curses.init_pair(10, curses.COLOR_WHITE, 56)
        stdscr.attron(curses.color_pair(10))
        stdscr.addstr(h - 3, w // 5, " " * (4 * w // 5), curses.color_pair(10))
        stdscr.addstr(h - 3, w // 5, name_str, curses.color_pair(10))
        key = stdscr.getch()
        k = 0
        onboard = ""
        while key != curses.KEY_ENTER and key != 10 and key != 13:
            if key == 8 or key == 127 or key == curses.KEY_BACKSPACE and k >= 0:
                if k <= 0:
                    continue
                k -= 1
                onboard = onboard[:-1]
                stdscr.addstr("\b \b")
            elif key != 263 and key != 258 and key != 259 and key != 261:
                k += 1
                onboard += chr(key)
                stdscr.move(h - 3, w // 5 + len(name_str) + len(onboard) - 1)
                stdscr.addch(key)
            key = stdscr.getch()
        tmp = onboard.split(".")
        if len(tmp) == 1:
            onboard = onboard + ".txt"
        return onboard
        # if onboard!="":
        #     file = open(onboard,"w")
        #     file.close()
        #     pass
"""
