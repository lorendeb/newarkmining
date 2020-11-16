import argparse

day = 'today'
URL = 'https://www.airport-ewr.com/newark-departures'


if day == 'yesterday':
    URL += '?day=yesterday'
    URLdetailsending = '?day=yesterday'
elif day == 'tomorrow':
    URL += '?day=tomorrow'
    URLdetailsending = '?day=tomorrow'

parser = argparse.ArgumentParser()
parser.add_argument("day", choices=['today', 'yesterday', 'tomorrow'],help="select date: today, yesterday or tomorrow")
parser.add_argument('-d', '--destination', action="store_true", help='list of day destination')
parser.add_argument('-ot', '--ontime', action="store_true", help='list of on time flight')
parser.add_argument('-dl', '--delay', action="store_true", help='list of delayed flight')
parser.add_argument('-b6', '--before6', action="store_true", help='list of flight between 00-6am')
parser.add_argument('-b12', '--before12', action="store_true", help='list of flight between 6-12pm')
parser.add_argument('-b18', '--before18', action="store_true", help='list of flight between 12-18pm')
parser.add_argument('-b0', '--before00', action="store_true", help='list of flight between 18-12am')