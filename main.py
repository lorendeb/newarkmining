from new import *
from cmdfunct import *
import argparse


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
        # print(ontime['City'])
        print("The flights on time are: {}".format(
                " and ".join([", ".join(ontime['City'][:len(ontime['City'])-1]),ontime['City'][ontime(df['City'])-1]])))

    if args.delayed:
        delayed = get_status_('Delayed', df)
        # print(delayed["City"])
        print("The flights delayed are: {}".format(
                ", ".join(delayed['City'])))


    if args.from0:
        slot = get_time_slot(CFG.FIRST_SECTION, df)
        print("The following flights will/have {} Newark from midnight to 6am {}:{}".format(
             verb, args.arrivals_departures, ", ".join(slot['City'])))

    if args.from6:
        slot = get_time_slot(CFG.SECOND_SECTION, df)
        print("The following flights will/have {} Newark from 6am to 12pm {}:{}".format(
            verb, args.arrivals_departures, ", ".join(slot['City'])))

    if args.from12:
        slot = get_time_slot(CFG.THIRD_SECTION, df)
        print("The following flights will/have {} Newark from 12pm to 6pm {}:{}".format(
            verb, args.arrivals_departures, ", ".join(slot['City'])))

    if args.from18:
        slot = get_time_slot(CFG.FOURTH_SECTION, df)
        print("The following flights {} Newark from 6pm to 12am {}:{}".format(
            verb, args.arrivals_departures, ", ".join(slot['City'])))

    if args.terminala:
        terminal = get_terminal(args.arrivals_departures, CFG.A, df)
        print("These flights {} Newark {} at terminal A:".format(
            verb, args.arrivals_departures, ", ".join(terminal['City'])))

    if args.terminalb:
        terminal = get_terminal(args.arrivals_departures, CFG.B, df)
        print("These flights {} Newark {} at terminal B:".format(
            verb, args.arrivals_departures,
            ", ".join(terminal['City'])))

    if args.terminalc:
        terminal = get_terminal(args.arrivals_departures, CFG.C, df)
        print("These flights {} Newark {} at terminal C:".format(
            verb, args.arrivals_departures,
            ", ".join(terminal['City'])))


if __name__ == '__main__':
    main()