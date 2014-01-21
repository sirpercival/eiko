#!/usr/bin/env python
"""
scores.py - phenny Scores Module
Copyright 2010-2013, Michael Yanovich (yanovich.net) and Matt Meinwald,
    and Samuel Clements

More info:
 * phenny: https://github.com/myano/phenny/
 * Phenny: http://inamidst.com/phenny/
"""

import codecs
from modules import unicode as uc
import pickle
import os
import time


class Scores:
    def __init__(self):
        self.scores_filename = os.path.expanduser('~/.phenny/scores.txt')
        self.scores_dict = dict()
        self.load()
        self.STRINGS = {
            "nochan": "Channel, {0}, has no users with scores.",
            "nouser": "{0} has no score in {1}.",
            "rmuser": "User, {0}, has been removed from room: {1}.",
            "cantadd": "I'm sorry, but I'm afraid I can't add that user!",
            "denied": "I'm sorry, but I can't let you do that!",
            "invalid": "Invalid parameters entered.",
        }

    def str_score(self, nick, channel):
        return "%s: +%s/-%s, %s" % (nick,
                                    self.scores_dict[channel][nick][0],
                                    self.scores_dict[channel][nick][1],
                                    self.scores_dict[channel][nick][0] -
                                    self.scores_dict[channel][nick][1])

    def editpoints(self, phenny, input, nick, points):
        if not nick:
            return
        nick = uc.encode(nick.lower())
        if not nick:
            phenny.reply(self.STRINGS["cantadd"])
        elif (input.nick).lower() == nick:
            phenny.reply(self.STRINGS["denied"])
        else:
            nick = nick.lower()
            if input.sender not in self.scores_dict:
                self.scores_dict[input.sender] = {}
            if not nick in self.scores_dict[input.sender]:
                self.scores_dict[input.sender][nick] = [0, 0]

            # Add a point if points is TRUE, remove if FALSE
            if points:
                self.scores_dict[input.sender][nick][0] += 1
            else:
                self.scores_dict[input.sender][nick][1] += 1

            self.save()
            chan = input.sender
            phenny.say(self.str_score(nick, chan))
            
    def edpoints(self, phenny, nick, chan, points):
        if not nick:
            return
        nick = uc.encode(nick.lower())
        if not nick:
            phenny.reply(self.STRINGS["cantadd"])
        else:
            nick = nick.lower()
            if chan not in self.scores_dict:
                self.scores_dict[chan] = {}
            if not nick in self.scores_dict[chan]:
                self.scores_dict[chan][nick] = [0, 0]

            # Add a point if points is TRUE, remove if FALSE
            if points:
                self.scores_dict[chan][nick][0] += 1
            else:
                self.scores_dict[chan][nick][1] += 1

            self.save()
            phenny.say(self.str_score(nick, chan))
            
    def getscore(self, phenny, nick, chan):
        if not nick: return 0
        if chan not in self.scores_dict: return 0
        if not nick in self.scores_dict[chan]: return 0
        return self.scores_dict[chan][nick][0] - self.scores_dict[chan][nick][1]
    
    def save(self):
        """ Save to file in comma seperated values """
        os.rename(self.scores_filename, '%s-%s' % (self.scores_filename, str(time.time())))
        scores_file = codecs.open(self.scores_filename, 'w', encoding='utf-8')
        for each_chan in self.scores_dict:
            for each_nick in self.scores_dict[each_chan]:
                line = '{0},{1},{2},{3}\n'.format(each_chan, each_nick, self.scores_dict[each_chan][each_nick][0], self.scores_dict[each_chan][each_nick][1])
                scores_file.write(uc.decode(line))
        scores_file.close()

    def load(self):
        try:
            sfile = open(self.scores_filename, 'r')
        except:
            sfile = open(self.scores_filename, 'w')
            sfile.close()
            return
        for line in sfile:
            values = line.split(',')
            if len(values) == 4:
                channel = (values[0]).lower()
                if channel not in self.scores_dict:
                    self.scores_dict[channel] = dict()
                self.scores_dict[channel][values[1]] = [int(values[2]),
                                                          int(values[3])]
        if not self.scores_dict:
            self.scores_dict = dict()
        sfile.close()

    def view_scores(self, phenny, input):

        def ten(channel, ranking):
            channel = channel.lower()
            if channel not in self.scores_dict:
                return self.STRINGS["nochan"].format(channel)
            q = 0
            top_scores = list()
            if ranking == 'b':
                tob = 'Bottom'
            elif ranking == 't':
                tob= 'Top'
            str_say = "\x02%s 10 (for %s):\x02" % (tob, channel)
            sort = True
            if ranking == 'b':
                sort = False
            scores = sorted(self.scores_dict[channel].iteritems(),
                            key=lambda (k, v): (v[0] - v[1]), reverse=sort)
            for key, value in scores:
                top_scores.append(self.str_score(key, channel))
                if len(scores) == q + 1:
                    str_say += ' %s' % (uc.decode(top_scores[q]))
                else:
                    str_say += ' %s |' % (uc.decode(top_scores[q]))
                q += 1
                if q > 9:
                    break
            return str_say

        def given_user(nick, channel):
            nick = uc.encode(nick.lower())
            channel = channel.lower()
            if channel in self.scores_dict:
                if nick in self.scores_dict[channel]:
                    return self.str_score(nick, channel)
                else:
                    return self.STRINGS["nouser"].format(nick, channel)
            else:
                return self.STRINGS["nochan"].format(channel)

        self.load()
        line = input.group()[7:].split()
        current_channel = input.sender
        current_channel = current_channel.lower()

        if len(line) == 0 or (len(line) == 1 and line[0] == 'top'):
            ## .scores
            t10 = ten(current_channel, 't')
            phenny.say(t10)

        elif len(line) == 1 and not line[0].startswith("#"):
            ## .scores <nick>
            phenny.say(given_user(line[0], current_channel))

        elif len(line) == 1 and line[0].startswith("#"):
            ## .scores <channel>
            t10_chan = ten(line[0], 't')
            phenny.say(t10_chan)

        elif len(line) == 2 and line[0].startswith("#") and line[1] != "all":
            ## .scores <channel> <nick>
            phenny.say(given_user(line[1], line[0]))

        elif len(line) == 2 and not line[0].startswith("#") and line[1].startswith("#") and line[0] == "botom":
            ## .scores bottom <channel>
            b10 = ten(line[1], 'b')
            phenny.say(b10)

        elif len(line) == 2:
            ## .scores <nick> all
            outstr = "Scores for {0} in: ".format(line[0])
            for channel in self.scores_dict:
                for nick in self.scores_dict[channel]:
                    if nick == line[0].lower():
                        nick_scores = self.scores_dict[channel][nick]
                        outstr += "{0}: {1}/{2}, {3} | ".format(channel,
                                                                nick_scores[0],
                                                                nick_scores[1],
                                                                int(
                                                                nick_scores[0]
                                                                ) - int(
                                                                nick_scores[1]
                                                                ))
            if outstr.endswith("| "):
                outstr = outstr[:-2]
            phenny.say(outstr)

    def setpoint(self, phenny, input, line):
        if not input.admin:
            return
        line = line[10:].split()
        if len(line) != 4:
            return
        channel = uc.encode(line[0])
        nick = uc.encode(line[1]).lower()
        try:
            add = int(line[2])
            sub = int(line[3])
        except:
            phenny.say(self.STRINGS["invalid"])
            return

        if add < 0 or sub < 0:
            phenny.reply("You are doing it wrong.")
            return

        if channel not in self.scores_dict:
            self.scores_dict[channel] = dict()

        self.scores_dict[channel][nick] = [int(add), int(sub)]
        self.save()
        phenny.say(self.str_score(nick, channel))

    def rmuser(self, phenny, input, line):
        if not input.admin:
            return
        if len(line) < 9:
            phenny.reply("No input provided.")
            return
        line = line[8:].split()
        channel = uc.encode(input.sender)
        nick = uc.encode(line[0]).lower()

        def check(nick, channel):
            nick = nick.lower()
            channel = channel.lower()
            if channel in self.scores_dict:
                if nick in self.scores_dict[channel]:
                    del self.scores_dict[channel][nick]
                    return self.STRINGS["rmuser"].format(nick, channel)
                else:
                    return self.STRINGS["nouser"].format(nick, channel)
            else:
                return self.STRINGS["nochan"].format(channel)

        if len(line) == 1:
            ## .rmuser <nick>
            result = check(nick, input.sender)
            self.save()
        elif len(line) == 2:
            ## .rumser <channel> <nick>
            result = check(line[1], nick)
            self.save()

        phenny.say(result)

