import random
import xmlrpclib

###A simple name generator using scrabble distribution

consonants = [('b',  2),('c',  2),('ch', 1),('d',  4),('f',  2),('g',  3),
	('h',  2),('j',  1),('k',  1),('l',  4),('m',  2),('n',  6),('p',  2),
	('q',  1),('qu', 1),('r',  6),('s',  4),('t',  6),('v',  2),('w',  2),
	('x',  1),('z',  1),]
vowels = [('a', 9),('e', 12),('i', 9),('o', 8),('u', 4),('y', 2)]

def selection(table):
	if type(table[-1]) is not type(0):
		s = 0
		for i in range(len(table)):
			s += table[i][1]
		table.append(s)
	else:
		s = table[-1]
	# now the selection
	n = random.randrange(s) + 1
	for i in range(len(table)-1):
		n -= table[i][1]
		if n <= 0:
			return table[i][0]
	# should not happen
	return ''

def simple_namegen(minsyl = 1, maxsyl = 3, n = 1):
	res = [] 
	for j in range(0,n):
		numsyl = random.randint(minsyl, maxsyl)
		word = []
		for i in range(numsyl):
			flag = 0
			if random.randrange(100) < 60:
				word.append(selection(consonants))
				flag = 1
			word.append(selection(vowels))
			if not flag or random.randrange(100) < 40:
				word.append(selection(consonants))
		res.append("".join(word))
	return res
	
###A name generator which grabs from dicelog.com

def web_namegen(minsyl = 1, maxsyl = 3, n = 1):
	proxy = xmlrpclib.ServerProxy("http://dicelog.com/yaf/rpc")
	return proxy.names(minsyl,maxsyl,n)
	
###A syllable agglutinator namegen for dragons

dragname = (('Vi','Ig','R','Ci','Ni','Ba','Be','Bi','Bre','Bry','Ca','Ce','Che','Ci','Co','Col',
	'Cu','Da','De','Do','Du','Em','Fe','Fi','Ga','Gi','He','He','Ho','In','Ir','Ith','Je','Ji',
	'Ka','Ke','Ki','Ko','Ky','Le','Li','Lo','Lu','Ly','Ma','Me','Mo','Mi','Mne','My','Na','Ne',
	'No','Pa','Pe','Po','Que','Qui','Quo','Ra','Re','Rho','Ri','Ro','Ru','Ry','Sa','Se','Sha',
	'She','Sho','Shu','Si','So','Ste','Su','Sy','Tae','Ta','Te','Ti','To','Tu','Ty','Va','Ve',
	'Vo','Ze','Zi','Ju','Hi','Fu','Bri','Oh','Gre','Gra','Av','Rha','Um','Hu','Nv','Ap','As','At',
	'Fa','Fra','Cor','Cul','Dal','Dar','Mer','Mar'),
	('ar','al','am','ath','an','ad','bi','el','en','lu','ta','thy','th','ir','il',
	'ith','in','re','ri','ro','ra','rth','rro','gh','ga','li','lth','lla','la','si',
	'sa','lo','vo','na','nth','ni','nnu','no','nno','ne','yo','yd','oth','dre','do',
	'de','da','du','mma','mro','mi','sso','ssi','zz','ze','vu','nni','ja','us','zo',
	'lle'))
	
def dragon_namegen(minsyl = 2, maxsyl = 4, n = 1):
	res = []
	for i in range(0,n):
		word = [random.choice([random.choice(dragname[0]) for k in range(0,6)])]
		numsyl = random.randint(minsyl,maxsyl)
		for j in range(0,numsyl):
			word.append(random.choice([random.choice(dragname[1]) for k in range(0,6)]))
		res.append("".join(word))
	return res
	
###Artifact generator!

