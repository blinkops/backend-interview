from unittest import TestCase
from location import Location, parse_location


class TestLocation(TestCase):
    def setUp(self):
        self.location = Location(45.7597, 4.8422)

    def test_set_invalid_latitude(self):
        with self.assertRaises(ValueError):
            self.location.latitude = -90.1
        with self.assertRaises(ValueError):
            self.location.latitude = 90.1
        with self.assertRaises(TypeError):
            self.location.latitude = "fake"

    def test_set_invalid_longitude(self):
        with self.assertRaises(ValueError):
            self.location.longitude = -180.1
        with self.assertRaises(ValueError):
            self.location.longitude = 180.1
        with self.assertRaises(TypeError):
            self.location.longitude = "fake"

    def test_calculate_distance(self):
        """
        Test the distance calculation between two locations. with a known result. (lyon to paris)
        """
        self.assertAlmostEqual(392.2172595594006, self.location.calculate_distance(Location(48.8567, 2.3508)))

    def test_calculate_distance_with_None(self):
        self.assertIsNone(self.location.calculate_distance(None))


class TestParseLocation(TestCase):
    def test_with_none(self):
        with self.assertRaises(ValueError):
            parse_location(None)

    def test_without_comma(self):
        with self.assertRaises(ValueError):
            parse_location("0 0")

    def test_with_too_many_values(self):
        with self.assertRaises(ValueError):
            parse_location("0,0,0")

    def test_with_valid_data(self):
        self.assertEqual(Location(0, 0).longitude, parse_location("0,0").longitude)
        self.assertEqual(Location(0, 0).latitude, parse_location("0,0").latitude)

    def test_with_invalid_latitude(self):
        with self.assertRaises(ValueError):
            parse_location("-90.1,0")
        with self.assertRaises(ValueError):
            parse_location("90.1,0")
        with self.assertRaises(ValueError):
            parse_location("fake,0")

    def test_with_invalid_longitude(self):
        with self.assertRaises(ValueError):
            parse_location("0,-180.1")
        with self.assertRaises(ValueError):
            parse_location("0,180.1")
        with self.assertRaises(ValueError):
            parse_location("0,fake")
