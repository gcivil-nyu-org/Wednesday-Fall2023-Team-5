from trip.helpers import city_present_in_country


def test_city_present_in_country(self):
    city = ["Bangalore"]
    country = ["India"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)

    city = ["Chicago"]
    country = ["United States"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)

    city = ["London"]
    country = ["United Kingdom"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)

    city = ["Cancun"]
    country = ["Mexico"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)

    city = ["Toronto"]
    country = ["Canada"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)

    city = ["Paris"]
    country = ["France"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)

    city = ["Florence"]
    country = ["Italy"]
    x = city_present_in_country(city, country)
    self.assertTrue(x)


def test_city_not_present_in_country(self):
    city = ["Florence"]
    country = ["UAE"]
    self.assertRaises(TypeError, lambda: city_present_in_country(city, country))
