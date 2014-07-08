import web
import random, shelve, os, re

def make_dialect(which, text):
    t = text
    dialects = shelve.open(os.path.expanduser('~/eiko/usrmod/dialects'))
    opt = which.lower()
    if 'chef' in opt or 'swedish' in opt:
        subs = dialects['chef']
    elif 'olde' in opt:
        subs = dialects['olde']
    elif 'fudd' in opt:
        subs = dialects['fudd']
    for frompat, topat in subs:
        t = re.sub(frompat, topat, t)
    return t

mAttributeNames = ("Athletics", "Affection", "Skill", "Cunning", "Luck", "Will")
mTypes = {'lolita': (-1, 0, 0, 0, 1, 0),
          'sexy':   ( 0, 0, 0, 1, 0,-1),
          'pure':   ( 0, 1, 0,-1, 0, 0),
          'cool':   ( 0,-1, 1, 0, 0, 0),
          'boyish': ( 1, 0,-1, 0, 0, 0),
          'heroic': ( 0, 0, 0, 0,-1, 1)}
mColors = ('red', 'purple', 'orange', 'pink', 'brown', 'vermillion',
'purple', 'blue', 'green', 'sky blue', 'navy', 'indigo',
'orange', 'green', 'yellow', 'cream', 'beige', 'gold',
'pink', 'sky', 'cream', 'white', 'gray', 'silver',
'brown', 'navy', 'beige', 'gray', 'black', 'metallic',
'vermillion', 'indigo', 'gold', 'silver', 'metallic', 'transparent or rainbow')
mQualities = ("wears glasses", "has freckles", "has an incurable disease",
              "is the cool quiet type", "is easygoing", "is a neat freak",
              "is brown-skinned", "is albino", "is very shy",
              "is actually a guy (or hermaphrodite)", "has an overactive imagination",
              "will do anything for the sake of money", "has pointed ears",
              "is a catgirl", "is an android", "is a vampire",
              "is a princess from a family more important than her master's",
              "is an angel or devil",
                  ("wears tights rather than a skirt", "wears a china dress", "has a suit of armor for a uniform",
                   "has a uniform that looks oddly like bondage gear", "wears a very short skirt",
                   "dresses in Japanese-style clothing"),
                  ("bears a skull symbol somewhere on her clothing or body", "bears a bat symbol somewhere on her clothing or body",
                   "bears a cross symbol somewhere on her clothing or body", "bears a yin-yang symbol somewhere on her clothing or body",
                   "bears a star symbol somewhere on her clothing or body", "bears the symbol of a playing card suit somewhere on her clothing or body"),
                  ("always has a cigarette or cigar in her mouth", "has one or more tattoos",
                   "wears sunglasses or mirror shades at all times",
                   "always has an unpleasant expression on her face",
                   "has some kind of body piercings",
                   "talks like a gangster"),
                  ("speaks with a Southern accent", "speaks with a British accent",
                   "speaks English only as a pidgin language", "makes frequent cat noises",
                   "speaks like a medieval knight", "is a foreigner"),
                  ("has hair done up in long ringlets", "has odango hair",
                   "wears a mesh haircut", "has gravity-defyingly curly hair",
                   "has hair that covers one of her eyes",
                   "has a hair antenna with a mind of its own (or two of them)"),
                  ("wears a collar like a dog's", "wears a large ribbon in her hair",
                   "has spikes on her uniform", "has chains dangling from her uniform",
                   "wears black leather gloves", "is always accompanied by her pet"),
                  ("is related to another character by blood",
                   "is childhood friends with another character",
                   "looks on another character as a mentor or even a mother/father figure",
                   "has a friendly rival among the other characters",
                   "is a love rival or ex-lover of another character",
                   "has sworn vengeance against another character for something they may not even remember"),
                  ("is a nymphomaniac", "is a sadist", "is a masochist", "is a womanizer",
                   "is attracted to youth", "is an exhibitionist"),
                  ("has a bad habit of killing people", "is a pyromaniac", "is a kleptomaniac",
                   "has some kind of chemical addiction", "is a huge otaku of some type",
                   "is stalking her master or another maid"),
                  ("has stitches all over her body like patchwork", "has only one eye",
                   "has painful-looking burns", "carries scars from whipping", "wears a lot of bandages",
                   "is blind"),
                  ("can never seem to make a relationship work",
                   "has avoided forming close relationships since the death of her lover",
                   "killed her last lover and fears she'll do it again",
                   "used to work as a cheap prostitute and hasn't fully recovered from the experience",
                   "has had trust issues since she was betrayed by the last person she loved",
                   "was once targeted by a stalker and fears members of their gender"),
                  ("has a secret past as a delinquent", "was once a hired killer",
                   "has lost some or all memories of her childhood", "has a legendarily bad reputation",
                   "is wanted by the police for questioning", "ran away from home"),
                  ("has more than once attempted suicide", "is responsible for the death of her parents",
                   "saw her parents die in front of her", "hates her sister(s)",
                   "suffered a family breakup", "was abused by her parents"),
                  ("is secretly an assassin", "is secretly a hacker", "is secretly a mad scientist",
                   "secretly works as a doctor or pharmacist", "is secretly a doujin artist",
                   "is secretly a famous artist or writer of some kind"),
                  ("is part of a plot to conquer or destroy the world",
                   "is a spy or secret agent", "is a member or leader of a cult",
                   "is part of some political organisation",
                   "is part a secret (possibly mystical) order that dates back to ancient times",
                   "is a government official such as a nurse or an undercover detective"),
                  ("is actually a kitsune", "is actually a shapeshifting spider",
                   "is actually a shapeshifting raven", "is actually a shapeshifting rabbit",
                   "is actually a shapeshifting big cat", "is actually a shapeshifting snake"),
                  ("is a mermaid", "is a zombie or mummy", "is a werewolf or weretiger",
                   "is a succubus", "is a ghost", "is a shinigami"),
                  ("is a priestess", "is an onmyouji", "is a fortuneteller",
                   "is a Western-style sorcerer or wizard", "is a demon summoner", "is a necromancer"),
                  ("is an alien", "is a cyborg", "is a runaway ninja", "is a magical girl",
                   "is a fairy", "is a mutant")
              )

