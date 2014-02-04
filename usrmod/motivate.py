#!/usr/bin/env python
'''
motivate.py - motivate Module
Copyright 2013 Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * phenny: https://github.com/myano/phenny/
 * Phenny: http://inamidst.com/phenny/
'''

import random, HTMLParser, json
import re, urllib, urllib2, shelve
h = HTMLParser.HTMLParser()

motiv = ("You're doing good work",
	"You're top-notch",
    "You're really rocking those corduroy pants",
    "You're looking quite lovely today",
    "You're just good people",
    "You're not half bad",
    "You're a real go-getter",
    "You're a nice person",
    "You're one of the best fish in the sea",
    "You're big pimpin', spendin G's",
    "8 out of 10 co-workers agree that your desk is the cleanest",
    "9 out of 10 dentists agree, you are the BEST",
    "All the 6th graders agreed, your baking soda volcano was the best at the science fair",
    "All your friends worry they aren't as funny as you",
    "Every other country is super jealous you're a citizen in this country",
    "Everyone was cool with that time you peed in the shower",
    "Everyone was super jealous of your SAT score",
    "Hey, not that you needed to, but it looks like you lost weight",
    "I want to kiss you. I hope that's not too forward of me",
    "I would totally trust you to dog-sit for a long weekend",
    "I'm not telling you what to do, but you could pull off orange corduroy",
    "Keep walking around naked. Your neighbors are into it",
    "Mensa would be so lucky",
    "No one has ever thought your feet look gross",
    "People at trivia night are terrified of you",
    "Rumor is Disney is basing its next cartoon on you",
    "That song was definitely written for you",
    "The kid you passed on the street today wants to grow up to be like you",
    "They've never told you this, but your boss is really impressed by you",
    "Those shoes were a great call",
    "Today's outfit = Thumbs up",
    "You actually looked super graceful that time you tripped in front of everyone",
    "You are the most charming person in a 50 mile vicinity",
    "NASA told me you could be an astronaut if you wanted",
    "You don't get drunk, you get superhuman",
    "You have the power to start and WIN a dance-off",
    "You pick the best radio stations when you're riding shotgun",
    "You think of the funniest names for wi-fi connections",
    "You'd be the last one standing in a horror movie",
    "You're a benevolent tipper",
    "You're as sweet as a can of artificially flavored diet soda",
    "You're funny, like, LOL style",
    "You're not crazy, they are 100% into you",
    "You're the best at making cereal",
    "You've never had morning breath. I swear",
    "Your blog is the best blog",
    "Your boss loved that thing you did at work today",
    "Your cousins refer to you as \"the cool cousin\"",
    "Your dental hygiene is impeccable",
    "Your hair looks great today, and also looked really good two days ago",
    "Your hair smells like freshly cut grass",
    "Your parents are more proud of you than you'll ever know",
    "Your parents aren't worried about you",
    "Your pet loves you too much to ever run away",
    "Your prom date still thinks about you all the time",
    "Your senior portrait was the best",
    "Your sneezes sound like a chorus of angels giggling",
    "Your voice sounds like a thousand cats purring")
ins1 = ('n artless',' bawdy',' beslubbering',' bootless',' churlish',' cockered',' clouted',' craven',' currish',' dankish',
    ' dissembling' ,' droning' ,'n errant' ,' fawning' ,' fobbing' ,' froward' ,' frothy' ,' gleeking' ,' goatish' ,' gorbellied' ,
    'n impertinent' ,'n infectious' ,' jarring' ,' loggerheaded' ,' lumpish' ,' mammering' ,' mangled' ,' mewling' ,' paunchy' ,
    ' pribbling' ,' puking' ,' puny' ,' qualling' ,' rank' ,' reeky' ,' roguish' ,' ruttish' ,' saucy' ,' spleeny' ,' spongy' ,' surly' ,
    ' tottering' ,'n unmuzzled' ,' vain' ,' venomed' ,' villainous' ,' warped' ,' wayward' ,' weedy' ,' yeasty' ,' cullionly' ,' fusty' ,
    ' caluminous' ,' wimpled' ,' burly-boned' ,' misbegotten' ,'n odiferous' ,' poisonous' ,' fishified' ,' wart-necked' )
