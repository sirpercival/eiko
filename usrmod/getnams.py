import re, json, time
from random import choice

def getnams(phenny, input):
    phenny.write(['NAMES'], input.sender)
    try:
        with open(phenny.logdir+'/nicks.json') as f:
            namesdb = json.load(f)
        names = namesdb.get(input.sender,None)
    except:
        names = []
    if not names:
        phenny.say("Nobody's here!")
        return
    #names.remove('$nick')
    phenny.msg(input.nick, "Guess who's in "+input.sender+": "+", ".join(names))
getnams.name = 'getnames'
getnams.commands = ['getnames']
getnams.priority = 'low'

def oinkbane(phenny, input):
    target = input.groups()[1]
    if not target:
        target = input.nick
    phenny.msg('OINKBANE', '.subtlety '+input.sender+' '+target)
oinkbane.name = 'oinkbane'
oinkbane.commands = ['subtle','oink','toosubtle']
oinkbane.priority = 'high' 

def subtlety(phenny, input):
    if not input.admin or input.sender.startswith('#'):
        return
    if phenny.nick != 'OINKBANE':
        return
    text = input.groups()[1]
    if not text or not text.startswith('#'):
        return
    text = text.split()
    chan = text[0]
    target = ' '.join(text[1:]) if len(text) > 1 else ''
    phenny.write(['JOIN'], chan)
    msg = choice(['MY TACTICS ARE TOO SUBTLE FOR YOU','SNEEEEEEEAK ATTAAAAAACK'])
    act = choice(['crashes through the wall','hurtles through the window','plummets out of the ventilation shaft'])
    phenny.msg(chan, chr(1)+'ACTION '+act+chr(1))
    phenny.msg(chan, msg)
    if target:
        phenny.msg(chan, chr(1)+'ACTION smashes '+target+'.'+chr(1))
    time.sleep(0.3)
    phenny.write(['PART'], chan)
subtlety.name = 'subtlety'
subtlety.commands = ['subtlety']
subtlety.priority = 'low'

def testnames(phenny, input):
    with open(phenny.logdir+'/nicks.json') as f:
        namesdb = json.load(f)
    names = namesdb.get(input.sender,None)
    if not names:
        phenny.say("Nobody's here!")
        return
    #names.remove('$nick')
    phenny.msg(input.nick, "Guess who's in "+input.sender+": "+", ".join(names))
testnames.name = 'testtnames'
testnames.commands = ['testnames']
testnames.priority = 'low'

def nametrigger(phenny, input):
    names = re.split(' ', input)
    names = [n.split('!')[0] for n in names]
    names = [n.replace('~','') for n in names]
    names = [n.replace('@','') for n in names]
    try:
        with open(phenny.logdir+'/nicks.json') as f:
            namesdb = json.load(f)
    except:
        namesdb = {}
    namesdb[input.args[2]] = names
    with open(phenny.logdir+'/nicks.json','w') as f:
        json.dump(namesdb,f)
nametrigger.event = '353'
nametrigger.rule = '(.*)'
nametrigger.priority = 'high'

def name_onjoin(phenny, input):
    phenny.write(['NAMES'], input)
name_onjoin.event = 'JOIN'
name_onjoin.rule = '(.*)'
name_onjoin.priority = 'high'

def name_onnick(phenny, input):
    phenny.write(['NAMES'], input)
name_onnick.event = 'NICK'
name_onnick.rule = '(.*)'
name_onnick.priority = 'high'

def name_onpart(phenny, input):
    phenny.write(['NAMES'], input)
name_onpart.event = 'PART'
name_onpart.rule = '(.*)'
name_onpart.priority = 'high'