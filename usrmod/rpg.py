"""
   ()    
   )(     
o======o           
   ||              
   ||    ___              _               _ _        ____                   _    
   ||   / _ \___ _ __ ___(_)_   ____ _| ( )__    /___ \_   _  ___  ___| |_ 
   ||  / /_)/ _ \ '__/ __| \ \ / / _` | |/ __|  //  / / | | |/ _ \/ __| __| 
   || / ___/  __/ | | (__| |\ V / (_| | |\__ \ / \_/ /| |_| |  __/\__ \ |_ 
   || \/    \___|_|  \___|_| \_/ \__,_|_||___/ \___,_\ \__,_|\___||___/\__| 
   ||                                                                     
   ||                            copyright 2013
   || 
   \/ 

"""

import random
import shelve
import namegen
import os
import re, json

with open(os.path.expanduser('~/percivalsquest/data/pq_classes.json')) as f:
    dclasses = json.load(f)

with open(os.path.expanduser('~/percivalsquest/data/pq_races.json')) as f:
    draces = json.load(f)
    
with open(os.path.expanduser('~/percivalsquest/data/pq_bestiary.json')) as f:
    dmonst = json.load(f)

dfeats = {'PowerAttack':0,'StoutDefense':1,'LightningReflexes':2, 
    'Toughness':3,'IronWill':4,'Prodigy':5,'ImprovedInitiative':-1}
        
dstats = {'Attack':0,'Defense':1,'Reflexes':2,'Fortitude':3,'Mind':4,'Skill':5,
    0:'Attack',1:'Defense',2:'Reflexes',3:'Fortitude',4:'Mind',5:'Skill'}
dst = {0:'Atk',1:'Def',2:'Ref',3:'Frt',4:'Mnd',5:'Skl'}

with open(os.path.expanduser('~/percivalsquest/data/pq_magic.json')) as f:
    dtreas = json.load(f)

with open(os.path.expanduser('~/percivalsquest/data/pq_gear.json')) as f:
    dgear = json.load(f)

dprice = (1,10,100,500,1000,5000,10000,50000,100000)

dskill = {'Bronze':'Evade','Gold':'Smite','Blue':'Backstab','Silver':'Cure','Brass':'Charm','Green':'Entangle',
    'Force':'Missile','Mercury':'Doublestrike','Red':'Rage','Black':'Poison','White':'Flee','Bone':'Fear',
    'Stone':'Petrify'}
    
def drating(type, item):
    txt = item.split()
    res = 0
    for i in txt:
        res += dgear[type[0]][type[1]].get(i,0) + dtreas[type[0]][type[1]].get(i,0)
    return res
        
def treasuregen(level):
    treas = {'armor':'', 'weapon':'', 'gp':0}
    treas['gp'] = random.randint(0,10*level) #roll for gp
    carm = random.randint(1,10) #roll for armor
    if carm <= level:
        typ = random.choice(dgear['armor'].keys())
        maxrat = min([level/2 + 1,5])
        rat = random.randint(1,maxrat)
        marm = random.randint(1,10) #roll for magic
        mag = ''
        if marm <= level:
            maxmag = min([level/3,3])
            mag = dtreas['rarmor'][typ].get(str(random.randint(0,maxmag)),'')
            if mag: mag += ' '
        treas['armor'] = mag + dgear['rarmor'][typ][str(rat)]
    cwep = random.randint(1,10) #roll for weapon
    if cwep <= level:
        typ = random.choice(dgear['weapon'].keys())
        maxrat = min([level/2,5])
        rat = random.randint(0,maxrat)
        mwep = random.randint(1,10) #roll for magic
        mag = ''
        if mwep <= level:
            maxmag = min([level/3,3])
            mag = dtreas['rweapon'][typ].get(str(random.randint(0,maxmag)),'')
            if mag: mag += ' '
        treas['weapon'] = mag + dgear['rweapon'][typ][str(rat)]
    crin = random.randint(3,15) #roll for ring
    if crin <= level:
        treas['ring'] = random.choice(dtreas['ring'].keys())
    return treas
        
def item_type(item):
    if item in dtreas['ring'].keys():
        return ['ring']
    itm = item.split()
    for i in itm:
        for j in dgear['armor'].keys():
            for k in dgear['armor'][j].keys():
                if i.lower() == k.lower():
                    return ['armor',j]
        for j in dgear['weapon'].keys():
            for k in dgear['weapon'][j].keys():
                if i.lower() == k.lower():
                    return ['weapon',j]
    return None
        
def item_worth(item):
    typ = item_type(item)
    if typ[0] == 'ring':
        return 3000
    elif typ:
        return dprice[drating(typ,item)]
    else:
        return 0
    
def collapse_list(tmp, srt = False):
    ret = []
    [ret.append(i) for i in tmp if not ret.count(i)]
    if srt:
        ret = sorted(ret)
    return ret
    
class dPuzzle:
    def __init__(self,lvl):
        riddle = namegen.riddlegen()
        self.answer = riddle[0]
        self.riddle = riddle[1]
        self.riddleguess = 3
        riches = []
        while not riches:
            tr = treasuregen(lvl+2)
            for t in tr.keys():
                if t == 'gp':
                    continue
                if tr[t]:
                    riches.append(tr[t])
        self.riches = random.choice(riches)
        self.numcode = namegen.numgen()
        self.numguess = 10
        self.gold = tr['gp']*100
        self.damage = 0
        self.tnum = lvl
        self.knowledge = lvl/2
        self.thing = random.choice(['mysterious dark spirit','regal sphinx','magic mirror','blind oracle'])
        self.choice = ""
        
    def puzzlemsg(self, phenny):
        msg1 = "Exploring the depths of the Dungeon, you encounter a "+self.thing+" in a lonely room."
        if self.thing == 'magic mirror':
            msg1 += " A sinister face materializes in its murky surface, looking directly at you."
        else:
            msg1 += " The "+self.thing+" addresses you."
        msg2 = "'Welcome to the Dungeon, adventurer. Portents have foreshadowed your coming. I am here to aid you on your journey, should you prove worthy."
        msg2 += " I offer you choices three: you may play a game, for Gold; solve a riddle, for Riches; or undergo a Trial of Being, for Knowledge. Choose your prize, and choose well.'"
        msg3 = "(Use .rpgpuzzle to make your choice {gold, riches, knowledge, or skip}, and for further interactions.)"
        phenny.say(msg1)
        phenny.say(msg2)
        phenny.say(msg3)
        
    def puzzleinit(self,phenny,rpg,choice):
        self.choice = choice.lower()
        if self.choice == "gold":
            msg = "The "+self.thing+" nods approvingly. 'You have chosen the game; here are the rules. I have selected a set of four digits, in some order. "
            msg += "You have 10 chances to guess the digits, in the correct order. If you are polite, I may be persuaded to give you a hint... Now, begin; you have 10 chances remaining.'"
            msg2 = "(Guess with .rpgpuzzle XXXX)"
            phenny.say(msg)
            phenny.say(msg2)
            return
        elif self.choice == "riches":
            msg = "The "+self.thing+" nods slowly. 'You have chosen the riddle; here are the rules. I will tell you the riddle, which has an answer one word long. "
            msg += "You have three chances to guess the answer. If it goes poorly, I may decide to give you a hint. Here is the riddle: "
            msg2 = "Now, begin your guess. You have three chances remaining.'"
            phenny.say(msg)
            phenny.say(self.riddle)
            phenny.say(msg2)
            phenny.say("(Guess with .rpgpuzzle <word>)")
            return
        elif self.choice == "knowledge":
            msg = "The "+self.thing+"'s face spreads in a predatory smile. 'As you wish. The Trial consists of three tests; if you succeed at all three, you will be rewarded."
            msg += " The first will begin as soon as you are ready.'"
            msg2 = "(Tell the "+self.thing+" that you're ready with .rpgpuzzle)"
            phenny.say(msg)
            phenny.say(msg2)
            return
        else:
            self.failure(phenny,rpg)
    
    def failure(self,phenny,rpg):
        char = rpg.character
        phenny.say("The "+self.thing+" stares at you impassively. 'You have been found wanting. How disappointing.' Then it vanishes, leaving no trace that this room of the dungeon was ever occupied.")
        if self.choice == "knowledge" and self.damage > 0:
            char.ouch(self.damage)
            msg = "The Trial was extremely taxing; you take "+str(self.damage)+" damage"
            if char.currenthp <= 0:
                msg += "..."
            else:
                msg += ", and have "+str(char.currenthp)+" hit points remaining."
            phenny.say(msg)
        rpg.destination("dungeon")
        return
    
    def success(self,phenny,rpg):
        char = rpg.character
        phenny.say("The "+self.thing+" seems pleased. 'You have proven worthy, and now may receive your reward.' Then it vanishes, leaving no trace that this room of the dungeon was ever occupied.")
        msg = "You gain "
        if self.choice == "gold":
            msg += str(self.gold)+" gp!"
            phenny.say(msg)
            char.defeat_enemy(0,{'gp':self.gold})
        if self.choice == "riches":
            typ = item_type(self.riches)
            msg += "a "
            if typ[0] == "ring":
                msg += "Ring of "
            msg += self.riches+"!"
            phenny.say(msg)
            char.defeat_enemy(0,{typ[0]:self.riches})
        if self.choice == "knowledge":
            msg = str(self.knowledge)+" experience!"
            if char.exp + self.knowledge >= 10*char.level:
                msg += " You have leveled up! Please choose a feat with .rpglvlup <feat> (if you need a reminder of what feats are available, use .rpghelp feats)."
            char.defeat_enemy(self.knowledge,{})
            phenny.say(msg)
        rpg.destination("dungeon")
        return
    
    def trialofbeing(self,phenny,rpg):
        char = rpg.character
        sta = random.sample(['Attack','Defense','Reflexes','Fortitude','Mind','Skill'],3)
        tests = {'Attack':"All of a sudden, you find yourself inside a wooden box, 10 feet on a side. The walls begin to close in! You try to hack your way out...",
            'Defense':"Stalactites and stalagmites of various sizes start to elongate, sprouting from the floor, walls, and ceiling! You attempt to avoid being impaled...",
            'Reflexes':"The ground rumbles, twisting and gyrating in an earthquake! You try to keep your balance as chasms in the floor gape open...",
            'Fortitude':"An enormous python slithers out of thin air, coiling around you in an instant! You attempt to remain conscious as it constricts you...",
            'Mind':"You reel from a sudden psychic onslaught! You fight to keep your senses...",
            'Skill':"You are faced with a challenge that is both deadly and idiosyncratic! You try to defeat it using your ingenuity and cunning..."}
        win = {'Attack':"You break through the box before being crushed!",'Defense':"You protect yourself from evisceration!",'Reflexes':"You remain on your feet!",
            'Fortitude':"You fight off the impending blackness!",'Mind':"You shake off the mental assault!",'Skill':"You are up to the task!"}
        lose = {'Attack':"The contracting walls squeeze you to unconsciousness...",'Defense':"The stone spikes break through your defenses...",
            'Reflexes':"You fall into a chasm...",'Fortitude':"You are forced to oblivion...",'Mind':"Your mental defenses are overcome...",'Skill':"You come up short..."}
        for i,s in enumerate(sta):
            phenny.say("The "+("first","second","third")[i]+" challenge begins. "+tests[s])
            res_char = random.choice([random.randint(0,char.stats[dstats[s]]) for j in range(6)])
            res_test = random.choice([random.randint(0,self.tnum) for j in range(6)])
            if res_char < res_test:
                phenny.say(lose[s])
                self.damage = res_test - res_char
                self.failure(phenny,rpg)
                return
            else:
                phenny.say(win[s])
                self.knowledge += rpg.dungeonlevel
        self.success(phenny,rpg)
        
    def check_riddleguess(self,phenny,rpg,guess):
        self.riddleguess -= 1
        #check for a valid guess
        badguess = 0
        import string
        if len(guess.split()) > 1:
            badguess = 1
        for i in guess:
            if i not in string.letters:
                badguess = 2
                break
        if badguess:
            badmsg = ["your guess should be one word only.","what you said isn't even a word."][badguess-1]
            phenny.say("The "+self.thing+" frowns. 'I do not know why you would waste a guess on that... "+badmsg+"'")
            if self.riddleguess <= 0:
                self.failure(phenny,rpg)
            return
        #are they right?
        if guess.upper() == self.answer:
            self.success(phenny,rpg)
            return
        ng = len(self.answer)
        pl = "s" if self.riddleguess != 1 else ""
        msg = "You have guessed incorrectly, leaving you with "+str(self.riddleguess)+" chance"+pl+" remaining. "
        if self.riddleguess == 2:
            msg += "Here is a hint to help you: the answer to the riddle is a single word with "+str(ng)+" letters."
        phenny.say(msg)
        if self.riddleguess <= 0:
            self.failure(phenny,rpg)
        return
        
    def check_numguess(self, phenny, rpg, guess):
        self.numguess -= 1
        #check for a valid guess
        badguess = False
        if len(guess) != 4:
            badguess = True
        for i in guess:
            try:
                j = int(i)
            except:
                badguess = True
        if badguess:
            phenny.say("The "+self.thing+" frowns. 'I do not know why you would waste a guess on that.'")
            if self.numguess <= 0:
                self.failure(phenny,rpg)
            return
        copy_ans = [i for i in self.numcode]
        copy_guess = [i for i in guess]
        res = []
        #first pass: check for correct positions
        perc = 0
        for i in range(4):
            if copy_guess[i] == copy_ans[i]:
                res.append('rectus')
                copy_ans[i] = '*'
                copy_guess[i] = '*'
                perc += 2
        #did they get it right?
        if ''.join(copy_ans) == '****' or perc == 8:
            self.success(phenny,rpg)
            return
        #if not, are they done?
        if self.numguess <= 0:
            self.failure(phenny,rpg)
            return
        #if not, let's check for correct digits, incorrect positions
        for i in range(4):
            if copy_guess[i] != '*' and copy_guess[i] in copy_ans:
                res.append('proxime')
                perc += 1
        #fill out the rest with evil BWHAHA
        nres = len(res)
        for i in range(4 - nres):
            res.append('malum')
        #concatenate results
        hint = []
        nos = ['','singuli','bini','terni','quaterni']
        for i in ['rectus','proxime','malum']:
            num = res.count(i)
            if num > 0:
                print num
                hint.append(nos[num]+' '+i)
        hint = ', '.join(hint)+'.'
        perc = (perc+1)/2
        percmsg = ("The "+self.thing+" sighs. 'You are nearly as far from correct as it is possible to be. Perhaps this hint will help:",
            "The "+self.thing+" nods slowly. 'You have some small skill at this sort of thing, it would seem. A hint to aid your progress:",
            "The "+self.thing+" quirks an eyebrow. 'Perhaps you do not even need this hint, but I will provide it anyway:",
            "The "+self.thing+" smiles, showing a little too many teeth. 'I am impressed -- you are nearly there. Another hint:")
        if self.numguess > 1:
            nummsg = "You have "+str(self.numguess)+" guesses remaining. Use them wisely."
        else:
            nummsg = "You have one guess remaining. Use it wisely."
        phenny.say(" ".join([percmsg[perc],hint,nummsg]))
        return
        
