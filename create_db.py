from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from newark import *
from small_df import *
import numpy as np
import config as CFG
import logging

logging.basicConfig(filename='newark.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE %(lineno)d: %(message)s',
                    level=logging.INFO)

def create_database(cursor):
    '''
    creating the database
    :param cursor: connection to mysql
    '''
    try:
        cursor.execute("CREATE DATABASE {}".format(CFG.DB_NAME))
        logging.info("CREATE DATABASE {}".format(CFG.DB_NAME))
        print('DATABASE {} created'.format(CFG.DB_NAME))
    except mysql.connector.Error as err:
        logging.error("Failed creating database: {}".format(err))
        print("Failed creating database: {}".format(err))
    mydb.commit()

def use_db(cursor):
    '''
    Using database. if db doesn't exist - print a message and create it.
    :param cursor: connection to mysql
    '''
    try:
        cursor.execute("USE {}".format(CFG.DB_NAME))
        logging.info('mysql is using {}'.format(CFG.DB_NAME))
        print('USING DB {}'.format(CFG.DB_NAME))
    except mysql.connector.Error as err:
        logging.error("Database {} does not exists.".format(CFG.DB_NAME))
        print("Database {} does not exists.".format(CFG.DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            logging.info("Database {} created successfully.".format(CFG.DB_NAME))
            print("Database {} created successfully.".format(CFG.DB_NAME))
            mydb.database = CFG.DB_NAME
        else:
            logging.error('Error trying using DATABASE {}. Error: {}'.format(CFG.DB_NAME,err))
            print(err)
            exit(1)

def create_table(cursor):
    '''
    Creating tables based on TABLES defined in config (if not exist already).
    :param cursor: connection to mysql
    '''
    for table_name in CFG.TABLES:
        table_description = CFG.TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            logging.info('Table {} was created'.format(table_name))
            print("OK")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error('Trying to create table that already exist')
                print("already exists.")
            else:
                print(err.msg)
    mydb.commit()

def insert_to_table(table,df):
    '''
    Insert data from df to tables
    :param table: table to insert
    :param df: df to pull data from.
    '''
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    for i,row in df.iterrows():
        sql = '''INSERT INTO ''' + table + ''' (''' + cols + ''') VALUES (''' + '''%s,''' * (len(row) - 1) + '''%s)'''
        cursor.execute(sql, tuple(row))
    logging.info('Insert values to table {} completed'.format(table))
    print('Insert values to table {} completed'.format(table))
    mydb.commit()



if __name__ == '__main__':
    print('Scraping data from website... please wait')
    #creating db based on scarped data
    arrivals_df_tod = newark_df('arrivals','today')
    arrivals_df_tom = newark_df('arrivals', 'tomorrow')
    arrivals_df_yes = newark_df('arrivals', 'yesterday')
    departures_df_tod = newark_df('departures','today')
    #departures_df_tom = newark_df('departures', 'tomorrow')
    departures_df_yes = newark_df('departures', 'yesterday')

    #concat all df to one big df - all information from 3 days and departures+arrivals
    all_flights_df = pd.concat([arrivals_df_tod,arrivals_df_tom,arrivals_df_yes,departures_df_tod,departures_df_yes])
    all_flights_df.drop_duplicates(inplace=True)

    #creating df for cities to use in city table
    cities = all_flights_df[['City','City_Shortname']]
    all_flights_df.drop('City_Shortname', axis=1, inplace=True)

    #connect to mysql
    user_name = input('Please enter username for MySql')
    password = input('Please enter password for MySql')
    mydb = mysql.connector.connect(user=user_name, password=password, host='localhost')
    cursor = mydb.cursor()

    #create db, use it and create tables
    create_database(cursor)
    use_db(cursor)
    create_table(cursor)

    #if data as already inserted to table, change index to match the last index on table
    cursor.execute("select flight_id from all_flights order by flight_id DESC LIMIT 1")
    last_ind = cursor.fetchall()
    if last_ind:
        last_ind = last_ind[0][0]
        if last_ind >= 0:
            all_flights = all_flights_df.set_index(np.arange(last_ind+1, last_ind+1+len(all_flights_df)))

    #using functions to split df to 3 df that matches the tables
    flights_df = flight_num_df(all_flights_df)
    city_df = cities_df(cities)

    #checking if the user want to insert data to db. if yes - insert data to 3 tables
    answer = input('Do you want to insert data to db? (y/n)')
    if answer == 'y':
        insert_to_table('all_flights',all_flights_df)
        insert_to_table('flights', flights_df)
        insert_to_table('city', city_df)

    #clost connection to mysql
    cursor.close()
    mydb.close()


