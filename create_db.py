from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from newark import *

DB_NAME = 'newark'

TABLES = {}
TABLES['arrivals'] = ('''CREATE TABLE arrivals 
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
                        Arrival_Departure VARCHAR(255))''')

TABLES['departures'] = ('''CREATE TABLE departures 
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
                        Arrival_Departure VARCHAR(255))''')

TABLES['flights'] = ('''CREATE TABLE flights
                        (ind INT PRIMARY KEY AUTO_INCREMENT, 
                        flight_index INT,
                        flight_number VARCHAR(255))''')

TABLES['city'] = ('''CREATE TABLE city 
                        (destination_id INT PRIMARY KEY AUTO_INCREMENT,
                        city_name VARCHAR(255),
                        city_short_name VARCHAR(255))''')

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
    print('Using {}'.format(DB_NAME))
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
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
        print("OK")
    mydb.commit()

def insert_to_table(table,df):
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    for i,row in df.iterrows():
        sql = '''INSERT INTO ''' + table + ''' (''' + cols + ''') VALUES (''' + '''%s,''' * (len(row) - 1) + '''%s)'''
        cursor.execute(sql, tuple(row))
    print('Insert values to table {} completed'.format(table))
    mydb.commit()

if __name__ == '__main__':
    to_from = input('Do you want to scrap over incoming flight (type *arrivals*) or leaving flight (type *departures*)')
    if to_from == 'arrivals':
        arrivals_df = newark_df(to_from)
    elif to_from == 'departures':
        departures_df = newark_df(to_form)
    flights_df = flight_num_df(newark_df(to_from))
    city_df = cities_df(newark_df(to_from))

    insert_to_table('arrivals',arrivals_df)
    insert_to_table('departures', departures_df)
    insert_to_table('flights', flights_df)
    insert_to_table('city', city_df)

cursor.close()
mydb.close()