arty = (("The Great","The Gray","The Black","The White","The Violent","The Deadly","The Gold",
	"The Powerful","The Lost","The Intrepid","The Ample","The High","The Grievous","The Prodigal",
	"The Terrible","The Vast","The Chief","The Master","The Commander","The Grand","The Noble",
	"The Holy","The Primal","The Noted","The Stately","The Royal","The Super","The Superior",
	"The Wise","The Famed","The Infamous","The Skilled","The Gilded","The Forged","The Stately",
	"The Guarded","The Guardian","The Acolyte","The Studious","The Brave","The Bold","The Dauntless",
	"The Gusty","The Feared","The Valiant","The Hero","The Gritty","The Rash","The Spectral",
	"The Righteous","The Blessed","The Perfect","The Pure","The Cured","The Gods'"),
	("Ablabius", "Abundanitus", "Agnellus", "Ammonianus", "Anicius", "Armenius", "Armentarius", 
	"Auxitius", "Avienus", "Beatus", "Bonifatius", "Callinicus", "Carinus", "Castinus", "Cerularius",
	"Constantianus", "Constantinianus", "Constantinus", "Dalmatius", "Decentius", "Domianus",
	"Domnicus", "Domninus", "Donus", "Dulcitius", "Florentinus", "Florentius", "Florian", 
	"Florus", "Francio", "Fructosus", "Fulgentius", "Gallienus", "Germanus", "Gratian", 
	"Honoratus", "Honorius", "Ianuarius", "Innocentius", "Iovinus", "Iovivus", "Lactanius", 
	"Latinius", "Leontius", "Macedonius", "Magnentius", "Marcian", "Martinianus", "Martyrius",
	"Maurentius", "Maurianus", "Mauricius", "Maurinus", "Maurus", "Maxentius", "Maximianus", 
	"Maximin", "Maximinus", "Mercurius", "Mundus", "Nepotian", "Nonnosus", "Nonnus", "Opilio", 
	"Palladius", "Paternus", "Patricius", "Paulus", "Pegarius", "Petronas", "Praesentinus", 
	"Praetextatus", "Principius", "Priscian", "Probus", "Regino", "Sebastianus", "Tribonianus", 
	"Tribunas", "Urbicus", "Venantius", "Venerandus", "Vetranis", "Viator", "Victorinus", 
	"Vigilius", "Vitlaun", "Vitalianus", "Vitalius", "Volusian"),
	(": A scimitar",": A cloak",": A belt",": A katana",": A broadsword",": A rapier",
	": A flintlock pistol",": A scabbard",": A leather boot",": A pointed hat",": A mace",
	": A caltrop",": A sling",": A scythe",": A blowgun",": A trident",": A dirk",": A sword",
	": A boomerang",": A staff",": A ring",": An amulet",": A charm",": A flower",": A seed",
	": A leather bracer",": A chainmail shirt",": A morning star",": A telescope",
	": An ancient book",": A tome",": A hooded cloak",": A club",": A branding iron",
	": An anvil",": A bellow",": A stone",": A rock",": A crystal",": A ruby",": An emerald stone",
	": A sapphire",": A gold ring",": A diamond",": A wristcuff",": A knife",": A pair of tongs",
	": A pair of calipers",": A locket",": A necklace",": A monocle",": A baldric",
	": A deck of cards",": A pipe",": A flute",": A lute",": A mandolin",": A bow",": A quiver",
	": A walking stick",": A big stick",": A glove",": A gauntlet",": A brooch",": A flask",
	": A canteen",": A mug",": A goblet",": A horn",": A bone",": A skull",": A thread",
	": A spindle",": A needle",": A pin",": A hairpin",": A torch",": A doll",": A hammer",
	": A mallet",": A nail",": A page",": A coin",": A gold coin",": A silver coin",": A pot",
	": A pan",": A ball",": A flagon",": A small box",": A snuffbox",": A length of twine",
	": A quilt",": A hook",": A bone",": A skull",": A kettle",": A helmet",": A bonnet",
	": A jar",": A wheel",": An orb",": A glass ball",": An ink bottle",": A bottle",
	": A feather",": A quill",": A pen",": A sock",": A bracelet",": A pelt",": A coat",
	": A jacket",": A flag",": A curtain rod",": A hand drill",": A tooth",": A fang",
	": A pail","A bucket",": A coinpurse",": A gemstone",": A fork",": A spoon",
	": A pair of chopsticks",": An arrow",": A dart",": A bolt",": A key",": A lockpick",
	": A pickaxe",": A pick",": A fan"),
	("with the","possessing the","harnessing the","that grants the","that invokes the",
	"that allows the"," that gifts the","that permits the"),
	("power of invisibility.","ability to create skeletal warriors.","power over the minds of others.",
	"ability to control fire.","ability to manipulate the wind.","power over water.",
	"power to control ice.","power over plants.","ability to erect invisible walls.",
	"mastery of all forms of martial arts.","ability to summon the dead.",
	"ability to awaken stone golems.","ability to control insects.","power to create small explosions.",
	"power to erase memories.","ability to foresee future events.","ability to read minds.",
	"power to read any language.","ability to speak any tongue.","power over the opposite sex.",
	"manipulation of gravity.","power of speed.","control over kinetic energy.",
	"power of superior sight.","ability to foresee future events.","power of energy blast.",
	"power to conduct electricity.","control of lightning.","manipulation of the weather.",
	"power to see in the darkness.","power of transmutation.",
	"ability to sap the strength from others.","power of teleportation.","ability to speak to animals.",
	"power to read minds.","ability to absorb spells.","power of shapeshifting.",
	"manipulation of clouds.","ability to heal.","capacity to cure male impotence.",
	"power of knowledge.","power to destroy.","power of fireball.","power to fling electric bolts.",
	"ability to spawn weapons.","ability to see great distances.",
	"manipulation of sonic frequencies.","power of sonic scream.","ability to summon dragons.",
	"ability to awaken the dead.","ability to summon ghosts.","ability to summon animals.",
	"offering of great wisdom.","power to freeze time.","power to paralyze.","ability to rain acid.",
	"ability to see through solid walls.","ability to leap great heights.","power to control odors.",
	"power to control the earth.","power of telekinesis.","manipulation of dirt.",
	"power to summon goblins.","ability to summon orcs.","ability to grow taller.",
	"ability to shrink oneself.","power to blot out the sun.","power to fly.",
	"ability to tunnel through the earth.","the power to stop human heart.","ability to kill on-sight.",
	"ability to throw cold energy.","ability to summon ancestral spirits.",
	"ability to commune with the dead.","ability to entrap people.","ability to create smoke.",
	"power of invulnerability.","power of crucifixion.","ability to purify water.",
	"ability to kill crops.","power to inflict disease.","manipulation of famine.",
	"power of memory loss.","power of lockpick.","power of stealth.","ability to breathe underwater.",
	"ability to walk on water.","ability to travel great distances.","ability to float.",
	"ability to poison.","ability to inflict pain.","power to ensnare.","power to attract.",
	"power of magnetism.","ability of superior agility.","power of great perception.",
	"ability to turn back time."))
	
