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
DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"
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

# comamnd line functions
MIDNIGHT = '00:00'
EARLY_MORNING = '06:00'
NOON = '12:00'
AFTERNOON = '18:00'

# Argparse
#time slot section
FIRST_SECTION = 0
SECOND_SECTION = 6
THIRD_SECTION = 12
FOURTH_SECTION = 18
# terminal name
A = 'A'
B = 'B'
C = 'C'