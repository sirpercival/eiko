#!/usr/bin/env python
"""
logger.py - Esteban Feldman
based on logger.py - Phenny Room Logging Module
Author: Peter Higgins (dante@dojotoolkit.org)
About: http://higginsforpresident.net
License: AFL | New BSD
"""
from datetime import datetime
import logging
import logging.handlers

import os

logger = None

def get_logger(filename):
    global logger
    if logger:
        return logger
    my_logger = logging.getLogger('ircbot')
    my_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    #Add the log message handler to the logger
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=filename,
        when='W5', # caturday
    )
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    logger = my_logger
    return logger


def get_file(phenny, chan):
    return phenny.nick + "-" + phenny.config.host + "-" + chan + ".log"


def setup(self):

# if we don't explicitly list channels to log, log them all:
    if not hasattr(self.config, "logchannels"):
        self.config.logchannels = self.config.channels

    # make the logdir path if not there
    logdir = self.config.logdir
    if logdir and os.path.exists(logdir):
        self.logdir = logdir
    else:
        self.logdir = os.path.join(os.path.expanduser('~/.phenny/'), 'logs');
    if not os.path.exists(self.logdir):
        os.mkdir(self.logdir)


def log_message(phenny, teller, chan, msg):
    # only log the channels we care about
    if chan in phenny.config.logchannels:
        line = "\t".join((chan, teller, msg))
        logger = get_logger(os.path.join(phenny.logdir, get_file(phenny, chan)))
        logger.info(line)


def loggit(phenny, input):
    msg = input.group(1).encode('utf-8')
    log_message(phenny, input.nick, input.sender, msg)

loggit.rule = r'(.*)'
loggit.priority = 'high'
loggit.thread = False

if __name__ == '__main__':
    print __doc__.strip()