class dCharacter:
    def __init__(self):
        self.name = ""
        self.level = 1
        self.hp = 1
        self.currenthp = 1
        self.sp = 1
        self.currentsp = 1
        self.race = ""
        self.clas = ""
        self.skill = []
        self.stats = [0,0,0,0,0,0]
        self.feats = [""]
        self.nick = ""
        self.init = 0
        self.atk = [0,0]
        self.dfn = 0
        self.gear = {"armor":{'name':'','rat':0},"weapon":{'name':'','rat':0}, "ring":""}
        self.loot = {"quest":'', "gp":0, "items":[]}
        self.exp = 0
        self.temp = {}
        self.tempturns = {}
    
    def chargen(self,nick,rac,cls,fets):
        rac = rac.lower()
        cls = cls.lower()
        self.nick = nick
        self.race = rac
        self.clas = cls
        self.name = namegen.web_namegen(5,12,2).replace('\n',' ')
        self.exp = 0
        self.loot["gp"] = 0
        for i in range(0,6):
            st = random.choice([random.randint(1,4) for j in range(0,6)])
            self.stats[i] = st + dclasses[cls]['stat'][i] + draces[rac]['stat'][i]
        self.feats = fets
        for i in fets:
            if i.lower() == 'improvedinitiative': 
                self.init += 2
            else:
                for j in dfeats.keys():
                    if i.lower() == j.lower():
                        self.stats[dfeats[j]] += 2
                        break
        self.hp = self.stats[3]
        self.sp = self.stats[5]
        self.currenthp = self.hp
        self.currentsp = self.sp
        self.gear['armor']['name'] = dgear['rarmor'][random.choice(dgear['rarmor'].keys())]['0']
        self.gear['armor']['rat'] = 0
        self.gear['weapon']['name'] = dgear['rweapon'][random.choice(dgear['rweapon'].keys())]['0']
        self.gear['weapon']['rat'] = 0
        self.gear['ring'] = ''
        self.atk = [self.gear['weapon']['rat'],self.stats[0]]
        self.dfn = [self.gear['armor']['rat'],self.stats[1]]
        self.skill = []
        self.skill.append(dclasses[self.clas]['skill'])
        
    def tellchar(self, phenny):
        phenny.say(self.name+' (Player: '+self.nick+')')
        phenny.say(' '.join([self.race.capitalize(),self.clas.capitalize(),str(self.level)]))
        statstr = sum([[dst[i],str(self.stats[i])] for i in range(0,6)],[])
        ft1 = collapse_list(self.feats,True)
        ft2 = []
        for f in ft1:
            if type(f) is list:
                f = f[0]
            cnt = self.feats.count(f)
            if cnt > 1:
                ft2.append(f+' x'+str(cnt))
            else:
                ft2.append(f)
        ft2 = ', '.join(sorted(ft2))
        phenny.say('; '.join([' '.join(statstr),'hp '+str(self.currenthp)+'/'+str(self.hp),
            'sp '+str(self.currentsp)+'/'+str(self.sp),'exp '+str(self.exp)+'/'+str(self.level*10),ft2]))
        if not self.gear['armor']['name']:
            arm = 'Armor: None (0)'
        else:
            arm = 'Armor: '+self.gear['armor']['name']+' ('+str(self.gear['armor']['rat'])+')'
        if not self.gear['weapon']['name']:
            wep = 'Weapon: None (-1)'
        else:
            wep = 'Weapon: '+self.gear['weapon']['name']+' ('+str(self.gear['weapon']['rat'])+')'
        if not self.gear['ring']:
            ring = 'Ring: None'
        else:
            ring = 'Ring: '+self.gear['ring']
        phenny.say('; '.join(['Skills: '+', '.join(self.skill),arm,wep,ring]))
        itm1 = collapse_list(self.loot['items'],True)
        fin = []
        if self.loot['quest']:
            fin = [self.loot['quest']]
        for f in itm1:
            if type(f) is list:
                f = f[0]
            cnt = self.loot['items'].count(f)
            if cnt > 1:
                out = f+' x'+str(cnt)
            else:
                out = f
            if f.lower() in [i.lower() for i in dtreas['ring'].keys()]:
                fin.append("Ring of "+out)
            else:
                fin.append(out)
        if not fin:
            loot = 'None'
        else:
            loot = ', '.join(fin)
        phenny.say(str(self.loot['gp'])+' gp; loot: '+loot)
        
    def levelup(self,fet):
        self.exp -= self.level * 10
        self.level += 1
        if type(fet) is list:
            fet = fet[0]
        if fet.lower() in 'improvedinitiative':
            self.init += 2
        else:
            for i in dfeats.keys():
                if i.lower() == fet.lower():
                    self.stats[dfeats[i]] += 2
                    self.feats.append(i)
        self.hp += random.choice([random.randint(max([1,self.stats[3]/2]),1+self.stats[3]) for j in range(0,6)])
        self.sp += 2
        self.atk = [self.gear['weapon']['rat'],self.stats[0]]
        self.dfn = [self.gear['armor']['rat'],self.stats[1]]
    
    def sleep(self):
        self.temp = {}
        self.tempturns = {}
        self.currenthp = self.hp
        self.currentsp = self.sp
        
    def ouch(self,dmg):
        self.currenthp -= dmg
        
    def sammich(self, lvl):
        self.temp = {}
        self.tempturns = {}
        self.currenthp = self.hp if self.currenthp + lvl > self.hp else self.currenthp + lvl
        self.currentsp = self.sp if self.currentsp + lvl > self.sp else self.currentsp + lvl
        
    def equip(self,neweq):
        old = ''
        if neweq.get('armor',None):
            narm = neweq['armor']
            nrat = drating(item_type(narm),narm)
            if self.gear['armor']['name']:
                arat = self.gear['armor']['rat']
                self.loot['items'].append(self.gear['armor']['name'])
                old = self.gear['armor']['name']
            else: arat = 0
            self.gear['armor']['name'] = narm
            self.gear['armor']['rat'] = nrat
            self.loot['items'].remove(narm)
        elif neweq.get('weapon',None):
            nwep = neweq['weapon']
            nrat = drating(item_type(nwep),nwep)
            if self.gear['weapon']['name']:
                wrat = self.gear['weapon']['rat']
                self.loot['items'].append(self.gear['weapon']['name'])
                old = self.gear['weapon']['name']
            else: wrat = 0
            self.gear['weapon']['name'] = nwep
            self.gear['weapon']['rat'] = nrat
            self.loot['items'].remove(nwep)
        elif neweq.get('ring',None):
            nring = neweq['ring']
            if self.gear['ring']:
                self.skill.remove(dtreas['ring'][self.gear['ring']])
                self.loot['items'].append(self.gear['ring'])
                old = self.gear['ring']
            self.skill.append(dtreas['ring'][nring])
            self.gear['ring'] = nring
            self.loot['items'].remove(nring)
        self.atk = [self.gear['weapon']['rat'],self.stats[0]]
        self.dfn = [self.gear['armor']['rat'],self.stats[1]]
        if old:
            return old
        return
            
    def complete_quest(self, exp, gp):
        self.loot['quest'] = ''
        self.exp += exp
        self.loot['gp'] += gp
    
    def sell_loot(self, sell, num = 1):
        if type(sell) is list:
            sell = sell[0]
        lowitems = [x.lower() for x in self.loot['items']]
        if sell.lower() not in lowitems: return False
        val = item_worth(sell)/2
        if val == 0:
            val = 1
        out = []
        for j in sorted(self.loot['items']):
            if sell.lower() == j.lower() and num > 0:
                self.loot['gp'] += val
                num -= 1
            else:
                out.append(j)
        self.loot['items'] = out
        return True
        
    def buy_loot(self, buy, gp):
        self.loot['items'].append(buy.lower().capitalize())
        self.loot['gp'] -= gp
    
    def defeat_enemy(self, lvl, loot):
        self.temp = {}
        self.tempturns = {}
        self.exp += lvl
        for i in loot.keys():
            if i == 'gp':
                self.loot['gp'] += loot[i]
            elif i == 'quest' and not self.loot['quest']:
                self.loot['quest'] = loot['quest'] 
            elif loot[i]:
                self.loot['items'].append(loot[i])
        
