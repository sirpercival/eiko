import random
import re
import xmlrpclib
import math

srace = {'human':[0,0,0,0,0,0],
  'half-elf':[0,0,0,0,0,0],
  'elf':[0,2,-2,0,0,0],
  'dwarf':[0,0,2,0,0,-2],
  'gnome':[-2,0,2,0,0,0],
  'halfling':[-2,2,0,0,0,0],
  'half-orc':[2,0,0,-2,0,-2]}
scord = {'bard':[5,1,2,3,4,0],
  'barbarian':[0,2,1,5,3,4],
  'cleric':[3,4,2,5,0,1],
  'druid':[5,4,1,2,0,3],
  'fighter':[0,2,1,5,4,3],
  'monk':[0,3,2,4,1,5],
  'paladin':[0,4,2,5,1,3],
  'ranger':[0,2,1,4,3,5],
  'rogue':[4,0,2,1,5,3],
  'sorcerer':[5,2,1,4,3,0],
  'wizard':[5,2,1,0,3,4]}
sfeat = {'bard':'Weapon Finesse',
  'barbarian':'Power Attack',
  'cleric':'Extend Spell',
  'druid':'Summon Elemental',
  'fighter':'Power Attack',
  'monk':'Combat Reflexes',
  'paladin':'Power Attack',
  'ranger':'Combat Reflexes',
  'rogue':'Weapon Finesse',
  'sorcerer':'Penumbra Bloodline',
  'wizard':'Spell Focus (Illusion)'}
ship = {'bard':6, 'barbarian':12, 'cleric':8, 'druid':8,
  'fighter':10, 'monk':8, 'paladin':10, 'ranger':8, 'rogue':6,
  'sorcerer':4, 'wizard':4}
ssta = {0:'Str',1:'Dex',2:'Con',3:'Int',4:'Wis',5:'Cha'}


def rs():
  stats = [0,0,0,0,0,0]
  for i in range(0,6):
    rol = sorted([random.choice([random.randint(1,6) for j in range(0,6)]) for k in range(0,4)])
    stats[i] = sum(rol[1:])
  return stats
  
def rollstats(phenny, input):
  initstats = rs()
  stats = ['','','','','','']
  pbd = {9:1,10:2,11:3,12:4,13:5,14:6,15:8,16:10,17:13,18:16}
  pb = 0
  for i,j in enumerate(initstats): 
    pb += pbd.get(j,0)
    stats[i] = str(j)
  phenny.reply('Str '+stats[0]+' Dex '+stats[1]+' Con '+stats[2]+' Int '+stats[3]+' Wis '+stats[4]+' Cha '+stats[5]+' ('+str(pb)+'pb)')
rollstats.name = 'rollstats'
rollstats.commands = ['rollstats','rs']
rollstats.priority = 'low'
  
def chargen(phenny,input):
  text = input.group().split()
  ranr = 1
  ranc = 1
  if len(text) < 2 or text[1].startswith('#'):
    tmp = 0
  else:
    if text[1] == 'help':
      phenny.say('syntax: .chargen/.cg [race] [class]. If you don\'t give me a valid race and/or class (including leaving them blank), I\'ll generate it or them randomly. Only PHB races and classes supported currently. Class ability priorities and feat selections as decided by sirpercival in the spur of the moment.')
      return
    for i in text[1:]:
      p1 = i.lower()
      if p1 in srace.keys() and ranr == 1:
        ranr = 0
        race = p1
      if p1 in scord.keys() and ranc == 1:
        ranc = 0
        clas = p1
  if ranr == 1: race = random.choice([random.choice(srace.keys()) for i in range(0,6)])
  if ranc == 1: clas = random.choice([random.choice(scord.keys()) for i in range(0,6)])
  initstat = sorted(rs(), reverse=True)
  stats = ['','','','','','']
  radj = srace.get(race)
  cord = scord.get(clas)
  feat = sfeat.get(clas)
  if race == 'human': 
    feat += ' and Improved Initiative feats.'
  else:
    feat += ' feat.'
  ist = []
  for i,j in enumerate(cord):
    ist.append(initstat[j])
  for i in range(0,6):
    stats[i] = str(ist[i] + radj[i])
  cmod = math.floor((int(stats[2])-10.)/2.)
  hp = str(ship.get(clas) + int(cmod))
  proxy = xmlrpclib.ServerProxy("http://dicelog.com/yaf/rpc")
  nam = proxy.names(5,12,2).replace('\n',' ')
  phenny.reply(nam+' is a 1st-level '+race+' '+clas+' with '+hp+' hit points and the '+feat+' Str '+stats[0]+' Dex '+stats[1]+' Con '+stats[2]+' Int '+stats[3]+' Wis '+stats[4]+' Cha '+stats[5])
chargen.name = 'chargen'
chargen.commands = ['chargen','cg']
chargen.priority = 'low'