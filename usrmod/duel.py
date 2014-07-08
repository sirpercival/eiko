import random
import re, shelve
from scores import *
#from sentience import *

def duel(phenny, input):
   #if sentient.get(input.sender,False): return
   if 'reload duel' in input.group():
      return
   if 'moirai' in input.nick.lower():
      phenny.say('!botsmack')
      return
   target = input.nick
   namesdb = shelve.open(phenny.logdir+'/nicks')
   if input.sender in namesdb:
      nicks = namesdb[input.sender]
      for i in input.split():
         for n in nicks:
            if n != phenny.nick and i.lower() == n.lower():
                target = n
                break
   namesdb.close()
   wpn1 = ('witchcraft','BEEEEES','pistols','blades','magic','psychic powers','fists','rocks','staff',
      'spears','gnomes','beauty','love','whispers','menacing looks','armies','chutes & ladders',
      'monopoly','yahtzee','logic','philosophy','rubber chickens','farm animals','mathematics',
      'science','words','damnation','opera','tic-tac-toe','global thermonuclear war','a nice game of chess',
      'social media','rap music','axes')
   wpn2 = ('a newt','one trillion bees','a glock 9mm','a claymore','a grimoire','her brain','her fist','a rock',
      'a human resources department','a spear','a baby gnome','Photoshop','a box of chocolates',
      'a whisper','a pointed glance','a Major General','a GOD DAMN LADDER','free parking',
      'five dice','an axiom','Jean-Paul Sartre','a rubber chicken','a sheep','a slide-rule',
      'a bunsen burner','a dictionary','the Twilight series','Richard Wagner in a viking costume',
      'her pencil in frustration after the 671st straight tie','WOPR','Matthew Broderick',
      'the decayed carcass of Friendster','A Tribe Called Quest','a Fender Stratocaster')
   sad = random.random()
   scor = user_scores.getscore(phenny,input.nick.lower(),input.sender.lower())
   if scor < 0:
      cut = float(1 - scor)/float(2 - 3 * scor)
   else:
      cut = float(1 + 2 * scor)/float(2 + 3 * scor)
   if sad < cut:
      rmr = ' no '
   else: rmr = '... '
   if re.match(input.nick,'.milo.*'):
      ind = 0
   if re.match(input.nick,'.sirpercival.*'):
      ind = random.randint(27,len(wpn1))
   elif 'gramarie' in input.group().lower():
      ind = random.choice([random.randint(0,14) for i in range(0,6)])
      g0 = ('Alchemetry','Kaleidomantics','Arcanodynamics','Biollurgy','Eldrikinetics',
         'Geoccultism','Heuristicism','Imachination','Yggdratecture','Divinentropy',
         'Travelemetry','Psychomantics','Puissamantics','Constructivity','Reliquadratics')[ind]
      g1 = ('incinerates ','eviscerates ','dissolves ','converts ','fires ','traps ','forces ',
         'traps ','splinches ','puts ','detonates a Gateway in ','drowns ','asplodes ','feeds ',
         'Benjamin-Buttons ')[ind]
      g2 = (' with a healthy dose of phlogiston',' with a violet filter sword',' with a tin out',
         ' into inert biostructure',' into space with a ballistic engine',' in a frozen cave filled with deadsnow zombies',
         ' to share senses with Cthulhu',' in a never-ending dreamscape',' with an entangled flux pair',
         ' in stasis with a stone rod','\'s face',' in self-loathing',' with a current of pulsants',
         ' to a hungry heart',' with an Inverted vessel')[ind]
      phenny.say('Certainly. It is my choice of discipline. I choose... '+g0+'!')
      phenny.msg(input.sender, chr(1)+'ACTION smirks, throwing back her cape, then '+g1+target+g2+', and feels'+rmr+'remorse.'+chr(1))
      if sad > cut:
         phenny.msg(input.sender, chr(1)+'ACTION quickly revives '+target+' while no one is looking.'+chr(1))
         user_scores.edpoints(phenny, target.lower(), input.sender.lower(), True)
      else:
         user_scores.edpoints(phenny, target.lower(), input.sender.lower(), False)
      return
   else:
      ind = random.choice([random.randrange(0,len(wpn1)) for i in range(0,6)])
   phenny.say('Certainly. It is my choice of weapon. I choose... '+wpn1[ind]+'!')
   phenny.msg(input.sender, chr(1)+'ACTION smirks, throwing back her cape, then stabs '+target+' through the heart with '+wpn2[ind]+', and feels'+rmr+'remorse.'+chr(1))
   if sad > cut:
      phenny.msg(input.sender, chr(1)+'ACTION quickly revives '+target+' while no one is looking.'+chr(1))
      user_scores.edpoints(phenny, target.lower(), input.sender.lower(), True)
   else:
      user_scores.edpoints(phenny, target.lower(), input.sender.lower(), False)
duel.name = 'duel'
duel.rule = (r'(?i)ei(ko|_0044)?(-(ch|t)an)?.*duel.*')
duel.priority = 'low'