def artygen(n = 1):
	res = []
	for k in range(0,n):
		rr = []
		for i in arty:
			rr.append(random.choice([random.choice(i) for j in range(0,6)]))
		res.append(' '.join(rr))
	return res


###MONSTER DESCRIPTION GENERATOR, courtesy of the awesome Swordgleam!
qmdesc = {'size':('bear-sized','bulky','diminutive','dog-sized','enormous',
	'horse-sized','hulking','human-sized','large','massive','medium-sized',
	'runty','small','tiny','towering'), 'type':('arachnoid','bat-like','bird-like',
	'canine','chimeric','demonic','draconic','equine','ethereal','feathered',
	'feline','fey','fiendish','frog-like','furred','humanoid','hybrid','infernal',
	'insect-like','mongrel','oozing','phantasmal','reptilian','rodent-like',
	'scaled','slimy','snake-like','undead','unnatural','ursine'), 'thing':(
	'creature','monster','beast'), 'lives':('lives','lairs','can be found',
	'makes its home','dwells'), 'place':('wooded areas','dungeons','caves',
	'mountains','plains','deep forests','underground caverns','mountainous areas',
	'volcanos','deserts','coastal areas','praries','temperate climates',
	'tropical climates','colder regions','icy climes','abandoned ruins',
	'deserted dwellings','city sewers','places touched by arcane power',
	'places touched by dark powers','places touched by otherworldly power',
	'secluded forests','deep lakes','the shadows of cities','forsaken wastelands',
	'deep canyons','lush valleys','island jungles','mountain passages',
	'untamed grasslands','marshes','bogs','swamps'), 'how':('lures','stalks',
	'lies in wait for','leaps upon','ensnares','stalks','tracks'), 'prey':(
	'other monsters of the same type','humans','small creatures','large creatures',
	'mundane beasts','magical beasts','monstrous humanoids','medium-sized creatures',
	'other predators'), 'attack':('fire','ice','venom','projectile weapons',
	'thrown weapons','an eldritch aura','draining magic','elemental magic',
	'a petrifying gaze','a hypnotic gaze','a hypnotic song','illusions',
	'lightning','acid','toxic bites','entangling webs','melee weapons',
	'piercing shrieks','necrotic energy','debilitating effects','psionics',
	'blinding light','creeping darkness','obscuring fog','acidic gas','scorching gas',
	'cold','electricity','sound','choking smoke','paralyzing toxins','noxious fumes',
	'grasping tentacles'), 'mattack':('rapid blows','dizzying blows','strangling grabs',
	'crushing blows','spikes','spines','a tail striker','slashing claws',
	'piercing claws','fangs'), 'weak':('fire','silver','cold iron','bronze',
	'certain herbs','holy icons','cold','heat','ice','certain sounds','bright light',
	'certain symbols','ash','oak','wooden weapons','enchanted weapons',
	'nonmagical weapons','a certain metal','a certain wood','certain talismans'),
	'dis':('dislikes','is weak against','can easily be injured with','fears',
	'can only be harmed by','is difficult to harm without','will flee from'), 'hl':(
	'hunt','lair','travel','live'), 'group':('groups','packs','prides','flocks',
	'mobs','bands','families','tribes'), 'rumor':('It is rumored that',
	'Rumor holds that','Legends say that','According to myth,','Rumor has it that',
	'Folktales say that','According to folktales,','Legend holds that',
	'Myths suggest that','It is believed that','Fragmentary myths suggest that',
	'Some legends say that','Local folktales say that'), 
	'rumor2':('they keep hordes of treasure','they posses arcane items',
	'they were created by a mad sorceror','they were created by an experiment gone wrong',
	'they were created by the gods','they are more ancient than humans',
	'they can live forever unless slain','they are reborn into a new form when slain',
	'they keep trophies from slain prey','they purposefully seek out adventurers to slay',
	'they will take vengeance for the death of their kin',
	'if their mate is slain, they will never rest until they have vengeance',
	'their hide can be made into tough armor',
	'their bones can be ground into powerful potions',
	'their claws can be used as ingredients for alchemy','they can see invisible beings',
	'eating their hearts gives a person some of their powers',
	'their eggs are powerful alchemical ingredients',
	'various body parts are much sought after as ritual components',
	'they prefer a certain type of weather','they only hunt when the moon is waning',
	'the soul of anyone slain by them will never find rest',
	'they migrate every once in a long while to a place no one has found',
	'their lairs are filled with traps','they often steal trinkets from civilized creatures',
	'they have a hidden, primitive civilization','they come from another world',
	'they are harbingers of something else','they cooperate with other monsters',
	'they are sometimes kept as pets by evil arcanists',
	'they are descended from a lost civilization',
	'they are not always violent, and sometimes merely play tricks on the unwary',
	'they can be negotiated with, though their demands are unusual',
	'there is something all of their kind seek','they can cast curses on those who injure them',
	'they are as smart as humans, and possibly smarter','they are holy to a certain cult',
	'they can move faster than the eye can see','the same one can appear in two places at once',
	'they seek out and attack a particular kind of person','they were born from nightmares',
	'their pelts are highly valued for making enchanted armor',
	'they are almost invulnerable when the sun is down',
	'they do most of their hunting at twilight','they are most vulnerable at dawn',
	'they are protected by a god','they are all telepathically linked to one another')}

