from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from newark import *
from small_df import *
import numpy as np
from query_api import *
import config as CFG
import logging


logging.basicConfig(filename='newark.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE %(lineno)d: %(message)s',
                    level=logging.INFO)


def create_database(mydb,cursor):
    """
    creating the database
    :param cursor: connection to mysql
    :param mydb: connection to mysql
    :return: None
    """

    try:
        cursor.execute("CREATE DATABASE {}".format(CFG.DB_NAME))
        logging.info("CREATE DATABASE {}".format(CFG.DB_NAME))
        print('DATABASE {} created'.format(CFG.DB_NAME))
    except mysql.connector.Error as err:
        logging.error("Failed creating database: {}".format(err))
        print("Failed creating database: {}".format(err))
    mydb.commit()

def use_db(mydb,cursor):
    """
    Using database. if db doesn't exist - print a message and create it.
    :param cursor: connection to mysql
    :param mydb: connection to mysql
    :return: None
    """
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

def create_table(mydb,cursor):
    """
    Creating tables based on TABLES defined in config (if not exist already).
    :param cursor: connection to mysql
    :param mydb: connection to mysql
    :return: None
    """
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

def insert_to_table(mydb,cursor,table,df):
    '''
    Insert data from df to tables
    :param cursor: connection to mysql
    :param mydb: connection to mysql
    :param table: table to insert
    :param df: df to pull data from.
    :return: None
    '''
    cols = ", ".join([str(i) for i in df.columns.tolist()])
    for i,row in df.iterrows():
        sql = '''INSERT INTO ''' + table + ''' (''' + cols + ''') VALUES (''' + '''%s,''' * (len(row) - 1) + '''%s)'''
        cursor.execute(sql, tuple(row))
    logging.info('Insert values to table {} completed'.format(table))
    print('Insert values to table {} completed'.format(table))
    mydb.commit()


def connect_mysql():
    '''
    creating connection to mysql
    :return: db instance and cursor to use for queries
    '''
    connected = False
    while not connected:
        try:
            user_name = input('Please enter username for MySql (usually root)')
            password = input('Please enter password for MySql')
            mydb = mysql.connector.connect(user=user_name, password=password, host='localhost')
            cursor = mydb.cursor()
            logging.info('Connected to mysql')
            connected = True
        except mysql.connector.Error as err:
            print("Connection to mysql failed. Please try again. Error: {}".format (err))
            logging.error('Connection to mysql failed')

    return mydb,cursor

def create_all_df(cursor):
    '''
    create 6 df for each information kind.
    concating all df to one df all_flights_df
    connect to mysql to check if there is a table and match the index of the new scarped info
    fixing the index.
    :param cursor: connection to mysql
    :return: all_df which is the big df of the last scraping
    '''

    print('Scraping data from website... please wait')

    # creating df based on scarped data
    arrivals_df_tod = newark_df('arrivals', 'today')
    arrivals_df_tom = newark_df('arrivals', 'tomorrow')
    arrivals_df_yes = newark_df('arrivals', 'yesterday')
    departures_df_tod = newark_df('departures', 'today')
    #departures_df_tom = newark_df('departures', 'tomorrow')
    departures_df_yes = newark_df('departures', 'yesterday')
    logging.info('Data scraped successfully')

    # concat all df to one big df - all information from 3 days and departures+arrivals
    all_df = pd.concat([arrivals_df_tod, arrivals_df_tom, arrivals_df_yes, departures_df_tod, departures_df_yes])
    all_df.drop_duplicates(inplace=True)

    #checking the last index in the table all_flights(if exist)
    #if so - defining the first index of the scraped table to match
    cursor.execute("select flight_id from all_flights order by flight_id DESC LIMIT 1")
    last_ind = cursor.fetchall()
    if last_ind:
        last_ind = last_ind[0][0]
        if last_ind >= 0:
            all_df = all_df.set_index(np.arange(last_ind + 1, last_ind + 1 + len(all_df)))
    logging.info('all_df created')

    return all_df


def create_small_df(all_df):
    '''
    creating small df for the tables
    :param all_df: the big df from scraping
    :return: df to match the tables in db
    '''
    airports = airports_df(all_df)
    status = status_df(all_df)
    all_flights = all_flights_df(all_df)
    flights_numbers = flights_numbers_df(all_df)
    airline_per_flight = airline_per_flight_df(all_df)
    logging.info('small df created')
    return airports,status,all_flights,flights_numbers,airline_per_flight

def create_db_tables(mydb,cursor):
    '''
    create the db and tables in mysql
    :param mydb: conncetion to db
    :param cursor: executing commands
    :return: None
    '''
    create_database(mydb,cursor)
    use_db(mydb,cursor)
    create_table(mydb,cursor)

def insert_info_to_tables(mydb,cursor):
    '''
    insert info from df to tables
    :return: None
    '''
    all_df = create_all_df(cursor)
    airports, status, all_flights, flights_numbers, airline_per_flight = create_small_df(all_df)

    insert_to_table(mydb,cursor,'airports',airports)
    insert_to_table(mydb, cursor, 'status', status)
    insert_to_table(mydb, cursor, 'all_flights', all_flights)
    insert_to_table(mydb, cursor, 'flights_numbers', flights_numbers)
    insert_to_table(mydb, cursor, 'airline_per_flight', airline_per_flight)


def close_connection(mydb,cursor):
    '''
    closing connection to mysql
    :param mydb: conncetion to db
    :param cursor: conncetion to db
    :return: None
    '''
    cursor.close()
    mydb.close()

def wrapper_db():
    mydb, cursor = connect_mysql()
    create_db_tables(mydb,cursor)
    insert_info_to_tables(mydb,cursor)
    update_api_airport(mydb, cursor, get_list_iata(cursor), get_df_api(get_list_iata(cursor)))
    close_connection(mydb,cursor)



