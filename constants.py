from cities_light.models import City, Country

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

DEST_COUNTRY = [(country['name_ascii'], country['name_ascii']) for country in Country.objects.all().values('name_ascii')]
DEST_CITY = [(city['name_ascii'], city['name_ascii']) for city in City.objects.all().values('name_ascii')]