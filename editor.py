import curses
import time
import os

import logging as log
from depend import empty_right

log.basicConfig(
    filename="logs.txt", filemode="a", level=log.INFO,
)


class Editor:
    def __init__(self, stdscr, file_name=f"temp{time.time()}.txt"):
        log.info("starting editor")
        self.stdscr = stdscr
        self.mode = "insert"
        self.column_no = 1
        self.line_number = 1
        self.writeable = 1
        try:
            self.curr_file = open(file_name, "r+")
        except PermissionError:
            self.curr_file = open(file_name, "r")
            self.writeable = 0
            log.info("the file is not writable")
        except IsADirectoryError:
            log.error("the file is a directory. reenter the file name")
            return 1
        self.content = self.curr_file.readlines()
        empty_right(self.stdscr)
        self.show_GUI()

    def show_GUI(self):
        try:
            curses.cbreak()
            curses.echo()
            curses.curs_set(1)
            self.stdscr.attron(curses.color_pair(2))
            log.info("turned off cbreak")
            self.print_content()
            self.insert()
        except Exception as e:
            log.error(f"exception occured in show_gui function{e}")
            pass
        finally:
            curses.curs_set(0)
            curses.noecho()
            empty_right(self.stdscr)
            return 1

    # def write(self):
    #     log.info(f"in {self.mode} mode")
    #     self.insert()
    #     pass

    def insert(self):
        # TODO
        p, w = self.stdscr.getmaxyx()
        while 1:
            key_pressed = self.stdscr.getch()
            if key_pressed == 27:
                self.mode = "command"
                break
            elif key_pressed == curses.KEY_UP:
                self.line_number = max(1, self.line_number - 1)
                self.column_no = min(
                    self.column_no, len(self.content[self.line_number - 1])
                )
                self.stdscr.move(self.line_number, self.column_no + w // 5)
            elif key_pressed == curses.KEY_DOWN:
                self.line_number = min(len(self.content), self.line_number + 1)
                self.column_no = min(
                    self.column_no, len(self.content[self.line_number - 1])
                )
                self.stdscr.move(self.line_number, self.column_no + w // 5)
            elif key_pressed == curses.KEY_LEFT:
                self.column_no = max(1, self.column_no - 1)
                self.stdscr.move(self.line_number, self.column_no + w // 5)
            elif key_pressed == curses.KEY_RIGHT:
                self.column_no = min(
                    len(self.content[self.line_number - 1]), self.column_no + 1
                )
                self.stdscr.move(self.line_number, self.column_no + w // 5)
            elif key_pressed == curses.KEY_BACKSPACE:
                if self.column_no == 1:
                    self.stdscr.move(self.line_number, w // 5 + 1)
                    continue
                self.column_no -= 1
                self.stdscr.delch(self.line_number, self.column_no + w // 5)
                self.stdscr.move(self.line_number, self.column_no + w // 5)
            else:
                self.column_no += 1
                self.stdscr.move(self.line_number, self.column_no + w // 5)

        if self.mode == "command":
            self.command()
        pass

    def command(self):
        # TODO
        key_pressed = self.stdscr.getch()
        return

    def print_content(self):
        p, w = self.stdscr.getmaxyx()
        # self.stdscr.cursyncup()
        for lno in range(len(self.content)):
            x = w // 5 + 1
            y = lno + 1

            # TODO - wrap text when line size is more than a particular length
            self.stdscr.addstr(y, x, self.content[lno])
        self.stdscr.move(1, w // 5 + 1)
        return