mReasons = ("because of her family's huge debts", "because she's a slave",
            "but she's more like her master's lover",
            "in order to get closer to her master so she can take revenge",
            "because the house took her in after her parents died",
            "because she's an illegitimate child of the house",
            "because her family have served her master's for generations",
            "to punish herself for her inexperience or sins",
            "out of unrequited love for her master",
            "because it pays well",
            "to spy on or assassinate her master",
            "out of loyalty to her master",
            "because her master is a childhood friend",
            "because she has always admired them",
            "to repay a great favor that her master did for her",
            "because her master is a distant relative and she's been placed in their care",
            "to train herself into the ideal bride",
            "for reasons even she herself isn't sure of")
mStresses = ("drinking or taking drugs", "stealing things", "attacking people", "gambling",\
             "driving at dangerous speeds", "teasing the other maids", "playing pranks",\
             "running away", "complaining about everything", "locking herself in her room",\
             "crying", "breaking things", "shopping", "sleeping all day", "overeating",\
             "praying", "acting like a spoiled child", "unknown means")
mWeapons = ("a mop or broom", "a stun gun", "a kitchen knife", "a frying pan",
            "a vase, bottle or pot", "her bare hands", "a revolver", "a machinegun",
            "a rifle", "bombs or grenades", "a bazooka", "a ray gun",
            "a pipe or a board with nails in it", "a hammer", "a scythe",
            "a kung fu weapon like nunchucks or a three-section staff",
            "a chainsaw", "a wooden sword or staff", "an axe or hatchet",
            "a flail or morningstar", "a western-style sword", "a whip or whip-like weapon",
            "a spear or lance", "an exotic weapon like a boomerang or qatar",
            "a knife or scalpel", "a chain or rope", "claws or claw-like weapons",
            "a katana", "shuriken or kunai", "a polearm", "a summoned helper", "magic",
            "psychic powers", "a book", "weapons built into her body", "a religious symbol")

mPowers = (("Super Evasion (In exchange for 1d6 Stress, you can completely avoid a single attack.)",
            "Iron Wall (You can use your Athletics attribute to defend up to two other characters.)",
            "Trespass (You can take 1d6 Stress to intrude on a battle, love scene, etc. You can also butt in after the action has ended, and this can even work when someone is using World For Two.)",
            "Weapon from Nowhere (You can pull your weapon out seemingly from nowhere, and get in a surprise attack. If you make a surprise attack, you get to make an attack roll without the target getting to make an opposed roll.)",
            "Giant Weapon (You can attack with a giant weapon. (+1 to Athletics for attacking).)",
            "Ultimate Retort (You can blow off an opponent completely by delivering a good retort (GM decides). You can make it impossible to defend against this by taking 2 Stress. (This must be role-played)."),
           ("Maiden's Tears (By taking 2D6 Stress, you can make a request that can't be refused. (This must be role-played).)",
            "World for Two (By taking 1D6 Stress, you can create a \"world\" for you and one other person, where for 5 minutes no one else can intrude.)",
            "Power of Friendship (You can take 1D6 Stress in order to remove 2D6 Stress from someone else.)",
            "Cooked with Love (When someone eats food you've prepared, they lose 1D6 Stress.)",
            "Windows of the Soul (You understand the master's feelings better than anyone, and can offer careful help. (Add 2 to Favor gained).)",
            "Passionate Gaze (With just a glance, you can ingratiate yourself with the master, taking 1D6 Stress to gain 1D3 Favor.)"),
           ("Lock Picking (You can enter any room whenever you feel like. This works even when someone is using World for Two.)",
            "Stalking (When you're following someone, there's no chance for them to detect you. Don't even bother rolling dice.)",
            "Lie Detector (By taking 1 Stress you can make other players or the master admit if they've lied.)",
            "Ultimate Menu (Add +1 to your Skill for the purposes of cooking.)",
            "Instant Cleaning (Add +1 to your Skill for the purposes of doing cleaning.)",
            "4-D Dress (You can produce anything in the mansion from within your maid uniform.)"),
           ("Punishment (When other maids make mistakes, you can gain the right to punish them, without them having a chance to make an opposed roll.)",
            "Instant Restraint (If you win a roll of Cunning Vs. Athletics, you can restrain someone from doing something indecent.)",
            "Coercion (If you win a roll of Cunning Vs. Athletics, you can completely damage or tear off someone's clothes, even \"accidentally\".)",
            "Trap (Even if you aren't there at the time, you can have a trap prepared in advance during a battle.)",
            "Fake Crying (You can use fake crying to use your Cunning for what would normally be an Affection roll. (This must be role-played).)",
            "Mockery (When someone is taking Stress points, you can mock them and cause them to gain an additional 2 Stress points. (This must be roleplayed).)"),
           ("Karma (You can use your Luck to dodge an attack, and if you roll a 10 or higher you cause twice as much Stress to the opponent.)",
            "Saw It (You can declare that you've seen something happening in the mansion; you can decide the timing too.)",
            "Teleport (You can go just about anywhere in the mansion instantly.)",
            "Escape (You can completely flee from a battle without taking any Stress.)",
            "Foreboding (You can tell when something dangerous is coming.)",
            "Chance Meeting (By taking 2 points of Stress, you can have an NPC that's just showing up for the first time be an acquaintance from some time before.)"),
           ("Immune to Pain (During a battle, even if you're sent flying, you don't take any Stress. Outside of battle, however, you can still take Stress points like usual.)",
            "Crisis Adrenaline (You can spend 1D6 points of Favor to add an Athletics roll to your Stress. You cannot use this to deliberately avoid the natural removal of Stress points.)",
            "Persistence (Whenever you take Stress, automatically reduce the amount by 1 point.)",
            "Tenacity (Even after being defeated in battle, you can take 2 Stress to get to your feet.)",
            "Hard Work (Your relentless hard work pays off in the form of a +3 bonus to the end result (not the attribute or die roll) of Skill rolls.)",
            "Absolute Maid (You are the very epitome of a maid, and you take no penalties when not in full uniform.)")
           )

