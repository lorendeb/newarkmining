from bs4 import BeautifulSoup
import requests


URL = 'https://www.airport-ewr.com/newark-departures'

# get web data
page = requests.get(URL)

# parse web data
soup = BeautifulSoup(page.content, "html.parser")
# print(soup.prettify())

destination_list = []
for destination in soup.find_all('div', class_="flight-col flight-col__dest-term"):
    destination_list.append(destination.text.strip('\n\t'))

hour_departure_list = []
for hour_departure in soup.find_all('div', class_="flight-col flight-col__hour"):
    hour_departure_list.append(hour_departure.text.strip('\n\t'))

flight_number_list = []
for flight_number in soup.find_all('div', class_="flight-col flight-col__flight"):
    flight_number_list.append(flight_number.text.strip('\n\t'))

airline_list = []
for flight_num in soup.find_all('div', class_="flight-col flight-col__dest-term"):
    airline_list.append(flight_num.text.strip('\n\t'))

terminal_departure_list = []
for terminal_departure in soup.find_all('div', class_="flight-col flight-col__terminal-mob"):
    terminal_departure_list.append(terminal_departure.text.strip('\n\t'))

status_list = []
for status in soup.find_all('div', class_="flight-col flight-col__status flight-col__status--GR"):
    status_list.append(status.text.strip('\n\t'))

detail_list = []

for flight_num in flight_number_list:
    URL = "https://www.airport-ewr.com/newark-flight-departure/" + flight_num.splitlines()[0]
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    temp_list = []
    for detail in soup.find_all('div', class_="flight-info__infobox-text"):
        temp_list.append(detail.text.strip('\n\t'))
    detail_list.append(temp_list)




print(detail_list)
print(destination_list)
print(hour_departure_list)
print(flight_number_list)
print(airline_list)
print(terminal_departure_list)
print(status_list)
print(len(destination_list))
print(len(hour_departure_list))
print(len(flight_number_list))
print(len(airline_list))
print(len(terminal_departure_list))
print(len(status_list))

