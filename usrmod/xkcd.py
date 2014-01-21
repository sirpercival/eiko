import random
import re

def portrait(phenny, input):
   phenny.say('http://i222.photobucket.com/albums/dd54/Prime32_temp/OotS/eiko_sudou_0044300x300_zps1dbbd5ed.png')
portrait.name = 'portrait'
portrait.commands = ['portrait','eiko']
portrait.priority = 'low'

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
