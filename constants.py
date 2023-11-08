DRINK_PREF_CHOICES = [
    ("Frequently", "Frequently"),
    ("Socially", "Socially"),
    ("Rarely", "Rarely"),
    ("Never", "Never"),
]

SMOKE_PREF_CHOICES = [
    ("Socially", "Socially"),
    ("Regularly", "Regularly"),
    ("Never", "Never"),
]

EDU_LEVEL_CHOICES = [
    ("In college", "In college"),
    ("Undergraduate degree", "Undergraduate degree"),
    ("In grad school", "In grad school"),
    ("Graduate degree", "Graduate degree"),
]

INTEREST_CHOICES = [
    ("hiking", "hiking"),
    ("clubbing", "clubbing"),
    ("beach", "beach"),
    ("sightseeing", "sightseeing"),
    ("bar hopping", "bar hopping"),
    ("food tourism", "food tourism"),
    ("museums", "museums"),
    ("historical/cultural sites", "historical/cultural sites"),
    ("spa", "spa"),
    ("relaxed", "relaxed"),
    ("camping", "camping"),
    ("sports", "sports"),
]

LANG_CHOICES = [
    ("Chinese", "Chinese"),
    ("Spanish", "Spanish"),
    ("English", "English"),
    ("Arabic", "Arabic"),
    ("Hindi", "Hindi"),
    ("Bengali", "Bengali"),
    ("Portuguese", "Portuguese"),
    ("Russian", "Russian"),
    ("Japanese", "Japanese"),
    ("Urdu", "Urdu"),
]

TRAVEL_TYPE = [("Solo", "Solo"), ("Companion", "Companion")]

COUNTRY_CHOICES = [
    ("India", "India"),
    ("United Kingdom", "United Kingdom"),
    ("United States", "United States"),
    ("Canada", "Canada"),
    ("Mexico", "Mexico"),
    ("Italy", "Italy"),
    ("France", "France"),
]

INDIAN_CITIES = [
    ("Ahmedabad", "Ahmedabad"),
    ("Bangalore", "Bangalore"),
    ("Chennai", "Chennai"),
    ("Hyderabad", "Hyderabad"),
    ("Jaipur", "Jaipur"),
    ("Kolkata", "Kolkata"),
    ("Mumbai", "Mumbai"),
    ("New Delhi", "New Delhi"),
    ("Pune", "Pune"),
]

UK_CITIES = [
    ("Bristol", "Bristol"),
    ("Glasgow", "Glasgow"),
    ("Leeds", "Leeds"),
    ("Liverpool", "Liverpool"),
    ("London", "London"),
    ("Newcastle", "Newcastle"),
    ("Nottingham", "Nottingham"),
    ("Sheffield", "Sheffield"),
]

US_CITIES = [
    ("Chicago", "Chicago"),
    ("Dallas", "Dallas"),
    ("Houston", "Houston"),
    ("Los Angeles", "Los Angeles"),
    ("New York City", "New York City"),
    ("Phoenix", "Phoenix"),
    ("Philadelphia", "Philadelphia"),
    ("San Antonio", "San Antonio"),
    ("San Diego", "San Diego"),
]

CANADA_CITIES = [
    ("Calgary", "Calgary"),
    ("Edmonton", "Edmonton"),
    ("Hamilton", "Hamilton"),
    ("Mississauga", "Mississauga"),
    ("Montreal", "Montreal"),
    ("Niagara Falls", "Niagara Falls"),
    ("Ottawa", "Ottawa"),
    ("Quebec City", "Quebec City"),
    ("Toronto", "Toronto"),
    ("Vancouver", "Vancouver"),
]

MEXICO_CITIES = [
    ("Cancun", "Cancun"),
    ("Chichen Itza", "Chichen Itza"),
    ("Guadalajara", "Guadalajara"),
    ("Los Cabos", "Los Cabos"),
    ("Mexico City", "Mexico City"),
    ("Oaxaca City", "Oaxaca City"),
    ("Playa del Carmen", "Playa del Carmen"),
    ("Puerto Vallarta", "Puerto Vallarta"),
]

FRANCE_CITIES = [
    ("Burgundy", "Burgundy"),
    ("Bordeaux", "Bordeaux"),
    ("Cannes", "Cannes"),
    ("Corsica", "Corsica"),
    ("Eze", "Eze"),
    ("Marseille", "Marseille"),
    ("Nice", "Nice"),
    ("Normandy", "Normandy"),
    ("Paris", "Paris"),
    ("Toulouse", "Toulouse"),
]

ITALY_CITIES = [
    ("Florence", "Florence"),
    ("Genoa", "Genoa"),
    ("Milan", "Milan"),
    ("Naples", "Naples"),
    ("Palermo", "Palermo"),
    ("Rome", "Rome"),
    ("Venice", "Venice"),
]


def concat_sort_city_tuples(*args):
    return_list = []
    for arg in args:
        return_list += arg
    return sorted(return_list)


CITY_CHOICES = concat_sort_city_tuples(
    INDIAN_CITIES,
    US_CITIES,
    UK_CITIES,
    CANADA_CITIES,
    MEXICO_CITIES,
    FRANCE_CITIES,
    ITALY_CITIES,
)
