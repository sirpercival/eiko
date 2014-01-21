import random
import re

def principles(phenny,input):
   try:
      n = int(input.group(2))
   except:
      n = 1
   if n > 5:
      n = 5
   foo = ('ALCH 101: Intro to Alchemetry',
      'ALCH 112: Spooky Solvents',
      'ARCD 101: Intro to Arcanodynamics',
      'ARCD 176: Disturbing Kinematics',
      'BIOY 101: Intro to Biollurgy',
      'BIOY 191: Blacksmithing for Biologists',
      'ELDK 101: Intro to Eldrikinetics',
      'ELDK 150: Kinetic Conversions',
      'GEOC 101: Intro to Geoccultism',
      'GEOC 117: Rocks for Jocks',
      'HEUR 101: Intro to Heuristicism',
      'HEUR 159: Experimental Thoughts',
      'IMCH 101: Intro to Imachination',
      'IMCH 167: Unbound Expectations',
      'KALD 101: Intro to Kaleidomantics',
      'KALD 107: Unearthly Colours',
      'YGGD 101: Intro to Yggdratecture',
      'YGGD 198: Unsettling Geometry I',
      'ALCH 202: Irregular Properties',
      'ALCH 286: Mysterious Metallurgy',
      'ARCD 204: Nonlinear Waves',
      'ARCD 230: Interpretive Charges',
      'BIOY 228: Animate Construction',
      'BIOY 273: Artificial Reckoning',
      'ELDK 219: Atypical Ballistics',
      'ELDK 276: Unnatural Propulsion',
      'GEOC 235: Bizarre Biomes',
      'GEOC 291: Unknown Oceans',
      'HEUR 245: Nonstatic Instruction',
      'HEUR 266: Unorthodox Triggers',
      'IMCH 228: Imperfect Images',
      'IMCH 295: Perturbed Mentalities',
      'KALD 238: Extrareal Hues',
      'KALD 282: Cthonic Dyes',
      'YGGD 212: Unsettling Geometry II',
      'YGGD 241: Incongruous Pathways',
      'ALCH 325: Preternatural Fluids',
      'ALCH 364: Unexpected Materials',
      'ARCD 350: Unlikely Thermodynamics',
      'ARCD 365: Unsubstantiated Light',
      'BIOY 340: Erratic Mutations',
      'BIOY 381: Eccentric Genetics',
      'ELDK 355: Strange Locomotion',
      'ELDK 399: Immaterial Travel',
      'GEOC 323: Curious Climates',
      'GEOC 374: Supernal Ecologies',
      'HEUR 302: Abnormal Behaviour',
      'HEUR 328: Exotic Intelligence',
      'IMCH 334: Nonsensical Senses',
      'IMCH 388: Glamorous Gramarie',
      'KALD 347: Superlunar Pigments',
      'KALD 379: Imperceptible Shades',
      'YGGD 353: Uncanny Cosmology II',
      'YGGD 371: Abstruse Causality',
      'Caloric Theory (6 ARCD)',
      'Chaos Theory (6 GEOC)',
      'Theory of Everything (one of each)',
      'Theory of Irreducible Complexity (6 YGGD)',
      'Theory of Kinetic Energy (4 ARCD, 4 ELDK)',
      'Theory of Luminiferous Aether (6 KALD)',
      'Theory of Monstrous Ecology (4 BIOY, 4 GEOC)',
      'Periodic Theory (6 ALCH)',
      'Theory of Soft Characteristics (6 BIOY)')
   for i in range(n):
      phenny.say(random.choice([random.choice(foo) for i in range(0,6)]))
principles.name = 'principles'
principles.commands = ['principles','gramarie']
principles.priority = 'low'

