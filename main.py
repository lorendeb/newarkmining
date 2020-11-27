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
    parser.add_argument('-f0', '--from0', action="store_true", help='list of flight between 00-6am')
    parser.add_argument('-f6', '--from6', action="store_true", help='list of flight between 6-12pm')
    parser.add_argument('-f12', '--from12', action="store_true", help='list of flight between 12-18pm')
    parser.add_argument('-f18', '--from18', action="store_true", help='list of flight between 18-12am')
    parser.add_argument('-ta','--terminala', action="store_true", help='list of flight from/to Terminal A')
    parser.add_argument('-tb','--terminalb', action="store_true", help='list of flight from/to Terminal B')
    parser.add_argument('-tc','--terminalc', action="store_true", help='list of flight from/to Terminal C')
    args = parser.parse_args()

    df = newark_df(args.arrivals_departures, args.day)
    if args.arrivals_departures == 'Departures':
        verb = 'leave'
    else:
        verb = 'arrive at'

    if args.destination:
        print("The following flights will {} Newark {}: {}".format(
                  verb, args.day, " and ".join([", ".join(df['City'][:len(df['City'])-1]),df['City'][len(df['City'])-1]])))

    if args.ontime:
        ontime = get_status_('On-time', df)
        print("The flights on time are: {}".format(
                " and ".join([", ".join(ontime[:len(ontime)-1]), ontime[len(ontime)-1]])))

    if args.delayed:
        delayed = get_status_('Delayed', df)
        print("The flights delayed are: {}".format(
            " and ".join([", ".join(delayed[:len(delayed) - 1]), delayed[len(delayed) - 1]])))

    if args.from0:
        slot = get_time_slot(0, df)
        print("The following flights will/have {} Newark from midnight to 6am {}:{}".format(
            verb, args.arrivals_departures, " and ".join([", ".join(slot[:len(slot) - 1]), slot[len(slot) - 1]])
        ))

    if args.from6:
        slot = get_time_slot(6, df)
        print("The following flights will/have {} Newark from 6am to 12pm {}:{}".format(
            verb, args.arrivals_departures, " and ".join([", ".join(slot[:len(slot) - 1]), slot[len(slot) - 1]])
        ))

    if args.from12:
        slot = get_time_slot(12, df)
        print("The following flights will/have {} Newark from 12pm to 6pm {}:{}".format(
            verb, args.arrivals_departures, " and ".join([", ".join(slot[:len(slot) - 1]), slot[len(slot) - 1]])
        ))

    if args.from18:
        slot = get_time_slot(18, df)
        print("The following flights {} Newark from 6pm to 12am {}:{}".format(
            verb, args.arrivals_departures, " and ".join([", ".join(slot[:len(slot) - 1]), slot[len(slot) - 1]])
        ))

    if args.terminala:
        terminal = get_terminal(args.arrivals_departures, "A", df)
        print("These flights {} Newark {} at terminal A:".format(
            verb, args.arrivals_departures,
            " and ".join([", ".join(terminal[:len(terminal) - 1]), terminal[len(terminal) - 1]])
        ))

    if args.terminalb:
        terminal = get_terminal(args.arrivals_departures, "B", df)
        print("These flights {} Newark {} at terminal B:".format(
            verb, args.arrivals_departures,
            " and ".join([", ".join(terminal[:len(terminal) - 1]), terminal[len(terminal) - 1]])
        ))

    if args.terminalc:
        terminal = get_terminal(args.arrivals_departures, "C", df)
        print("These flights {} Newark {} at terminal C:".format(
            verb, args.arrivals_departures,
            " and ".join([", ".join(terminal[:len(terminal) - 1]), terminal[len(terminal) - 1]])
        ))


if __name__ == '__main__':
    main()