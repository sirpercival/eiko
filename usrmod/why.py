#!/usr/bin/env python
"""
why.py - phenny Why Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * phenny: https://github.com/myano/phenny/
 * Phenny: http://inamidst.com/phenny/
"""

import re, os, web, shelve
import json, random

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

with open(os.path.expanduser('~/phenny/usrmod/wonder.json')) as f:
    wonder = json.load(f)

def rodofwonder(phenny, input):
    namesdb = shelve.open(phenny.logdir+'/nicks')
    if input.sender in namesdb:
        nicks = namesdb[input.sender]
    else:
        phenny.say("Nick db error")
        phenny.write(['NAMES'], input.sender)
        namesdb.close()
        return
    namesdb.close
    if phenny.nick in nicks:
        nicks.remove(phenny.nick)
    if "IronHeart" in nicks:
        nicks.remove("IronHeart")
    target = input.groups()[1]
    if not target:
        target = random.choice(nicks)
#    for n in nicks:
#        print target, n, re.match(r'.*'+target.lower()+'.*', r'.*'+n.lower()+'.*')
#        if re.match(r'.*'+target.lower()+'.*', n.lower()):
#            target = n
#            break
#    else:
#        target = random.choice(nicks)
    effect = random.choice(wonder['effect'])
    effect = effect.replace('%(user)', str(input.nick))
    effect = effect.replace('%(target)', str(target.strip()))
    effect = effect.replace('%(plane)', random.choice(wonder['plane']))
    effect = effect.replace('%(summonix)', random.choice(wonder['summonix']))
    effect = effect.replace('%(summonviii)', random.choice(wonder['summonviii']))
    effect = effect.replace('%(summonii)', random.choice(wonder['summonii']))
    effect = effect.replace('%(color)', random.choice(wonder['color']))
    effect = effect.replace('%(polymorph)', random.choice(wonder['polymorph']))
    effect = effect.replace('%(heavy)', random.choice(wonder['heavy']))
    phenny.say(effect)
rodofwonder.name = 'wonder'
rodofwonder.commands = ['wonder']
rodofwonder.priority = 'low'

with open(os.path.expanduser('~/phenny/usrmod/surge.json')) as f:
    surge = json.load(f)

def wsurge(phenny, input):
    phenny.reply(random.choice(surge))
wsurge.name = 'wildsurge'
wsurge.commands = ['wildsurge','surge']
wsurge.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
