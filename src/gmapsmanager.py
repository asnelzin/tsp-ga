import os
import time
import urllib.request
import urllib.parse
import json
import jinja2

from city import City
from config import gmaps


class GMapsManager:

    @staticmethod
    def get_cities_from_database():
        data = None
        try:
            database = open(gmaps['DATABASE_PATH'], 'r', encoding='utf-8')
            try:
                data = database.readlines()
            finally:
                database.close()
        except IOError:
            print('IOError: Can\'t open file or read data')

        if data:
            cities = list()
            for line in data:
                name, lat, lng = line.split(', ')
                lat, lng = float(lat[1:]), float(lng[:-2])
                cities.append(City(name, lat, lng))
            return cities

        return list()

    @staticmethod
    def write_cities_to_database(cities):
        if cities:
            try:
                database = open(gmaps['DATABASE_PATH'], 'a', encoding='utf-8')
                try:
                    database.write('\n'.join([str(city) for city in cities]))
                    database.write('\n')
                finally:
                    database.close()
            except IOError:
                print('IOError: Can\'t write data')

    @staticmethod
    def get_city_from_gmaps(city_name):
        parameters = {
            'address': city_name,
            'sensor': 'false'
        }

        param_string = urllib.parse.urlencode(parameters)
        req = urllib.request.Request(gmaps['URL'] + param_string)
        response = urllib.request.urlopen(req).read()
        json_data = json.loads(response.decode('utf-8'))
        city_pos = json_data['results'][0]['geometry']['location']

        new_city = City(city_name, float(city_pos['lat']), float(city_pos['lng']))
        print('Just add new city: ', new_city)
        return new_city

    @staticmethod
    def get_cities(cities_names):
        existing_cities = GMapsManager.get_cities_from_database()
        existing_names = [city.name for city in existing_cities]

        new_cities = list()
        for city_name in cities_names:
            if city_name not in existing_names:
                new_cities.append(GMapsManager.get_city_from_gmaps(city_name))
                time.sleep(1)

        GMapsManager.write_cities_to_database(new_cities)
        return existing_cities + new_cities

    @staticmethod
    def make_gmaps_webpage(tour, iter_counter):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        template = env.get_template('templates/template.html')

        tour_lats = [city.lat for city in tour]
        tour_lngs = [city.lng for city in tour]

        center_lat = (max(tour_lats) + min(tour_lats)) / 2
        center_lng = (max(tour_lngs) + min(tour_lngs)) / 2

        gmaps_content = template.render({
            'center_lat': center_lat,
            'center_lng': center_lng,
            'tour': tour,
            'iter_counter': iter_counter
        })

        try:
            webpage = open(gmaps['WEBMAP_PATH'], 'w', encoding='utf-8')
            try:
                webpage.write(gmaps_content)
            finally:
                webpage.close()
        except IOError:
            print('IOError: Can\'t write data')




