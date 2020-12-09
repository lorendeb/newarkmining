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
TABLES['airports'] = ('''CREATE TABLE airports 
                        (airport_id INT PRIMARY KEY AUTO_INCREMENT,
                        airport VARCHAR(255),
                        iata VARCHAR(255))''')

TABLES['status'] = ('''CREATE TABLE status 
                        (status_id INT PRIMARY KEY AUTO_INCREMENT,
                        status VARCHAR(255))''')


TABLES['all_flights'] = ('''CREATE TABLE all_flights 
                        (flight_id INT PRIMARY KEY AUTO_INCREMENT,
                        airport_id INT,
                        estimated_hour DATETIME,
                        departure_hour DATETIME,
                        departure_terminal VARCHAR(255),
                        departure_gate VARCHAR(255),
                        arrival_hour DATETIME,
                        arrival_terminal VARCHAR(255),
                        arrival_gate VARCHAR(255),
                        status_id INT,
                        arrival_departure VARCHAR(255),
                        date DATETIME,  
                        CONSTRAINT fk_airport FOREIGN KEY(airport_id) REFERENCES airports(airport_id),
                        CONSTRAINT fk_status FOREIGN KEY(status_id) REFERENCES status(status_id))''')

TABLES['flights_numbers'] = ('''CREATE TABLE flights_numbers 
                        (flights_numbers_id INT PRIMARY KEY AUTO_INCREMENT,
                        flight_id INT,
                        flight_number VARCHAR(255),
                        CONSTRAINT fk_all_flights FOREIGN KEY(flight_id) REFERENCES all_flights(flight_id))''')

TABLES['airlines_per_flight'] = ('''CREATE TABLE airlines_per_flight
                                 (airlines_per_flight_id INT PRIMARY KEY AUTO_INCREMENT,
                                 flight_id INT,
                                 airline_name VARCHAR(255),
                                 CONSTRAINT fk_all_flights2 FOREIGN KEY(flight_id) REFERENCES all_flights(flight_id))''')

