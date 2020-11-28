import pandas as pd


def flight_num_df(df):
    flight_num = list(enumerate(df['Flight_number']))

    flight_num_split = []
    for tup in flight_num:
        flight = tup[1].split(',')
        for j in range(len(flight)):
            new_tup = []
            new_tup.append(tup[0])
            new_tup.append(flight[j])
            flight_num_split.append(new_tup)
    first_column = pd.DataFrame([range(len(flight_num_split))]).T
    first_column = first_column.rename(columns={0: 'orig_ind'})
    flight_num = pd.DataFrame(flight_num_split, columns=['flight_ind','flight_num'])
    all_flight_num = pd.concat([first_column,flight_num], axis=1)

    return all_flight_num

def cities_df(df):
    city_dict = {}
    for index,row in df.iterrows():
        city_dict[row['City']] = row['City_Shortname']
    city_df = pd.DataFrame(list(city_dict.items()), columns=['city_name','city_short_name'])
    return city_df

