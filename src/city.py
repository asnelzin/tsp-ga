import math


class City(object):

    def __init__(self, name, lat, lng):
        self._name = name
        self._lat = lat
        self._lng = lng

    @property
    def lat(self):
        return self._lat

    @property
    def lng(self):
        return self._lng

    @property
    def name(self):
        return self._name

    def distance_to(self, city):
        return math.sqrt((self._lat - city.lat)**2 + (self._lng - city.lng)**2)

    def __str__(self):
        return '{}, ({}, {})'.format(self._name, self._lat, self._lng)

    def __repr__(self):
        return self.__str__()