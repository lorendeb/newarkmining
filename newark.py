from bs4 import BeautifulSoup
import requests


# list of indexes
DESTINATION_INDEX = 0
AIRCOMPANY_INDEX = 1
FLIGHT_NUMBER = 2
ESTIMATED_HOUR_INDEX= 3
HOUR_DEPARTURE_INDEX = 4
HOUR_ARRIVAL_INDEX = 5
TERMINAL_DEPARTURE_INDEX = 6
GATE_DEPARTURE_INDEX = 7
TERMINAL_ARRIVAL_INDEX = 8
GATE_ARRIVAL_INDEX = 9
STATUS_INDEX = 10


def newark_list(day='today'):
    """
    :param day: yesterday, today of tomorrow
    :return: list with all chosen day flights
    """
    times = [0, 6, 12, 18]
    final_list = []
    for time in times:
        URL = 'https://www.airport-ewr.com/newark-departures?tp=' + str(time) + '&day=' + day

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
            URLdetails = "https://www.airport-ewr.com/newark-flight-departure/" + flight_num.splitlines()[
                0] + "?day=" + day
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

        HOUR_DEPARTURE_INDEX_DETAILED = 0
        TERMINAL_DEPARTURE_INDEX_DETAILED = 1
        GATE_DEPARTURE_INDEX_DETAILED = 2
        HOUR_ARRIVAL_INDEX_DETAILED = 3
        TERMINAL_ARRIVAL_INDEX_DETAILED = 4
        GATE_ARRIVAL_INDEX_DETAILED = 5
        result_list = []

        # create a finale list of lists of details per flight
        for index in range(1, len(destination_list)):
            temp = []
            temp.append(destination_list[index])
            temp.append(airline_list[index])
            temp.append(flight_number_list[index])
            temp.append(estimated_hour_list[index])
            temp.append(detail_list[index][HOUR_DEPARTURE_INDEX_DETAILED])
            temp.append(detail_list[index][HOUR_ARRIVAL_INDEX_DETAILED])
            temp.append(detail_list[index][TERMINAL_DEPARTURE_INDEX_DETAILED])
            temp.append(detail_list[index][GATE_DEPARTURE_INDEX_DETAILED])
            temp.append(detail_list[index][TERMINAL_ARRIVAL_INDEX_DETAILED])
            temp.append(detail_list[index][GATE_ARRIVAL_INDEX_DETAILED])
            temp.append(status_list[index])
            result_list.append(temp)
        final_list += result_list

    return final_list


def get_destination_list(newarklist):
    """ returns list of day destination"""
    return [flight[DESTINATION_INDEX] for flight in newarklist]


def get_terminal(terminal, newarklist):
    """ return all terminal departure"""
    return [flight for flight in newarklist if flight[TERMINAL_DEPARTURE_INDEX].lower().strip(" ") == terminal]


def get_time_slot(slot, newarklist):
    """ returns all flights that leave during the time slot"""
    return [flight for flight in newarklist if int(flight[ESTIMATED_HOUR_INDEX][:2]) in range(slot, slot+6)]


def get_status(status, newarklist):
    """ return all flight with status status"""
    return [flight for flight in newarklist if status.lower() in flight[STATUS_INDEX].lower()]
