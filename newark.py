import grequests
from bs4 import BeautifulSoup
import requests
import config as CFG
import logging
import pandas as pd
from datetime import date
from datetime import timedelta
from small_df import *



# logging configuration- from Info level
logging.basicConfig(filename='newark.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE %(lineno)d: %(message)s',
                    level=logging.INFO)


def get_list(soup, class_):
    feature_list = [feature.text.strip('\n\t') for feature in soup.find_all('div', class_)]
    return feature_list


def get_soup(URL):
    # get web data
    page = requests.get(URL)
    resp = page.status_code
    if resp != CFG.RESPONSE:
        logging.error(f'Invalid website, request response: {resp}')
        return
    logging.info(f'Website successfully scrapped')
    # parse web data
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_url(arr_depar, day):
    if arr_depar == CFG.ARRIVALS:
        prefix = CFG.ARRIVAL_URL
    else:
        prefix = CFG.DEPARTURE_URL
    return [prefix + str(time) + '&day=' + day for time in CFG.TIMES]


def get_url_flight(arr_depar, flight_num,day):
    if arr_depar == CFG.ARRIVALS:
        return CFG.ARRIVAL_FLIGHT_URL + flight_num + "?day=" + day
    elif arr_depar == CFG.DEPARTURES:
        return CFG.DEPARTURE_FLIGHT_URL + flight_num + "?day=" + day


def get_status(soup):
    status = soup.find('div', class_="flight-status__title")
    return status


def get_df_column(soup):
    destination_list = get_list(soup, class_="flight-col flight-col__dest-term")
    # city_list = [destination.split('\n')[0] for destination in destination_list]
    # city_sn_list = [destination.split('\n')[1] for destination in destination_list]
    flight_number_list = get_list(soup, class_="flight-col flight-col__flight")
    airline_list = get_list(soup, class_="flight-col flight-col__airline")
    estimated_hour_list = get_list(soup, class_="flight-col flight-col__hour")
    flight_dictionary = {'City': destination_list,
                         # 'City_Shortname': city_sn_list,
                         'Flight_number': flight_number_list,
                         'Airline': airline_list,
                         'Estimated_hour': estimated_hour_list}
    df = pd.DataFrame(flight_dictionary)
    df.drop(df.index[0], inplace=True)
    return df


def get_df_row(arr_depar, day, flight_num_list):
    url_list = [get_url_flight(arr_depar, flight_num, day) for flight_num in flight_num_list]
    final_list = []
    for url in url_list:
        sp = get_soup(url)
        temp = get_list(sp, class_="flight-info__infobox-text")
        temp.append(get_status(sp))
        final_list.append(temp)
    df = pd.DataFrame(final_list, columns=['Departure_Hour', 'Departure_Terminal', 'Departure_Gate',
                                        'Arrival_Hour', 'Arrival_Terminal', 'Arrival_Gate', 'Status'])
    return df

def get_df_row_g(arr_depar, day, flight_num_list):
    url_list = [get_url_flight(arr_depar, flight_num, day) for flight_num in flight_num_list]
    final_list = []
    loop_end = len(url_list)//10
    for index in range(0, loop_end*10, 10):
        reqs = (grequests.get(u) for u in url_list[index:index + 10])
        resp = grequests.map(reqs)
        if not resp:
            logging.error(f'Invalid website, request response: {resp}')
            return
        logging.debug(f'Website for director info successfully scrapped')
        for r in resp:
            sp = BeautifulSoup(r.content, "html.parser")
            temp = get_list(sp, class_="flight-info__infobox-text")
            temp.append(get_status(sp))
            final_list.append(temp)
    req = (grequests.get(u) for u in url_list[loop_end*10:len(url_list)])
    res = grequests.map(req)
    if not res:
        logging.error(f'Invalid website, request response: {res}')
        return
    logging.debug(f'Website for director info successfully scrapped')
    for r in res:
        s = BeautifulSoup(r.content, "html.parser")
        temp = get_list(s, class_="flight-info__infobox-text")
        temp.append(get_status(s))
        final_list.append(temp)

    df = pd.DataFrame(final_list, columns=['Departure_Hour', 'Departure_Terminal', 'Departure_Gate',
                                        'Arrival_Hour', 'Arrival_Terminal', 'Arrival_Gate', 'Status'])
    return df


def newark_df(arr_depart, day='today'):
    """
    :param
    to_from: departure flights from Newark or arrival flights to Newark
    day: yesterday, today of tomorrow
    :return: list with all chosen day flights
    """
    if arr_depart in CFG.ARR_DEPART:
        pass
    else:
        raise ValueError('You should select departures or arrivals as input')

    newark_df_col = pd.DataFrame(columns=['City','Flight_number','Airline','Estimated_hour'])
    for url in get_url(arr_depart, day):
        temp = get_df_column(get_soup(url))
        newark_df_col = pd.concat([newark_df_col,temp], ignore_index=True)

    flight_list = [flight.split('\n')[0] for flight in newark_df_col['Flight_number']]
    newark_df_row = get_df_row_g(arr_depart,day, flight_list)

    newark_df_row['Departure_Hour'] = pd.to_datetime(newark_df_row['Departure_Hour'].str.strip(" "), format='%H:%M').dt.time
    newark_df_row['Arrival_Hour'] = pd.to_datetime(newark_df_row['Arrival_Hour'].str.strip(" "), format='%H:%M').dt.time

    if newark_df_col.shape[0] == newark_df_row.shape[0]:
        newark_df = pd.concat([newark_df_col,newark_df_row], axis=1)
    else:
        raise IndexError('Missing data')

    if arr_depart == 'departures':
        newark_df['Arrival_Departure'] = 'departure'
    else:
        newark_df['Arrival_Departure'] = 'arrival'

    if day == 'today':
        today = date.today()
        today.strftime('%d%m%y')
        newark_df['date'] == today
    elif day == 'yesterday':
        yesterday = date.today() - timedelta(days=1)
        yesterday.strftime('%d%m%y')
        newark_df['date'] == yesterday
    else:
        tomorrow = date.today() + timedelta(days=1)
        tomorrow.strftime('%d%m%y')
        newark_df['date'] == tomorrow

    return newark_df


# print(newark_df('departures'))
# print([city.split('\n') for city in newark_df('departures')['City']])
# print(get_df_column(get_soup(get_url('departures','today'))))
if __name__ == '__main__':
    to_from = input('Do you want to scrap over incoming flight (type *arrivals*) or leaving flight (type *departures*)')
    if to_from == 'arrivals':
        arrivals_df = newark_df(to_from)
        #arrivals_df.to_csv()
    elif to_from == 'departures':
        departures_df = newark_df(to_form)
        #departures_df.to_csv()
    flights_df = flight_num_df(newark_df(to_from))
    #flights_df.to_csv()
    city_df = cities_df(newark_df(to_from))
    #city_df.to_csv()
