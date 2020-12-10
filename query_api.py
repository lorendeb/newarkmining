import requests
import config as CFG
import pandas as pd
import logging
import re


def get_df_api(list_of_iata):
    """
    build df from api query
    :param list_of_iata: list of iata
    :return: df
    """
    querystring = CFG.querystring
    list_dict_api = []
    if not querystring:
        logging.error(f'Invalid website for airports details to query')
        raise ValueError('Site for airports details does not respond. Impossible to scrap')
    logging.info(f'Airports details successfully scrapped')
    for iata in list_of_iata:
        querystring[CFG.IATA]=iata
        headers = CFG.headers
        response = requests.request("GET", CFG.url, headers=headers, params=querystring)
        list_dict_api.append(response.json())
    return pd.DataFrame(list_dict_api)


def get_list_iata(cursor):
    """
    get list of iata from airports table
    :param cursor: cursor on database newark
    :return: list of iata
    """
    cursor.execute(CFG.query_list_iata)
    tuple_of_iata = cursor.fetchall()
    list_of_iata = [re.sub(r'\W+', '', elem[0]) for elem in tuple_of_iata]
    return list_of_iata


def add_column_airport(mydb, cursor):
    """
    add new column to table airports from db newark
    :param mydb: connection to newark
    :param cursor: instance of mydb
    :return: none
    """
    for column in CFG.api_columns:
        query_add_column = '''ALTER TABLE airports ADD '''+ column + ''' VARCHAR(255)'''
        cursor.execute(query_add_column)
    logging.info('Add API columns to airports table')
    print('Add API columns to airports table')
    mydb.commit()


def update_api_airport(mydb, cursor, list_of_iata, df_api):
    """
    update api columns of table airports with data from api query
    :param mydb: connection to newark
    :param cursor: instance od newark
    :param list_of_iata: list of iata
    :param df_api: scrapping api query
    :return: none
    """
    cursor.execute(CFG.query_list_columns)
    columns_names = cursor.fetchall()
    if len(columns_names) == 3:
        add_column_airport(mydb, cursor)
    cursor.execute(CFG.query_safe_updates_0)
    logging.info('Add API data to airports column')
    print('Add API data to airports column')
    for iata in list_of_iata:
        cursor.execute(CFG.query_update_airport_table, (df_api[df_api['iata'] == iata]['icao'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['name'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['location'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['street_number'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['street'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['city'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['county'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['state'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['country_iso'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['country'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['postal_code'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['phone'].iloc[0],
                                                        df_api[df_api['iata'] == iata]['website'].iloc[0],
                                                        iata))
    mydb.commit()
    cursor.execute(CFG.query_safe_updates_1)

