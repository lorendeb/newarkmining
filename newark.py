from bs4 import BeautifulSoup
import requests
import config as CFG


def newark_list(to_from, day='today'):
    """
    :param
    to_from: departure flights from Newark or arrival flights to Newark
    day: yesterday, today of tomorrow
    :return: list with all chosen day flights
    """
    if to_from in CFG.to_from:
        pass
    else:
        raise ValueError('You should select departures or arrivals as input')

    final_list = []
    for time in CFG.times:
        URL = 'https://www.airport-ewr.com/newark-'+ to_from+'?tp=' + str(time) + '&day=' + day

        # get web data
        page = requests.get(URL)

        # parse web data
        soup = BeautifulSoup(page.content, "html.parser")

        # create an empty list for flight destinations, then scrapped for all destinations (in order)
        destination_list = []
        for destination in soup.find_all('div', class_="flight-col flight-col__dest-term"):
            destination_list.append(destination.text.strip('\n\t'))

        # create an empty list for flight numbers, then scrapped for all flight numbers (in order)
        flight_number_list = []
        for flight_number in soup.find_all('div', class_="flight-col flight-col__flight"):
            flight_number_list.append(flight_number.text.strip('\n\t'))

        # create an empty list for airlines, then scrapped for all airlines (in order)
        airline_list = []
        for flight_num in soup.find_all('div', class_="flight-col flight-col__airline"):
            airline_list.append(flight_num.text.strip('\n\t'))

        estimated_hour_list = []
        for estimated_hour in soup.find_all('div', class_="flight-col flight-col__hour"):
            estimated_hour_list.append(estimated_hour.text.strip('\n\t'))

        detail_list = []
        status_list = []
        # for each flight number, get a new url to scrap more data
        for flight_num in flight_number_list:
            URLdetails = "https://www.airport-ewr.com/newark-flight-"+to_from+"/" + flight_num.splitlines()[CFG.FIRST_FLIGHT_INDEX] + "?day=" + day
            page = requests.get(URLdetails)
            soup = BeautifulSoup(page.content, "html.parser")
            temp_list = []
            # for each flight number, scrap for departure and arrival time, terminal and gate at both departure and arrival and status
            for detail in soup.find_all('div', class_="flight-info__infobox-text"):
                temp_list.append(detail.text.strip('\n\t'))
            status = soup.find('div', class_="flight-status__title")
            try:
                status_list.append(status.text.strip('\n\t'))
            except Exception:
                status_list.append('Status')
            detail_list.append(temp_list)

        result_list = []

        # create a finale list of lists of details per flight
        for index in range(1, len(destination_list)):
            temp = []
            temp.append(destination_list[index])
            temp.append(airline_list[index])
            temp.append(flight_number_list[index])
            temp.append(estimated_hour_list[index])
            temp.append(detail_list[index][CFG.HOUR_DEPARTURE_INDEX_DETAILED])
            temp.append(detail_list[index][CFG.HOUR_ARRIVAL_INDEX_DETAILED])
            temp.append(detail_list[index][CFG.TERMINAL_DEPARTURE_INDEX_DETAILED])
            temp.append(detail_list[index][CFG.GATE_DEPARTURE_INDEX_DETAILED])
            temp.append(detail_list[index][CFG.TERMINAL_ARRIVAL_INDEX_DETAILED])
            temp.append(detail_list[index][CFG.GATE_ARRIVAL_INDEX_DETAILED])
            temp.append(status_list[index])
            result_list.append(temp)
        final_list += result_list

    return final_list

if __name__ == '__main__':
    to_from = input('Do you want to parse over incoming flight (type *arrivals*) or leaving flight (type *departures*)')
    print(newark_list(to_from))