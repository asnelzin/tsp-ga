import random

from config import ga
from tour import Tour


class Population(object):

    def __init__(self):
        self._tours = []

    @property
    def size(self):
        return len(self._tours)

    def add(self, tour):
        self._tours.append(tour)

    def get_fittest(self):
        fittest = self._tours[0]
        for tour in self._tours:
            if tour.fitness() > fittest.fitness():
                fittest = tour
        return fittest

    def tournament_selection(self):
        tournament_population = Population()

        for i in range(ga['TOURNAMENT_SIZE']):
            tournament_population.add(random.choice(self._tours))

        return tournament_population.get_fittest()

    def evolve_population(self):
        new_population = Population()

        new_population.add(self.get_fittest())

        for i in range(self.size - 1):
            parent_tour1 = self.tournament_selection()
            parent_tour2 = self.tournament_selection()

            child_tour = parent_tour1.crossover(parent_tour2)

            child_tour.mutate()

            new_population.add(child_tour)
        return new_population

    @staticmethod
    def generate_random_population(size, cities):
        random_population = Population()
        for i in range(size):
            random_population.add(Tour.generate_random_tour(cities))
        return random_population
