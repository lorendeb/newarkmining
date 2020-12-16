from create_db import *
import argparse
from query_api import *
import config as CFG


def wrapper_db():
    mydb, cursor = connect_mysql()
    create_db_tables(mydb,cursor)
    insert_info_to_tables(mydb,cursor)
    update_api_airport(mydb, cursor, get_list_iata(cursor), get_df_api(get_list_iata(cursor)))
    close_connection(mydb,cursor)


def main():
    parser = argparse.ArgumentParser(description='Scrapping Newark website!')
    parser.add_argument("arrivals_departures", choices=['arrivals', 'departures'],
                        help="select incoming or leaving flights: arrivals or departures")
    parser.add_argument('day', choices=['today', 'yesterday', 'tomorrow'],
                        help="select day: today, yesterday or tomorrow")
    parser.add_argument('-d', '--destination',  help='Filter by destination / origin')
    parser.add_argument('-s', '--status',
                        help='Filter by flight status: On-time, Delayed, Canceled, Landed ...')
    parser.add_argument('-a', '--airline', help='Filter by airline')
    parser.add_argument('-t','--terminal', help='Filter by Terminal (A, B or C)')
    parser.add_argument('-fn','--flightnumber', help='Filter by flight number')
    parser.add_argument('-cb','--createdb',action="store_true", help='Create database for yesterday, today and tomorow flight')
    args = parser.parse_args()

    if args.createdb:
        wrapper_db()
    else:

        df = newark_df(args.arrivals_departures, args.day)
        if args.day == CFG.TOMORROW:
            if args.arrivals_departures.lower() == CFG.DEPARTURES:
                verb = CFG.FUTURE_L
            else:
                verb = CFG.FUTURE_A
        elif args.day == CFG.TODAY:
            if args.arrivals_departures.lower() == CFG.DEPARTURES:
                verb = CFG.PAST_L
            else:
                verb = CFG.FUTURE_A
        else:
            if args.arrivals_departures.lower() == CFG.DEPARTURES:
                verb = CFG.PRESENT_L
            else:
                verb = CFG.PRESENT_A
        if args.arrivals_departures.lower() == CFG.DEPARTURES:
            prep = CFG.TO
        else:
            prep = CFG.FROM

        if args.destination:
            df = df.dropna(subset=['City'])
            df = df[df['City'].str.contains(args.destination)]

        if args.status:
            df = df.dropna(subset=['Status'])
            df = df[df['Status'].str.contains(args.status)]

        if args.airline:
            df = df.dropna(subset=['Airline'])
            df = df[df['Airline'].str.contains(args.airline)]

        if args.terminal:
            if args.arrivals_departures.lower() == CFG.DEPARTURES:
                df = df.dropna(subset=['Departure_Terminal'])
                df = df[df['Departure_Terminal'].str.contains(args.terminal.upper())]
            else:
                df = df.dropna(subset=['Arrival_Terminal'])
                df = df[df['Arrival_Terminal'].str.contains(args.terminal.upper())]

        if args.flightnumber:
            df = df.dropna(subset=['Flight_number'])
            df = df[df['Flight_number'] == args.flightnumber]

        if df.shape[CFG.NUMBER_ROWS] != CFG.EMPTY:
            print('{}, the following flights {} Newark:'.format(args.day.capitalize(),verb))
            flight_num = [", ".join(flightnum.split(CFG.NEW_LINE)) for flightnum in df['Flight_number']]
            dest = [dest for dest in df['City']]
            term = [term for term in df['Departure_Terminal']]
            gate = [gate for gate in df['Departure_Gate']]
            airline = [airline for airline in df['Airline']]
            status = [status for status in df['Status']]
            for index in range(len(flight_num)):
                print('Flight number :{}, {} {} from Terminal {} and Gate {} with {}, Status :{}'.format(
                    flight_num[index], prep, dest[index], term[index], gate[index], airline[index],
                    status[index]
                ))

        else:
            print('No flight are meeting our filters ! ')


if __name__ == '__main__':
    main()
