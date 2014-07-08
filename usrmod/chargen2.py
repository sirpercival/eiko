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

hbrewc = ['AEtherforge', 'Astronomer', 'Carrionwalker', 'Crystal Mage', 'Cycle Warden', 'Divhead', 'Dodger', 'Domeskipper', 
    'Dragonmage', 'Dread Champion', 'Extractor', 'Gerudo Marauder', 'Grunt', 'GW Cleric', 'GW Druid', 'GW Ranger', 
    'Holomancer', 'Hylian Warrior', 'Jongleur', 'Ley Engineer', 'Magitechnician', 'Mentalist', 'Morphling', 'Nullblade', 
    'Panphobic', 'Planeswalker (sirp)', 'Powerbard', 'Psykin', 'Sage', 'Sandman', 'Scaleshaper', 'Shadowcaster (sirp)', 
    'Spelljammer', 'Sublime Rogue', 'Synthevolver', 'Thaumurai', 'Thrawn', 'Time Dimensional', 'Warcrafter', 'Wardancer', 
    'Warpsoul', 'Wyrm Warrior', 'Zen Fundamentalist', 'Academist', 'Evolutionist', 'Chronomancer', 'Historian', 'Echocaller',
    'Anabolist', 'Thaumaturge', 'Arcwielder', 'Champion (MG)', 'Stargazer', 'Empath', 'Plague Doctor', 'Ozodrin', 
    'Xenotheurgist', 'Xenoalchemist', 'Machinist', 'Teramach', 'Bellator', 'Kathados', 'Olethrofex', 'Spider Blood Assassin', 
    'War-Frenzy', 'Nomad', 'Gambler', 'Dimensional Conduit','Scion of Legacy', 'Daring Outlaw', 'Harrowed', 'Pariah', 
    'Chronoshifter', 'Monsterbound','Baneseeker', 'Golden Alchemist', 'Mahou Kodomo', 'Metagamer', 'Psi-shade', 'Ritualist', 
    'Shadow Artificer', 'Blasphemous Preacher', 'Blue Mage', 'Channeler', 'Dementist', 'Deviant', 'Ebon Initiate', 
    'Eventide Magus', 'Exarch of the Emerald Shield', 'Hakurei Shrine Maiden', 'Haruspex', 'Incarnation', 'Jinnblood', 
    'Limit Mage', 'Limit Psion', 'Monstrous Armiger', 'Sanguine Knight', 'Summoner', 'Tendersoul', 'War-Marked', 'Wordsmith', 
    'Worldrender', 'Avatar', 'Blade Scholar', 'Botanist', 'Chronoshifter', 'Courtier', 'Dark Knight', 
    'Delirium Blade', 'Elder', 'Emberhaunt', 'Eternal Royal', 'Grandmaster', 'Greybeard', 'Gunslinger', 'Legend', 
    'Legendary Warrior', 'Magister', "Nord's Blade", 'Planeswalker', 'Primordialist', 'Protean Chimera', 'Rappeler', 
    'Scholar', 'Shapeshifter', 'Son of Man', 'Soulblade', 'Soulweaver', 'Stoner', 'Teleporter', 'Temporalist', 
    'Vector Witch', 'Void Disciple', 'Witch', 'Battle Psychic', 'Bemantelter Schatten', 'Chorister', 'Chozo Warrior', 
    'Companion', 'Conceptualist', 'Connoisseur', 'Convoker', 'Corrupted', 'Dawnblade', 'Debaser', 'Devil Hunter', 
    'Divine Champion', 'Dovahkiin', 'Earth Dreamer', 'Engineer', 'False Prophet', 'Flowists', 'Green Knight', 
    'Grimwight', 'Hemoscribe', 'Improviser', 'Indigo Trickster', 'Invisible Guardian', 'Jack of All Blades', 
    'Kaijin', 'Kensei of the Five Rings', 'Kyodai', 'Librarian', 'Limit Dragoon', 'Lord of the Uttercold', 
    'Magus of Blades', 'Malefactor', 'Mamono', 'Masque', 'Olympian', 'Overdrive Knight', 'Primal', 'Sagittarius', 
    'Sentai', 'Shield Warrior', 'Soul Devourer', 'Soul Disciple', 'Spellbound', 'Storm Lord', 'Sublime Archer', 
    'Sublime Matador', 'Sublime Sohei', 'Traveler]', 'Trueforged', 'Warlord', 'Warrior-Poet', 'Wavekeeper', 'Arbiter', 
    'Blackguard', 'Blood King', 'Cardcaller', 'Cultist', 'Dabblemaster', 'Destined Hero', 'Disciple of Anima', 
    'Elemental Adept', 'Gaoler of Frostflame ', 'Iron Man', 'Limit Freak', 'Machiavellian', 'Magitech Templar', 
    'Runewarden', 'Solar Ascendant', 'Soulblade', 'Sniper', 'Tainted Scion of Venom', 'Twilight Caster', 'Witch Doctor', 
    'Alchemist', 'Barrier Mage', 'Battle Shinigami', 'Biskmatar', 'Blademaster', 'Chosen Warrior', 'Death Knight', 
    'Drunken Master', 'Dualists', 'Ephemeral Watcher', 'Esper Knight', 'Gentle Fist Adept', 'Jester', 'Kido Shinigami', 
    'Limit Knight', 'Limit Monk', 'Limit Ninja', 'Limit Sniper', 'Magician', 'Mind-Filcher', 'Muse', 'Psychotherapist', 
    'Punchmaster', 'Pyromancer', 'Runner', 'Sentinel', 'Shield', 'Skirmisher', 'Solar Avatar', 'Speedster', 
    'Thief-Acrobat', 'Werewolf', 'White Clad', 'Z-Fighter', 'Barkeeper', 'Botanimorphist', 'Channeler of the Planes', 
    'Fanatic', 'Farmer', 'Grappler', 'Handyman', 'Hollow', 'Liberal Arts Major', 'Midnight Seer', 'Swift Kinetic', 
    'Redshirt', 'Servant Soul', 'Stylist', 'Traveller', 'Anchorite', 'Elemental Adept (donq)', 'Impulse Mage', 
    'Savant (donq)', 'Spellsage', 'Spellshape champion', 'Avatar', 'Mage']
