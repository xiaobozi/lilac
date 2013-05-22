# coding=utf8

"""
  Utils for lilac: colored output, log etc.
"""

import sys
from termcolor import colored


class ProgressLogger(object):
    """
      Log progress's status to console::
          [...] progress's description
      or::
          [done] progress's description
      usage::
          progress_logger = ProgressLogger()
          with progress_logger.reset(description):  # reset description
            task()  # do task
    """

    DONE = 1
    UNDO = 2
    ERROR = 3

    def __init__(self, description=''):
        self.reset(description)

    def reset(self, description):
        self.description = description
        self.state = self.UNDO
        return self

    @property
    def text(self):
        if self.state is self.DONE:
            state = "[done]"
            color = "green"
        elif self.state is self.UNDO:
            state = "[....]"
            color = "yellow"
        elif self.state is self.ERROR:
            state = "[error]"
            color = "red"

        if self.description:
            return colored(state, color) + "  " + self.description
        else:
            return ''

    def __enter__(self):
        sys.stdout.write(self.text)
        sys.stdout.flush()

    def __exit__(self, etype, evalue, traceback):
        # clean this line
        sys.stdout.write("\r" + ' '*len(self.text))

        if evalue:  # if has exceptions, raise it
            self.state = self.ERROR
            self.description = str(evalue)
        else:  # task has been done
            self.state = self.DONE

        # back to left
        sys.stdout.write("\r")
        sys.stdout.write(self.text)
        sys.stdout.write("\n")
        sys.stdout.flush()
        # TODO: Judge exception type,  if fatal, kill the script
        # if warning,  go through
        if etype:
            sys.exit(1)


progress_logger = ProgressLogger()


def chunks(lst, number):
    """
      A generator to split list `lst` into `number` equal size parts.

      ::

          lst = range(1, 9)
          chunks(lst, 3)  # return a list each time
                          # [1, 2, 3]
                          # [4, 5, 6]
                          # [7, 8]
    """
    l = len(lst)
    for i in xrange(0, l, number):
        yield lst[i:i + number]


def update_nested_dict(a, b):
    """
      Update nested dict recursivly
    """

    for k, v in b.iteritems():
        if isinstance(v, dict):
            d = a.setdefault(k, {})
            update_nested_dict(d, v)
        else:
            a[k] = v
    return a


def fatal(message):
    """Display error and exit the script"""
    sys.exit(message)  # just raise Systemexit
