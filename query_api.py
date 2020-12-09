import pandas as pd
import requests
import config as CFG



def list_dict_api(list_of_iata):
    querystring = CFG.querystring
    my_list = []
    for iata in list_of_iata:
        querystring[CFG.IATA]=iata
        headers = CFG.headers
        response = requests.request("GET", CFG.url, headers=headers, params=querystring)
        my_list.append(response.json())


def df_api(list_of_iata):
    return pd.DataFrame(list_of_iata(list_of_iata))


def add_to_df(df, list_of_iata):
    return pd.merge(df, df_api(list_of_iata), left_on='iata', right_on='iata')