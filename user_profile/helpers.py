import datetime

PREFERENCE_MAP = [
    "hiking",
    "clubbing",
    "beach",
    "sightseeing",
    "bar hopping",
    "food tourism",
    "museums",
    "historical/cultural sites",
    "spa",
    "relaxed",
    "camping",
    "sports",
]


def email_is_valid(email):
    if email.endswith(".edu") and email[0].isalpha():
        return True
    return False


def dob_gte18_and_lt100(dob):
    time_delta = datetime.date.today() - dob
    age = int(time_delta.days / 365)
    if 18 <= age < 100:
        return True, None
    else:
        if age < 18:
            return False, "You must be over 18 to use SoloConnect"
        else:
            return (
                False,
                "The age you entered is over 99. Please verify your inputs and try again",
            )


def return_lang_tuple():
    return ("English", "English")
