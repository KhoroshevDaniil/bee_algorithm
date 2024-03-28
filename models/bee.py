import random
from typing import List


class SimpleBee:
    def __init__(self):
        # Интервалы изменений искомых величин (координат)
        self.min_val: List = []
        self.max_val: List = []

        # Положение пчелы (искомые величины)
        self.position: List = []

        # Значение целевой функции
        self.fitness: float = 0.0

    @staticmethod
    def get_start_range():
        pass

    @staticmethod
    def get_range_coefficient():
        pass

    def calc_fitness(self):
        """
        Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы
        """
        pass

    def check_other_patch(self, bee_list, range_list):
        """
        Проверить находится ли пчела на том же участке, что и одна из пчел в bee_list.
        range_list - интервал изменения каждой из координат
        """
        if len(bee_list) == 0:
            return True

        for curr_bee in bee_list:
            position = curr_bee.get_position()

            for n in range(len(self.position)):
                if abs(self.position[n] - position[n]) > range_list[n]:
                    return True

        return False

    def get_position(self):
        return self.position.copy()

    def goto(self, other_pos, range_list):
        """
        Перелет в окрестность места, которое нашла другая пчела. Не в то же самое место!
        """

        # К каждой из координат добавляем случайное значение
        self.position = [other_pos[n] + random.uniform(-range_list[n], range_list[n]) for n in range(len(other_pos))]

        # Проверим, чтобы не выйти за заданные пределы
        self.check_position()

        # Расчитаем и сохраним целевую функцию
        self.calc_fitness()

    def goto_random(self):
        # Заполним координаты случайными значениями
        self.position = [random.uniform(self.min_val[n], self.max_val[n]) for n in range(len(self.position))]
        self.check_position()
        self.calc_fitness()

    def check_position(self):
        """
        Скорректировать координаты пчелы, если они выходят за установленные пределы
        """

        for n in range(len(self.position)):
            if self.position[n] < self.min_val[n]:
                self.position[n] = self.min_val[n]
            elif self.position[n] > self.max_val[n]:
                self.position[n] = self.max_val[n]