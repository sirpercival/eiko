import sys, argparse
from parser import * #roll, ParseException

def diceroll(phenny, input):
    parser = argparse.ArgumentParser(description="Return the results of a dice expression")
    parser.add_argument('expression', type=str,    help='the expression to roll')
    args = parser.parse_args(input.groups(1))
    try:
        result = roll(**vars(args))
        phenny.reply(result)
    except ParseException as exception:
        phenny.reply("Parse failed: " + exception)
diceroll.name = 'diceroll'
diceroll.commands = ['diceroll', 'dr']
diceroll.priority = 'low'
