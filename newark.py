from bs4 import BeautifulSoup
import requests


URL = 'https://www.airport-ewr.com/newark-departures'

# get web data
page = requests.get(URL)

# parse web data
soup = BeautifulSoup(page.content, "html.parser")

destination_list = []
for destination in soup.find_all('div', class_="flight-col flight-col__dest-term"):
    destination_list.append(destination.text.strip('\n\t'))

hour_list = []
for hour in soup.find_all('div', class_="flight-col flight-col__hour"):
    hour_list.append(hour.text.strip('\n\t'))

flight_list = []
for flight in soup.find_all('div', class_="flight-col flight-col__flight"):
    flight_list.append(flight.text.strip('\n\t'))

airline_list = []
for airline in soup.find_all('div', class_="flight-col flight-col__dest-term"):
    airline_list.append(airline.text.strip('\n\t'))

terminal_list = []
for terminal in soup.find_all('div', class_="flight-col flight-col__terminal-mob"):
    terminal_list.append(terminal.text.strip('\n\t'))

status_list = []
for status in soup.find_all('div', class_="flight-col flight-col__status flight-col__status--GR"):
    status_list.append(status.text.strip('\n\t'))


print(destination_list)
print(hour_list)
print(flight_list)
print(airline_list)
print(terminal_list)
print(status_list)
print(len(destination_list))
print(len(hour_list))
print(len(flight_list))
print(len(airline_list))
print(len(terminal_list))
print(len(status_list))

