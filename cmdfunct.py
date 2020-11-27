import config as CFG


def get_terminal(arr_depar, terminal, df):
    """ return all terminal departure"""
    df.dropna(inplace=True)
    if arr_depar == CFG.ARRIVALS:
        return df[df['Arrival_Terminal'].str.contains(terminal)]
    else:
        return df[df['Departure_Terminal'].str.contains(terminal)]


def get_time_slot(slot, df):
    """ returns all flights that leave during the time slot"""
    df.dropna(inplace=True)
    if slot == 0:
        return df[(df['Estimated_hour'].str.strip(" ") >= '00:00') & (df['Estimated_hour'].str.strip(" ") < '06:00')]
    elif slot == 6:
        return df[(df['Estimated_hour'].str.strip(" ") >= '06:00') & (df['Estimated_hour'].str.strip(" ") < '12:00')]
    elif slot == 12:
        return df[(df['Estimated_hour'].str.strip(" ") >= '12:00') & (df['Estimated_hour'].str.strip(" ") < '18:00')]
    else:
        return df[(df['Estimated_hour'].str.strip(" ") >= '18:00') & (df['Estimated_hour'].str.strip(" ") < '00:00')]

def get_status_(status, df):
    """ return all flight with status status"""
    df.dropna(inplace=True)
    return df[df['Status'].str.contains(status)]

