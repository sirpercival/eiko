#!/usr/bin/env python

import cleverbot
import json
import random
import re
import time
import web, shelve, os

mycb = cleverbot.Session()

nowords = ('reload', 'help', 'tell', 'ask', 'duel','make me a sandwich')

sentient = {'#Gramarie':True,'#mmxgeneral':True, '#Legend':True, '#giantitp':True, '#homestuck':True}
dialect = {'#Gramarie':'none', '#mmxgeneral':'fudd', '#homestuck':'none'}

def make_dialect(which, text):
    t = text
    dialects = shelve.open(os.path.expanduser('~/eiko/usrmod/dialects'))
    opt = which.lower()
    if 'chef' in opt or 'swedish' in opt:
        subs = dialects['chef']
    elif 'olde' in opt:
        subs = dialects['olde']
    elif 'fudd' in opt:
        subs = dialects['fudd']
    else:
        return text
    for frompat, topat in subs:
        t = re.sub(frompat, topat, t)
    return t

def sentience(phenny, input): 
   global sentient
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   channel = input.group(2)
   if (not channel): return
   if input.admin:
       if sentient.get(channel,False):
           sentient[channel] = False
       else:
           sentient[channel] = True
       phenny.reply("Sentience " + ("OFF","ON")[sentient.get(channel)]+" in channel "+channel)
       print("Sentience " + ("OFF","ON")[sentient.get(channel)]+" in channel "+channel)
sentience.commands = ['sentience']
sentience.priority = 'low'

def sent_dialect(phenny, input):
   global dialect
   if input.sender.startswith('#'): return
   channel, d = input.group(2).split(' ')
   if (not channel): return
   if input.admin:
       if dialect.get(channel,False):
           dialect[channel] = d
       else:
           dialect[channel] = d
       phenny.reply("Dialect " + d + " in channel "+channel)
       print("Dialect " + d + " in channel "+channel)
sent_dialect.commands = ['sentdialect']
sent_dialect.priority = 'low'

def chat(phenny, input):
    if input.groups()[5].lower() == 'are you sentient?':
       if sentient.get(input.sender,False):
           phenny.reply('Yes!')
       else:
           phenny.reply('Nope.')
       return
    if sentient.get(input.sender,False):
       txt = input.groups()
       if len(txt) > 0:
           text = txt[1]
           try:
               if txt[1].startswith('\x03') or txt[1].startswith('\x01'):
                   ## block out /ctcp
                   return
           except:
               return
       else:
           print time.time(), 'Something went wrong with chat.py'
           return
   
       if not text:
           return
       channel = input.sender
       for x in nowords:
           if x in input.groups()[5].lower():
               return
       #msgi = txt.strip()
       msgi = re.sub('(?i)(EI_0044|Ei(ko)?(-(ch|t)an)?)', 'Cleverbot', input.group().strip())
       msgo = str()
       if channel.startswith('#') and txt[0]:
           ## in a channel and prepended with phenny's name
           pm = False
           try:
               msgo = mycb.Ask(msgi)
           except:
               return
       elif not channel.startswith('#'):
           ## in a PM and not prepended with phenny's name
           pm = True
           if text.startswith('.'):
               return
           #elif text.startswith(phenny.config.nick + ':'):
           elif re.match('(?i)((EI_0044|Ei(ko)?(-(ch|t)an)?):', text):
               spt = txt.split(':')[1].strip()
               for x in nowords:
                   if spt.lower().startswith(x):
                       return
           try:
               msgo = mycb.Ask(msgi)
           except:
               return
       else:
           return
       if msgo:
           rand_num = random.randint(0, 20)
           #time.sleep(5 + rand_num)
           response = re.sub('(?i)cleverbot', 'Eiko', msgo)
           response = make_dialect(dialect.get(channel,''), response)
           if pm:
               phenny.say(response)
               beginning = ':%s PRIVMSG %s :' % (phenny.config.nick, input.sender)
               if hasattr(phenny.config, 'logchan_pm'):
                   phenny.msg(phenny.config.logchan_pm, beginning + response)
           else:
               delim = ':'
               msg = '%s%s %s' % (input.nick, delim, response)
               phenny.say(msg)
chat.rule = r'(?i)((EI_0044|Ei(ko)?(-(ch|t)an)?)[:,]?\s)?(.*)'

if __name__ == '__main__':
    print __doc__.strip()