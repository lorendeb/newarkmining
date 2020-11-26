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
    parser.add_argument("arrivals_departures", choices=['arrivals', 'departures'],help="select incoming or leaving flights: arrivals or departures")
    parser.add_argument("day", choices=['today', 'yesterday', 'tomorrow'],help="select date: today, yesterday or tomorrow")
    parser.add_argument('-d', '--destination', action="store_true", help='list of day destination')
    parser.add_argument('-ot', '--ontime', action="store_true", help='list of on time flight')
    parser.add_argument('-dl', '--delayed', action="store_true", help='list of delayed flight')
    parser.add_argument('-b6', '--before6', action="store_true", help='list of flight between 00-6am')
    parser.add_argument('-b12', '--before12', action="store_true", help='list of flight between 6-12pm')
    parser.add_argument('-b18', '--before18', action="store_true", help='list of flight between 12-18pm')
    parser.add_argument('-b0', '--before00', action="store_true", help='list of flight between 18-12am')
    parser.add_argument('-ta','--terminala', action="store_true", help='list of flight from/to Terminal A')
    parser.add_argument('-tb','--terminalb', action="store_true", help='list of flight from/to Terminal B')
    parser.add_argument('-tc','--terminalc', action="store_true", help='list of flight from/to Terminal C')
    args = parser.parse_args()

    df = newark_df(args.arrivals_departures, args.day)

    if args.destination:
        print(df['City'])
    if args.ontime:
        print(df[df['Status'== ]])
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
        print(df[df['']])
    if args.terminalb:
        print(get_terminal('b', total_list))
    if args.terminalc:
        print(get_terminal('c', total_list))


if __name__ == '__main__':
    main()