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