pubcl = [x.title() for x in ['adept', 'aristocrat', 'artificer', 'barbarian', 'bard', 'bardic sage', 'battle sorcerer', 
    'cleric', 'cloistered cleric', 'commoner', 'divine bard', 'domain wizard', 'druid', 'druidic avenger', 'eidolon', 
    'eidoloncer', 'expert', 'factotum', 'favored soul', 'fighter', 'healer', 'hexblade', 'marshal', 'monk', 
    'mystic', 'ninja', 'noble', 'paladin', 'paladin of freedom', 'paladin of slaughter', 'paladin of tyranny', 
    'psion', 'psychic warrior', 'ranger', 'rogue', 'samurai (CW)', 'samurai (OA)', 'savage bard', 'scout', 
    'shaman', 'shugenja', 'sohei', 'sorcerer', 'soulknife', 'spellcaster', 'spellthief', 'spirit shaman', 
    'swashbuckler', 'thug', 'totem barbarian', 'urban adept', 'urban ranger', 'warlock', 'warmage', 'warrior', 
    'wilder', 'wilderness rogue', 'wizard', 'wu jen', 'archivist', 'dread necromancer', 'psionic artificer', 
    'incarnate', 'soulborn', 'totemist', 'binder', 'shadowcaster', 'truenamer', 'ardent', 'divine mind', 'lurk', 
    'beguiler', 'dragon shaman', 'duskblade', 'knight', 'crusader', 'swordsage', 'warblade', 'dragonfire adept', 
    'battle dancer', 'death master', 'mountebank', 'jester', 'mountebank', 'savant', "sha'ir", 'urban druid']]
pubr = ['Lesser Aasimar', 'Aelfborn', 'Anthropomorphic Bat', 'Anthropomorphic Lizard', 'Anthropomorphic Monkey', 
    'Anthropomorphic Rat', 'Anthropomorphic Raven', 'Anthropomorphic Toad', 'Anthropomorphic Weasel', 'Asherati', 
    'Aventi', 'Lesser Axani', 'Lesser Azerblood', 'Azurin', 'Bakemono', 'Beguiler', 'Bhuka', 'Buomman', 'Lesser Cansin', 
    'Lesser Celadrin', 'Changeling', 'Lesser Chaond', 'Feral-Kind Cyclopean', 'Menta Cyclopean', "Lesser D'hin'ni", 
    'Daelkyr Half-Blood', 'Darfellan', 'Deep Imaskari', 'Lesser  Drow', 'Lesser  Duergar', 'Duskling', 'Aleithian Dwarf', 
    'Aquatic Dwarf', 'Arctic Dwarf', 'Athasian Dwarf', 'Badlands Dwarf', 'Dark Dwarf', 'Deep Dwarf', 'Desert Dwarf', 
    'Dream Dwarf', 'Earth Dwarf', 'Exiled Dwarf', 'Fireblood Dwarf', 'Glacier Dwarf', 'Gold Dwarf', 'Gully Dwarf', 
    'Hill  Dwarf', 'Jungle Dwarf', 'Mountain Dwarf', 'Seacliff Dwarf', 'Shield Dwarf', 'Stonefire Dwarf', 'Wild Dwarf', 
    'Elan', 'Aquatic Elf', 'Arctic Elf', 'Athasian Elf', 'Declining Elf', 'Desert Elf', 'Fire Elf', 'Forestlord Elf', 
    'Gray Elf', 'High  Elf', 'Illaeli Elf', 'Jungle Elf', 'Moon Elf', 'Painted Elf', 'Snow Elf', 'Star Elf', 'Sun Elf', 
    'Wild Elf', 'Wood Elf', 'Extaminar', 'Faun', 'Lesser Air Genasi', 'Lesser Earth Genasi', 'Lesser Fire Genasi', 
    'Lesser Water Genasi', 'Glimmerfolk', 'Air Gnome', 'Aquatic Gnome', 'Arcane Gnome', 'Arctic Gnome', 'Desert Gnome', 
    'Forest Gnome', 'Ice Gnome', 'Jungle Gnome', 'Mad Gnome', 'River Gnome', 'Rock  Gnome', 'Stonehunter Gnome', 
    'Techno Gnome', 'Tinker Gnome', 'Wavecrest Gnome', 'Whisper Gnome', 'Wild Gnome', 'Goblin', 'Air Goblin', 
    'Aquatic Goblin', 'Arctic Goblin', 'Desert Goblin', 'Jungle Goblin', 'Grippli', 'Gruwaar', 'Hadozee', 'Hairy Spider', 
    'Half-Drow', 'Deepwyrm Half-Drow', 'Half-Elf', 'Aquatic Half-Elf', 'Arctic Half-Elf', 'Athas Half-Elf', 
    'Desert Half-Elf', 'Fire Half-Elf', 'Forestlord Half-Elf', 'Jungle Half-Elf', 'Half-Gnome', 'Half-Human Elf', 
    'Half-Orc', 'Aquatic Half-Orc', 'Arctic Half-Orc', 'Desert Half-Orc', 'Frostblood Half-Orc', 'Jungle Half-Orc', 
    'Scablands Half-Orc', 'Water Half-Orc', 'Aquatic Halfling', 'Arctic Halfling', 'Athasian Halfling', 'Deep Halfling',
    'Anthropomorphic Ape', 'Anthropomorphic Dromedary Camel', 'Anthropomorphic Heavy Horse', 'Anthropomorphic Light Horse', 
    'Anthropomorphic Mule', 'Anthropomorphic Giant Octopus', 'Anthropomorphic Large Shark', 'Anthropomorphic Huge Viper', 
    'Anthropomorphic Large Viper', 'Anthropomorphic  Baleen Whale', 'Desert Halfling', 'Ghostwise Halfling', 
    'Glimmerskin Halfling', 'Jungle Halfling', 'Lightfoot Halfling', 'Shoal Halfling', 'Strongheart Halfling', 
    'Tallfellow Halfling', 'Tundra Halfling', 'Unsheltered Halfling', 'Water Halfling', 'Hellbred (Body)', 'Hellbred (Spirit)', 
    'Badger Hengeyokai', 'Carp Hengeyokai', 'Cat Hengeyokai', 'Crab Hengeyokai', 'Crane Hengeyokai', 'Dog Hengeyokai', 
    'Fox Hengeyokai', 'Hare Hengeyokai', 'Monkey Hengeyokai', 'Raccoon Dog Hengeyokai', 'Rat Hengeyokai', 'Sparrow Hengeyokai', 
    'Weasel Hengeyokai', 'Human', 'Complacent Human', 'Silverbrow Human', 'Illumian', 'Jermlaine', 'Jerren', 'Kagonesti', 
    'Kalashtar', 'Kender', 'Kenku', 'Khepri', 'Killoren', 'Kobold', 'Aquatic Kobold', 'Arctic Kobold', 'Desert Kobold', 
    'Earth Kobold', 'Jungle Kobold', 'Korobokuru', 'Krinth', 'Laika', 'Lupin', 'Lesser Maeluth', 'Maenad', 'Lesser Mechanatrix', 
    'Minotaur (Krynn)', 'Mongrelfolk', 'Muckdweller', 'Neanderthal', 'Neraphim', 'Nezumi', 'Orc', 'Aquatic Orc', 'Arctic Orc', 
    'Desert Orc', 'Frostblood Orc', 'Jungle Orc', 'Water Orc', 'Lesser Dust Para-Genasi', 'Lesser Ice Para-Genasi', 
    'Lesser Magma Para-Genasi', 'Lesser Ooze Para-Genasi', 'Lesser Smoke Para-Genasi', 'Lesser Steam Para-Genasi', 'Phanaton', 
    'Pterran', 'Qualinesti', 'Raptoran', 'Rilkan', 'Saurian Shifter', 'Sea Kin', 'Lesser Shadowswyft', 'Shalarin', 'Shifter', 
    'Silvanesti', 'Skarns', 'Spellscale', 'Spiker', 'Bamboo Spirit Folk', 'Mountain Spirit Folk', 'River Spirit Folk', 
    'Sea Spirit Folk', 'Lesser Svirfneblin', 'Synad', "T'kel", 'Tasloi', 'Tibbit', 'Lesser Tiefling', 'Tortle', 'Underfolk', 
    'Vanara', 'Varsharan', 'Vril', 'Warforged', 'Warforged Scout', 'Lesser Wispling', 'Xeph', 'Xvart', 'Lesser Zenythri']
