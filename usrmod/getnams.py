import re, shelve

def getnams(phenny, input):
    phenny.write(['NAMES'], input.sender)
    namesdb = shelve.open(phenny.logdir+'/nicks')
    names = namesdb.get(input.sender,None)
    if not names:
        phenny.say("Nobody's here!")
        return
    #names.remove('$nick')
    phenny.msg(input.nick, "Guess who's in "+input.sender+": "+", ".join(names))
getnams.name = 'getnames'
getnams.commands = ['getnames']
getnams.priority = 'low'

def testnames(phenny, input):
    namesdb = shelve.open(phenny.logdir+'/nicks')
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
    namesdb = shelve.open(phenny.logdir+'/nicks')
    namesdb[input.args[2]] = names
    namesdb.close()
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