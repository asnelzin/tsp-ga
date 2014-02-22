import webbrowser
import os

from gmapsmanager import GMapsManager
from population import Population
from config import ga, cities_names, gmaps


def main():
    cities = GMapsManager.get_cities(cities_names)

    population = Population.generate_random_population(ga['INIT_POPULATION_SIZE'], cities)

    print('Starting genetic algorithm...')

    iter_counter = 0
    min_distance = population.get_fittest().distance()
    while (min_distance > ga['LAST_BEST_DIST']) and (iter_counter < ga['MAX_STEPS']):
        population = population.evolve_population()
        min_distance = population.get_fittest().distance()
        iter_counter += 1
        print('Minimal distance after {} iterations: {}'.format(iter_counter, min_distance))

    best_tour = population.get_fittest()

    GMapsManager.make_gmaps_webpage(best_tour, iter_counter)

    url = 'file://' + os.path.realpath(gmaps['WEBMAP_PATH'])
    webbrowser.open_new(url)


if __name__ == '__main__':
    main()