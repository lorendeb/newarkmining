import config as CFG


def get_terminal(arr_depar, terminal, df):
    """ return all terminal departure"""
    if arr_depar == CFG.ARRIVALS:
        return df[df['Arrival_Terminal'].str.strip(" ") == terminal]
    else:
        return df[df['Departure_Terminal'].str.strip(" ") == terminal]


def get_time_slot(slot, df):
    """ returns all flights that leave during the time slot"""
    df[df['Estimated_hour'].str[:2]]
    return [flight for flight in newarklist if int(flight[CFG.ESTIMATED_HOUR_INDEX][:2]) in range(slot, slot+6)]


def get_status(status, newarklist):
    """ return all flight with status status"""
    return [flight for flight in newarklist if status.lower() in flight[CFG.STATUS_INDEX].lower()]
