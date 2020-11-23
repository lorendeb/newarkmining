import config as CFG


def get_destination_list(newarklist):
    """ returns list of day destination"""
    return [flight[CFG.DESTINATION_INDEX] for flight in newarklist]


def get_terminal(terminal, newarklist):
    """ return all terminal departure"""
    return [flight for flight in newarklist if flight[CFG.TERMINAL_DEPARTURE_INDEX].lower().strip(" ") == terminal]


def get_time_slot(slot, newarklist):
    """ returns all flights that leave during the time slot"""
    return [flight for flight in newarklist if int(flight[CFG.ESTIMATED_HOUR_INDEX][:2]) in range(slot, slot+6)]


def get_status(status, newarklist):
    """ return all flight with status status"""
    return [flight for flight in newarklist if status.lower() in flight[CFG.STATUS_INDEX].lower()]
