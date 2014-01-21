import random

castro = ('Earth-like','Shorter Days/Nights','Longer Days/Nights','Dimmer Sun(s)',
   'Brighter Sun(s)','Farther Moon(s)','Nearer Moon(s)','Fewer Meteors','More Meteors',
   'Higher Cosmic Radiation','Lesser Cosmic Radiation','Higher Gravity','Lesser Gravity',
   'No Moons','Two or More Moons','Two or More Suns','Planar Cosmology','Creationist Cosmology',
   'Choose Two','Choose Three')
cgeog = ('Earth-like','Fully Aquatic','Mostly Aquatic','Fully Mountainous',
   'Mostly Mountainous','Fully Volcanic','Mostly Volcanic','Fully Forested',
   'Mostly Forested','Fully Arable','Mostly Arable','Fully Desert','Mostly Desert',
   'Fully Marshy','Mostly Marshy','Fully Artificial','Mostly Artificial',
   'Fully Gaseous','Choose Two','Choose Three')
cclim = ('Earth-like','Extremely Low Precipitation','Low Precipitation',
   'High Precipitation','Extremely High Precipitation','Extremely Low Temperature',
   'Low Temperature','High Temperature','Extremely High Temperature','Extremely Thin Atmosphere',
   'Thin Atmosphere','Dense Atmosphere','Extremely Dense Atmosphere','Extremely Low Pollution',
   'Low Pollution','High Pollution','Extremely High Pollution','Artifical Climate','Choose Two',
   'Choose Three')
cbio = ('Earth-like','Mostly Animals','Mostly Plants','Mostly Microbes','Mostly Artificial',
   'Mostly Aerial','Mostly Surface','Mostly Subsurface','One Predator','Multiple Predators',
   'One Prey','Multiple Prey','One Parasite','Multiple Parasites','One Pathogen',
   'Multiple Pathogens','One Symbiote','Multiple Symbiotes','Choose Two','Choose Three')
cnciv = ('One','One','Two','Two','Two','Two','Three','Three','Three','Three',
   'Three','Four','Four','Four','Four','Four','Five','Five','Five','Five')
caes = ('Mesopotamia','Egyptian Antiquity','Greco-Roman Classicism','Tribal Mesoamerica',
   'Tribal Scandinavia','Feudal Far East','European Middle Ages','Islamic Golden Age',
   'Italian Renaissance','Age of Exploration','Industrial Revolution','Early 20th Century',
   'Middle 20th Century','Late 20th Century','Present Day','Utopian Future','Dystopian Future',
   'Post-Apocalypse','Choose Two','Choose Three')
cdom = ('Humans','Elves/Tall Humanoids','Orcs/Strong Humanoids','Dwarves/Stout Humanoids',
   'Mamallian Beastmen','Avian Beastmen','Aquatic Beastmen','Reptilian Beastmen',
   'Insectoid Beastmen','Amorphous','Hive Minds','Divines','Infernals','Synthetics',
   'Humanoid Aliens','Non-Humanoid Aliens','Hybrid (Choose Two)','Two Hybrids (2 Pairs)',
   'Choose Two','Choose Three')
cval = ('Temperance','Prudence','Courage','Justice','Happiness','Redemption','Conquest',
   'Wealth','Tolerance','Knowledge','Innovation','Service','Mercy','Dignity','Industry',
   'Truth','Cooperation','Endurance','Choose Two','Choose Three')
cecon = ('Agriculture','Mining','Soldiers/Mercs','Weapons/Arms','Textiles/Clothing',
   'Construction','Academics','Finance','Entertainment','Machinery','Medicine',
   'Information','Transportation','Slavery','Tourism','Consumer Goods','Luxury Goods',
   'Illegal Goods','Choose Two','Choose Three')