def principle_data(phenny, input):
   try:
      quer = input.group(2)
      if quer == 'help':
         phenny.say("Syntax: '.principle [searchterm]', where searchterm is a one-word term you'd like to search on.")
         phenny.say('You can try the index (e.g., ALCH101), which should always work. You can also try the name of the principle, or some part of it.')
         phenny.say('Finally, if more than one result matches, it should return all of them, as long as there are less than 6 results (e.g., .principle ARCD returns all arcanodynamics principles).')
         return
      foo = ['ALCH101: Intro to Alchemetry - Alter durability, hardness, heat capacity, or sturdiness.',
         'ALCH112: Spooky Solvents - Create alchemical fluids. [Spec]',
         'ALCH202: Irregular Properties - Alter buffering, flammability, magnetism, or resonance.',
         'ALCH286: Mysterious Metallurgy - Transmute between planetary metals. [Spec]',
         'ALCH325: Preternatural Fluids - Alter density and phase change properties.',
         'ALCH364: Unexpected Materials - Create ascended metals. [Spec]',
         'ARCD101: Intro to Arcanodynamics - Create silver (vital) and wood (puissance) transformers.',
         'ARCD176: Disturbing Kinematics - Create leather (wind) and iron (spin) transformers. [Spec]',
         'ARCD204: Nonlinear Waves - Create crystal (sonic) and gold (light) transformers.',
         'ARCD230: Interpretive Charges - Create copper (electric) and tin (acidic) transformers. [Spec]',
         'ARCD350: Unlikely Thermodynamics - Create ice (fire) and mercury (cold) transformers.',
         'ARCD365: Unsubstantiated Light - Create lead (nuclear) and platinum (faith) transformers. [Spec]',
         'BIOY101: Intro to Biollurgy - Create biostructure.',
         'BIOY191: Blacksmithing for Biologists - Create stuff out of biostructure. [Spec]',
         'BIOY228: Animate Construction - Convert biostructure into a chassis, and add grafts.',
         'BIOY273: Artificial Reckoning - Create circuited, instinctual, or sentient chassis. [Spec]',
         'BIOY340: Erratic Mutations - Add higher-level grafts to a chassis.',
         'BIOY381: Eccentric Genetics - Make a chassis able to reproduce. [Spec]',
         'ELDK101: Intro to Eldrikinetics - Create a simple orthogonal engine (iron, wood fuel).',
         'ELDK150: Kinetic Conversions - Store puissance in an engine for later use. [Spec]',
         'ELDK219: Atypical Ballistics - Create a ballistic engine (copper, bone fuel).',
         'ELDK276: Unnatural Propulsion - Create an ascending (silver, daylight fuel) or submerging (flesh, blood fuel) engine. [Spec]',
         'ELDK355: Strange Locomotion - Create badgerdrawn (stone/nuts+acorns), beeform (amber/honey), lightningleap (solid mercury/electricity), stonefish (diamond/seawater) engines.',
         'ELDK399: Immaterial Travel - Create aetherial (cold iron, moonsteel fuel) or planejumping (adamantine, sunmetal fuel) engines. [Spec]',
         'GEOC101: Intro to Geoccultism - Create copper (forest), gold (arctic), iron (desert), lead (swamp), or tin (grasslands) biomes.',
         'GEOC117: Rocks for Jocks - Create crystal (caverns) or platinum (city) biomes. [Spec]',
         'GEOC235: Bizarre Biomes - Place terrain features in your biomes.',
         'GEOC291: Unknown Oceans - Create mercury (freshwater) and silver (saltwater) biomes. [Spec]',
         'GEOC323: Curious Climates - Add climates and extreme weather to your biomes.',
         'GEOC374: Supernal Ecologies - Add supernatural terrain features to your biomes. [Spec]',
         'HEUR101: Intro to Heuristicism - Join gramarie into circuits, including logical decisions.',
         'HEUR159: Experimental Thoughts - Creatures inside a circuit bubble can communicate telepathically, share senses. [Spec]',
         'HEUR245: Nonstatic Instruction - Place control points in your circuits.',
         'HEUR266: Unorthodox Triggers - Allow logical decisions controlled by contingencies. [Spec]',
         'HEUR302: Abnormal Behavior - Principles preparing principles? DEAR GOD',
         'HEUR328: Exotic Intelligence - Create an Exotic Intelligence to be awesome. [Spec]',
         'IMCH101: Intro to Imachination - Create additive, static illusions (auditory, gustatory, olfactory, tactile, visual).',
         'IMCH167: Unbounded Expectations - Create ablative or differential illusions. [Spec]',
         'IMCH228: Imperfect Images - Create adaptive, programmed, or controlled illusions.',
         'IMCH295: Perturbed Mentalities - Illusions cause conditions, can be dream state. [Spec]',
         'IMCH334: Nonsensical Senses - Create illusions (mental, thermal, vestibular, vibratory).',
         'IMCH388: Glamorous Gramarie - Illusions can hurt people. [Spec]',
         'KALD101: Intro to Kaleidomantics - Create red (heat) and yellow (solid stone and metal) filters.',
         'KALD107: Unearthly Colors - Create blue (water) and orange (loose gases) filters. [Spec]',
         'KALD238: Extrareal Hues - Create green (poisons) and indigo (acids and bases) filters.',
         'KALD282: Cthonic Dyes - Create pink (space and time) filters. [Spec]',
         'KALD347: Superlunar Pigments - Create violet (living things) filters.',
         'KALD379: Imperceptible Shades - Create black (information) filters. [Spec]',
         'YGGD101: Intro to Yggdratecture - Create a semi-space.',
         'YGGD198: Unsettling Geometry - Create an alternating flux. [Spec]',
         'YGGD212: Unsettling Geometry II - Create a gravity or polarcane flux.',
         'YGGD241: Incongruous Pathways - Create closed and/or joined semispaces. [Spec]',
         'YGGD353: Uncanny Cosmology - Create a demiplane.',
         'YGGD371: Abstruse Casuality - Set time traits on your demiplanes. [Spec]',
         'THRY401: Caloric Theory - Create phlogiston (caloric) transformers.',
         'THRY402: Chaos Theory - Convert a geoccult pole into a self-sustaining environment.',
         'THRY403: The Theory of Everything - Reproduce the effects of any other non-theory principle.',
         'THRY404: The Theory of Irreducible Complexity - Become a minor deity on a demiplane of your creation.',
         'THRY405: The Theory of Kinetic Energy - Create eldrikinetic engine (kinetic) transformers.',
         'THRY406: The Theory of Luminiferous Aether - Create a huge rejuvenating sphere with color-dependent traits.',
         'THRY407: The Theory of Monstrous Ecology - Transform a biollurgical chassis into a living geoccult pole.',
         'THRY408: The Periodic Theory - Transmute any material into any other material of the same phase.',
         'THRY409: The Theory of Soft Characteristics - Pass on class levels and feats as genetic traits for a biollurgical chassis.']
      try:
         res = [i for i in foo if quer.upper() in i.upper()]
      except:
         phenny.say("Syntax: 'principle [searchterm], where searchterm is a one-word term you'd like to search on.")
         phenny.say('You can try the index (e.g., ALCH101), which should always work. You can also try the name of the principle, or some part of it.')
         phenny.say('Finally, if more than one result matches, it should return all of them, as long as there are less than 6 results (e.g., .principle ARCD returns all arcanodynamics principles).')
         return
      if len(res) == 0:
         phenny.say("I'm so sorry, "+input.nick+", but I don't recognize that principle. Try the principle index (e.g. KALD101), with no space; that should work better.")
         return
      if len(res) > 10:
         phenny.say("Sorry, "+input.nick+", there are too many results. Can you try again with more strict search parameters?")
         return
      for i,j in enumerate(res):
         phenny.say(j)
      return
   except:
      phenny.say("Syntax: 'principle [searchterm], where searchterm is a one-word term you'd like to search on.")
      phenny.say('You can try the index (e.g., ALCH101), which should always work. You can also try the name of the principle, or some part of it.')
      phenny.say('Finally, if more than one result matches, it should return all of them, as long as there are less than 6 results (e.g., .principle ARCD returns all arcanodynamics principles).')
principle_data.name = 'principle_data'
principle_data.commands = ['principle','prin']
principle_data.priority = 'low'