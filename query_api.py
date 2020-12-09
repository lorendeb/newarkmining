import requests
import config as CFG
import pandas as pd
import logging
import pymysql
import re


def get_df_api(list_of_iata):
    querystring = CFG.querystring
    list_dict_api = []
    for iata in list_of_iata:
        querystring[CFG.IATA]=iata
        headers = CFG.headers
        response = requests.request("GET", CFG.url, headers=headers, params=querystring)
        list_dict_api.append(response.json())
    return pd.DataFrame(list_dict_api)


def get_list_iata(cursor):
    cursor.execute(CFG.query_list_iata)
    tuple_of_iata = cursor.fetchall()
    list_of_iata = [re.sub(r'\W+', '', elem[0]) for elem in tuple_of_iata]
    return list_of_iata


def add_column_airport(mydb, cursor):
    for column in CFG.api_columns:
        query_add_column = '''ALTER TABLE airports ADD '''+ column + ''' VARCHAR(255)'''
        cursor.execute(query_add_column)
    logging.info('Add API columns to airports table')
    print('Add API columns to airports table')
    mydb.commit()


def update_api_airport(mydb, cursor, list_of_iata, df_api):
    cursor.execute(CFG.query_list_columns)
    columns_names = cursor.fetchall()
    if len(columns_names)==3:
        add_column_airport(mydb, cursor)
    cursor.execute(CFG.query_safe_updates_0)
    for iata in list_of_iata:
        # cursor.execute("""UPDATE airports set latitude=%s WHERE iata=%s""",(df_api[df_api['iata'] == iata]['latitude'].iloc[0],iata))
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


user_name = 'root'
password = 'soeursDER4'
mydb = pymysql.connect(user=user_name, password=password, host='localhost')
cursor = mydb.cursor()
cursor.execute("USE newark")


update_api_airport(mydb,cursor,get_list_iata(cursor),get_df_api(get_list_iata(cursor)))
# cursor.execute(CFG.query_safe_updates_0)
# cursor.execute('UPDATE airports set icao=%s WHERE iata=%s',('voila','IAD'))
# print(cursor.fetchall())
# mydb.commit()
# cursor.execute(CFG.query_safe_updates_1)
