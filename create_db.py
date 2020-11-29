from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from newark import *
from small_df import *
import numpy as np

DB_NAME = 'newark'

TABLES = {}
TABLES['all_flights'] = ('''CREATE TABLE all_flights 
                        (flight_id INT PRIMARY KEY AUTO_INCREMENT,
                        City VARCHAR(255),
                        Flight_number VARCHAR(255),
                        Airline VARCHAR(255),
                        Estimated_hour VARCHAR(255),
                        Departure_Hour VARCHAR(255),
                        Departure_Terminal VARCHAR(255),
                        Departure_Gate VARCHAR(255),
                        Arrival_Hour VARCHAR(255),
                        Arrival_Terminal VARCHAR(255),
                        Arrival_Gate VARCHAR(255),
                        Status VARCHAR(255),
                        Arrival_Departure VARCHAR(255),
                        date VARCHAR(255))''')

TABLES['flights'] = ('''CREATE TABLE flights
                        (orig_ind INT PRIMARY KEY, 
                        flight_id INT,
                        flight_number VARCHAR(255))''')


TABLES['city'] = ('''CREATE TABLE city 
                        (city_id INT PRIMARY KEY AUTO_INCREMENT,
                        City VARCHAR(255),
                        City_Shortname VARCHAR(255))''')

mydb = mysql.connector.connect(user='root',password='winston1', host= 'localhost')
cursor = mydb.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    mydb.commit()

try:
    cursor.execute("USE {}".format(DB_NAME))
    print('USING TABLE {}'.format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        mydb.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
        print("OK")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

    mydb.commit()

def insert_to_table(table,df):
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    for i,row in df.iterrows():
        sql = '''INSERT INTO ''' + table + ''' (''' + cols + ''') VALUES (''' + '''%s,''' * (len(row) - 1) + '''%s)'''
        cursor.execute(sql, tuple(row))
    print('Insert values to table {} completed'.format(table))
    mydb.commit()

if __name__ == '__main__':
    arrivals_df_tod = newark_df('arrivals','today')
    arrivals_df_tom = newark_df('arrivals', 'tomorrow')
    arrivals_df_yes = newark_df('arrivals', 'yesterday')
    departures_df_tod = newark_df('departures','today')
    #departures_df_tom = newark_df('departures', 'tomorrow')
    departures_df_yes = newark_df('departures', 'yesterday')

    all_flights_df = pd.concat([arrivals_df_tod,arrivals_df_tom,arrivals_df_yes,departures_df_tod,departures_df_yes])
    all_flights_df.drop_duplicates(inplace=True)
    cities = all_flights_df[['City','City_Shortname']]
    all_flights_df.drop('City_Shortname', axis=1, inplace=True)


    cursor.execute("select flight_id from all_flights order by flight_id DESC LIMIT 1")
    last_ind = cursor.fetchall()
    if last_ind:
        last_ind = last_ind[0][0]
        if last_ind >= 0:
            all_flights = all_flights_df.set_index(np.arange(last_ind+1, last_ind+1+len(all_flights_df)))

    flights_df = flight_num_df(all_flights_df)
    city_df = cities_df(cities)

    insert_to_table('all_flights',all_flights_df)
    insert_to_table('flights', flights_df)
    insert_to_table('city', city_df)

cursor.close()
mydb.close()


