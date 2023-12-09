import datetime

from constants import (
    INDIAN_CITIES,
    US_CITIES,
    UK_CITIES,
    CANADA_CITIES,
    MEXICO_CITIES,
    ITALY_CITIES,
    FRANCE_CITIES,
)


def start_date_in_future(std):
    if isinstance(std, datetime.date):
        return std >= datetime.date.today()
    else:
        raise TypeError("Arguments must be of type datetime.date")


def end_date_after_start_date(std, end):
    if isinstance(std, datetime.date) and isinstance(end, datetime.date):
        return end > std
    else:
        raise TypeError("Arguments must be of type datetime.date")


def city_present_in_country(city, country):
    city = city[0].title()
    country = country[0].title()
    city_tuple = (city, city)
    if country == "India":
        return True if city_tuple in INDIAN_CITIES else False
    elif country == "United States":
        return True if city_tuple in US_CITIES else False
    elif country == "United Kingdom":
        return True if city_tuple in UK_CITIES else False
    elif country == "Canada":
        return True if city_tuple in CANADA_CITIES else False
    elif country == "Mexico":
        return True if city_tuple in MEXICO_CITIES else False
    elif country == "France":
        return True if city_tuple in FRANCE_CITIES else False
    elif country == "Italy":
        return True if city_tuple in ITALY_CITIES else False
    else:
        raise TypeError("Country not supported currently")


def get_emergency_contacts(country):
    if country == "India":
        return {
            'Medical': '102',
            'Fire': '101',
            'Police': '100, 103'
        }
    elif country == "United Kingdom":
        return {
            'Medical': '112, 999',
            'Fire': '112, 999',
            'Police': '112, 999'
        }
    elif country == "United States":
        return {
            'Medical': '911',
            'Fire': '911',
            'Police': '911'
        }
    elif country == "Canada":
        return {
            'Medical': '911',
            'Fire': '911',
            'Police': '911'
        }
    elif country == "Mexico":
        return {
            'Medical': '065',
            'Fire': '068',
            'Police': '060'
        }
    elif country == "Italy":
        return {
            'Medical': '112, 118',
            'Fire': '112, 115',
            'Police': '112, 113'
        }
    elif country == "France":
        return {
            'Medical': '112, 15',
            'Fire': '112, 18',
            'Police': '112, 17'
        }
    return {
        'Medical': 'NA',
        'Fire': 'NA',
        'Police': 'NA'
    }