ins2 = ('base-court','bat-fowling','beef-witted','beetle-headed','boil-brained','clapper-clawed','clay-brained',
    'common-kissing','crook-pated','dismal-dreaming','dizzy-eyed','doghearted','dread-bolted','earth-vexing',
    'elf-skinned','fat-kidneyed','fen-sucked','flap-mouthed','fly-bitten','folly-fallen','fool-born','full-gorged',
    'guts-griping','half-faced','hasty-witted','hedge-born','hell-hated','idle-headed','ill-breeding','ill-nurtured',
    'knotty-pated','milk-livered','motley-minded','onion-eyed','plume-plucked','pottle-deep','pox-marked','reeling-ripe',
    'rough-hewn','rude-growing','rump-fed','shard-borne','sheep-biting','spur-galled','swag-bellied','tardy-gaited',
    'tickle-brained','toad-spotted','unchin-snouted','weather-bitten','whoreson','malmsey-nosed','rampallian','lily-livered',
    'scurvy-valiant','brazen-faced','unwash\'d','bunch-back\'d','leaden-footed','muddy-mettled','pigeon-liver\'d','scale-sided')
ins3 = ('apple-john','baggage','barnacle','bladder','boar-pig','bugbear','bum-bailey','canker-blossom','clack-dish','clotpole',
    'coxcomb','codpiece','death-token','dewberry','flap-dragon','flax-wench','flirt-gill','foot-licker','fustilarian','giglet',
    'gudgeon','haggard','harpy','hedge-pig','horn-beast','hugger-mugger','joithead','lewdster','lout','maggot-pie','malt-worm',
    'mammet','measle','minnow','miscreant','moldwarp','mumble-news','nut-hook','pigeon-egg','pignut','puttock','pumpion','ratsbane',
    'scut','skainsmate','strumpet','varlot','vassal','whey-face','wagtail','knave','blind-worm','popinjay','scullian','jolt-head',
    'malcontent','devil-monk','toad','rascal','Basket-Cockle')
    
def motivate(phenny, input):
    '''!m -- motivate somebody!'''
    if input.groups()[1]:
        nick = input.groups()[1].strip()
    else:
        nickdb = shelve.open(phenny.logdir+'/nicks')
        nicks = nickdb[input.sender]
        nickdb.close()
        nicks.remove(phenny.nick)
        if "IronHeart" in nicks:
            nicks.remove("IronHeart")
        nick = random.choice(nicks)
    #coinflip: compliment, or CHUCK?
    if random.randint(0,1):
        try:
            r = urllib2.urlopen('http://api.icndb.com/jokes/random').read()
        except:
            mot = random.choice([random.choice(motiv) for i in range(0,6)])
            phenny.say(mot+", %s!" % (nick))
        data = json.loads(r)
        text = h.unescape(data['value']['joke'])
        if text.startswith("#"):
            text = text.replace("#")
        text = text.replace("Chuck Norris's", nick+"'s")
        text = text.replace("Chuck Norris'", nick+"'s")
        text = text.replace("Chuck Norris", nick)
        text = text.replace("Chuck", nick.replace(" ","-"))
        phenny.say(text)
    else:
        mot = random.choice([random.choice(motiv) for i in range(0,6)])
        phenny.say(mot+", %s!" % (nick))
motivate.commands = ['motivate','m']

def insult(phenny, input):
    '''!i -- insult somebody!'''
    if input.groups()[1]:
        nick = input.groups()[1].strip()
    else:
        nickdb = shelve.open(phenny.logdir+'/nicks')
        nicks = nickdb[input.sender]
        nickdb.close()
        nicks.remove(phenny.nick)
        if "IronHeart" in nicks:
            nicks.remove("IronHeart")
        nick = random.choice(nicks) 
    i1 = random.choice([random.choice(ins1) for i in range(0,6)])
    i2 = random.choice([random.choice(ins2) for i in range(0,6)])
    i3 = random.choice([random.choice(ins3) for i in range(0,6)])
    phenny.say(nick+', thou art a'+i1+' '+i2+' '+i3+'!')
insult.commands = ['insult','i']

if __name__ == '__main__':
    print __doc__.strip()