def meido(phenny, input):
   nick = input.nick
   if nick.lower() == 'brobot':
      phenny.say('benzrf is an asshole')
      return
   mTypesK = list(mTypes.keys())
   mType1, mType2 = random.choice(mTypesK), random.choice(mTypesK)
   mColor = random.choice(mColors) + ' and ' + random.choice(mColors)
   message = (nick + ' is a ' + mType1 + ', ' + mType2 + ' maid with ' + random.choice(mColors) +
    ' hair and ' + random.choice(mColors) + ' eyes, who dresses in ' + mColor + '. ' +
    nick + ' works as a maid ' + random.choice(mReasons) +
    ". She copes with stress by " + random.choice(mStresses) +
    ', and fights with ' + random.choice(mWeapons) + '.')

   message += ' ' + nick + ' '
   for i in range(2):
       if i==1: message += ', and '
       mQuality = random.choice(mQualities)
       if not isinstance(mQuality, str): mQuality = random.choice(mQuality) #Handle nested options
       message += mQuality
   message += '.'

   #Set attributes to (2d6)/3 rounding down, plus modifiers from maid types; minimum 0
   mAttributes = tuple(max(0, mTypes[mType1][x] + mTypes[mType2][x] + (random.randint(1,6)+random.randint(1,6))//3) for x in range(6))
   mAttrZip = tuple(zip(mAttributeNames, mAttributes))

   message2 = (', '.join((x+": "+str(y) for x,y in mAttrZip)) +
   ' (Favor: ' + str(mAttributes[1]*2) + ', Spirit: ' + str(mAttributes[5]*10) + ')')

   ##Find the highest attribute to determine powers, choosing a random one if it's a tie
   ##Zip from earlier is reused so that each entry is unique, allowing .index() to
   ##tell them apart
   maxAttrib = max(mAttributes)
   availPowers = tuple(a for x in mAttrZip for a in mPowers[mAttrZip.index(x)] if x[1]==maxAttrib)

   message3 = "Maid Power"
   if sum(mAttributes)<=9:
      message3 += "s: " + random.choice(availPowers) + ", "
   else:
      message3 += ": "
   message3 += random.choice(availPowers)
   
   opt = input.groups()[1]
   if opt:
      message = make_dialect(opt, message)
      message2 = make_dialect(opt, message2)
      message3 = make_dialect(opt, message3)
   phenny.say(message)
   phenny.say(message2)
   phenny.say(message3)
meido.commands = ['maid','meido']
meido.priority = 'low'

def superpower(phenny, input):
   uri = 'http://powerlisting.wikia.com/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json'
   for i in range(3):
      bytes = web.get(uri)
      pos = bytes.find('"title":"')+9
      answer = bytes[pos:].replace('/','"').replace('\\','"').split('"',1)[0]
      if answer: 
         phenny.say(answer + ': http://powerlisting.wikia.com/wiki/' + answer.replace(' ', '_'))
      else:
         break
   else:
      return
   phenny.say('Sorry, no result.')
superpower.commands = ['superpower','power']
superpower.priority = 'low'