def monster_gen(n = 1):
	ret = []
	for kk in range(0,n):
		sz = random.choice(qmdesc['size'])
		ty0 = random.randint(0,len(qmdesc['type']))
		typ = qmdesc['type'][ty0]
		if random.randint(0,1): 
			', '.join([typ,random.choice([x for x in qmdesc['type'] if x != typ])])
		th = random.choice(qmdesc['thing'])
		lv = random.choice(qmdesc['lives'])
		pl = random.choice(qmdesc['place'])
		desc1 = 'This '+' '.join([sz,typ,th,lv,'in',pl+'.'])
		if random.randint(0,1):
			hw = random.choice(qmdesc['how'])
			pt = 'its prey, which includes'
			z = random.randint(1,3)
			if z > 1:
				pr = ''
				for i in range(0,z):
					pr += random.choice([x for x in qmdesc['prey'] if x not in pr])+', '
			else: pr = random.choice(qmdesc['prey'])
			pr += 'and '+random.choice([x for x in qmdesc['prey'] if x not in pr])
			desc2 = ' '.join(['It',hw,pt,pr+'.'])
			desc = ' '.join([desc1,desc2])
		else: desc = desc1
		pt = 'It attacks with'
		matk = random.choice(qmdesc['mattack'])
		z=0
		if random.randint(0,2) != 1: z += 1
		if random.randint(0,5) == 1: z += 1
		atk = ''
		for i in range(0,z):
			atk += random.choice([x for x in qmdesc['attack'] if x not in atk])+', '
		atk += 'and '+random.choice([x for x in qmdesc['attack'] if x not in atk])
		if not atk.startswith('and'):
			matk += ','
		desc = ' '.join([desc,pt,matk,atk+'.'])
		if random.randint(0,2) == 1: 
			desc = ' '.join([desc,'It',random.choice(qmdesc['dis']),
				random.choice(qmdesc['weak'])+'.'])
		if random.randint(0,9) > 5:
			hl = random.choice(qmdesc['hl'])
			if random.randint(0,5) == 1: 
				grp = 'alone'
			else:
				r1 = random.randint(1,5)
				r2 = random.randint(1,20)+r1
				grp = ' '.join(['in',random.choice(qmdesc['group']),'of',
					'-'.join([str(r1),str(r2)])])
			desc = ' '.join([desc,'They',hl,grp+'.'])
		if random.randint(0,9) > 5:
			desc = ' '.join([desc,random.choice(qmdesc['rumor']),random.choice(qmdesc['rumor2'])+'.'])
		ret.append(desc)
	return ret
	
	
#Tavern name generator!
tvrn=(("Angry ","Berserk ","Black ","Blind ","Bloody ","Blue ","Brass ","Broken ","Cheerfull ",
	"Crimson ","Dancing ","Dark ","Dead ","Death's ","Dirty ","Doomed ","Drunken ","Fiery ",
	"Flying ","Golden ","Growling ","Howling ","Hungry ","Iron ","Jovial ","Joyfull ","Laughing ",
	"Leaping ","Little ","Lone ","Mighty ","Murky ","Mystic ","Nine ","Old ","Olden ","Pale ",
	"Rouge ","Ruddy ","Running ","Savage ","Scarlett ","Screaming ","Seven ","Silver ","Sleeping ",
	"Small ","Staggering ","Stone ","Toothless ","Twin ","White ","Wild ","Winking ",""),
	("Ale ","Angel ","Archer ","Arms ","Balrog ","Bandit ","Bard ","Barrel ","Battle Axe ","Begger ",
	"Bottle ","Centaur ","Champion ","Crossroads ","Cyclops ","Dagger ","Demon ","Dragon ","Dwarf ",
	"Fist ","Flame ","Flask ","Flood ","Fox ","Gargoyle ","Gazelle ","Giant ","Goblet ","Goblin ",
	"Godling ","Griphin ","Grog ","Hand ","Harpy ","Helm ","Heretic ","Hippogriff ","Hunter ","Kelpie ",
	"Knave ","Knight ","Knuckle ","Lance ","Lion ","Litch ","Lizard ","Minotaur ","Naga ","Nobleman ",
	"Nymph ","Ogre ","Orc ","Prophet ","Rat ","Rouge ","Sage ","Scepter ","Scribe ","Spirits ","Squire ",
	"Sword ","Tankard ","Titan ","Traveller ","Troll ","Unicorn ","Vagabond ","Vixen ","Wanderer ",
	"Warrior ","Wench ","Wheel ","Wind ","Wolf "),
	("Alehouse","Cellar","Clubhouse","Guesthouse","House","Inn","Lodge","Meadhall","Resthouse",
	"Tavern","Hall","Grogshop","Taproom","Barroom"))
	
def taverngen(n = 1, long = False):
	ret = []
	for kk in range(0,n):
		res = random.choice([random.choice(tvrn[0]) for i in range(0,6)])
		res += random.choice([random.choice(tvrn[1]) for i in range(0,6)]) 
		if long:
			res += random.choice([random.choice(tvrn[2]) for i in range(0,6)])
		ret.append(res)
	return ret
	
#riddle generator, using wordlock chest riddles from betrayal at krondor

