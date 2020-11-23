from newark import *
from cmdfunct import *
import argparse


DESTINATION_INDEX = 0
AIRCOMPANY_INDEX = 1
FLIGHT_NUMBER = 2
ESTIMATED_HOUR_INDEX= 3
HOUR_DEPARTURE_INDEX = 4
HOUR_ARRIVAL_INDEX = 5
TERMINAL_DEPARTURE_INDEX = 6
GATE_DEPARTURE_INDEX = 7
TERMINAL_ARRIVAL_INDEX = 8
GATE_ARRIVAL_INDEX = 9
STATUS_INDEX = 10


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", choices=['today', 'yesterday', 'tomorrow'],help="select date: today, yesterday or tomorrow")
    parser.add_argument('-d', '--destination', action="store_true", help='list of day destination')
    parser.add_argument('-ot', '--ontime', action="store_true", help='list of on time flight')
    parser.add_argument('-dl', '--delayed', action="store_true", help='list of delayed flight')
    parser.add_argument('-b6', '--before6', action="store_true", help='list of flight between 00-6am')
    parser.add_argument('-b12', '--before12', action="store_true", help='list of flight between 6-12pm')
    parser.add_argument('-b18', '--before18', action="store_true", help='list of flight between 12-18pm')
    parser.add_argument('-b0', '--before00', action="store_true", help='list of flight between 18-12am')
    parser.add_argument('-ta','--terminala', action="store_true", help='list of flight from Terminal A')
    parser.add_argument('-tb','--terminalb', action="store_true", help='list of flight from Terminal B')
    parser.add_argument('-tc','--terminalc', action="store_true", help='list of flight from Terminal C')
    args = parser.parse_args()

    total_list = newark_list(args.day)

    if args.destination:
        print(get_destination_list(total_list))
    if args.ontime:
        print(get_status('on-time',total_list))
    if args.delayed:
        print(get_status('delayed', total_list))
    if args.before6:
        print(get_time_slot(0, total_list))
    if args.before12:
        print(get_time_slot(6, total_list))
    if args.before18:
        print(get_time_slot(12, total_list))
    if args.before00:
        print(get_time_slot(18, total_list))
    if args.terminala:
        print(get_terminal('a', total_list))
    if args.terminalb:
        print(get_terminal('b', total_list))
    if args.terminalc:
        print(get_terminal('c', total_list))


if __name__ == '__main__':
    main()