class dMonster:
    def __init__(self):
        self.name = ''
        self.level = 0
        self.hp = 0
        self.currenthp = 0
        self.sp = 0
        self.currentsp = 0
        self.stats = [0,0,0,0,0,0]
        self.treasure = {'weapon':'', 'armor':'', 'ring':'', 'gp':0}
        self.skill = ''
        self.temp = {}
        self.tempturns = {}
        self.atk = [0,self.stats[0]]
        self.dfn = [0,self.stats[1]]
        self.skillcounter = 1
        
    def gen(self, lvl):
        if lvl >= 10:
            self.dragongen(lvl)
        else:
            self.level = lvl
            self.name = random.choice(dmonst[str(lvl)].keys())
            tmp = dmonst[str(lvl)][self.name]
            for i in range(0,6):
                st = random.choice([random.randint(1,6) for j in range(0,6)])
                self.stats[i] = st + tmp['stat'][i]
            self.skill = tmp['skill']
            for i in range(0,lvl):
                self.hp += random.choice([random.randint(max([1,self.stats[3]/2]),self.stats[3]) for j in range(0,6)])
            self.currenthp = self.hp
            self.sp = random.choice([random.randint(1,self.stats[5]) for j in range(0,6)])+2*(lvl-1)
            self.currentsp = self.sp
            self.treasure = treasuregen(lvl)
            self.atk = [0,self.stats[0]]
            self.dfn = [0,self.stats[1]]
    
    def dragongen(self, lvl):
        self.level = lvl
        color = random.choice([random.choice(dskill.keys()) for i in range(0,6)])
        self.name = namegen.dragon_namegen(2,6)[0] + ' the '+color+' Dragon'
        for i in range(0,6):
            st = random.choice([random.randint(1,6) for j in range(0,6)])
            self.stats[i] = st + lvl - 5
        self.skill = dskill[color]
        for i in range(0,lvl):
            self.hp += random.choice([random.randint(1,self.stats[3]) for j in range(0,6)])
        self.currenthp = self.hp
        self.sp = random.choice([random.randint(1,self.stats[5]) for j in range(0,6)])+2*(lvl-1)
        self.currentsp = self.sp
        self.treasure = treasuregen(lvl)
        self.atk = [lvl/3,self.stats[0]]
        self.dfn = [lvl/3,self.stats[1]]
        
class dQuest(dMonster):
    def __init__(self):
        dMonster.__init__(self)
        self.desc = ''
    
    def gen(self, lvl):
        self.level = lvl
        self.name = namegen.simple_namegen(2,5)[0].capitalize()
        self.desc = namegen.monster_gen()[0]
        for i in range(0,6): 
            st = random.choice([random.randint(1,6) for j in range(0,6)])
            self.stats[i] = st + lvl
        art = namegen.artygen()[0].split(':')
        self.treasure['quest'] = art[0].strip()
        self.arty = [a.strip() for a in art]
        self.skill = 'Cure'
        for i in range(0,lvl):
            self.currenthp += random.choice([random.randint(max([1,self.stats[3]/2]),self.stats[3]) for j in range(0,6)])
        self.currentsp = random.choice([random.randint(1,self.stats[5]) for j in range(0,6)]) + 2*(lvl-1)
        self.hp = self.currenthp
        self.sp = self.currentsp
        self.atk = [lvl/2,self.stats[0]]
        self.dfn = [lvl/2,self.stats[1]]

class Combat:
    def __init__(self, lvl, char, enemy):
        if not enemy:
            self.enemy = dMonster()
            self.enemy.gen(lvl)
        else:
            self.enemy = enemy
        self.turn = -1
        self.charname = char.name
        cint = 1 + char.init if char.stats[2] < 2 else random.choice([random.randint(1,char.stats[2])+char.init for j in range(0,6)])
        mint = 1 if self.enemy.stats[2] < 2 else random.choice([random.randint(1,self.enemy.stats[2]) for j in range(0,6)])
        self.turnorder = ['monster','player']
        if cint > mint:
            self.turnorder = ['player','monster']
        elif cint == mint:
            if char.stats[2] > self.enemy.stats[2]:
                self.turnorder = ['player','monster']
            elif char.stats[2] == self.enemy.stats[2]:
                if 'ImprovedInititiative' in char.feats:
                    self.turnorder = ['player','monster']
                elif random.randint(0,1):
                    self.turnorder = ['player','monster']
        
    def advance_turn(self, phenny, rpg, char):
        self.turn += 1
        whos = self.turnorder[self.turn % 2]
        self.enemy.skillcounter -= 1
        for i in char.temp.keys():
            char.tempturns[i] -= 1
            if char.tempturns[i] < 0:
                del char.tempturns[i], char.temp[i]
                if char.currenthp <= 0:
                    rpg.death(phenny,char)
                    return
        for i in self.enemy.temp.keys():
            self.enemy.tempturns[i] -= 1
            if self.enemy.tempturns[i] < 0:
                del self.enemy.tempturns[i], self.enemy.temp[i]
                if self.enemy.currenthp <= 0:
                    rpg.death(phenny,self.enemy)
                    return
        if whos == 'monster':
            if self.enemy.currentsp > 0 and ((self.enemy.skill == 'Petrify' and self.enemy.skillcounter < -2) or self.enemy.skillcounter < 0):
                phenny.say("The enemy uses "+self.enemy.skill+"!")
                rpg.use_skill(phenny,self.enemy.skill,self.enemy,rpg.character)
                self.enemy.skillcounter = 1 if self.enemy.skill != 'Flee' else -1
            else:
                phenny.say("It tries to cause you bodily harm!")
                rpg.attack_enemy(phenny,self.enemy,rpg.character)
        
