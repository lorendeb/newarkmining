from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
DB_NAME = 'newark'


DB_NAME = 'employees'
TABLES = {}
TABLES['flight'] = ('''CREATE TABLE flight 
                        (flight_id INT PRIMARY KEY, 
                        destination_id VARCHAR(255),
                        airline_id INT,
                        flight_number VARCHAR(255),
                        status VARCHAR(255))''')

TABLES['departure'] = ('''CREATE TABLE departure
                        (flight_id INT PRIMARY KEY, 
                        terminal VARCHAR(255),
                        gate VARCHAR(255),
                        estimated_hour DATETIME,
                        real_hour DATETIME)''')

TABLES['arrival'] = ('''CREATE TABLE arrival 
                        (flight_id INT PRIMARY KEY, 
                        terminal VARCHAR(255),
                        gate VARCHAR(255),
                        estimated_hour DATETIME,
                        real_hour DATETIME)''')

TABLES['airline'] = ('''CREATE TABLE airline
                        (airline_id INT PRIMARY KEY, 
                        airline_name VARCHAR(255),
                        airline_shortname VARCHAR(255))''')

TABLES['destination'] = ('''CREATE TABLE destination
                        (destination_id INT PRIMARY KEY,
                        destination_name VARCHAR(255),
                        destination_short VARCHAR(255),
                        destination_site VARCHAR(255))''')

mydb = mysql.connector.connect(user='root',password='winston1', host= 'localhost', database = DB_NAME)
cursor = mydb.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
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

cursor.close()
mydb.close()


