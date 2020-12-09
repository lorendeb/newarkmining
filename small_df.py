import pandas as pd
from newark import newark_df
import re


def airports_df(all_df):
    airports_dict = {}
    for index, row in all_df.iterrows():
        airports_dict[row['airport']] = row['iata'].strip()
    airports = pd.DataFrame(list(airports_dict.items()), columns=['airport', 'iata'])
    airports.index = airports.index + 1
    return airports


def status_df(all_df):
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


def airline_per_flights_df(all_df):
    airlines = list(enumerate(all_df['airline'], 1))
    airlines_split = []
    for tup in airlines:
        airline = tup[1].split('\n')
        for j in range(len(airline)):
            new_tup = list()
            new_tup.append(tup[0])
            new_tup.append(airline[j])
            airlines_split.append(new_tup)
    airlines_per_flight = pd.DataFrame(airlines_split, columns=['flight_id', 'airline_name'])
    airlines_per_flight.index = airlines_per_flight.index + 1
    return airlines_per_flight