class Rpg:
    def __init__(self):
        self.character = dCharacter()
        self.player_nick = ""
        self.game_channel = ""
        self.questlevel = 0
        self.dungeonlevel = 1
        self.maxdgnlevel = 1
        self.quest = {}
        self.queststatus = "inactive"
        self.store = ['Dagger']
        self.chardeath = False
        self.whereareyou = ""
        self.shrinexp = 0
        self.shrinegp = 0
    
    def validate_player(self, phenny, input):
        if input.nick.lower() != self.player_nick.lower():
            phenny.say("Sorry, "+input.nick+", you're not the active player right now.")
            return False
        if input.sender.lower() != self.game_channel.lower():
            phenny.say("Sorry, "+input.nick+", that command wasn't in the right channel.")
            return False
        return True
    
    def initialize_channel(self, phenny, input):
        if not self.player_nick:
            try:
                self.player_nick = input.nick
                self.game_channel = "#EikoRPG_"+input.nick.strip()
                phenny.write(['JOIN'], self.game_channel)
                #phenny.msg('ChanServ','SET '+self.game_channel+' OWNERMODE ON')
                #phenny.msg('ChanServ','SET '+self.game_channel+' PROTECTMODE ON')
                #phenny.msg('ChanServ','SYNC '+self.game_channel)
                #phenny.write(['MODE'], self.game_channel+' +m')
                #phenny.msg('ChanServ','VOP '+self.game_channel+' ADD '+input.nick)
                phenny.say('OK, '+input.nick+', your game is ready in '+self.game_channel+' -- when you get there, type ".rpginit" to begin. If anyone else would like to watch, join the channel, but you won\'t be able to give any commands.')
                phenny.say('It\'s possible sirp will make this game multiplayer in the future, though.')
                return True
            except:
                phenny.say('Sorry, '+input.nick+', there was an error in initializing your game session.')
                return False
        elif not self.validate_player(phenny, input):
            return False
        else: 
            return True
            
    def atk_roll(self, atk, dfn, atkadj = 0, defadj = 0):
        if atk[1] <= atk[0]:
            atk_res = atk[0] + atkadj
        else:
            atk_res = random.choice([random.randint(atk[0],atk[1]) for i in range(0,6)]) + atkadj    
        if dfn[1] <= dfn[0]:
            dfn_res = dfn[0] + defadj 
        else:
            dfn_res = random.choice([random.randint(dfn[0],dfn[1]) for i in range(0,6)]) + defadj
        return atk_res - dfn_res
        
    def be_hit(self, phenny, target, dmg):
        target.currenthp -= dmg
        if target == self.character:
            phenny.say("Ouch! You're bleeding, maybe a lot. You take "+str(dmg)+" damage, and have "+str(target.currenthp)+" hit points remaining.")
        else:
            phenny.say("A hit! A very palpable hit! You deal "+str(dmg)+" damage.")
        if target.currenthp <= 0:
            self.death(phenny, target)
            return True
    
    def win_combat(self,phenny):
        self.character.defeat_enemy(self.combat.enemy.level, self.combat.enemy.treasure)
        exp = self.combat.enemy.level
        msg = 'You receive '+str(exp)+' experience.'
        limit = self.character.level*10
        if self.character.exp >= limit:
            msg += ' You have leveled up! Please choose a feat with .rpglvlup <feat> (if you need a reminder of what feats are available, use .rpghelp feats).'
        phenny.say(msg)
        tr = self.combat.enemy.treasure
        msg = "In the monster's pockets, you find: "
        fin = []
        for i in tr.keys():
            if tr[i]:
                if i == 'gp':
                    fin.append(str(tr[i])+" gp")
                elif i == 'ring':
                    fin.append("a Ring of "+tr[i])
                elif i == 'quest':
                    fin.append(tr[i])
                    self.queststatus = "complete"
                else:
                    fin.append("a "+tr[i])
        if not fin:
            fin = "Nothing!"
        else:
            fin = ', '.join(fin) + '.'
        phenny.say(msg + fin)
        self.whereareyou = "dungeon"
        self.combat = None
    
    def death(self, phenny, target):
        if target == self.character:
            phenny.say('Sorry, '+self.character.nick+', you have died. You can use the command ".rpgload" to load from your last save, ".rpgquit" to quit, or ".rpgchargen" to make a new character.')
            self.temp = {}
            self.tempturns = {}
            self.chardeath = True
            self.combat = None
            return
        if target == self.combat.enemy:
            phenny.say('You have defeated the '+self.combat.enemy.name+'!')
            self.win_combat(phenny)
            return
            
    def temp_bonus(self, phenny, target, stat, bon, turns):
        for i in stat:
            if target.temp.get(i,False):
                sign = -1 if bon < 0 else 1
                bon = sign * max([abs(target.temp[i]),abs(bon)])
            target.temp[i] = bon
            target.tempturns[i] = turns
                
    def new_char(self):
        self.chardeath = 0
        self.questlevel = 0
        self.dungeonlevel = 1
        self.maxdgnlevel = 1
        self.quest = {}
        self.queststatus = "inactive"
        self.store = ['Dagger']
    
    def attack_enemy(self, phenny, user, target):
        hit = self.atk_roll(user.atk, target.dfn, user.temp.get("Attack",0), target.temp.get("Defense",0))
        if hit > 0:
            if not self.be_hit(phenny, target, hit):
                self.combat.advance_turn(phenny,self,self.character)
        else:
            phenny.say("The attack is unsuccessful.")
            self.combat.advance_turn(phenny,self,self.character)
    
    def use_skill(self, phenny, skill, user, target):
        if skill not in user.skill:
            return 0
        if user.currentsp == 0:
            return 1
        user.currentsp -= 1
        
        if skill == 'Smite': #attack with Atk+Skill
            tmp_atk = user.atk
            tmp_atk[1] += random.randint(0,user.stats[5])
            hit = self.atk_roll(tmp_atk, target.dfn,user.temp.get("Attack",0), target.temp.get("Defense",0))
            if hit > 0:
                if not self.be_hit(phenny, target, hit):
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                phenny.say("The Smite failed to connect.")
                self.combat.advance_turn(phenny,self,self.character)
                
        if skill == 'Dominate': #Skill vs Mind to make monster attack itself
            affect = self.atk_roll([0, user.stats[5]], [0, target.stats[4]], user.temp.get("Skill", 0), \
                target.temp.get("Mind", 0))
            if affect > 0:
                hit = self.atk_roll(target.atk, target.dfn, target.temp.get("Attack", 0) + affect, \
                    target.temp.get("Defense", 0))
                targstring = "The monster is " if hasattr(user, "gear") else "You are "
                targstring2 = "s itself!" if hasattr(user, "gear") else " yourself!"
                phenny.say(targstring + "dominated, and attack" + targstring2)
                if hit > 0:
                    if not self.be_hit(phenny, target, hit):
                        self.combat.advance_turn(phenny, self, self.character)
                        return 2
                else:
                    phenny.say("The monster fails to injure itself.")
                    self.combat.advance_turn(phenny, self, self.character)
            else:
                phenny.say("The Dominate failed.")
                self.combat.advance_turn(phenny, self, self.character)
        
        if skill == 'Cure': #regain hp
            cure = random.randint(1,user.stats[5]+user.temp.get("Skill",0)) + user.level
            if user.currenthp + cure > user.hp:
                user.currenthp = user.hp
            else:
                user.currenthp += cure
            cur = "You are " if user == self.character else "The monster is "
            phenny.say(cur+"cured for "+str(cure)+" hp! An attack follows.")
            self.attack_enemy(phenny,user,target)
        
        if skill == 'Charm': #chance to end encounter, vs Mind
            hit1 = self.atk_roll([0,user.stats[5]],[0,target.stats[4]],user.temp.get("Skill",0),target.temp.get("Mind",0))
            hit2 = self.atk_roll([0,user.stats[5]],[0,target.stats[4]],user.temp.get("Skill",0),target.temp.get("Mind",0))
            hit3 = self.atk_roll([0,user.stats[5]],[0,target.stats[4]],user.temp.get("Skill",0),target.temp.get("Mind",0))
            if hit1 > 0 and hit2 > 0 and hit3 > 0:
                self.death(phenny, target)
                return 2
            else:
                phenny.say("The Charm failed.")
                self.combat.advance_turn(phenny,self,self.character)
                
        if skill == 'Entangle': #debuff targets atk, def for 2 turns, vs Ref
            hit = self.atk_roll([0,user.stats[5]],[0,target.stats[2]],user.temp.get("Skill",0),target.temp.get("Reflex",0))
            if hit > 0:
                cur = "The monster is " if user == self.character else "You are "
                phenny.say(cur+"entangled!")
                self.temp_bonus(phenny, target,['Attack','Defense'],-hit,4)
            else:
                phenny.say("The Entangle failed.")
            self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Trip': #deal dmg and target loses turn, vs Atk
            hit = self.atk_roll(user.atk,target.atk,user.temp.get("Attack",0),target.temp.get("Attack",0))
            if hit > 0:
                hit = max([hit/2,1])
                if not self.be_hit(phenny, target, hit):
                    cur = "The monster is " if user == self.character else "You are "
                    phenny.say(cur+"tripped!")
                    deb = max([0,random.choice([random.randint(0,user.stats[5]) for i in range(0,6)]) + user.temp.get("Skill",0)])
                    self.temp_bonus(phenny, target, ["Attack"], deb,4)
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                phenny.say("The Trip failed.")
                self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Missile': #deal dmg vs Ref
            num_missile = user.level[1]/3 + 1
            targstring = "You send " if hasattr(user, "gear") \
                else "The monster sends "
            phenny.say(targstring + str(num_missile) +" missiles!")
            hit = 0
            for i in range(num_missile):
                hit += max([0, atk_roll([0, user.stats[5]], [0, target.stats[2]], \
                    user.temp['stats'].get("Skill", 0), \
                    target.temp['stats'].get("Reflex", 0))])
            if hit > 0:
                if not self.be_hit(phenny, target, hit):
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                phenny.say("The Missiles failed to connect.")
                self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Doublestrike': #two attacks at smaller bonus
            hit1 = self.atk_roll(user.atk,target.dfn,user.temp.get("Attack",0)-2,target.temp.get("Defense",0))
            hit2 = self.atk_roll(user.atk,target.dfn,user.temp.get("Attack",0)-2,target.temp.get("Defense",0))
            if hit1 < 0 : hit1 = 0
            if hit2 < 0 : hit2 = 0
            hit = hit1 + hit2
            if hit > 0:
                if not self.be_hit(phenny, target, hit):
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                phenny.say("The Doublestrike failed to connect.")
                self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Backstab': #Skill vs Fort for double dmg on attack
            check = self.atk_roll([0,user.stats[5]],[0,target.stats[3]],user.temp.get("Skill",0),target.temp.get("Fortitude",0))
            hit = self.atk_roll(user.atk,target.dfn,user.temp.get("Attack",0),target.temp.get("Defense",0))
            if hit > 0:
                if check > 0: hit *= 2
                if not self.be_hit(phenny, target, hit):
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                phenny.say("The Backstab failed to connect.")
                self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Rage': #attack with +atk, -def
            hit = self.atk_roll(user.atk,target.dfn,user.temp.get("Attack",0)+user.stats[5],target.temp.get("Defense",0))
            self.temp_bonus(phenny,user,["Defense"],-2,4)
            if hit > 0:
                if not self.be_hit(phenny, target, hit):
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                phenny.say("The Rage-fueled attack failed to connect.")
                self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Evade': #gain +def
            self.temp_bonus(phenny, user, ('Defense'), user.stats[5],4)
            cur = "You are " if user == self.character else "The monster is "
            phenny.say(cur+"feeling much more evasive!")
            self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Flee': #escape from combat
            cur = "You are " if user == self.character else "The monster is "
            phenny.say(cur+"running away!")
            self.runaway(phenny, user, 1.)
            self.whereareyou = "dungeon"
            self.combat = None
            return 2
        
        if skill == 'Poison': #Auto-dmg if not at max hp
            if target.currenthp < target.hp:
                if not self.be_hit(phenny, target, user.stats[5]):
                    self.combat.advance_turn(phenny,self,self.character)
                    return 2
            else:
                cur = " the monster." if user == self.character else " you."
                phenny.say("The Poison failed to affect"+cur)
                self.combat.advance_turn(phenny,self,self.character)
                
        if skill == 'Fear': #Debuff vs Mind
            hit = self.atk_roll([0,user.stats[5]],[0,target.stats[4]],user.temp.get("Skill",0),target.temp.get("Mind",0))
            if hit > 0:
                amt = hit / 2
                if amt == 0:
                    amt = 1
                cur = "The monster is " if user == self.character else "You are "
                phenny.say(cur+"frightened!")
                self.temp_bonus(phenny, target, ['Attack','Defense','Skill'], -amt, 3)
            else:
                cur = " the monster." if user == self.character else " you."
                phenny.say("The Fear failed to affect"+cur)
            self.combat.advance_turn(phenny,self,self.character)
        
        if skill == 'Petrify': #chance to end encounter, vs Fort
            hit1 = self.atk_roll([0,user.stats[5]],[0,target.stats[3]],user.temp.get("Skill",0),target.temp.get("Fortitude",0))
            hit2 = self.atk_roll([0,user.stats[5]],[0,target.stats[3]],user.temp.get("Skill",0),target.temp.get("Fortitude",0))
            hit3 = self.atk_roll([0,user.stats[5]],[0,target.stats[3]],user.temp.get("Skill",0),target.temp.get("Fortitude",0))
            if hit1 > 0 and hit2 > 0 and hit3 > 0:
                self.death(phenny, target)
                return 2
            else:
                phenny.say("The Petrify failed.")
                self.combat.advance_turn(phenny,self,self.character)
        
        return 2
    
    def runaway(self,phenny, who, ch = 0.5):
        if random.random() < ch:
            if who == self.character:
                phenny.say("You successfully exercise your valor, vis a vis discretion.")
            else:
                phenny.say("Your enemy turns tail and books it back into the dungeon.")
            return True
        else:
            if who == self.character:
                phenny.say("You try to run, but the enemy boxes you in.")
            else:
                phenny.say("You prevent your enemy from skedaddling.")
            return False

    def check_backtrack(self):
        chk = self.character.stats[4] - self.dungeonlevel
        if chk < 0:
            cut = float(3 - chk)/float(6 - 6 * chk)
        else:
            cut = float(3 + 5 * chk)/float(6 + 6 * chk)
        bak = True if random.random() < cut else False
        return bak
            
    def init_quest(self, level):
        self.quest = dQuest()
        self.quest.gen(level)
        
    def addshopitem(self):
        tr = treasuregen(self.questlevel)
        for i in tr.keys():
            if tr[i]:
                if i != 'gp' and tr[i] not in self.store:
                    self.store.append(tr[i])
        
    def telltown(self,phenny,start = False):
        msg = "You begin in the town square. " if start else ""
        msg += "To the East is your humble abode and warm bed; to the North, the General Store where various and sundry goods may be purchased; "
        msg += "to the West, the Questhall where the mayor makes his office; "
        msg += "to the Northwest, the local Shrine to the Unknowable Gods; and to the South lie the gates of the city, leading out to the Dungeon."
        phenny.say(msg)
    
    def questhall(self, phenny):
        if self.queststatus == "active":
            phenny.say("As you enter the Questhall, Mayor Percival looks at you expectantly. 'Did you collect the item and defeat the monster? No? Well, then, get back out there! I suggest you try Dungeon level "+str(self.questlevel)+".")
            return
        self.questlevel += 1
        self.quest = dQuest()
        self.quest.gen(self.questlevel)
        if self.queststatus == "inactive":
            msg1 = "In the Questhall, Mayor Percival frets behind his desk. '"+self.character.name+"! Just the person I was looking for. There's... something I need you to do."
            msg2 = " See, there are rumors of a horrible creature, called "+self.quest.name+", roaming the dungeon."
            phenny.say(msg1+msg2)
            phenny.say(self.quest.desc)
            msg1 = "This monstrosity draws its power from "+self.quest.arty[0]+","+self.quest.arty[1].lower()+" I need you to go into the dungeon, kill that beast, and bring back the artifact so my advisors can destroy it."
            msg2 = " The townspeople will be very grateful, and you'll receive a substantial reward! Now, get out of here and let me finish my paperwork.'"
            phenny.say(msg1+msg2)
            self.queststatus = "active"
        elif self.queststatus == "complete":
            self.queststatus = "active"
            phenny.say("Mayor Percival looks up excitedly. 'You have it! Well, thank my lucky stars. You're a True hero, "+self.character.name+"!'")
            exp = 5 * (self.questlevel-1)
            gp = int(random.random()*2+1) * exp
            msg = "You gain "+str(exp)+" experience and "+str(gp)+" gp."
            self.character.complete_quest(exp,gp)
            limit = self.character.level*10
            if self.character.exp + exp > limit:
                msg += ' You have leveled up! Please choose a feat with .rpglvlup <feat> (if you need a reminder of what feats are available, use .rpghelp feats).'
            phenny.say(msg)
            self.addshopitem()
            msg1 = "Percival clears his throat hesitantly. 'Since I have you here, there... have been rumors of another problem in the dungeon. "
            msg2 = self.quest.name+" is its name. "+self.quest.desc
            phenny.say(msg1+msg2)
            phenny.say("The source of its power is "+self.quest.arty[0]+", "+self.quest.arty[1]+" Will you take this quest, same terms as last time (adjusting for inflation)? Yes? Wonderful! Now get out.'")
            
    def destination(self,loc):
        self.whereareyou = loc
        
    def godownstairs(self, phenny):
        if self.whereareyou != "stairs":
            print "NO STAIRS BLARGH"
            return
        self.whereareyou = "start"
        self.dungeonlevel += 1
        if self.dungeonlevel > self.maxdgnlevel:
            self.maxdgnlevel = self.dungeonlevel
        phenny.say("You head down the stairs to level "+str(self.dungeonlevel))
        return

    def explore(self, phenny):
        room = random.choice([random.randint(1,20) for i in range(0,6)])
        if room <= 2:
            phenny.say("You find a flight of stairs, leading down! Explore again to go down to the next level, or backtrack to stay on this one.")
            self.whereareyou = "stairs"
            return
        elif room > 2 and room <= 5:
            msg = "You found a chest! "
            tr = treasuregen(self.dungeonlevel)
            self.character.defeat_enemy(0,tr)
            fin = []
            for i in tr.keys():
                if tr[i]:
                    if i == 'gp':
                        fin.append(str(tr[i])+" gp")
                    elif i == 'ring':
                        fin.append("a Ring of "+tr[i])
                    else:
                        fin.append("a "+tr[i])
            if not fin:
                msg += "Sadly, it was empty."
            else:
                msg += 'Inside, you find '+', '.join(fin) + '.'
            phenny.say(msg)
            return
        elif room > 5 and room <= 8:
            dl = self.dungeonlevel
            if 'milo' in self.player_nick.lower():
                foo = 'a taco-like'
            else:
                from xkcd import sandgen
                foo = sandgen()
            phenny.say("The room echoes with a hollow emptiness, and you reflect on the vagaries of living life alone... Then you eat"+foo+" sandwich, and get ready to kill more things.")
            phenny.say("You regain "+str(dl)+" hp and sp!")
            self.character.sammich(dl)
        elif room > 8 and room <= 10:
            self.whereareyou = "puzzle"
            self.puzzle = dPuzzle(self.dungeonlevel)
            self.puzzle.puzzlemsg(phenny)
        elif room > 10:
            msg = "You've stumbled on an enemy! It seems to be... "
            chk = self.maxdgnlevel - self.questlevel
            cut = float(1 + chk)/float(10 + 2*chk)
            if self.dungeonlevel == self.questlevel and self.quest and self.queststatus == "active" and random.random() < cut:
                self.combat = Combat(self.dungeonlevel, self.character, self.quest)
                msg += self.quest.name+'!'
            else: 
                self.combat = Combat(self.dungeonlevel, self.character, None)
                if self.dungeonlevel >= 10:
                    msg += self.combat.enemy.name+'!'
                else:
                    msg += 'a '+self.combat.enemy.name+'!'
            if self.combat.turnorder[0] == 'player':
                msg += ' You get the jump on it.'
            else:
                msg += ' It gets the jump on you.'
            phenny.say(msg)
            self.whereareyou = "combat"
            self.combat.advance_turn(phenny, self, self.character)

    def display_itemlist(self,itemlist,sell = False):
        itm1 = collapse_list(itemlist, True)
        fin = []
        for j,f in enumerate(itm1):
            price = item_worth(f)
            if sell:
                price = max([price/2,1])
            if type(f) is list:
                f = f[0]
            cnt = itemlist.count(f)
            if cnt > 1:
                out = f+' x'+str(cnt)
            else:
                out = f
            if f.lower() in [i.lower() for i in dtreas['ring'].keys()]:
                fin.append(str(j+1)+". Ring of "+out+" ("+str(price)+")")
            else:
                fin.append(str(j+1)+". "+out+" ("+str(price)+")")
        return fin

    def visit_shop(self, phenny):
        self.whereareyou = "shop"
        msg1 = "The shopkeep greets you cheerfully. 'Welcome, hero! What can I do for you?' His current inventory is: "
        fin = self.display_itemlist(self.store)
        if not fin:
            msg1 += "Nothing!"
        else:
            msg1 += " ".join(fin) + "."
        phenny.say(msg1)
        msg2 = "Your current loot bag contains "+str(self.character.loot['gp'])+" gp, and: "
        fin = self.display_itemlist(self.character.loot['items'],True)
        if not fin:
            msg2 += "Nothing!"
        else:
            msg2 += " ".join(fin) + "."
        phenny.say(msg2)
        phenny.say("Use .rpgbuy and .rpgsell for transactions, or .rpgtown to leave the shop.")
        
    def visit_shrine(self, phenny):
        self.whereareyou = "shrine"
        self.gods = namegen.godgen(2)
        msg = "The Shrine is mostly deserted at this time of day. Two of the altars catch your eye: one to "+self.gods[0]+", which offers Enlightenment on a sliding tithe scale; "
        msg += "and one to "+self.gods[1]+", which promises Materialism for a single lump sum of 30,000gp."
        msg2 = "(Use .rpgshrine <choice> <offering> to make an offering; choice 1 is Enlightenment, choice 2 is Materialism.)"
        phenny.say(msg)
        phenny.say(msg2)
        
    def offering(self,phenny,choice,amt):
        if amt < 0:
            phenny.say("You can't take money out of the offering bowl, not without offending "+self.gods[int(choice)-1]+", which you do NOT want to do.")
            return
        elif amt == 0:
            phenny.say("Nothing ventured, nothing gained.")
            return
        elif amt > self.character.loot['gp']:
            phenny.say("You don't have enough gold for that, man. Go back to the dungeon and make some scratch! (Or at least, put less in the offering bowl.)")
            return
        if str(choice) == '1':
            try:
                self.shrinegp += amt
            except AttributeError:
                self.shrinegp = amt
            from math import sqrt
            newexp = int((1. + sqrt(1. + 8. * float(self.shrinegp)))/4.)
            try:
                net = newexp - self.shrinexp
            except AttributeError:
                net = newexp
            self.shrinexp = newexp
            phenny.say("The bounds of your mind are expanded by a moment of attention from "+self.gods[0]+"; this may not actually be a good thing, but at least you gain "+str(net)+" experience.")
            self.character.defeat_enemy(net,{'gp':-amt})
            if self.character.exp >= self.character.level * 10:
                phenny.say("You have leveled up! Please choose a feat with .rpglvlup <feat> (if you need a reminder of what feats are available, use .rpghelp feats).")
            return
        elif str(choice) == '2':
            if amt < 30000:
                phenny.say("Nothing happens except for a feeling of insufficient funds... you scoop the gold back out of the offering bowl before anyone sees you, cheapskate.")
                return
            t = random.choice([random.randint(0,2) for i in range(6)])
            typ1 = ["ring","rarmor","rweapon"][t]
            t2 = ["ring","armor","weapon"][t]
            if typ1 == "ring":
                tr = random.choice([random.choice(dtreas['ring'].keys()) for i in range(6)])
            else:
                typ2 = random.choice([random.choice(dtreas[typ1].keys()) for i in range(6)])
                rat = random.choice([random.randint(0,8) for i in range(6)])
                if rat == 0:
                    tr = dgear[typ1][typ2][0]
                else:
                    mrat = random.choice([random.randint(max([rat-5,0]),min([3,rat])) for i in range(6)]) if rat < 8 else 3
                    irat = rat - mrat
                    tr = '' if mrat == 0 else dtreas[typ1][typ2][mrat]+' '
                    tr += dgear[typ1][typ2][irat]
            self.character.defeat_enemy(0,{'gp':-amt,t2:tr})
            msg = "The gold disappears from the offering bowl"
            if amt > 30000:
                msg += " (with a thank you very much for the extra donation)"
            msg += ", and you discover a "
            if t2 == "ring":
                msg += "Ring of "
            msg += tr+" in your lootbag!"
            phenny.say(msg)
            return

    def save(self):
        d = shelve.open(os.path.expanduser('~/.phenny/rpgsaves.db'))
        d[self.player_nick] = self
        d.close()

