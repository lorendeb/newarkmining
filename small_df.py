import pandas as pd


def flight_num_df(df):
    flight_num = list(enumerate(df['Flight_number']))

    flight_num_split = []
    for tup in flight_num:
        flight = tup[1].split('\n')
        for j in range(len(flight)):
            new_tup = []
            new_tup.append(tup[0])
            new_tup.append(flight[j])
            flight_num_split.append(new_tup)

    all_flight_num = pd.DataFrame(flight_num_split)

    return all_flight_num

def cities_df(df):
    city_dict = {}
    for city in list(df['City']):
        city = city.split('\n')
        city_dict[city[0]] = city[1].strip()[1:-1]
    city_df = pd.DataFrame(list(city_dict.items()), columns=['full_name','short_name'])
    return city_df

