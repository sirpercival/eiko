#!/usr/bin/env python
"""
quote.py - phenny Quote Module
Copyright 2008-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * phenny: https://github.com/myano/phenny/
 * Phenny: http://inamidst.com/phenny/
"""

import random
from modules import unicode as uc


def addquote(phenny, input):
    '''.addquote <nick> something they said here -- adds the quote to the quote database.'''
    text = input.group(2)
    if not text:
        return phenny.say('No quote provided')
    fn = open('quotes.txt', 'a')
    output = uc.encode(text)
    fn.write(output)
    fn.write('\n')
    fn.close()
    phenny.reply('Quote added.')
addquote.commands = ['addquote']
addquote.priority = 'low'
addquote.example = '.addquote'


def retrievequote(phenny, input):
    '''.quote <number> -- displays a given quote'''
    text = input.group(2)
    try:
        fn = open('quotes.txt', 'r')
    except:
        return phenny.reply('Please add a quote first.')

    lines = fn.readlines()
    MAX = len(lines)
    fn.close()
    random.seed()
    try:
        number = int(text)
        if number < 0:
            number = MAX - abs(number) + 1
    except:
        number = random.randint(1, MAX)
    if not (0 <= number <= MAX):
        phenny.reply("I'm not sure which quote you would like to see.")
    else:
        line = lines[number - 1]
        phenny.reply('Quote %s of %s: ' % (number, MAX) + line)
retrievequote.commands = ['quote']
retrievequote.priority = 'low'
retrievequote.example = '.quote'


def delquote(phenny, input):
    '''.rmquote <number> -- removes a given quote from the database. Can only be done by the owner of the bot.'''
    if not input.owner: return
    text = input.group(2)
    number = int()
    try:
        fn = open('quotes.txt', 'r')
    except:
        return phenny.reply('No quotes to delete.')
    lines = fn.readlines()
    MAX = len(lines)
    fn.close()
    try:
        number = int(text)
    except:
        phenny.reply('Please enter the quote number you would like to delete.')
        return
    newlines = lines[:number-1] + lines[number:]
    fn = open('quotes.txt', 'w')
    for line in newlines:
        txt = uc.decode(line)
        if txt:
            fn.write(txt)
            if txt[-1] != '\n':
                fn.write('\n')
    fn.close()
    phenny.reply('Successfully deleted quote %s.' % (number))
delquote.commands = ['rmquote', 'delquote']
delquote.priority = 'low'
delquote.example = '.rmquote'


if __name__ == '__main__':
    print __doc__.strip()
