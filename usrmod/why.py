#!/usr/bin/env python
"""
why.py - phenny Why Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * phenny: https://github.com/myano/phenny/
 * Phenny: http://inamidst.com/phenny/
"""

import re
import web
import json
import random

def get_from_thesaurus(word):
    thesaurus = 'http://words.bighugelabs.com/api/2/a72dc8568568d8d9204b415f846b264a/%s/json'
    aa = web.get(thesaurus % word)
    try:
        syns = json.loads(aa)
    except:
        return []
    res = []
    for i in syns.keys():
        res.append(syns[i].get(u"syn",[]))
    try:
        out = sum(res,[])
    except:
        out = []
    return out
     
def getsyn(phenny,input):
    text = input.groups()
    syn = get_from_thesaurus(text[1])
    if not syn:
        phenny.reply('Sorry, couldn\'t find "'+text[1]+'" in the thesaurus.')
        return
    res = ', '.join(syn)
    phenny.reply(text[1]+' - '+res)
getsyn.name = 'getsyn'
getsyn.commands = ['thesaurus','synonyms','syn']
getsyn.priority = 'low'

shibe = ('such ','so ','very ','much ','','yes ')

def doge(phenny,input):
    text = input.groups()
    if not text[1]:
        phenny.reply('  no word       such fail             wow               bad say')
        return
    syn = get_from_thesaurus(text[1])
    if not syn:
        phenny.reply('  no word       such fail             wow               bad say')
        return
    syn = [(x.split())[0] for x in syn]
    syn = set(syn)
    n = min([random.randint(3,6), len(syn)])
    dog = random.sample(shibe,n)
    ss = random.sample(syn,n)
    out = []
    wow = 0
    for i in range(0,n):
        sp = [' ' for j in range(0,random.randint(5,20))]
        if not wow and random.randint(0,1):
            out.append(''.join(sp)+'wow')
            wow = 1
            i = i - 1
        else:
            out.append(''.join(sp)+dog[i]+ss[i])
    phenny.reply(' '.join(out))
doge.name = 'doge'
doge.commands = ['doge','shibe']
doge.priority = 'low'


whyuri = 'http://www.leonatkinson.com/random/index.php/rest.html?method=advice'
r_paragraph = re.compile(r'<quote>.*?</quote>')


def getwhy(phenny, input):
    page = web.get(whyuri)
    paragraphs = r_paragraph.findall(page)
    line = re.sub(r'<[^>]*?>', '', unicode(paragraphs[0]))
    phenny.say(line.lower().capitalize() + ".")
getwhy.commands = ['why', 'tubbs']
getwhy.thread = False
getwhy.rate = 30

if __name__ == '__main__':
    print __doc__.strip()