# phenny commands
user_scores = Scores()


def addpoint_command(phenny, input):
    """.addpoint <nick> - Adds 1 point to the score system for <nick>."""
    nick = input.group(2)
    if nick:
        nick = nick.strip().split()[0]
    user_scores.editpoints(phenny, input, nick, True)
addpoint_command.commands = ['addpoint']
addpoint_command.priority = 'high'
addpoint_command.rate = 180


def rmpoint_command(phenny, input):
    """.rmpoint <nick> - Removes 1 point to the score system for <nick>."""
    nick = input.group(2)
    if nick:
        nick = nick.strip().split()[0]
    user_scores.editpoints(phenny, input, nick, False)
rmpoint_command.commands = ['rmpoint']
rmpoint_command.priority = 'high'
rmpoint_command.rate = 180


def view_scores(phenny, input):
    """.scores <channel> <user> - Lists all users and their point values in the system. channel and user parameters are optional"""
    user_scores.view_scores(phenny, input)
view_scores.commands = ['points', 'point', 'scores', 'score']
view_scores.priority = 'medium'
view_scores.rate = 180


def setpoint(phenny, input):
    """.setpoint <channel> <nick> <number> <number> - Sets score for user."""
    line = input.group()
    if line:
        line = line.lstrip().rstrip()
    user_scores.setpoint(phenny, input, line)
setpoint.commands = ['setpoint']
setpoint.priority = 'medium'


def removeuser(phenny, input):
    """.rmuser <nick> -- Removes a given user from the system."""
    line = input.group()
    if line:
        line = line.lstrip().rstrip()
    user_scores.rmuser(phenny, input, line)
removeuser.commands = ['rmuser']
removeuser.priority = 'medium'

def epoints(phenny, nick, channel, points):
    user_scores.edpoints(phenny, nick, channel, points)


if __name__ == '__main__':
    print __doc__.strip()