hbrewr = ['Xevu', 'Dwaerrow', 'Animus', 'Adolboleth', 'Aeroki', 'Ameena', 'Ancestors', 'Antha', 'Arte', 'Bloodbred', 'Ashwalker', 
    'Bombina', 'Canilu', 'Cilid', 'City Gnomes', 'Crafted', 'Dolant', 'Dolrii', 'Dorzun', 'Drajar', 'Drazai', 'Dung Elf', 'Dwelf', 
    'Elvaan', 'Galka', 'Gnoblin', 'Half-halfling', 'Hanlers', 'Haukea', 'Hume', 'Jarek', 'Ka-Sivence', 'Kamapalolo', 'Kitsune', 
    'Kuthan', 'Lalana', 'Leonin', 'Lycolts', 'Mephian', 'Mepholk', 'Merrow', 'Mil', 'Mithra', 'Moogle', 'Muckdweller', 'Muscheron', 
    'Mushroomfolk', 'Mwnci', 'Olmaji', 'Polka Gnome', 'Prinny', 'Progenitor Kobold', 'Psuedo-Illithid', 'Quis', 'Satyr', 
    'Si-Sivence', 'Skaven', 'Skink', 'Somnambul', 'Sphinx', 'Stoutgnome', 'Taerlae', 'Tanuki', 'Taru-Taru', 'Techgnome', 
    'Titanium Dwarves', "Tn'lch", 'Tursiel', 'Woodwarf', 'Aarococra', 'Armless Running Albino Star', 'Blagen', 'Cheval', 'Dorc', 
    'Eyedusa', 'Fenix-Blooded', 'Fleshwrought', 'Gunchadh', 'Indhaar', 'Lloshhi', 'Metathran', 'Mothman', 'Muuten', 'Raptor', 
    'Russiti', 'Sangheili', 'Saurus', 'Songtouched', 'Sphoraxunes', 'Spyrian', 'Zakken', 'Darkling', 'Deathwalker', 'Elm-Tiela', 
    'Raptorfolk', 'Vanar', 'Maggot Archon', 'Orochi', 'Alien Brood Watcher', 'Talansidhe', 'Human (milo)', 'Jaycah', 'Kith', 
    'Titan', 'Dwarf (milo)','Lifetorn','Gremlin','Leprechaun','Cellochoroid','Chloromorph','Cambian','Caymir','Living Spellshape',
    'Masked One','Spellsoul Armor','Stoichen']
    
def charconcept(phenny, input):
    opts = input.groups()[1]
    pub = True
    multi = 1
    homebrew = True
    if opts:
        opts = opts.split()
        if 'nopub' in opts:
            pub = False
        if 'nobrew' in opts:
            homebrew = False
        if not (pub or homebrew):
            phenny.reply("Well, you haven't given me any source options!")
            return
        if 'gestalt' in opts:
            multi = 2
        if 'tristalt' in opts:
            multi = 3
        if 'quadstalt' in opts:
            multi = 4
    races = []
    classes = []
    if pub:
        races += pubr
        classes += pubcl
    if homebrew:
        races += hbrewr
        classes += hbrewc
    race = random.choice(races)
    clas = ' // '.join(random.sample(classes, multi))
    level = str(random.randint(1,30))
    phenny.reply(' '.join(['Level',level,race,clas]))
charconcept.name = 'charconcept'
charconcept.commands = ['concept']
charconcept.priority = 'low'

class WRandom(object):
    def __init__(self, weights):
        self.__max = .0
        self.__weights = []
        for value, weight in weights.items():
            self.__max += weight
            self.__weights.append((self.__max, value))

    def random(self):
        r = random.random() * self.__max
        for ceil, value in self.__weights:
            if ceil > r: return value
            

reinc = WRandom({'Aberration':0.6,'Animal':0.6,'Construct':0.6,'Dragon':0.6,'Elemental':0.6,'Fey':0.6,
    'Giant':0.6,'Humanoid':1.,'MagicalBeast':0.6,'MonstrousHumanoid':0.6,'Ooze':0.6,'Outsider':0.6,'Plant':0.6,
    'Undead':0.6,'Vermin':0.6,'Template':0.4})

