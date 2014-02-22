import random
import itertools

from config import ga


class Tour(object):
    def __init__(self, tour):
        self._fitness = 0
        self._distance = 0
        self._tour = tour

    def __getitem__(self, index):
        return self._tour[index]

    def __iter__(self):
        return self._tour.__iter__()

    def _pairwise(self):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = itertools.tee(self._tour)
        next(b, None)
        return zip(a, b)

    def _swap(self, i, j):
        self._tour[i], self._tour[j] = self._tour[j], self._tour[i]

    @property
    def size(self):
        return len(self._tour)

    def distance(self):
        if self._distance == 0:
            for current, next in self._pairwise():
                self._distance += current.distance_to(next)

        return self._distance

    def fitness(self):
        if self._fitness == 0:
            self._fitness = 1 / self.distance()
        return self._fitness

    def crossover(self, parent):
        child = [None] * parent.size

        start = int(random.random() * parent.size)
        end = int(random.random() * parent.size)

        if start > end:
            start, end = end, start

        child[start:end] = parent[start:end]

        for city in self._tour:
            if city not in child:
                child[child.index(None)] = city

        return Tour(child)

    def mutate(self):
        for index in range(self.size):
            if random.random() < ga['MUTATION_RATE']:
                random_index = int(random.random() * self.size)
                self._swap(index, random_index)

    @staticmethod
    def generate_random_tour(cities):
        tour = cities.copy()
        random.shuffle(tour)
        return Tour(tour)

    def fine_print(self):
        route_str = '->'.join([city.name for city in self._tour])
        out_string = 'Route: {}\n' \
                     'Distance: {}'.format(route_str, self.distance())

        print(out_string)


