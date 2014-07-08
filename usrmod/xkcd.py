import random, re
import json, os

def portrait(phenny, input):
   phenny.say('http://i222.photobucket.com/albums/dd54/Prime32_temp/OotS/eiko_sudou_0044300x300_zps1dbbd5ed.png')
portrait.name = 'portrait'
portrait.commands = ['portrait','eiko']
portrait.priority = 'low'

with open(os.path.expanduser('~/eiko/usrmod/dhcrit.json')) as f:
    crits = json.load(f)

def dhcrit(phenny, input):
    text = input.groups()[1]
    choiceset = [0,0,0]
    typemap = {"X":"explosive", "I":"impact", "E":"energy", "R":"rending"}
    if not text:
        crittype = random.choice(crits.keys())
        critloc = random.choice(crits[crittype].keys())
        critnum = random.choice(crits[crittype][critloc])
        phenny.reply(critnum)
        return
    text = text.split()
    for opt in text:
        if opt.upper() in typemap:
            opt = typemap[opt.upper()]
        if opt.lower() in crits:
            crittype = opt.lower()
            break
    else:
        crittype = random.choice(crits.keys())
    for opt in text:
        if opt.lower() in crits[crittype]:
            critloc = opt.lower()
            break
    else:
        critloc = random.choice(crits[crittype].keys())
    for opt in text:
        try:
            opt = int(opt)
            if opt > 0 and opt <= 10:
                critnum = crits[crittype][critloc][opt-1]
                break
        except ValueError:
            pass
    else:
        critnum = random.choice(crits[crittype][critloc])
    phenny.reply(critnum)
dhcrit.name = 'dhcrit'
dhcrit.commands = ['dhcrit','dhc']
dhcrit.priority = 'low'

def sandgen(n=1):
	such = random.choice([random.sample((' a beautiful',' a delicious',' an elegant',' a fantastic',
       ' a mesmerizing',' an enchanting',' an amazing',' a fabulous',' a deadly',
       ' an adventurous',' an ambitious',' a brave',' a creative',' a discreet',
       ' an exuberant',' a faithful',' a friendly',' a gentle',' a damn good',
       ' an imaginative',' an intellectual',' a loving',' a loyal',' a modest',
       ' a neat',' an optimistic',' a jovial',' a kick-ass',' a healthy',' a passionate',
       ' a pioneering',' a plucky',' a philosophical',' a quirky',' a reliable',
       ' a sincere',' a thoughtful',' a terrific',' an understated',' a vivacious',
       ' a wonderful',' a xenophilic',' a youthful',' a zany'),n) for i in range(6)])
	topping = random.choice([random.sample(('avocado','lettuce','tomato','mozzarella cheese','bacon',
       'spam','peanut butter','bratwurst','cruelty-free PETA-approved fake guinea-pig',
       'digital','cucumber','tofu','-if slightly burnt-','recursive','banana','ice-cream',
       'ham&jam','tuna','double cheese','olive','..erm.. just','self-made','generic','sand',
       'witch','two-hander'),n) for i in range(6)])
	ret = [such[i]+' '+topping[i] for i in range(n)]
	if n == 1:
		return ret[0]
	return ret

def sandwich(phenny, input):
  if 'sudo' in input.group().lower():
    phenny.say('Certainly. *bows*')
    if re.match(input.nick,'(?i).milo.*'):
       foo = ' a taco-like'
    else:
       foo = sandgen()
    phenny.msg(input.sender, chr(1)+'ACTION makes '+input.nick+foo+' sandwich'+chr(1))
  else:
    phenny.say('I will not.  Make it yourself.')
sandwich.name = 'sandwich'
sandwich.rule = (r'(?i)(EI_0044|ei(ko)?(-(ch|t)an)?).? (sudo )?make me a sandwich')
#sandwich.rule = ('$nick', r'(sudo )?make me a sandwich')
sandwich.priority = 'low'
