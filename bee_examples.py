# -*- coding: utf-8 -*-
import random
import math

from bee import SimpleBee


class SphereBee(SimpleBee):
    """Функция - сумма квадратов по каждой координате"""

    coordinates_count = 4

    @staticmethod
    def get_start_range():
        return [150.0] * SphereBee.coordinates_count

    @staticmethod
    def get_range_coefficient():
        return [0.98] * SphereBee.coordinates_count

    def __init__(self):
        super().__init__()

        self.min_val = [-150.0] * self.coordinates_count
        self.max_val = [150.0] * self.coordinates_count

        self.position = [random.uniform(self.min_val[i], self.max_val[i]) for i in range(self.coordinates_count)]
        self.calc_fitness()

    def calc_fitness(self):
        self.fitness = 0.0
        for x_i in self.position:
            self.fitness -= x_i ** 2


class GoldsteinBee(SimpleBee):
    """Функция Goldstein & Price"""

    coordinates_count: int = 2

    @staticmethod
    def get_start_range():
        return [2.0] * GoldsteinBee.coordinates_count

    @staticmethod
    def get_range_coefficient():
        return [0.98] * GoldsteinBee.coordinates_count

    def __init__(self):
        super().__init__()

        self.min_val = [-2.0] * self.coordinates_count
        self.max_val = [2.0] * self.coordinates_count

        self.position = [random.uniform(self.min_val[i], self.max_val[i]) for i in range(self.coordinates_count)]
        self.calc_fitness()

    def calc_fitness(self):
        x1 = self.position[0]
        x2 = self.position[1]

        self.fitness = (
                -(1.0 + ((x1 + x2 + 1.0) ** 2) *
                  (19.0 - 14.0 * x1 + 3.0 * x1 * x1 - 14.0 * x2 + 6.0 * x1 * x2 + 3.0 * x2 * x2)) *
                (30.0 + ((2.0 * x1 - 3.0 * x2) ** 2) *
                 (18.0 - 32.0 * x1 + 12.0 * x1 * x1 + 48.0 * x2 - 36.0 * x1 * x2 + 27.0 * x2 * x2))
        )


class RosenbrockBee(SimpleBee):
    """Функция Rosenbrock"""

    # Количество координат
    coordinates_count = 4

    @staticmethod
    def get_start_range():
        return [10.0] * RosenbrockBee.coordinates_count

    @staticmethod
    def get_range_coefficient():
        return [0.98] * RosenbrockBee.coordinates_count

    def __init__(self):
        super().__init__()

        self.min_val = [-10.0] * self.coordinates_count
        self.max_val = [10.0] * self.coordinates_count

        self.position = [random.uniform(self.min_val[i], self.max_val[i]) for i in range(self.coordinates_count)]
        self.calc_fitness()

    def calc_fitness(self):
        self.fitness = 0.0
        for n in range(3):
            xi = self.position[n]
            xi_1 = self.position[n + 1]

            self.fitness -= 100.0 * (((xi * xi - xi_1) ** 2) + ((1 - xi) ** 2))


class HimmelblauBee(SimpleBee):
    """Функция Химмельблау (4 минимума)"""

    # Количество координат
    coordinates_count = 2

    @staticmethod
    def get_start_range():
        return [5.0] * HimmelblauBee.coordinates_count

    @staticmethod
    def get_range_coefficient():
        return [0.98] * HimmelblauBee.coordinates_count

    def __init__(self):
        super().__init__()

        self.min_val = [-5.0] * self.coordinates_count
        self.max_val = [5.0] * self.coordinates_count

        self.position = [random.uniform(self.min_val[i], self.max_val[i]) for i in range(self.coordinates_count)]
        self.calc_fitness()

    def calc_fitness(self):
        x, y = self.position
        self.fitness = 0.0
        self.fitness -= (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2
