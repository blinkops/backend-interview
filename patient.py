from typing import Any, Optional
import random

from location import Location


class Patient:
    def __init__(self, id: str, name: str, location: Optional[Location], age: Optional[int],
                 acceptedOffers: Optional[int], canceledOffers: Optional[int], averageReplyTime: Optional[int],
                 pre_score: float = 0.0, potential_randomly_added_score: int = 0):
        self.id: str = id
        self.name: str = name
        self.location: Optional[Location] = location
        self.age: Optional[int] = age
        self.acceptedOffers: Optional[int] = acceptedOffers
        self.canceledOffers: Optional[int] = canceledOffers
        self.averageReplyTime: Optional[int] = averageReplyTime
        self.pre_score: float = pre_score
        self.potential_randomly_added_score: int = potential_randomly_added_score
        self.score: float = 0.0

    def get_by_field(self, field: str, default: Any) -> Any:
        """
        Use for sorting the patients by a specific field, If the patient has no value for the field, return the default
        *If field is 'location' return self.get_distance(default)*
        :param field: name of the field
        :param default: if the patient has no value for the field, return the default  **If field is 'location'
         default = <other_location>**
        :return: value of the field or default
        """
        if field == "location":
            return self.get_distance(default)

        value = self.__getattribute__(field)
        if value is None:
            return default
        return value

    def get_distance(self, other_location: Location) -> float:
        """
        Get the distance between the patient and the other location,
        if the patient has no location, return float('inf')
        :param other_location: the other location
        :return: the distance between the patient and the other location, or float('inf') if the patient has no location
        """

        if self.location is None:
            return float('inf')
        return self.location.calculate_distance(other_location)

    def set_score(self, location_score: float) -> None:
        """
        Set the score of the patient to -> pre_score + location_score +
         (random * potential_randomly_added_score)
        :param location_score: the score of the distance between the patient and the location
        :return: None
        """

        self.score = round(self.pre_score + location_score +
                           (random.random() * self.potential_randomly_added_score), 10)
