import pandas as pd
from newark import newark_df
import re
import mysql.connector
from mysql.connector import errorcode

user_name = input('Please enter username for MySql (usually root)')
password = input('Please enter password for MySql')
mydb = mysql.connector.connect(user=user_name, password=password, host='localhost')
cursor = mydb.cursor()

def airports_df(all_df):
    # checking if table airports exist:
    try:
        cursor.execute("select * from airports")
        # checking if table not empty
        q_result = cursor.fetchall()
        if q_result:
            # creating dict of index:[airport,iata] for old airports
            airport_dict = {index: [airport, iata] for index, airport, iata in cursor.fetchall()}
            # list of all former airports to compare
            former_airports_list = [i[0] for i in list(airport_dict.values())]
            # checking what is the last index
            last_ind = max(airport_dict.keys())
            new_ap_dict = {}
            # checking if the new airport name is in the oldies list
            for index, row in all_df.iterrows():
                if row['airport'] not in former_airports:
                    # if so - add to the new dict the index and name and iata
                    new_ap_dict[last_ind + 1] = [row['airport'], row['iata']]
                    last_ind += 1
            # concat 2 dicts
            airport_dict = airport_dict.update(new_ap_dict)
            # create df
            airports = pd.DataFrame(list(airports_dict.items()), columns=['airport', 'iata'])
            return airports

        # if table is empty
        else:
            airports_dict = {}
            for index, row in all_df.iterrows():
                airports_dict[row['airport']] = row['iata'].strip()
            airports = pd.DataFrame(list(airports_dict.items()), columns=['airport', 'iata'])
            airports.index = airports.index + 1
            return airports

    except mysql.connector.Error as err:
        airports_dict = {}
        for index, row in all_df.iterrows():
            airports_dict[row['airport']] = row['iata'].strip()
        airports = pd.DataFrame(list(airports_dict.items()), columns=['airport', 'iata'])
        airports.index = airports.index + 1
        return airports


def status_df(all_df):
    # checking if table status exist:
    try:
        cursor.execute("select * from status")
        # checking if table not empty
        q_result = cursor.fetchall()
        if q_result:
            # dictionary that contain former status from query
            status_dict = {index: status for index, status in q_result}
            # list that contain new status from df ant not in the former dict
            new_status = [i for i in all_df['status'].unique() if not i in status_dict.values()]
            # checking what index give the new status
            last_ind = max(status_dict.keys())
            # looping over the list too
            ind_for_new = 0
            for i in range(last_ind + 1, last_ind + len(new_status) + 1):
                # adding the new status to th dict
                status_dict[i] = new_status[ind_for_new]
                ind_for_new += 1
            # make df from the new dictinary
            status = pd.DataFrame(all_df['status'].unique(), columns=['status'])
            return status
        # if table exist but empty
        else:
            status = pd.DataFrame(all_df['status'].unique(), columns=['status'])
            status.index = status.index + 1
            return status

    # if it's the first scrape - create status df:
    except mysql.connector.Error as err:
        # logging.error('first scraping')
        status = pd.DataFrame(all_df['status'].unique(), columns=['status'])
        status.index = status.index + 1
        return status


def all_flights_df(all_df):
    airports = airports_df(all_df)
    airports_dict = {v: k for k, v in airports.to_dict()['airport'].items()}
    airport_id = all_df['airport'].replace(airports_dict)

    status = status_df(all_df)
    status_dict = {v: k for k, v in status.to_dict()['status'].items()}
    status_id = all_df['status'].replace(status_dict)

    bench1 = airport_id
    bench2 = all_df[['estimated_hour', 'departure_hour', 'departure_terminal', 'departure_gate',
                     'arrival_hour', 'arrival_terminal', 'arrival_gate']]
    bench3 = status_id
    bench4 = all_df[['arrival_departure', 'date']]

    all_flights = pd.concat([bench1, bench2, bench3, bench4], axis=1)
    all_flights = all_flights.rename(columns={'airport': 'airport_id', 'status': 'status_id'})

    all_flights['estimated_hour'] = pd.to_datetime(
        all_flights['estimated_hour'].apply(lambda x: x.split('(')[0]), infer_datetime_format=True).dt.time
    all_flights['departure_hour'] = pd.to_datetime(
        all_flights['departure_hour'].apply(lambda x: x.split('(')[0]), infer_datetime_format=True).dt.time
    all_flights['arrival_hour'] = pd.to_datetime(
        all_flights['arrival_hour'].apply(lambda x: x.split('(')[0]), infer_datetime_format=True).dt.time
    return all_flights


def flights_numbers_df(all_df):
    flight_num = list(enumerate(all_df['flight_number'], 1))
    flight_num_split = []
    for tup in flight_num:
        flight = tup[1].split(',')
        for j in range(len(flight)):
            new_tup = list()
            new_tup.append(tup[0])
            new_tup.append(flight[j])
            flight_num_split.append(new_tup)
    flights_numbers = pd.DataFrame(flight_num_split, columns=['flight_id', 'flight_number'])
    return flights_numbers


def airline_per_flight_df(all_df):
    airlines = list(enumerate(all_df['airline'], 1))
    airlines_split = []
    for tup in airlines:
        airline = tup[1].split('\n')
        for j in range(len(airline)):
            new_tup = list()
            new_tup.append(tup[0])
            new_tup.append(airline[j])
            airlines_split.append(new_tup)
    airline_per_flight = pd.DataFrame(airlines_split, columns=['flight_id', 'airline_name'])
    airline_per_flight.index = airline_per_flight.index + 1
    return airline_per_flight
