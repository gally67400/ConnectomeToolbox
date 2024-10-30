#! /usr/bin/env python


def print_(msg, print_it=True):  # print_it=False when not verbose
    if print_it:
        pre = "cect      >>> "
        txt = msg.replace("\n", "\n" + pre) if msg is not None else msg
        print("%s %s" % (pre, txt))
