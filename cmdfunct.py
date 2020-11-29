import config as CFG


def get_terminal(arr_depar, terminal, df):
    """ return all terminal departure"""
    df.dropna(inplace=True)
    if arr_depar == CFG.ARRIVALS:
        return df[df['Arrival_Terminal'] == terminal]
    else:
        return df[df['Departure_Terminal'] == terminal]


def get_time_slot(slot, df):
    """ returns all flights that leave during the time slot"""
    df.dropna(inplace=True)
    if slot == 0:
        return df[(df['Estimated_hour'].str.strip(" ") >= CFG.MIDNIGHT) &
                  (df['Estimated_hour'].str.strip(" ") < CFG.EARLY_MORNING)]
    elif slot == 6:
        return df[(df['Estimated_hour'].str.strip(" ") >= CFG.EARLY_MORNING) &
                  (df['Estimated_hour'].str.strip(" ") < CFG.NOON)]
    elif slot == 12:
        return df[(df['Estimated_hour'].str.strip(" ") >= CFG.NOON) &
                  (df['Estimated_hour'].str.strip(" ") < CFG.AFTERNOON)]
    else:
        return df[(df['Estimated_hour'].str.strip(" ") >= CFG.AFTERNOON) &
                  (df['Estimated_hour'].str.strip(" ") < CFG.MIDNIGHT)]

def get_status_(status, df):
    """ return all flight with status status"""
    df.dropna(inplace=True)
    return df[df['Status'].str.contains(status)]