rpgs = {}

def rpg0(phenny, input):
    global rpgs
    if input.nick in rpgs.keys():
        if input.sender == rpgs[input.nick].game_channel:
            phenny.say("You're already here...?")
            return
        phenny.say("You realize you're already playing, right? Or... maybe you didn't quit when you were done? Well either way, your channel is "+rpgs[input.nick].game_channel+".")
        return
    rpgs[input.nick] = Rpg()
    rpgs[input.nick].initialize_channel(phenny, input)
rpg0.name = 'rpg0'
rpg0.commands = ['rpg']
rpg0.priority = 'low'

def rpginit(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.character.name:
        phenny.say("Your game is already initialized, what's the problem?")
        return
    phenny.say("Welcome to Percival's Quest! This is a solo (as of yet) random dungeoncrawl rpg written for IRC. The current player is "+input.nick+"! If this is your first time playing, I suggest you start with .rpghelp; otherwise, you can load your previous progress (if any) with .rpgload, or start a new game with .rpgchargen.")
    phenny.say("Once you have a character, the fast track to the dungeon (if you don't want to wander around the town) is .rpgtown dungeon, and then once you're there, .rpgdungeon explore.")
    rpg.destination("town")
rpginit.name = 'rpginit'
rpginit.commands = ['rpginit']
rpginit.priority = 'low'

def rpgload(phenny, input):
    global rpgs
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    d = shelve.open(os.path.expanduser('~/.phenny/rpgsaves.db'))
    if input.nick not in d:
        phenny.say("You don't currently have a character saved...")
        return
    rpg = d[input.nick]
    d.close()
    phenny.say("Game successfully loaded. You're in the town square.")
    rpgs[input.nick] = rpg
    rpg.character.tellchar(phenny)
    rpg.destination("town")
rpgload.name = 'rpgload'
rpgload.commands = ['rpgload']
rpgload.priority = 'low'

def rpgsheet(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.character.nick != input.nick:
        phenny.say("Sorry, "+input.nick+", you don't have a character sheet for me to show you. Try making one with .rpgchargen...")
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", your character is dead, so I tore up the sheet. If you load again, I'll try and find some scotch tape.")
        return
    rpg.character.tellchar(phenny)
    return
rpgsheet.name = 'rpgsheet'
rpgsheet.commands = ['rpgsheet']
rpgsheet.priority = 'low'

def rpgbuy(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", you can't buy stuff if you're dead.")
        return
    if rpg.whereareyou != "shop":
        phenny.say("You're not shopping right now...")
        return
    opt = input.groups()[1]
    if not opt:
        phenny.say("So... what did you want to buy, then?")
        return
    try:
        opt = int(opt.split()[0]) - 1
    except:
        phenny.say("The shopkeep has no idea what you're trying to buy.")
        return
    if opt > len(rpg.store) or opt < 0:
        phenny.say("The shopkeep gives you a strange look. 'How many fingers am I holding up?'")
        return
    buy = rpg.store[opt]
    price = item_worth(buy)
    if price > rpg.character.loot['gp']:
        phenny.say("Sorry, you don't have enough moola to purchase that item.")
        return
    else:
        phenny.say("You snag that swag.")
        rpg.character.buy_loot(buy,price)
        del rpg.store[opt]
        msg1 = "Shop inventory: "
        msg1 += " ".join(rpg.display_itemlist(rpg.store)) + "."
        phenny.say(msg1)
        msg2 = "Your loot bag: "+str(rpg.character.loot['gp'])+" gp, and "
        msg2 += " ".join(rpg.display_itemlist(rpg.character.loot['items'],True)) + "."
        phenny.say(msg2)
        return
rpgbuy.name = 'rpgbuy'
rpgbuy.commands = ['rpgbuy']
rpgbuy.priority = 'low'

def rpgsell(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", you can't sell stuff if you're dead.")
        return
    if rpg.whereareyou != "shop":
        phenny.say("You're not shopping right now...")
        return
    opt = input.groups()[1]
    if not opt:
        phenny.say("So... what did you want to sell, then?")
        return
    oo = opt.split()
    try:
        opt = int(oo[0]) - 1
    except:
        phenny.say("The shopkeep has no idea what you're trying to sell.")
        return
    lootbag = collapse_list(rpg.character.loot['items'], True)
    if opt > len(lootbag) or opt < 0:
        phenny.say("The shopkeep gives you a strange look. 'How many fingers am I holding up?'")
        return
    sell = lootbag[opt]
    price = max([item_worth(sell) / 2, 1])
    num = 1
    maxnum = [x.lower() for x in rpg.character.loot['items']].count(sell.lower())
    if len(oo) > 1:
        print oo[1]
        if oo[1].lower() == 'all':
            num = maxnum
        else:
            try:
                num = int(oo[1])
            except:
                phenny.say("I can't tell how many of that you want to sell, so we're going to go with just one.")
                num = 1
    if num > maxnum:
        phenny.say("You're trying to sell too many of those, so I'm going to sell all of them.")
        num = maxnum
    elif num < 0:
        phenny.say("You can't sell a negative amount, that's called 'buying'. How's about we just sell one.")
        num = 1
    elif num == 0:
        phenny.say("Well... OK, I guess.  You sell zero items, and receive 0 gp.")
        return
    if rpg.character.sell_loot(sell,num):
        phenny.say("You exchange goods for gps, and the shopkeep stashes the loot in his back room.")
    msg1 = "Shop inventory: "
    msg1 += " ".join(rpg.display_itemlist(rpg.store)) + "."
    phenny.say(msg1)
    msg2 = "Your loot bag: "+str(rpg.character.loot['gp'])+" gp, and: "
    fin = rpg.display_itemlist(rpg.character.loot['items'],True)
    if fin:
        msg2 += " ".join(fin)+"."
    else:
        msg2 += "Nothing!"
    phenny.say(msg2)
    return
rpgsell.name = 'rpgsell'
rpgsell.commands = ['rpgsell']
rpgsell.priority = 'low'

def rpgturn(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", this game doesn't have zombie-mode support yet.")
        return
    opt = input.groups()[1]
    if not opt:
        phenny.say("So... what did you want to do, then?")
        return
    opt = opt.split()
    o = opt[0].lower()
    if o == 'equip':
        if len(opt) < 2:
            phenny.say("You're not going to equip anything?")
            return
        o1 = [x.lower().capitalize() for x in opt[1:]]
        ox = ' '.join(o1)
        if ox == rpg.character.loot['quest']:
            phenny.say("You can't equip the quest item... it's too AWESOME for you, nyah nyah")
            return
        if ox not in rpg.character.loot['items']:
            phenny.say("You don't have one of those, or it's already equipped.")
            return
        typ = item_type(ox)
        if 'ring' in typ:
            neweq = {'ring':ox}
        elif 'weapon' in typ:
            neweq = {'weapon':ox}
        elif 'armor' in typ:
            neweq = {'armor':ox}
        else:
            phenny.say("Sorry, there's been an equipment malfunction.")
            return
        rpg.character.equip(neweq)
        phenny.say(ox+" equipped!")
        if rpg.whereareyou == "combat":
            rpg.combat.advance_turn(phenny,rpg,rpg.character)
        return
    if rpg.whereareyou != "combat":
        if rpg.whereareyou == "puzzle":
            phenny.say("Whatever you were going to do, you steal a look at the "+rpg.puzzle.thing+", and decide against it.")
        elif o == 'flee':
            phenny.say("You run away from your own shadow, but it KEEPS CHASING YOU AAAAAAAAAAAAAAAAAAARGH")
        elif rpg.whereareyou == "shop":
            phenny.say("The shopkeep nimbly avoids your attack, and waggles a finger at you. 'Ah-ah-ah, that's no way to earn a discount!'")
        else:
            phenny.say("You swing at the air, which dies a little.")
        return
    if o == 'attack':
        rpg.attack_enemy(phenny,rpg.character,rpg.combat.enemy)
        return
    if o == 'flee':
        if rpg.runaway(phenny,rpg.character):
            rpg.destination("dungeon")
            rpg.combat = None
        else:
            rpg.combat.advance_turn(phenny,rpg,rpg.character)
        return
    if o == 'skill':
        if len(opt) < 2:
            if len(rpg.character.skill) == 1:
                phenny.say("You use the skill: "+rpg.character.skill[0]+"!")
                res = rpg.use_skill(phenny,rpg.character.skill[0],rpg.character,rpg.combat.enemy)
                if res == 0:
                    phenny.say("You don't have that skill.")
                    return
                if res == 1:
                    phenny.say("You don't have enough skill points remaining to use that skill.")
                    return
                else:
                    return
            else:
                phenny.say("You need to specify a skill.")
                return
        o1 = opt[1]
        if o1.lower() in [i.lower() for i in rpg.character.skill]:
            phenny.say("You use the skill: "+opt[1].lower().capitalize()+"!")
            res = rpg.use_skill(phenny,opt[1].lower().capitalize(),rpg.character,rpg.combat.enemy)
            return
        else:
            phenny.say("You need to specify a skill that you actually have.")
            return
        if res == 0:
            phenny.say("You don't have that skill.")
            return
        if res == 1:
            phenny.say("You don't have enough skill points remaining to use that skill.")
            return
        else:
            return
    else:
        phenny.say("You do what with the what now?")
        return
rpgturn.name = 'turn'
rpgturn.commands = ['rpgturn']
rpgturn.priority = 'low'

def rpgtown(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", your character has already been buried in the town cemetary, too deep to dig out.")
        return
    if rpg.whereareyou == "shop":
        phenny.say("You leave the shop and head back into the town square.")
        rpg.destination("town")
        return
    if rpg.whereareyou == "shrine":
        phenny.say("You leave the shrine and head back into the town square.")
        rpg.destination("town")
        return
    if rpg.whereareyou == "puzzle":
        phenny.say("Wow, is the puzzle really so hard that you want to go back to bed? You have to step it up, man, if you wanna be a True hero...")
        return
    if rpg.whereareyou != "town":
        phenny.say("You're in the dungeon, dimwit. You'd think the dank air and growl of monsters would have clued you in...")
        return
    opt = input.groups()[1]
    if not opt:
        rpg.telltown(phenny)
        return
    opt = opt.split()
    if opt[0].lower() == 'dungeon':
        rpg.save()
        if len(opt) < 2:
            phenny.say("You head into the dungeon.")
            rpg.dungeonlevel = 1
            rpg.destination("start")
            return
        else:
            try:
                lvl = int(opt[1])
            except:
                lvl = 1
            if lvl > rpg.maxdgnlevel:
                phenny.say("You haven't found the stairs to that level yet.")
                return
            rpg.dungeonlevel = lvl
            phenny.say("You head to level "+str(lvl)+" of the dungeon.")
            rpg.destination("start")
            return
    elif opt[0].lower() == 'shrine':
        rpg.visit_shrine(phenny)
        return
    elif opt[0].lower() == 'shop':
        rpg.visit_shop(phenny)
        return
    elif opt[0].lower() == 'quest':
        rpg.questhall(phenny)
        return
    elif opt[0].lower() == 'rest':
        phenny.say("You hit the sack. Once you've annoyed all the bedbugs with your ineffectual fists, you lay down and sleep.")
        rpg.character.sleep()
        rpg.save()
        return
    else:
        phenny.say("Sorry, I didn't recognize that command. Try again?")
        return
rpgtown.name = 'rpgtown'
rpgtown.commands = ['rpgtown']
rpgtown.priority = 'low'

def rpgdungeon(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", your character is dead, so you can't explore the dungeon.")
        return
    if rpg.whereareyou == "town":
        tvn = namegen.taverngen()[0]
        phenny.say("You're not in the dungeon, you're in town. Have you been drinking at the "+tvn+"again?")
        return
    if rpg.whereareyou == "shop":
        phenny.say("You're in the shop. There's a secret door into the dungeon behind the canned goods, but the shopkeep certainly won't let you in...")
        return
    if rpg.whereareyou == "combat":
        phenny.say("You... are already fighting something? I mean, you can wander around while being bludgeoned to death with your own stupidity, but I don't recommend it.")
        return
    if rpg.whereareyou == "puzzle":
        phenny.say("If I were you, I wouldn't leave a "+rpg.puzzle.thing+" hanging like that...")
    opt = input.groups()[1]
    if not opt:
        phenny.say("So... what did you want to do, then?")
        return
    opt = opt.split()[0].lower()
    if opt == 'explore':
        if rpg.whereareyou == "stairs":
            rpg.godownstairs(phenny)
            return
        else:
            phenny.say("You head deeper into the dungeon...")
            rpg.destination("dungeon")
            rpg.explore(phenny)
            return
    elif opt == 'backtrack':
        if rpg.whereareyou == "start":
            phenny.say("You're already at the beginning of the level, Captain Redundant.")
            return
        if rpg.whereareyou == "stairs":
            phenny.say("You decide to hang around on level "+str(rpg.dungeonlevel)+" a little while longer.")
            rpg.destination("dungeon")
            return
        if rpg.check_backtrack():
            phenny.say("You successfully find your way back to the beginning of the level.")
            rpg.destination("start")
            return
        else:
            phenny.say("On your way back, you get lost! You find yourself in another room of the dungeon...")
            rpg.explore(phenny)
            return
    elif opt == 'return':
        if rpg.whereareyou != "start":
            phenny.say("You can't go back to town unless you're at the beginning of the level...")
            return
        rpg.destination("town")
        phenny.say("You head back to town.")
        return
    else:
        phenny.say("Sorry, I didn't recognize that command. Try again?")
        return
rpgdungeon.name = 'rpgdungeon'
rpgdungeon.commands = ['rpgdungeon']
rpgdungeon.priority = 'low'

def rpgpuzzle(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", your character is dead, so you can't do puzzle-y things... at least, not in this game, not until you have an alive character.")
        return
    if rpg.whereareyou != "puzzle":
        phenny.say("You're not being tested right now... lucky for you!")
        return
    opt = input.groups()[1]
    if not opt and rpg.puzzle.choice != "knowledge":
        phenny.say("The "+rpg.puzzle.thing+" is not amused by your hesitation.")
        return
    if not rpg.puzzle.choice:
        if type(opt) is list:
            opt = opt[0]
        if opt.lower() in ["gold","riches","knowledge","skip"]:
            rpg.puzzle.puzzleinit(phenny,rpg,opt)
            return
        else:
            phenny.say("The "+rpg.puzzle.thing+" is not amused. 'Make your choice, mortal. My patience grows short.'")
            return
    else:
        if rpg.puzzle.choice == "gold":
            rpg.puzzle.check_numguess(phenny,rpg,opt)
            return
        elif rpg.puzzle.choice == "riches":
            rpg.puzzle.check_riddleguess(phenny,rpg,opt)
            return
        elif rpg.puzzle.choice == "knowledge":
            rpg.puzzle.trialofbeing(phenny,rpg)
        else:
            phenny.say("There's been a puzzle malfunction...")
rpgpuzzle.name = 'rpgpuzzle'
rpgpuzzle.commands = ['rpgpuzzle']
rpgpuzzle.priority = 'low'

def rpgshrine(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath == 1:
        phenny.say("Sorry, "+input.nick+", your character is dead, and the Unknowable Gods are busy consuming its soul, so they can't pay attention to offerings.")
        return
    if rpg.whereareyou != "shrine":
        phenny.say("You're not in the Shrine right now...")
        return
    opt = input.groups()[1]
    if not opt:
        phenny.say("Yes. Shrine. OK?")
        return
    opt = opt.split()
    amt = 0 if len(opt) == 1 else opt[1]
    try:
        amt = int(amt)
    except:
        phenny.say("Hey! No funny business with the offering, bucko.")
        return
    choice = opt[0]
    if choice != '1' and choice != '2':
        phenny.say("You toss an offering into some imaginary bowl, and it clatters onto the floor. You scoop it up again before anyone notices.")
        return
    rpg.offering(phenny,choice,amt)
    return
rpgshrine.name = 'rpgshrine'
rpgshrine.commands = ['rpgshrine']
rpgshrine.priority = 'low'

def rpgchargen(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.character.name and not rpg.chardeath:
        phenny.say("You have an active character already... if you really want to make a new one, please quit and restart the game.")
        return
    opts = input.groups()[1]
    race = ''
    cls = ''
    fts = []
    nfeat = 1
    if not opts:
        pass
    else:
        opts = opts.split()
        nfeat = 1
        for o in opts:
            if o.lower() in draces.keys():
                race = o.lower()
                if race == 'human':
                    nfeat = 2
            if o.lower() in dclasses.keys():
                cls = o.lower()
            for j in dfeats.keys():
                if o.lower() == j.lower():
                    if len(fts) + 1 > nfeat:
                        phenny.say("You've chosen too many feats; I'll take them in the order you gave them.")
                    else:
                        fts.append(j)
    if not race:
        race = random.choice([random.choice(draces.keys()) for i in range(0,6)])
    if not cls:
        cls = random.choice([random.choice(dclasses.keys()) for i in range(0,6)])
    if not fts: 
        nfeat = 1
        if race == 'human':
            nfeat = 2
        fts = []
        for i in range(0,nfeat):
            fts.append(random.choice([random.choice(dfeats.keys()) for j in range(0,6)]))
    if nfeat == 2 and len(fts) == 1:
        fts.append(random.choice([random.choice(dfeats.keys()) for j in range(0,6)]))
    rpg.character.chargen(input.nick,race,cls,fts)
    rpg.new_char()
    rpg.destination("town")
    rpg.save()
    msg = "In the town of North Granby, the town militia has recently discovered that the plague of monsters harrassing the townspeople originates from a nearby dungeon crammed with nasties."
    msg += " As the resident adventurer, the Mayor of North Granby (a retired adventurer by the name of Sir Percival) has recruited you to clear out the dungeon."
    phenny.say(msg)
    rpg.character.tellchar(phenny)
    rpg.telltown(phenny,True)
rpgchargen.name = 'rpgchargen'
rpgchargen.commands = ['rpgchargen','rpgcg']
rpgchargen.priority = 'low'

def rpglvlup(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    if rpg.chardeath:
        phenny.say("Sorry, you can't level up because your character is dead.")
        return
    lim = rpg.character.level * 10
    if rpg.character.exp <lim:
        phenny.say("Sorry, it's not time for you to level up yet. You need "+str(lim - rpg.character.exp)+" more experience.")
        return
    opt = input.groups()[1]
    if not opt:
        rpg.character.levelup(random.choice([random.choice(dfeats.keys()) for j in range(0,6)]))
        return
    opt = opt.split()
    if len(opt) > 1:
        phenny.say("You picked too many feats! I'll use the first one I recognize.")
    for i in opt:
        for j in dfeats.keys():
            if i.lower() == j.lower():
                rpg.character.levelup(j)
                phenny.say("You have leveled up! You gained the "+j+" feat, and now have "+str(rpg.character.hp)+" hit points and "+str(rpg.character.sp)+" skill points.")
                return
    phenny.say("I didn't recognize your feat choice, sorry. You can try again; use .rpghelp feats to see the list of available feats.")
rpglvlup.name = 'rpglvlup'
rpglvlup.commands = ['rpglvlup']
rpglvlup.priority = 'low'

def rpgwhere(phenny,input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny,input):
        return
    wh = rpg.whereareyou
    if wh == 'dungeon':
        phenny.say("You're in the dungeon, on level "+str(rpg.dungeonlevel)+".")
    elif wh == 'town':
        phenny.say("You're in the town square.")
    elif wh == 'shop':
        phenny.say("You're in the General Store.")
    elif wh == 'combat':
        trn = " your " if rpg.combat.turnorder[rpg.combat.turn % 2] == "player" else " the monster's "
        phenny.say("You're in the middle of a fight! It's"+trn+"turn.")
    elif wh == 'start':
        phenny.say("You're in the dungeon, at the beginning of level "+str(rpg.dungeonlevel)+".")
    elif wh == 'stairs':
        phenny.say("You're in the dungeon, standing atop a flight of stairs.")
    elif wh == 'puzzle':
        phenny.say("You're testing your mettle against a "+rpg.puzzle.thing+", of course.")
    elif wh == 'shrine':
        phenny.say("You're bumbling around in the Shrine.")
    else:
        phenny.say("Hm, I don't know /where/ you are.")
rpgwhere.name = 'rpgwhere'
rpgwhere.commands = ['rpgwhere']
rpgwhere.priority = 'low'

def rpgquit(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny,input):
        return
    phenny.say("Well... see you later, I guess... *sob*")
    phenny.write(['PART'], rpg.game_channel)
    del rpgs[input.nick]
rpgquit.name = 'rpgquit'
rpgquit.commands = ['rpgquit']
rpgquit.priority = 'low'

def rpg_active(phenny, input):
    if input.nick != 'sirpercival':
        return
    global rpgs
    if not rpgs:
        phenny.say("No active games right now.")
    else:
        chans = []
        for i in rpgs.keys():
            chans.append(rpgs[i].game_channel)
        phenny.say(', '.join(chans))
rpg_active.name = 'rpg_active'
rpg_active.commands = ['rpga']
rpg_active.priority = 'low'


def rpghelp(phenny, input):
    rpg = rpgs.get(input.nick,None)
    if not rpg:
        return
    if not rpg.validate_player(phenny, input):
        return
    #topics:
    topic = input.groups()[1]
    if not topic:
        phenny.say("Welcome to Percival's Quest! Here's a list of help topics: Commands [can also ask for help on each individual command], Backtrack, Classes, Dungeon, Equip, Explore, Feats, Game, Quest, Races, Rest, Shop, Skills, Stats, Treasure. You can also get a more complete version of this help at http://eikorpg.wikia.com/wiki/EikoRPG_Wiki")
        return
    topic = topic.lower()
    if topic == 'commands':
        phenny.say("Here is the list of possible commands (each should be preceded with a '.' when using): rpg, rpghelp, rpgbuy, rpgchargen, rpgdungeon, rpginit, rpglvlup, rpgload, rpgquit, rpgsell, rpgsheet, rpgtown, rpgturn, rpgwhere")
    elif topic == 'rpghelp' or topic == 'topics':
        phenny.say("Welcome to Percival's Quest! Here's a list of help topics: Commands [can also ask for help on each individual command], Backtrack, Classes, Dungeon, Equip, Explore, Feats, Game, Quest, Races, Rest, Shop, Skills, Stats, Treasure. You can also get a more complete version of this help at http://eikorpg.wikia.com/wiki/EikoRPG_Wiki")
    elif topic == 'rpgchargen':
        phenny.say("Once you've begun a new game, this is how you generate your character. Syntax: .rpgchargen [race], [class], [feats] -- note that if you don't provide them, any and all of those will be randomly generated.")
    elif topic == 'rpg':
        phenny.say("This is how you start the game in the main channel.")
    elif topic == 'rpgdungeon':
        phenny.say("This is how you explore the dungeon. Syntax: .rpgdungeon option -- options are Explore, Backtrack, or Return (to town). You can only return to town when you are at the beginning of a level; otherwise, you have to backtrack, which may or may not work.")
    elif topic == 'rpginit':
        phenny.say("This command initializes the game when you enter the channel. Syntax: .rpginit")
    elif topic == 'rpgload':
        phenny.say("When you initialize the game, use this command to load your progress, or .rpgchargen to start a new game. Syntax: .rpgload")
    elif topic == 'rpgtown':
        phenny.say("Back in town, this lets you select your next move. Syntax: .rpgtown option -- options are Dungeon [level] (note that you can only visit dungeon levels you've been to before), Questhall, Rest, or Shop.")
    elif topic == 'rpgturn':
        phenny.say("If you're in combat, use this command to act. Syntax: .rpgturn action -- actions are Attack, Equip, Flee, Skill [skill].")
    elif topic == 'backtrack':
        phenny.say("An option for .rpgdungeon to go back to the beginning of the level (so you can return to town). Your chance of backtracking successfully depends on your Will score.")
    elif topic == 'classes':
        phenny.say("The available classes are: "+", ".join(sorted(dclasses.keys())))
    elif topic == 'dungeon':
        phenny.say("An option for .rpgtown to enter the dungeon. You may specify a level number for a level you've already visited, and you'll go directly to that level.")
    elif topic == 'explore':
        phenny.say("An option for .rpgdungeon to explore the next room in the current level. When exploring a room, you'll find one of the following: a Monster, a Chest, Nothing, or Stairs. In the future, sirp may add Traps to the list.")
    elif topic == 'feats':
        phenny.say("The available feats are: "+", ".join(sorted(dfeats.keys())))
    elif topic == 'game':
        phenny.say("This is Percival's Quest, an IRC RPG written by sirpercival, and run by the ever-surprising Eiko.")
    elif topic == 'quest':
        phenny.say("An option for .rpgtown to visit the Questhall. At the Questhall, you will be given a quest to retrieve a certain item from a certain unique monster. There's one quest per dungeon level, and you have to complete them in order (though you can explore other dungeon levels, you won't encounter the quest monster off-level). When you complete a quest, you will be given... rewards.")
    elif topic == 'races':
        phenny.say("The available races are: "+", ".join(sorted(draces.keys())))
    elif topic == 'rest':
        phenny.say("An option for .rpgtown to regain your HP and SP. You can only rest while in town.")
    elif topic == 'shop':
        phenny.say("An option for .rpgtown to visit the shop so you can sell loot and buy equipment.")
    elif topic == 'equip':
        phenny.say("An option for .rpgturn to equip an item, unequipping whatever you have in the same slot (if anything). You can also use this out of combat.")
    elif topic == 'skills':
        phenny.say("The available skills are: "+", ".join(sorted(dskill.values())))
    elif topic == 'stats':
        phenny.say("Percival's Quest has 6 attributes ('stats'): Attack, which governs your physical attack prowess; Defense, which governs your defense against physical attacks; Reflex, which determines your initiative and your defense against some skills;")
        phenny.say("Fortitude, which determines your hit points and your defense against some skills; Mind, which affects your backtrack chance and your defense against some skills; and Skill, which determines your skill points and the effectiveness of your skills.")
    elif topic == 'treasure':
        phenny.say("When you defeat a monster or find a chest, you may find some loot, in the form of gold (GP), armors, weapons, or rings. sirp may add potions sometime in the future.")
    elif topic == 'rpgquit':
        phenny.say("The command to quit the game. Please do this when you're done playing!")
    elif topic == 'rpglvlup':
        phenny.say("Use this command to pick your feat when you gain a level. Syntax: .rpglvlup [feat] -- .rpghelp feats will give you the list of available feats. If you don't supply a feat, one will be chosen for you at random.")
    elif topic == 'rpgbuy':
        phenny.say("Buy stuff from the shop with this command. Syntax: .rpgbuy itemnumber")
    elif topic == 'rpgsell':
        phenny.say("Sell stuff back to the shop with this command. Syntax: .rpgsell lootnumber")
    elif topic == 'rpgwhere':
        phenny.say("Tells you where you are.")
    elif topic == 'rpgsheet':
        phenny.say("A command to display your character sheet.")
    else:
        phenny.say("I'm sorry, I don't recognize that topic. Try .rpghelp topics for a list of topics I can help you with.")
rpghelp.name = 'rpghelp'
rpghelp.commands = ['rpghelp']
rpghelp.priority = 'low'