cgov = ('Dictatorship','Monarchy','Theocracy','Oligarchy','Aristocracy','Mob Rule',
   'Corporate Rule','Transitional','Communism','Socialism','Democracy','Republic','Fascism',
   'Martial Law','Secret Cabal(s)','Meritocracy','Federalism','Imperial','Choose Two',
   'Choose Three')
cphil = ('Natural Monotheism','Cosmic Monotheism','Conceptual Monotheism','Natural Pantheism',
   'Cosmic Pantheism','Conceptual Pantheism','Native American Folk Religion',
   'Mesoamerican Folk Religion','African Folk Religion','Pagan Folk Religion',
   'Arabic Folk Religion','Indian Folk Religion','Far East Folk Religion',
   'Polynesian Folk Religion','Heaven/Hell','Reincarnation/Karma','Tolerant Atheism',
   'Militant Atheism','Choose Two','Choose Three')
cfeat = ('Festival','Language','Craft/Industry','Superstition','Guardian','Guardian',
   'Legend','Artifact','Advantage','Disadvantage','Hero/Heroine','Coming-of-Age Ritual',
   'Energy Source','Trade Partner','Invention','Wildlife','Previous Conflict','Disaster',
   'Choose Two','Choose Three')
csup = ('No Supernatural','No Supernatural','No Supernatural','No Supernatural',
   'Rare, Weak Supernatural','Rare, Weak Supernatural','Rare, Weak Supernatural',
   'Rare, Weak Supernatural','Rare, Strong Supernatural','Rare, Strong Supernatural',
   'Rare, Strong Supernatural','Rare, Strong Supernatural','Common, Weak Supernatural',
   'Common, Weak Supernatural','Common, Weak Supernatural','Common, Weak Supernatural',
   'Common, Strong Supernatural','Common, Strong Supernatural','Common, Strong Supernatural',
   'Common, Strong Supernatural')
cthem = ('Destined Heroes','Crime Investigation','Political Intrigue','Hunting Treasure',
   'Impending War','Search and Rescue','Search and Destroy','Discovery of Culture',
   'Discovery of Artifact','Discovery of Knowledge','Seeking Revenge','Seeking Enlightenment',
   'Travelling Merchants','Rebuilding Civilization','Preventing Disaster','Encouraging Disaster',
   'Visited by Strangers','Friendly Competition','Choose Two','Choose Three')
cstart = ('\"You all meet in a tavern...\"','\"You wake up in a jail cell.\"',
   '\"Let\'s go! There\'s no time!\"','\"Here, take this! Just do it!\"',
   '\"You have been cursed.\"','\"You come to in a dark place.\"',
   '\"You\'re here for the job.\"','\"You\'re the sole survivor(s).\"',
   '\"You hear a loud boom!\"','\"An army approaches near.\"','\"A strange being appears.\"',
   '\"You are bored. Do something.\"','\"You hear your name called.\"',
   '\"You\'re in line for something.\"','\"Someone runs into you.\"',
   '\"You have a bad hangover.\"','\"You have seen this before.\"','\"You have a vision.\"',
   '\"The sky turns green.\"','Make Your Own')
cenem= ('Corrupt Government','Overpowered Warrior','Emotional Wreck','Mad Scientist/Wizard',
   'Extraplanar Creature','The End of the World Itself','Creepy Cult Leader',
   'Possessive Ghost','Microscopic Disease','Self-Aware Robot/Construct','Hungry Zombies',
   'Former Allies','Giant Monsters','Unexpected Savant','Barbarian Horde','Revolting Peasants',
   'Mysterious Merchant','Homeless People','Choose Two','Make Your Own')
