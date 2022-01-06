
"""
"""

# Native
import random
import time
import curses
from curses import wrapper

# # 3rd-Party

# # Proprietary
from foe.db import session

class Monitor(object):
    """
    """

    SEPERATOR = 145 * '-'

    def __init__(self, screen, interval=1):
        """
        """

        self.screen = screen
        self.interval = float(interval)
        # How long the monitor has been running for in seconds
        self.running = 0

        return

    def setup(self):
        """
        """

        self.increment = Inc()

        return

    def run(self):
        """
        """

        self.setup()

        # Clear screen
        self.screen.clear()
        #
        curses.start_color()

        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.screen.nodelay(True)

        try:
            while True:
                #
                session.expire_all()
                # TODO: Add some standard header to the top? (like interval time etc)
                #
                self.render()
                #
                self.increment.reset()
                #
                self.screen.refresh()
                #
                time.sleep(self.interval)

                c = self.screen.getch() # Get char from input.  If none is available, will return -1.
                if c == 3:
                    raise KeyboardInterrupt
                else:
                    curses.flushinp() # Clear out buffer.  We only care about Ctrl+C.

                self.running += self.interval
        except KeyboardInterrupt:
            self.screen.addstr(3, 0, "Ctrl+C detected, Program Stopping")
            self.screen.refresh()

        return

    def render(self):
        """
        """

        raise Exception("Abstract")

    @property
    def line(self):
        """
        """

        return self.increment.inc()

    def fixed(self, value, length, padding=' '):
        """
        """

        diff = length - len(str(value))

        return '%s%s' % (value, padding * diff)


# Bleh.. all because we can't do num++
class Inc(object):
    """
    """

    def __init__(self, start=0, step=1):
        """
        """

        self.num = start
        self.step = step

        return

    def inc(self):
        """
        """

        self.num += self.step

        return self.num

    def dec(self):
        """
        """

        self.num -= self.step

        return self.num

    def reset(self):
        """
        """

        self.num = 0

        return self
