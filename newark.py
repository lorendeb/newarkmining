import grequests
from bs4 import BeautifulSoup
import requests
import config as CFG
import logging
import pandas as pd
from datetime import date
from datetime import timedelta


# logging configuration- from Info level
logging.basicConfig(filename='newark.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE %(lineno)d: %(message)s',
                    level=logging.INFO)


def get_list(soup, class_):
    """
    get soup and return for a specific class the list of all occurences in the soup
    :param soup
    :param class_
    :return: list
    """
    feature_list = [feature.text.strip('\n\t') for feature in soup.find_all('div', class_)]
    return feature_list


def get_soup(URL):
    """
    get URL and return soup if website responds 200
    :param URL
    :return: soup
    """
    page = requests.get(URL)
    resp = page.status_code
    if resp != CFG.RESPONSE:
        logging.error(f'Invalid website, request response: {resp}')
        return
    logging.info(f'Website successfully scrapped')
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_url(arr_depar, day):
    """
    build url to scrap according to departure or arrival flight and date
    :param arr_depar: arrivals or departures
    :param day: yesterday, today, tomorrow
    :return: list of 4 urls for each periods of the day
    """
    if arr_depar == CFG.ARRIVALS:
        prefix = CFG.ARRIVAL_URL
    else:
        prefix = CFG.DEPARTURE_URL
        # the day is splitted into 4 websites according to the hour
    return [prefix + str(time) + '&day=' + day for time in CFG.TIMES]


def get_url_flight(arr_depar, flight_num,day):
    """
    build url for each flight number to get more details about the flight
    :param arr_depar: arrivals or departures
    :param day: yesterday, today, tomorrow
    :param flight_num
    :return: return the url of the flight num for this specific day
    """
    if arr_depar == CFG.ARRIVALS:
        return CFG.ARRIVAL_FLIGHT_URL + flight_num + "?day=" + day
    elif arr_depar == CFG.DEPARTURES:
        return CFG.DEPARTURE_FLIGHT_URL + flight_num + "?day=" + day


def get_status(soup):
    """
    get soup and return the status of the flight.
    :param soup
    :return: status of the flight as string
    """
    status = soup.find('div', class_="flight-status__title")
    if status:
        return status.text.strip('\n\t')
    else:
        return ""


def get_df_column(soup):
    """
    build a dataframe, by column, from the main website
    :param soup
    :return: dataframe with details of the flight from the main website.
    """
    destination_list = get_list(soup, class_="flight-col flight-col__dest-term")
    city_list = [destination.split('\n')[0] for destination in destination_list]
    city_sn_list = [destination.split('\n')[-1].replace('(','').replace(')','') for destination in destination_list]
    flight_number_list = get_list(soup, class_="flight-col flight-col__flight")
    flight_number_list = [", ".join(flight_num.split('\n')) for flight_num in flight_number_list]
    airline_list = get_list(soup, class_="flight-col flight-col__airline")
    estimated_hour_list = get_list(soup, class_="flight-col flight-col__hour")
    flight_dictionary = {'City': city_list,
                         'City_Shortname': city_sn_list,
                         'Flight_number': flight_number_list,
                         'Airline': airline_list,
                         'Estimated_hour': estimated_hour_list}
    df = pd.DataFrame(flight_dictionary)
    df.drop(df.index[0], inplace=True)
    return df


def get_df_row(arr_depar, day, flight_num_list):
    """
    build dataframe by row(flight by flight), from the flight number page, using requests
    :param arr_depar: arrivals, departures
    :param day: yesterday, today, tomorrow
    :param flight_num_list
    :return: dataframe with details of flight from flight number page
    """
    # create list of urls for each flight number
    url_list = [get_url_flight(arr_depar, flight_num, day) for flight_num in flight_num_list]
    final_list = []
    for url in url_list:
        sp = get_soup(url)
        temp = get_list(sp, class_="flight-info__infobox-text")
        temp.append(get_list(sp))
        final_list.append(temp)
    df = pd.DataFrame(final_list, columns=['Departure_Hour', 'Departure_Terminal', 'Departure_Gate',
                                        'Arrival_Hour', 'Arrival_Terminal', 'Arrival_Gate', 'Status'])
    return df


def get_df_row_g(arr_depar, day, flight_num_list):
    """
    build dataframe by row(flight by flight), from the flight number page, using grequests
    :param arr_depar: arrivals, departures
    :param day: yesterday, today, tomorrow
    :param flight_num_list
    :return: dataframe with details of flight from flight number page
    """
    # create list of urls for each flight number
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
            #append to a list of each flight number details list
            final_list.append(temp)
    # for the last urls that are not a multiple of 10
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
    # convert list of details lists to dataframe
    df = pd.DataFrame(final_list, columns=['Departure_Hour', 'Departure_Terminal', 'Departure_Gate',
                                        'Arrival_Hour', 'Arrival_Terminal', 'Arrival_Gate', 'Status'])
    return df


def newark_df(arr_depart, day='today'):
    """
    build dataframe with all details of flights, arrivals or depatures, of the day
    :param
    arr_depart: arrivals, departures
    day: yesterday, today of tomorrow
    :return: dataframe with all flights of the selected day
    """
    # check inputs are correct
    if arr_depart in CFG.ARR_DEPART:
        pass
    else:
        raise ValueError('You should select departures or arrivals as input')

    # check inputs are correct and create datetime
    if day in CFG.DAYS:
        if day == 'today':
            date_ = date.today()
        elif day == 'yesterday':
            date_ = date.today() - timedelta(days=1)
        elif day == 'tomorrow':
            date_ = date.today() + timedelta(days=1)
        date_.strftime("%m/%d/%Y, %H:%M:%S")
    else:
        raise ValueError('You should select today,yesterday or tomorrow as input')

    # create dataframe from the main website, 4 times for each part of the day
    newark_df_col = pd.DataFrame(columns=['City','Flight_number','Airline','Estimated_hour'])
    for url in get_url(arr_depart, day):
        temp = get_df_column(get_soup(url))
        newark_df_col = pd.concat([newark_df_col,temp], ignore_index=True)

    # from new_df_col, get list of flight number to build the url for scrapping each flight number page
    # some flights are multiple flight numbers, getting the first one (same data on all pages)
    flight_list = [flight.split('\n')[0] for flight in newark_df_col['Flight_number']]
    # create dataframe from the flight numbers pages
    newark_df_row = get_df_row_g(arr_depart,day, flight_list)

    # check the two dataframe have the same number of lines, and concatenate them side by side
    if newark_df_col.shape[0] == newark_df_row.shape[0]:
        newark_df = pd.concat([newark_df_col,newark_df_row], axis=1)
    else:
        raise IndexError('Missing data')

    # add column with departure or arrival, to know which kind of flight it is
    if arr_depart == 'departures':
        newark_df['Arrival_Departure'] = 'departure'
    else:
        newark_df['Arrival_Departure'] = 'arrival'

    # add column with date and time
    # a flight can appear multiple time in the dataframe, but the status and hour can be updated
    newark_df['date'] = date_

    return newark_df


if __name__ == '__main__':
    to_from = input('Do you want to scrap over incoming flight (type *arrivals*) or leaving flight (type *departures*)')
    try:
        df = newark_df(to_from)
        #df.to_csv('check.csv')
        print(df)


    except Exception as ex:
        print(ex)