pick = {'Aberration':WRandom({'Aboleth':1., 'Ahuizotl':1., 'Athach':1., 'Avolakia':1., 'Balhannoth':1., 'Beholder':1., 
    'Gauth Beholder':1., 'Carrion Crawler':1., 'Catoblepas':1., 'Chilblain':1., 'Choker':1., 'Chuul':1., 'Chwidencha':1., 
    'Cloaker':1., 'Darktentacles':1., 'Darkweaver':1., 'Delver':1., 'Destrachan':1., 'Drider':1., 'Dustblight':1., 
    'Ethereal Filcher':1., 'Black Ethergaunt':1., 'Red Ethergaunt':1., 'White Ethergaunt':1., 'Ettercap':1., 'Fihyr':1., 
    'Great Fihyr':1., 'Gibbering Mouther':1., 'Grell':1., 'Grick':1., 'Harpoon Spider':1., 'Hook Horror':1., 'Howler Wasp':2., 
    'Howler Wasp Queen':1., 'Ixitxachitl':1., 'Vampiric Ixitxachitl':1., 'Julajimus':1., 'Lodestone Marauder':1., 
    'Lurking Strangler':1., 'Mageripper Swarm':1., 'Malasynep':1., 'Maulgoth':1., 'Meenlock':1., 'Mimic':1., 'Mind Flayer':1., 
    'Mindshredder Larva':2., 'Mindshredder Warrior':1., 'Moonbeast':1., 'Morkoth':1., 'Dark Naga':1., 'Guardian Naga':1., 
    'Spirit Naga':1., 'Water Naga':1., 'Adult Neogi':1., 'Neogi Spawn':2., 'Ocularon':1., 'Odopi':1., 'Elder Odopi':1., 
    'Otyugh':1., 'Lifeleech Otyugh':1., 'Phasm':1., 'Phiuhl':1., 'Average Psurlon':1., 'Elder Psurlon':1., 'Giant Psurlon':1., 
    'Prismatic Roper':1., 'Rot Reaver':1., 'Rukanyr':1., 'Runehound':1., 'Rust Monster':1., 'Seryulin':1., 'Greater Seryulin':1., 
    'Shivhad':1., '10-headed Shrieking Terror':1., '5-headed Shrieking Terror':1., 'Skum':1., 'Skybleeder':1., 'Slasrath':1., 
    'Snowcloak':1., 'Spectral Lurker':1., 'Stonesinger':1., 'Susurrus':1., 'Abyssal Ant Swarm':1., 'Tunnel Terror':1., 
    'Uchuulon':1., 'Umber Hulk':1., "Will-O'-Wisp":1., 'Windghost':1., 'Wyste':1., 'Anathema Yuan-Ti':1., 'Zern Arcanovore':1.}),
    'Animal':WRandom({'Ape':1., 'Baboon':1., 'Badger':1., 'Barracuda':1., 'Bat':1., 'Black Bear':1., 'Brown Bear':1., 
    'Polar Bear':1., 'Bison':1., 'Boar':1., 'Camel':1., 'Caribou':1., 'Cat':1., 'Cheetah':1., 'Constrictor Snake':1., 
    'Giant Constrictor Snake':1., 'Crocodile':1., 'Giant Crocodile':1., 'Dire Ape':1., 'Dire Badger':1., 'Dire Barracuda':1., 
    'Dire Bat':1., 'Dire Bear':1., 'Dire Boar':1., 'Dire Eel':1., 'Dire Hawk':1., 'Dire Horse':1., 'Dire Jackal':1., 
    'Dire Lion':1., 'Dire Puma':1., 'Dire Rat':1., 'Dire Tiger':1., 'Dire Toad':1., 'Dire Tortoise':1., 'Dire Vulture':1., 
    'Dire Weasel':1., 'Dire Wolf':1., 'Dire Wolverine':1., 'Dog':1., 'Donkey':1., 'Eagle':1., 'Eel':1., 'Elephant':1., 
    'Arctic Fox':1., 'Hawk':1., 'Hippopotamus':1., 'Horned Lizard':1., 'Heavy Horse':1., 'Light Horse':1., 'Hyena':1., 
    'Leopard':1., 'Lion':1., 'Lizard':1., 'Monitor Lizard':1., 'Manta Ray':1., 'Monkey':1., 'Mule':1., 'Octopus':1., 'Otter':1., 
    'Sea Otter':1., 'Owl':1., 'Penguin':1., 'Pony':1., 'Porpoise':1., 'Rat':1., 'Raven':1., 'Rhinoceros':1., 'Roc':1., 
    'Sea Lion':1., 'Sea Tiger':1., 'Seal':1., 'Huge Shark':1., 'Large Shark':1., 'Medium Shark':1., 'Smilodon':1., 
    'Snapping Turtle':1., 'Squid':1., 'Stingray':1., 'Tiger':1., 'Toad':1., 'Huge Vipe ':1., 'Large Viper':1., 'Medium Viper':1., 
    'Small Viper':1., 'Tiny Viper':1., 'Vulture':1., 'Walrus':1., 'Weasel':1., 'Baleen Whale':1., 'Cachalot Whale':1., 
    'Orca Whale':1., 'Wolf':1., 'Wolverine':1., 'Woolly Mammoth':1.}),
    'Construct':WRandom({'Colossal Animated Object':1., 'Gargantuan Animated Object':1., 'Huge Animated Object':1., 
    'Large Animated Object':2., 'Medium Animated Object':2., 'Small Animated Object':2., 'Tiny Animated Object':2., 
    'Hammerer Automaton':2., 'Pulverizer Automaton':2., 'Blackstone Gigant':1., 'Bogun':2., 'Bronze Serpent':1., 
    'Cadaver Collector':1., 'Greater Cadaver Collector':1., 'Caryatid Column':2., 'Clockroach':2., 
    'Adamantine Clockwork Horror':1., 'Electrum Clockwork Horror':2., 'Gold Clockwork Horror':1., 'Platinum Clockwork Horror':1., 
    'Clockwork Mender':2., 'Clockwork Mender Swarm':2., 'Clockwork Pony':2., 'Clockwork Stallion':2., 'Retriever Demon':1., 
    'Dread Guard':2., 'Alchemical Golem':1., 'Blood Golem of Hextor':1., 'Brain Golem':1., 'Brass Golem':1., 'Chain Golem':1., 
    'Clay Golem':1., 'Coral Golem':1., 'Demonflesh Golem':1., 'Dragonflesh Golem':1., 'Fang Golem':1., 'Flesh Golem':1., 
    'Gloom Golem':1., 'Hangman Golem':1., 'Hellfire Golem':1., 'Ice Golem':1., 'Iron Golem':1., 'Mud Golem':1., 
    'Prismatic Golem':1., 'Sand Golem':1., 'Shadesteel Golem':1., 'Stained Glass Golem':1., 'Stone Golem':1., 'Web Golem':1., 
    'Grisgol':1., 'Homunculus':2., 'Kolyarut':1., 'Marut':1., 'Quarut':1., 'Varakhut':1., 'Zelekhut':1., 'Iron Cobra':2., 
    'Juggernaut':1., 'Maug':2., 'Necrophidius':2., 'Nimblewright':1., 'Common Raggamoffyn':1., 'Guttersnipe':1., 'Shrapnyl':1., 
    'Tatterdemanimal':1., 'Rogue Eidolon':1., 'Runic Guardian':1., 'Seaforged':1., 'Shield Guardian':1., 
    'Slaughterstone Behemoth':1., 'Slaughterstone Eviscerator':1., 'Warforged':1., 'Waste Crawler':1., 'Wicker Man':1., 'Zodar':1}),
    'Dragon':WRandom({'Ambush Drake':0.6, 'Dragon Eel':0.4, 'Dragon Turtle':0.5, 'Black Dragon':0.2, 'Blue Dragon':0.1, 
    'Green Dragon':0.2, 'Red Dragon':0.1, 'White Dragon':0.2, 'Amethyst Dragon':0.2, 'Crystal Dragon':0.2, 'Emerald Dragon':0.1, 
    'Sapphire Dragon':0.1, 'Topaz Dragon':0.1, 'Brass Dragon':0.2, 'Bronze Dragon':0.1, 'Copper Dragon':0.1, 'Gold Dragon':0.1, 
    'Silver Dragon':0.1, 'Crested Felldrake':0.7, 'Horned Felldrake':0.6, 'Spitting Felldrake':0.6, 'Hellfire Wyrm':0.2, 
    'Corpse Tearer Linnorm':0.2, 'Dread Linnorm':0.3, 'Gray Linnorm':0.3, 'Pseudodragon':0.6, 'Rage Drake':0.5, 'Sea Drake':0.3, 
    'Ssvaklor':0.4, 'Greater Ssvaklor':0.2, 'Sunwyrm':0.4, 'Wyvern':0.5}),
    'Elemental':WRandom({'Black Rock Triskelion':0.1, 'Cyclonic Ravager':0.1, 'Holocaust Disciple':0.1, 'Waterveiled Assassin':0.1, 
    'Belker':0.2, 'Breathdrinker':0.2, 'Caller from the Deeps':0.2, 'Chraal':0.2, 'Dust Twister':0.2, 'Air Elemental Weird':0.1, 
    'Earth Elemental Weird':0.1, 'Fire Elemental Weird':0.1, 'Ice Elemental Weird':0.1, 'Snow Elemental Weird':0.1, 
    'Water Elemental Weird':0.1, 'Elder Air Elemental':0.1, 'Greater Air Elemental':0.1, 'Huge Air Elemental':0.2, 
    'Large Air Elemental':0.2, 'Medium Air Elemental':0.2, 'Small Air Elemental':0.3, 'Elder Earth Elemental':0.1, 
    'Greater Earth Elemental':0.1, 'Huge Earth Elemental':0.2, 'Large Earth Elemental':0.2, 'Medium Earth Elemental':0.2, 
    'Small Earth Elemental':0.3, 'Elder Fire Elemental':0.1, 'Greater Fire Elemental':0.1, 'Huge Fire Elemental':0.2, 
    'Large Fire Elemental':0.2, 'Medium Fire Elemental':0.2, 'Small Fire Elemental':0.3, 'Elder Storm Elemental':0.1, 
    'Greater Storm Elemental':0.1, 'Huge Storm Elemental':0.1, 'Large Storm Elemental':0.2, 'Medium Storm Elemental':0.2, 
    'Small Storm Elemental':0.3, 'Elder Water Elemental':0.1, 'Greater Water Elemental':0.1, 'Huge Water Elemental':0.2, 
    'Large Water Elemental':0.2, 'Medium Water Elemental':0.2, 'Small Water Elemental':0.3, 'Fire Bat':0.2, 'Galeb Duhr':0.2, 
    'Immoth':0.1, 'Inferno Spider':0.2, 'Invisible Stalker':0.2, 'Living Holocaust':0.1, 'Magmin':0.3, 'Omnimental':0.1, 
    'Stone Spike':0.2, 'Tempest':0.1, 'Thoqqua':0.3}),
    'Fey':WRandom({'Domovoi':0.5, 'Dryad':0.4, 'Feytouched':0.7, 'Fossergrim':0.4, 'Jermlaine':0.7, 'Joystealer':0.2, 
    'Kelpie':0.2, 'Lunar Ravager':0.1, 'Nymph':0.1, 'Ocean Strider':0.1, 'Oread':0.2, 'Petal':0.6, 'Rimefire Eidolon':0.1, 
    'Rusalka':0.6, 'Satyr':0.3, 'Shadar-Kai':0.5, 'Sirine':0.3, 'Spirit of the Land':0.1, 'Splinterwaif':0.4, 'Spriggan':0.3, 
    'Grig':0.5, 'Nixie':0.5, 'Pixie':0.4, 'Uldra':0.6, 'Verdant Prince':0.1, 'Vodyanoi':0.3, 'Yuki-On-Na':0.2}),
    'Giant':WRandom({'Ogre':0.8, 'Ettin':0.6, 'Fensir':0.7, 'Rakka Fensir':0.5, 'Firbolg':0.2, 'Fomorian':0.2, 'Geriviar':0.1, 
    'Bog Giant':0.7, 'Cloud Giant':0.4, "Craa'ghoran Giant":0.3, 'Fire Giant':0.3, 'Forest Giant':0.4, 'Frost Giant':0.4, 
    'Hill Giant':0.6, 'Mountain Giant':0.1, 'Ocean Giant':0.1, 'Shadow Giant':0.2, 'Stone Giant':0.5, 'Storm Giant':0.2, 
    'Sun Giant':0.3, 'Ogre Mage':0.6, 'Troll':0.7, 'Cave Troll':0.5}),
    'Humanoid':WRandom({'Bugbear':0.1, 'Dark Creeper':0.1, 'Dark Stalker':0.5, 'Dwarf':0.5, 'Duergar':0.3, 'Glacier Dwarf':0.4, 
    'Elf':0.5, 'Drow':0.2, 'Engineer':0.5, 'Githyanki':0.2, 'Githzerai':0.2, 'Gnoll':0.2, 'Gnome':0.5, 'Svirfneblin':0.2, 
    'Goblin':0.4, 'Snow Goblin':0.5, 'Halfling':0.5, 'Hobgoblin':0.3, 'Human':0.5, 'Kobold':0.4, 'Lizardfolk':0.2, 
    'Locathah':0.3, 'Merfolk':0.3, 'Mongrelfolk':0.4, 'Neanderthal':0.5, 'Orc':0.3, 'Selkie':0.1, 'Skulk':0.1, 'Troglodyte':0.1}),
    'MagicalBeast':WRandom({'Abrian':0.2, 'Ankheg':0.2, 'Aranea':0.1, 'Ash Rat':0.2, 'Ashworm':0.2, 'Asperi':0.2, 
    'Avalancher':0.1, 'Basilisk':0.1, 'Bearhound':0.1, 'Behir':0.1, 'Blink Dog':0.2, 'Blood Ape':0.2, 'Blood Hawk':0.2, 
    'Bloodsilk Spider':0.2, 'Branta':0.2, 'Brood Keeper':0.1, 'Bulette':0.1, 'Camelopardel':0.2, 'Chaos Roc':0.1, 
    'Chekryan':0.2, 'Chimera':0.1, 'Chronotyryn':0.1, 'Cloaked Ape':0.2, 'Cloud Ray':0.1, 'Cockatrice':0.2, 'Corollax':0.2, 
    'Darkmantle':0.2, 'Death Dog':0.2, 'Digester':0.1, 'Disenchanter':0.1, 'Displacer Beast':0.1, 'Dragonne':0.1, 
    'Dunewinder':0.1, 'Giant Eagle':0.2, 'Ethereal Marauder':0.2, 'Feral Yowler':0.1, 'Fiendwurm':0.1, 'Greater Flame Snake':0.1, 
    'Lesser Flame Snake':0.1, 'Minor Flame Snake':0.2, 'Frost Salamander':0.1, 'Frost Worm':0.1, 'Gambol':0.1, 'Gathra':0.1, 
    'Girallon':0.1, 'Gorgon':0.1, 'Gravorg':0.1, 'Gray Render':0.1, 'Griffon':0.1, 'Grimalkin':0.2, 'Hammerclaw':0.2, 
    'Hippocampus':0.2, 'Hippogriff':0.2, 'Hydra':0.1, 'Cryohydra':0.1, 'Pyrohydra':0.1, 'Ice Toad':0.2, 'Ironclad Mauler':0.1, 
    'Jackalwere':0.2, 'Kraken':0.1, 'Krenshar':0.2, 'Kuldurath':0.1, 'Lamia':0.1, 'Lammasu':0.1, 'Leviathan':0.1, 
    'Lucent Worm':0.1, 'Manticore':0.1, 'Mivilorn':0.1, 'Mooncalf':0.1, 'Moonrat':0.2, 'Mudmaw':0.1, 'Nethersight Mastiff':0.1, 
    'Nightmare Beast':0.1, 'Giant Owl':0.2, 'Owlbear':0.2, 'Pegasus':0.2, 'Phase Spider':0.2, 'Phase Wasp':0.2, 'Phoenix':0.1, 
    'Phoera':0.2, 'Purple Worm':0.1, 'Quanlos':0.1, 'Ramfish':0.1, 'Rampager':0.1, 'Giant Raven':0.2, 'Razor Boar':0.1, 
    'Remorhaz':0.1, 'Roper':0.1, 'Sand Hunter':0.2, 'Sea Cat':0.1, 'Seawolf':0.6, 'Senmurv':0.2, 'Shadow Asp':0.2, 
    'Shadow Spider':0.1, 'Shedu':0.1, 'Shocker Lizard':0.2, 'Sisiutl':0.1, 'Skiurid':0.2, 'Spellgaunt':0.1, 'Androsphinx':0.1, 
    'Canisphinx':0.1, 'Criosphinx':0.1, 'Crocosphinx':0.1, 'Gynosphinx':0.1, 'Hieracosphinx':0.1, 'Saurosphinx':0.1, 
    'Threskisphinx':0.1, 'Spider Eater':0.2, 'Spirit of the Air':0.1, 'Stirge':0.2, 'Swamplight Lynx':0.1, 
    'Cranium Rat Swarm':0.4, 'Hellwasp Swarm':0.1, 'Tarrasque':0.1, 'Terlen':0.2, 'Thunder Worm':0.1, 'Thunderbird':0.1, 
    'Tlalusk':0.1, 'Tomb Spider':0.1, 'Tomb Spider Broodswarm':0.2, 'Unicorn':0.2, 'Urskan':0.1, 'Varrangoin Arcanist':0.1, 
    'Lesser Varrangoin':0.1, 'Varrangoin Rager':0.1, 'Winter Wolf':0.1, 'Worg':0.2, 'Yrthak':0.1, 'Zezir':0.1}),
    'MonstrousHumanoid':WRandom({'Queen Abeil':0.1, 'Soldier Abeil':0.1, 'Abeil Vassal':0.3, 'Boggle':0.2, 'Braxat':0.1, 
    'Centaur':0.2, 'Derro':0.2, 'Desmodu':0.1, 'Doppelganger':0.2, 'Ethereal Doppelganger':0.1, 'Frost Folk':0.3, 'Gargoyle':0.2, 
    'Goatfolk':0.3, 'Grimlock':0.4, 'Annis Hag':0.2, 'Green Hag':0.1, 'Sea Hag':0.3, 'Harpy':0.1, 'Jackal Lord':0.1, 'Khaasta':0.2, 
    'Kopru':0.1, 'Kuo-Toa':0.3, 'Loxo':0.2, 'Marzanna':0.1, 'Medusa':0.2, 'Minotaur':0.2, 'Greathorn Minotaur':0.1, 'Nagatha':0.1, 
    'Nycter':0.3, 'Ophidian':0.4, 'Ormyrr':0.1, 'Sahuagin':0.3, 'Sarkrith Spelleater':0.1, 'Sarkrith Thane':0.1, 'Scorpionfolk':0.1, 
    'Skindancer':0.1, 'Spell Weaver':0.1, 'Thri-Kreen':0.3, 'Yak Folk':0.2, 'Yeti':0.2, 'Yuan-Ti Abomination':0.1, 
    'Yuan-Ti Halfblood':0.1, 'Yuan-Ti Ignan':0.1, 'Yuan-Ti Pureblood':0.2, 'Yurian':0.2, 'Zern':0.1, 'Zern Blade Thrall':0.2}),
    'Ooze':WRandom({'Bloodbloater Ooze':0.9, 'Flotsam Ooze':0.9,  'Reekmurk Ooze':0.6, 'Arcane Ooze':0.1, 'Bloodfire Ooze':0.2, 
    'Bone Ooze':0.1, 'Conflagration Ooze':0.4, 'Corrupture':0.2, 'Ethereal Ooze':0.2, 'Flesh Jelly':0.1, 'Black Pudding':0.3, 
    'Brine Ooze':0.3, 'Gelatinous Cube':0.8, 'Gray Ooze':0.8, 'Lava Ooze':0.5, 'Ochre Jelly':0.6, 'White Pudding':0.4, 
    'Reason Stealer':0.7, 'Snowflake Ooze':0.5, 'Summoning Ooze':0.7, 'Teratomorph':0.1}),
    'Outsider':WRandom({'Formian Worker':1, 'Ether Scarab':1, 'Aasimar':1, 'Maeluth':1, 'Mechanatrix':1, 'Tiefling':1, 
    'Wispling':1, 'Lantern Archon':1, 'Lemure':1, 'Chaond':1, 'Zenythri':1, 'Vargouille':1, 'Bacchae':1, 'Bladeling':1, 
    'Filth Imp':1, 'Quasit':1, 'Demonhive Attendant':1, 'Demonet Swarm':1, 'Imp':1, 'Kaorti':1, 'Varoot':1, 'Shyft':1, 
    'Windrazor':1, 'Aoa Droplet':1, 'Juvenile Arrowhawk':1, 'Abyssal Maw':1, 'Abyssal Skulker':1, 'Dretch':1, 'Nashrou':1, 
    'Juvenile Tojanida':1, 'Minor Xorn':1, 'Formian Warrior':1, 'Bloodbag Imp':1, 'Euphoric Imp':1, 'Triton':1, 'Vorr':1, 
    'Wrackspawn':1, 'Skeroloth':1, 'Azer':1, 'Skulvyn':1, 'Ravid':1, 'Air Mephit':1, 'Dust Mephit':1, 'Earth Mephit':1, 
    'Fire Mephit':1, 'Glass Mephit':1, 'Ice Mephit':1, 'Magma Mephit':1, 'Ooze Mephit':1, 'Salt Mephit':1, 'Steam Mephit':1, 
    'Sulfur Mephit':1, 'Water Mephit':1, 'Rast':1, 'Yeth Hound':1, 'Voor':1, 'Barghest':1, 'Hell Hound':1, 'Visilight':1, 
    'Achaierai':1, 'Advespa':1, 'Dwarf Ancestor':1, 'Flamebrother Salamander':1, 'Adult':1, 'Cervidal':1, 
    'Formian Winged Warrior':1, 'Durzagon':1, 'Howler':1, 'Kalareem ':1, 'Shadow Mastiff':1, 'Mud Slaad':1, 'Adult Tojanida':1, 
    'Abyssal Ravager':1, 'Babau':1, 'Formian Taskmaster':1, 'Sylph':1, 'Average Xorn':1, 'Greater Barghest':1, 'Haraknin':1, 
    'Jovoc':1, 'Maurezhi':1, 'Demonhive Queen':1, 'Araton':1, 'Keeper':1, 'Hound Archon':1, 'Chaos Beast':1, 'Movanic Deva':1, 
    'Hellcat':1, 'Janni':1, 'Nightmare':1, 'Xill':1, 'Formian Armadon':1, 'Avoral Guardinal ':1, 'Rejkar ':1, 'Trilloch ':1, 
    'Canoloth':1, 'Corruptor of Fate':1, 'Justice Archon ':1, 'Barbazu ':1, 'Midgard Dwarf ':1, 'Bralani Eladrin ':1, 
    'Night Hag':1, 'Windscythe':1, 'Djinni':1, 'Efreeti':1, 'Qorrashi':1, 'Maelephant ':1, 'Marrash ':1, 'Piscoloth':1, 
    'Succubus':1, 'Zovvut':1, 'Bone Devil':1, 'Vaporighu':1, 'Lupinal':1, 'Chain Devil':1, 'Dune Stalker':1, 'Formian Observer':1, 
    'Glimmerskin':1, 'Lillend':1, 'Average Salamander':1, 'Red Slaad':1, 'Vultivor':1, 'Whisper Demon':1, 'Amnizu':1, 
    'Mezzoloth':1, 'Farastu':1, 'Bebilith':1, 'Palrethee':1, 'Monadic Deva':1, 'Formian Myrmarch':1, 'Ferrumach':1, 'Blue Slaad':1, 
    'Echinoloth':1, 'Arrowhawk Elder':1, 'Jarilith':1, 'Barbed Devil':1, 'Ghaele Eladrin':1, 'Elder Xorn':1, 'Devil':1, 
    'Leonal Guardinal':1, 'Rakshasa':1, 'Elder Tojanida':1, 'Shadurakul':1, 'Alkilith':1, 'Arrow Demon':1, 'Glabrezu':1, 
    'Malebranche':1, 'Nessian Warhound':1, 'Noble Salamander':1, 'Green Slaad':1, 'Steel Predator':1, 'Marraenoloth':1, 'Couatl':1, 
    'Kelubar':1, 'Kastighur':1, 'Rukarazyll':1, 'Gray Slaad':1, 'Yagnoloth':1, 'Vrock':1, 'Ice Devil':1, 'Aoa Sphere':1, 
    'Nalfeshnee':1, 'Ethereal Slayer':1, 'Death Slaad':1, 'Cuprilach':1, 'Scyllan':1, 'Nycaloth':1, 'Planetar':1, 'Hezrou':1, 
    'Kelvezu':1, 'Justicator':1, 'Shator':1, 'Horned Devil':1, 'Sillit':1, 'Wastrilith':1, 'Marilith':1, 'Xerfilstyx':1, 
    'Astral Deva':1, 'Trumpet Archon':1, 'Sorrowsworn Demon':1, 'Arcanaloth':1, 'Ultroloth':1, 'Formian Queen':1, 
    'Concordant Killer':1, 'Pit Fiend':1, 'Myrmyxicus':1, 'Marruspawn Abomination':1, 'Balor':1, 'Paeliryon':1, 'Titan':1, 
    'Aurumach':1, 'Solar':1, 'Deathdrinker':1, 'Klurichir':1}),
    'Plant':WRandom({'Assassin Vine':0.5, 'Battlebriar':0.5, 'Warbound Impaler':0.5, 'Bloodthorn':0.5, 'Briarvex':0.5, 
    'Shrieker':0.5, 'Violet Fungus':0.5, 'Greenvise':0.4, 'Ironmaw':0.4, 'Ironthorn':0.4, 'Kelp Angler':0.4, 'Myconid':1.7, 
    'Needlefolk':0.2, 'Night Twist':0.2, 'Oaken Defender':0.2, 'Octopus Tree':0.2, 'Orcwort':0.2, 'Wortling':0.2, 
    'Phantom Fungus':0.1, 'Plague Brush':0.1, 'Porcupine Cactus':0.1, 'Red Sundew':0.1, 'Saguaro Sentinel':0.1, 
    'Shambling Mound':0.1, 'Sporebat':0.1, 'Tendriculos':0.1, 'Treant':0.1, 'Tumbling Mound':0.1, 'Twig Blight':0.1, 
    'Vine Horror':0.1, 'Wizened Elder':0.1, 'Yellow Musk Creeper':0.1}),
    'Undead':WRandom({'Abyssal Ghoul':0.1, 'Allip':0.3, 'Ashen Husk':0.3, 'Banshee':0.1, 'Bhut':0.2, 'Blackskate':0.3, 
    'Bloodhulk Crusher':0.1, 'Bloodhulk Fighter':0.2, 'Bloodhulk Giant':0.1, 'Bodak':0.2, 'Bone Naga':0.1, 'Boneclaw':0.2, 
    'Bonedrinker':0.2, 'Lesser Bonedrinker':0.2, 'Charnel Hound':0.1, 'Corpse Gatherer':0.1, 'Crawling Apocalypse':0.1, 
    'Crawling Head':0.1, 'Crimson Death':0.1, 'Crypt Thing':0.3, 'Deathbringer':0.1, 'Deathshrieker':0.1, 'Defacer':0.2, 
    'Blood Fiend':0.1, 'Devourer':0.1, 'Dust Wight':0.1, 'Effigy':0.1, 'Entombed':0.1, 'Famine Spirit':0.1, 'Ghoul':0.3, 
    'Ghast':0.3, 'Gravecrawler':0.1, 'Hullathoin':0.1, 'Icegaunt':0.2, 'Jahi':0.1, 'Mohrg':0.1, 'Mummy':0.2, 'Necronaut':0.1, 
    'Necrotic Carnex':0.3, 'Nightcrawler':0.1, 'Nightwalker':0.1, 'Nightwing':0.1, 'Plague Spewer':0.1, 'Plague Walker':0.3, 
    'Quth-Maren':0.2, 'Ragewind':0.1, 'Shadow':0.3, 'Spawn of Kyuss':0.2, 'Spectre':0.2, 'Ulgurstasta':0.1, 'Vampire Spawn':0.3, 
    'Vasuthant':0.3, 'Vitreous Drinker':0.1, 'Wight':0.3, 'Winterspawn':0.1, 'Wraith':0.2, 'Dread Wraith':0.1}),
    'Vermin':WRandom({'Giant Ant Lion':0.1, 'Giant Queen Ant':0.1, 'Giant Soldier Ant':0.2, 'Giant Worker Ant':0.2, 
    'Giant Bee':0.2, 'Giant Bombardier Beetle':0.2, 'Giant Fire Beetle':0.3, 'Giant Stag Beetle':0.1, 'Bonespear ':0.1, 
    'Brine Swimmer':0.1, 'Colossal Monstrous Centipede':0.1, 'Gargantuan Monstrous Centipede':0.1, 'Huge Monstrous Centipede':0.1, 
    'Large Monstrous Centipede':0.2, 'Medium Monstrous Centipede':0.3, 'Small Monstrous Centipede':0.2, 
    'Tiny Monstrous Centipede':0.2, 'Century Worm':0.1, 'Chelicera ':0.1, 'Colossal Monstrous Crab':0.1, 
    'Gargantuan Monstrous Crab':0.1, 'Huge Monstrous Crab':0.1, 'Large Monstrous Crab':0.1, 'Medium Monstrous Crab':0.2, 
    'Small Monstrous Crab':0.3, 'Knell Beetle':0.1, 'Giant Leech':0.3, 'Leechwalker ':0.1, 'Megapede ':0.1, 
    'Great Old Master Neogi':0.1, 'Giant Praying Mantis':0.1, 'Colossal Monstrous Scorpion':0.1, 
    'Gargantuan Monstrous Scorpion':0.1, 'Huge Monstrous Scorpion':0.1, 'Large Monstrous Scorpion':0.1, 
    'Medium Monstrous Scorpion':0.2, 'Small Monstrous Scorpion':0.2, 'Tiny Monstrous Scorpion':0.2, 'Siege Crab':0.1, 
    'Large Snow Spider':0.1, 'Medium Snow Spider':0.2, 'Small Snow Spider':0.3, 'Colossal Monstrous Spider':0.1, 
    'Gargantuan Monstrous Spider':0.1, 'Huge Monstrous Spider':0.1, 'Large Monstrous Spider':0.1, 'Medium Monstrous Spider':0.2, 
    'Small Monstrous Spider':0.3, 'Tiny Monstrous Spider':0.2, 'Bloodfiend Locust Swarm':0.1, 'Centipede Swarm':0.1, 
    'Jellyfish Swarm':0.1, 'Leech Swarm':0.2, 'Locust Swarm':0.1, 'Plague Ant Swarm':0.1, 'Rapture Locust Swarm':0.1, 
    'Scarab Beetle Swarm':0.1, 'Spider Swarm':0.2, 'Wasp Swarm':0.1, 'Giant Queen Termite':0.1, 'Giant Soldier Termite':0.2, 
    'Giant Worker Termite':0.2, 'Giant Wasp':0.1}),
    'Template':WRandom({'Anarchic':0.1, 'Axiomatic':0.1, 'Celestial':0.3, 'Chameleon':0.4, 'Child of the Sea':0.2, 'Draconic':0.4, 
    'Dragon Vassal':0.2, 'Dragonspawn':0.4, 'Dry Lich':0.1, 'Entropic':0.2, 'Feral':0.4, 'Fiendish':0.3, 'Ghost':0.1, 
    'Gravetouched Ghoul':0.2, 'Half-Celestial':0.1, 'Half-Dragon':0.2, 'Half-Elemental':0.2, 'Half-Farspawn':0.1, 'Half-Fey':0.2, 
    'Half-Fiend':0.1, 'Half-Illithid':0.1, 'Half-Troll':0.1, 'Half-Vampire':0.2, 'Hooded Pupil':0.1, 'Insectile':0.2, 'Lich':0.1, 
    'Lolth-Touched':0.4, 'Mineral Warrior':0.4, 'Mummified':0.1, 'Necropolitan':0.5, 'Primordial':0.5, 'Risen Martyr':0.5, 
    'Shadow':0.2, 'Spellwarped':0.2, 'Tainted One':0.2, 'Vampire':0.1, 'Vivacious':0.1, 'Werebear':0.3, 'Wereboar':0.2, 
    'Wererat':0.3, 'Weretiger':0.3, 'Werewolf':0.3, 'Woodling':0.2})}

def reincarnate(phenny, input):
    target = input.groups()[1]
    if not target:
        target = input.nick
    result = []
    while True:
        typ = reinc.random() 
        result.append(pick[typ].random())
        if typ != 'Template':
            break
    res = ' '.join(result)
    article = 'a'
    if res[0].lower() in 'aeiou':
        article += 'n'
    phenny.say(' '.join([target,'is reincarnated as',article,res]))
reincarnate.name = 'reincarnate'
reincarnate.commands = ['reincarnate']
reincarnate.priority = 'low'
    
    