riddles={"HANGMAN":"Swollag, the famous drow craftsman, guarantees his work until the end of time.",
	"FIRE":"The chill of its death, you may soon mourn. But though it dies, It cannot be born.",
	"RAIN":"You see it about in field and town. It cannot get up, but will oft fall down.",
	"DEAD":"They feel no pain, no sorrow, no greed. They have no anger, no hatred, nor need.",
	"SMOKE":"Though easy to spot when allowed to plume, it is hard to see, when held in a room.",
	"EYES":"Be you ever so quick, with vision keen, by your eyes we are never seen -- unless, perchance, it should come to pass, you see our reflection in a looking glass.",
	"RING":"A precious gift, this, yet it has no end or beginning, and in the middle, nothing.",
	"SHADOW":"Silently he stalks me: running as I run, creeping as I creep. Dressed in black, he disappears at night, only to return with the sun.",
	"GLOVES":"Buckets, barrels, baskets, cans; what must you fill with empty hands?",
	"ARROW":"It flies without wings, strikes without beak, teeth, or talons. It has no eyes in its pointed head, but it can kill birds in flight.",
	"STAIRS":"Up and down they go, but never move...",
	"CANDLE":"He gets short when he gets old; he goes out, then it gets cold.",
	"WIND":"The strongest chains will not bind it, ditch and rampart will not slow it down. A thousand soldiers cannot beat it, and it can knock down trees with a single push.",
	"RIVER":"An untiring servant it is, carrying loads across muddy earth. But one thing that cannot be forced is a return to the place of its birth.",
	"SWORD":"With sharp edged wit and pointed poise, it can settle disputes without a noise.",
	"ICE":"Power enough to smash ships and crush roofs, yet it still must fear the sun.",
	"ALCOHOL":"Today he is there to trip you up, and he will torture you tomorrow; yet he is also there to ease the pain when you are lost in grief and sorrow.",
	"HOLE":"It can hold you, but you cannot hold it, and the more you remove, the bigger it will get.",
	"RUST":"It can pierce the best armor, and make swords crumble with a rub; yet for all its power, it can't harm a club.",
	"VICTORY":"With this one thing alone, you will have defeated even the strongest foe.",
	"THORN":"He got it in the woods and brought it home in his hand because he couldn't find it. The more he looked for it, the more he felt it. When he finally found it, he threw it away.",
	"HOLES":"A barrel of rainwater weighs twenty pounds. What must you add to make it weigh fifteen?",
	"HAIR":"Human babes are born without a lot of this, there is no doubt.",
	"NOTHING":"We love it more than life, fear it more than death. The wealthy want for it, while the poor have it in plenty.",
	"KNOCKER":"Asks no questions, but demands many answers. Don't knock it until you are ready to see what waits on the other side.",
	"RIDDLE":"At last you have the answer to this.",
	"MILK":"You can spin, wheel and twist, but it can turn without moving.",
	"BARD":"Who works when he plays, and plays when he works?",
	"SILENCE":"Names give power, for magic to control. But, what is broken by naming it?",
	"WRONG":"The language of men can be mastered. But what word is always pronounced wrong?",
	"CARDS":"Brought to the table, cut and served, never eaten.",
	"PEACE":"Widows and orphans, parents and kin, this is disturbed most by riots and war.",
	"SHADOWS":"They can move over water, but cannot fly. They can move under water, but stay quite dry.",
	"WAGON":"It has a tongue, but cannot talk; it runs, but cannot walk.",
	"SAWS":"We don't need wine, we don't need meat. We have sharp teeth, but cannot eat.",
	"TABLE":"It stands while others sit, groans when it is too full, has four legs, but cannot run.",
	"WALL":"It goes past gates, but asks no one's leave. It runs clear around castles without taking a step.",
	"SUNSHINE":"Never resting, never still, moving silently, hill to hill. It does not walk, run or trot; all is cool where it is not.",
	"NAME":"Passed from father to son, and shared between brothers, its importance is unquestioned, though it is used more by others.",
	"COFFIN":"The one who made it didn't want it. The one who bought it didn't need it. The one who used it never saw it.",
	"COLTS":"What has a mare, that the cow has not?",
	"OUTSIDE":"This side of a wolfhound has the most hair.",
	"WHEELBARROW":"Two legs it has, and this will confound: only at rest do they touch the ground.",
	"ONION":"She has tasteful friends and tasteless enemies. Tears are often shed on her behalf, yet never has she broken a heart.",
	"SPIDER":"In all the world, none can compare to this tiny weaver, her deadly cloth so silky and fair.",
	"BREATH":"You can see it in winter, never in summer. Even though it is as light as a feather, the mightiest dwarf can't hold it for long.",
	"YESTERDAY":"Every creature in the world has seen it, but to their dying day they'll never see the same one again.",
	"BOTTLE":"Soldiers will look like it, when the headsman gives them a lop, for then, like it, they'll have a neck, but not a head on top.",
	"GAUNTLET":"What is the thing, with fingers long, that grips our deadly swords so strong?",
	"HORSEMAN":"Six legs, two heads, two hands, one long nose, yet he uses only four legs wherever he goes.",
	"COALS":"Black when bought, red when used, grey when thrown away.",
	"SECRET":"It is too much for one; two it is meant for, but it no longer exists when the two become more.",
	"FUTURE":"It never was before, it is not now. Fools wait for it forever.",
	"PADDLE":"Held firmly in the hands, like a sword it cuts deep. Bloodless strokes, all, then forward we leap.",
	"SNAIL":"Bloodless and boneless, it travels about, yet it never leaves home.",
	"BELL":"You hear it speak, for it has a hard tongue; but it cannot breathe, for it has not a lung.",
	"SHOE":"Has a tongue, but never talks; has no legs, but sometimes walks.",
	"STOVE":"You seek it out when your hunger's ripe. It sits on four legs and smokes a pipe.",
	"MATTRESS":"Has feathers but can't fly; rests on legs but can't walk.",
	"SQUARE":"One pace to the North, two paces to the East, two paces to the South, two paces to the West, one pace to the North.",
	"SNOWFLAKE":"It flies without wings, drops without fear; but held in warm hands, it will soon disappear.",
	"FLEAS":"When they are caught, they are thrown away. When they escape, you itch all day.",
	"THISTLE":"He stands beside the road in a purple cap and tattered green cloak. Those who touch him, curse him.",
	"BROOM":"All about the house, with his Lady he dances, yet he always works and never romances.",
	"PATH":"All across the countryside, to front doors he travels, but you never invite him in.",
	"KEY":"Axes and swords will not help you through, yet it and a little push will do. Some in the road would have fought and soon died, were it not close at hand to let them inside.",
	"SURF":"Pounds all day, beats all night, never rests.",
	"WATERFALL":"This old one runs forever, but never moves at all. He has not lungs nor throat, but still lets forth a mighty roaring call.",
	"DICE":"You can count on them, though some would rather curse them. You can speak dear to them, though well all know 'tis just in vain.",
	"LOGS":"They have not lips nor tongues, yet lead them green to the pit, and as they die you will hear them sputter, hiss and spit.",
	"FARRIER":"There is a shoemaker in the dell who makes his shoes with steel and nail. Although his goods last right well, folks need two pair, without fail.",
	"BRIDGE":"When it is stout, people gladly tread. When it is thin, people walk in dread.",
	"MIRROR":"Look in my face, and I am somebody. Look at my back, and I am nobody.",
	"BOOK":"It is a journey whose path depends on another's vision of where it ends.",
	"BLADE":"Blessed are the first. Slow are the second. Playful are the third. Bold are the fourth. Brave are the fifth.",
	"ASHES":"After the final fire, the winds will blow, and these, which are already dead, will cover the ones who have yet to die.",
	"ORANGE":"Men seize it from its home, tear apart its flesh, drink the sweet blood, then cast its skin aside.",
	"ICICLE":"You see me oft in woods and town. With my roots above, I must grow down.",
	"GRAVE":"A strange earthen house that brings nought but disdain; and yet, those who stay there never do complain.",
	"RAINDROPS":"With flashing sword and booming cry, with darkness staining land and sky, the army comes, prepared to die. Soldiers fall in glistening dress, as battles are joined without egress, save comfort in the earth's caress.",
	"STARS":"The wheel is steered despite the night; they prefer our lead more than the light.",
	"SADDLE":"When it is down, it is lower than a horse's belly; when it is up, it is higher than a horse's back.",
	"SPONGE":"Holes at the top, holes at the bottom, holes in the middle, but still it holds water.",
	"BRIARS":"Claws like a cat, crooked as a snake's hiss. Patch together your guesses, you won't guess this.",
	"SIEVE":"Rounds as an apple, deep as a cup, all the water in the sea can't fill it up.",
	"DRUM":"Although my cow is dead, I continue to beat her -- what a racket she makes!",
	"BUTTON":"Flat as a leaf, round as a ring, I have two eyes, but can't see a thing.",
	"TRADE":"Two brothers wanted to race a course, to see which had the slowest horse. Since neither wanted to spur his mare, what must they do to make it fair?",
	"WALNUT":"A box beneath a tree, inside some tasty meat. Kept for a month or more, it still tastes just as sweet.",
	"PIPE":"Its tail is round and hollow, seems to get chewed a bit, but you'll rarely see this thing, unless the other end is lit.",
	"DOOR":"It doesn't live within a house, nor does it live without. Most will use it when they come in, and again when they go out.",
	"BOOK":"Though not a plant, has leaves. Though not a beast, has spine. Though many wouldn't need this thing, 'tis more valuable than wine.",
	"PLOW":"Four legs in front, two behind, its steely armor scratched and dented by rocks and sticks, still it toils as it helps feed the hungry.",
	"BULL":"In the fields a frightful thing, watch it and you will find it has a pitchfork in the front, and a broom back behind.",
	"PROMISE":"You will keep this only after you have given it.",
	"DEATH":"What is this thing that having it, you can no longer give it away, but lacking it, for the moment at least, you can give it to those who must pay?",
	"ARGUMENT":"Whoever has it is angry, whoever loses it is angrier, and whoever wins it has it no more.",
	"MUSIC":"This wondrous thing, though not an herb, can help comfort the weak and the dying. It can even be used to rally the troops, or make one start laughing or crying.",
	"BUBBLE":"This sparkling globe can float on water, and weighs not more than a feather. Yet despite its weight ten giants could never pick it up.",
	"ROPE":"Ten troll's strength, ten troll's length; one troll can pick it up, no troll can stand it up.",
	"OCEAN":"A shimmering field that reaches far, yet it has no tracks, and is crossed without paths.",
	"SHOES":"You tie these things before you go, and untie them after you stop.",
	"DARKNESS":"This engulfing thing is strange indeed; the greater it grows, the less you see.",
	"LIFE":"Don't grow too attached to this thing. Without it you will never even know it is gone. But be careful friend, it is much easier to lose in the Dungeon.",
	"JACKET":"Neck, but no head; arms, but no hands; waist, but no legs.",
	"SAWDUST":"A carpenter left some wood, would not take it back. I saw some dust where he left it, but couldn't find his stack.",
	"NOOSE":"Once alive, but now twisted 'round. It is used by elves and men to punish their own kind.",
	"EGGS":"No visible flesh, nor blood, nor bone, but given time, they will walk alone.",
	"FIRE":"Put into a pit, locked behind a steel grate, guarded all through the night, still it goes out.",
	"ECHO":"Answers its caller without being asked. Responds within seconds, and speaks all languages with equal ease.",
	"ALPHABET":"This marvelous thing, though it sounds absurd, contains all letters, but is only a word.",
	"PRIEST":"This fool has married many women, yet he has never been married.",
	"TOWEL":"This odd thing seems to get wetter the more it dries.",
	"CANE":"Though blind as well, can lead the blind well.",
	"CAT":"What goes down to the cellar with four legs, but comes back with eight?",
	"TEMPER":"You must keep this thing. Its loss will affect your brothers, for once yours is lost, it will soon be lost by others.",
	"HONEY":"Though a tasty treat made in spiral towers, rarely will it be eaten alone.",
	"WATER":"This great thing can be swallowed, but can also swallow us.",
	"HASTE":"Inside a burning house, this thing is best to make, and best to make it quickly before the fire's too much to take.",
	"TIRED":"Plow and hoe, reap and sow, what soon does every farmer grow?",
	"ADVICE":"Everyone offers this thing, but few will take it when it is offered by someone else.",
	"STRANGER":"You will invite him into your house, yet you know him not. Once you get to know him, this thing he will no longer be.",
	"LAKE":"I saw him where he never was, and where he could not be. And yet within this place, I saw a wavering face staring back at me.",
	"SPURS":"We travel much, yet prisoners are, end close confined, to boot. Yet with any horse we will keep pace, and always go on foot.",
	"GALLOWS":"When people come for me to meet, they come to me with heavy feet. The one I hold, when I get my chance, will turn and spin and start to dance.",
	"FOG":"When it comes in from sea to shore, twenty paces you'll see -- no less, no more.",
	"BARK":"Like dogs shouting at the moon, or armor worn by the trees. Like a sharply spoken command, or a tiny vessel upon the seas."}
	
