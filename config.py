# scrapping
RESPONSE = 200

# cleaning the data from scrapping
NEW_LINE = '\n'
CITY_NAME = 0
CITY_SHORTNAME = -1
FIRST_FLIGHT = 0
FIRST_ROW = 0

# grequest grouping size
GROUPING = 10
START_URL = 0

# scrapping 4 website to have all day flight
TIMES = [0, 6, 12, 18]
DATE_FORMAT = "%d/%m/%Y %H:%M"
TODAY = 'today'
YESTERDAY = 'yesterday'
YESTERDAY_DELTA = 1
TOMORROW_DELTA = 1
TOMORROW = 'tomorrow'

# checking shape dataframes
ROWS = 0

ARR_DEPART = ["departures", "arrivals"]
DAYS = ['today','yesterday','tomorrow']

# url prefix to scrap
ARRIVAL_URL = 'https://www.airport-ewr.com/newark-arrivals?tp='
DEPARTURE_URL = 'https://www.airport-ewr.com/newark-departures?tp='
ARRIVAL_FLIGHT_URL = "https://www.airport-ewr.com/newark-flight-arrival/"
DEPARTURE_FLIGHT_URL = "https://www.airport-ewr.com/newark-flight-departure/"
ARRIVALS = 'arrivals'
DEPARTURES = 'departures'
ARRIVAL = 'arrival'
DEPARTURE = 'departure'

# argparse:
NUMBER_ROWS = 0
EMPTY = 0
FUTURE_L = 'will leave'
FUTURE_A = 'will arrive at'
PAST_L = 'left'
PAST_A = 'arrived at'
PRESENT_L = 'leave'
PRESENT_A = 'arrive'
TO = 'to'
FROM = 'from'

#database
DB_NAME = 'newark'
TABLES = {}
TABLES['all_flights'] = ('''CREATE TABLE all_flights 
                        (flight_id INT PRIMARY KEY AUTO_INCREMENT,
                        City VARCHAR(255),
                        Flight_number VARCHAR(255),
                        Airline VARCHAR(255),
                        Estimated_hour VARCHAR(255),
                        Departure_Hour VARCHAR(255),
                        Departure_Terminal VARCHAR(255),
                        Departure_Gate VARCHAR(255),
                        Arrival_Hour VARCHAR(255),
                        Arrival_Terminal VARCHAR(255),
                        Arrival_Gate VARCHAR(255),
                        Status VARCHAR(255),
                        Arrival_Departure VARCHAR(255),
                        date VARCHAR(255))''')

TABLES['flights'] = ('''CREATE TABLE flights
                        (orig_ind INT PRIMARY KEY, 
                        flight_id INT,
                        flight_number VARCHAR(255))''')


TABLES['city'] = ('''CREATE TABLE city 
                        (city_id INT PRIMARY KEY AUTO_INCREMENT,
                        City VARCHAR(255),
                        City_Shortname VARCHAR(255))''')