def campset(phenny, input):
   try:
      nrol = {'easy':4, 'normal':8, 'hard':12, 'nightmare':16, 'help':-1}.get(input.group(2).lower(), 0)
   except:
      nrol = 0
   if nrol == 0:
      phenny.say('Whoops, '+input.nick+', you\'re missing the game mode: easy (4 rolls), normal (8 rolls), hard (12 rolls), or nightmare (16 rolls). Or you just put in something I didn\'t recognize, like gibberish or something in another language. Please try again, or if you\'re confused, try .setting help.')
      return
   if nrol == -1:
      phenny.say('This is "Make a Damn Setting v3.0". Graphical representation: http://i.imgur.com/lL1moDi.png')
      return
   roll1 = random.choice([random.choice(castro) for i in range(0,6)])
   roll2 = random.choice([random.choice(cgeog) for i in range(0,6)])
   roll3 = random.choice([random.choice(cclim) for i in range(0,6)])
   roll4 = random.choice([random.choice(cbio) for i in range(0,6)])
   phenny.say('*Astrophysics:* '+roll1+'. *Geography:* '+roll2+'. *Climate:* '+roll3+'. *Biology:* '+roll4+'.')
   if nrol < 5:
      return
   roll5 = random.choice([random.choice(cnciv) for i in range(0,6)])
   nciv = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}.get(roll5,1)
   civn = {1:'One', 2:'Two', 3:'Three', 4:'Four', 5:'Five'}
   for i in range(0,nciv):
      roll6 = random.choice([random.choice(caes) for i in range(0,6)])
      roll7 = random.choice([random.choice(cdom) for i in range(0,6)])
      roll8 = random.choice([random.choice(cval) for i in range(0,6)])
      if nrol > 8:
         roll9 = random.choice([random.choice(cecon) for i in range(0,6)])
         rolla = random.choice([random.choice(cgov) for i in range(0,6)])
         rollb = random.choice([random.choice(cphil) for i in range(0,6)])
         rollc = random.choice([random.choice(cfeat) for i in range(0,6)])
         phenny.say('*Civilization:* aesthetic is '+roll6+'; dominant race is '+roll7+'; primary values are '+roll8+'; economy is '+roll9+'; government is '+rolla+'; philosophy is '+rollb+'; defining feature is '+rollc+'.')
      else:
      	 phenny.say('*Civilization:* aesthetic is '+roll6+'; dominant race is '+roll7+'; primary values are '+roll8+'.')
   if nrol < 13:
      return
   rolld = random.choice([random.choice(csup) for i in range(0,6)])
   rolle = random.choice([random.choice(cthem) for i in range(0,6)])
   rollf = random.choice([random.choice(cstart) for i in range(0,6)])
   rollg = random.choice([random.choice(cenem) for i in range(0,6)])
   phenny.say('*Supernatural:* '+rolld+'. *Overall Theme:* '+rolle+'. *Campaign Start:* '+rollf+' *The Enemy:* '+rollg+'.')
campset.nam = 'campset'
campset.commands = ['campaign','setting','campset']
campset.priority = 'low'

def compsetlist(phenny, input):
   foo = {'Astrophysics':'castro', 'Geography':'cgeog', 'Climate':'cclim', 'Biology':'cbio', 'Aesthetic':'caes',
      'Dominant Race':'cdom', 'Primary Values':'cval', 'Economy':'cecon', 'Government':'cgov', 'Defining Feature':'feat',
      'Overall Theme':'cthem', 'Campaign Start':'cstart', 'The Enemy':'cenem'}
   antifoo = {}
   for key,val in foo.items():
      antifoo[val] = key
   fook = foo.keys()
   quer = [i for i in fook if input.group(2).upper() in i.upper()]
   if len(quer) == 0:
      tmp = ', '.join(fook)
      phenny.say('Nope, '+input.nick+', that didn\'t work. Can you try again? Your options are: '+tmp)
      return
   if len(quer) > 1:
      phenny.say('Sorry, '+input.nick+', that query isn\'t specific enough. I\'m not going to recite a million lists, here. Can you try again?')
      return
   t0 = foo[quer[0]]
   res = globals()[t0]
   tmp = '; '.join(res)
   phenny.say(quer[0]+': '+tmp)
compsetlist.name = 'compsetlist'
compsetlist.commands = ['cslist']
compsetlist.priority = 'low'