def riddlegen(n = 1):
	ret = []
	for i in range(n):
		ans = random.choice([random.choice(riddles.keys()) for j in range(6)])
		rid = riddles[ans]
		ret.append((ans,rid))
	if n == 1:
		ret = ret[0]
	return ret
	
	
#generate a random set of numbers, as a string

def numgen(l = 4, n = 1):
	ret = []
	for i in range(n):
		ans = ''
		for j in range(l):
			ans += str(random.randint(0,9))
		ret.append(ans)
	if n == 1:
		ret = ret[0]
	return ret
	
#produce a random deity from the Lovecraft mythos
gods=("Abholos, Devourer in the Mist","Alala, Herald of S'glhuo","Ammutseba, Devourer of Stars","Aphoom-Zhah, the Cold Flame",
	"Apocolothoth, the Moon-God","Arwassa, the Silent Shouter on the Hill","Atlach-Nacha, Spinner in Darkness","Ayi'ig, the Serpent Goddess",
	"Aylith, the Many-Mother","Baoht Z'uqqa-Mogg, the Bringer of Pestilence","Basatan, Master of the Crabs","B'gnu-Thun, the Soul-Chilling Ice-God",
	"Bokrug, the Doom of Sarnath","Bugg-Shash, He Who Comes in the Dark","Byatis, the Berkeley Toad","Chaugnar Faugn, Horror from the Hills",
	"Coatlicue, Serpent Skirted One","Coinchenn","Crom Cruach, Master of the Runes","Cthaat, the Dark Water God","Cthaeghya","Cthugha, the Living Flame",
	"Dread Cthulhu","Cthylla, Secret Daughter","Ctoggha, the Dream-Daemon","Cyaegha, the Waiting Dark","Cynothoglys, She Whose Hand Embalms",
	"Dhumin, Eidolon of the Blind","Dygra, the Stone-Thing","Dythalla, Lord of Lizards","Dzewa, the White God","Eihort, the Pale Beast",
	"Ei'lor, the Star-Seed","Etepsed Egnis","Ghadamon, Seed of Azathoth","Ghatanothoa, Lord of the Volcano","Ghisguth, the Sound of the Deep Waters",
	"Glaaki, Lord of Dead Dreams","Gleeth, the Blind God of the Moon","Gloon, the Corrupter of Flesh","Gog-Hoor, Eater on the Insane",
	"Gol-goroth, God of the Black Stone,","Golothess, the Horror Under Warrendown","Groth-Golka, the Bird-God of Balsagoth",
	"Gtuhanai, the Destroyer God of the Aartna","Gurathnaka, Eater of Dreams","Gur'la-ya, Lurker in Doom-laden Shadows","Gzxtyos, Mate of Othuyeg",
	"Han, the Dark One","Hastalyk, the Contagion","Hastur, the King in Yellow","H'chtelegoth, the Great Tentacled God","Hziulquoigmnzhah, the God of Cykranosh",
	"Idh-yaa, Xothic Matriarch","Inpesca, the Sea Horror","Iod, the Shining Hunter","Istasha, Mistress of Darkness","Ithaqua, God of the Cold White Silence",
	"Janai'ngo, Guardian and the Key of the Watery Gates","Juk-Shabb, God of Yekub","Kaalut, the Ravenous One","Kag'Naru of the Air",
	"Kassogtha, Leviathan of the Diseased","Kaunuzoth, the Great One","Khal'kru, All-in-All, Greater-than-Gods","Klosmiebhyx","K'nar'st, Spawn of the Forgotten",
	"Kurpannga, the Devil-dingo","Lam, the Grey","Lythalia, the Forest-Goddess","Mappo no Ryujin, Harbinger of Doom","M'basui Gwandu, the River Abomination",
	"M'Nagalah, the Cancer God","Mnomquah, Lord of the Black Lake","Mordiggian, the Charnel God","Mormo, the Thousand-Faced Moon","Mortllgh, Storm of Steel",
	"Mynoghra, She-Daemon of the Shadows","Nctosa & Nctolhu, the Twin Spawn","Ngirrth'lu, Stalker in the Snows","Northot, the Thing That Should Not Be",
	"Nssu-Ghahnb, Leech of the Aeons","Nug and Yeb, the Twin Blasphemies","Nyaghoggua, the Kraken Within","Nycrama, the Zombifying Essence",
	"Nyogtha, Haunter of the Red Abyss","Ob'mbu, the Shatterer","Oorn, Mnomquah's Mate","Othuum, the Oceanic Horror","Othuyeg, the Doom-Walker",
	"Pharol the Black","Poseidon","Psuchawrl, the Elder One","Ptar-Axtlan, the Leopard That Stalks the Night","Quachil Uttaus, Treader of the Dust",
	"Quyagen, the Eye of Z'ylsm","Q'yth-az, the Crystalloid Intellect","Raandaii-B'nk","Ragnalla, Seeker in the Skies","Raphanasuan, the One From Sun Race",
	"Rhan-Tegoth, He of the Ivory Throne","Rhogog, the Bearer of the Cup of the Blood of the Ancients","Rh'Thulla of the Wind","Rlim Shaikorth, the White Worm",
	"Rokon","Ruhtra Dyoll, the Fire God","Saa'itii, the Hog","Scathach","Sebek, the Crocodile God","Sedmelluq, the Great Manipulator","Sfatlicllp, the Fallen Wisdom",
	"Shaklatal, Eye of Wicked Sight","Shathak, Death Reborn","Shaurash-Ho","Sheb-Teth[, Devourer of Souls","Shlithneth","Sho-Gath, the God in the Box",
	"Shterot, the Tenebrous One","Shudde M'ell, the Burrower Beneath","Sthanee, the Lost One","S'tya-Yg'Nalle, the Whiteness",
	"Summanus, the Terror that Walketh in Darkness","Swarog","Thanaroa, the Shining One","Tharapithia, the Shadow in the Crimson Light","Thog, the Demon-God of Xuthal",
	"Th'rygh, the Godbeast","Tsathoggua, the Sleeper of N'kai","Tulushuggua, the Watery Dweller Beneath","Turua, Father of the Swamps","Uitzilcapac, Lord of Pain",
	"Ut'Ulls-Hr'Her, Black Glory of the Creation","Vhuzompha, Mother and Father of the Seas","Vibur, the Thing from Beyond","Vile-Oct",
	"Volgna-Gath, Keeper of the Secrets","Voltiyig, Terrifying Son","Vthyarilops, the Starfish God","Vulthoom, the Worm that Gnaws in the Night","Xalafu, the Dread One",
	"Xcthol, the Goat God","Xinlurgash, the Ever-Consuming","Xirdneth, Lord of Unreality","Xotli, the Black Kraken of Atlantis","Xoxiigghua","Yegg-Ha, the Faceless One",
	"Y'golonac, the Defiler","Yhagni","Yhashtur, the Worm-God of the Lords of Thule","Yig, Father of Serpents","Y'lla, Master of the Seas","'Ymnar, the Dark Stalker",
	"Yog-Sapha, the Dweller in the Depths","Yorith, the Oldest Dreamer","Ysbaddaden, Chief of the Giants","Ythogtha, the Thing in the Pit",
	"Yug-Siturath, the All-Consuming Fog","Zathog, the Black Lord of Whirling Vortices","Zhar and Lloigor, the Twin Obscenities","Zindarak, the Fiery Messenger",
	"Zoth-Ommog, Dweller in the Depths","Zstylzhemghi, Matriarch of Swarms","Zushakon, Old Night","Z'toggua","Zvilpogghua, Feaster from the Stars","Abhoth",
	"Aiueb Gnshal","Azathoth","Azhorra-Tha","The Blackness from the Stars","The Cloud-Thing","C'thalpa","Cxaxukluth","Daoloth","D'endrrah","Ghroth","Gi-Hoveg",
	"Haiogh-Yai","Huitloxopetl","the Hydra","Ialdagorth","Kaajh'Kaalbh","Lu-Kthu","Mh'ithrha","Mlandoth and Mril Thorion","Mother of Pus","The Nameless Mist",
	"Ngyr-Korath","Nyctelios","Olkoth","Shabbith-Ka","Shub-Niggurath","Star Mother","Tru'nembra","Tulzscha","Ubbo-Sathla","Uvhash","Xa'ligha","Xexanoth",
	"Ycnagnnisssz","Yhoundeh","Yibb-Tstll","Yidhra","Yomagn'tho")
	
def godgen(n = 1):
	ret = random.choice([random.sample(gods,n) for j in range(6)])
	if len(ret) == 1:
		return ret[0]
	return ret