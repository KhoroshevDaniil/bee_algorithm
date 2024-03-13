# -*- coding: utf-8 -*-
"""
Реализация алгоритма роя пчел
"""

import random
import math


class SimpleBee:
    """Класс пчел, где в качестве координат используется список дробных чисел"""

    def __init__(self):
        # Положение пчелы (искомые величины)
        self.position = None

        # Интервалы изменений искомых величин (координат)
        self.min_val = None
        self.max_val = None

        # Значение целевой функции
        self.fitness = 0.0

    def calc_fitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        pass

    # def sort(self, other_bee):
    #     """Функция для сортировки пчел по их целевой функции (здоровью) в порядке убывания."""
    #     if self.fitness < other_bee.fitness:
    #         return -1
    #     elif self.fitness > other_bee.fitness:
    #         return 1
    #     else:
    #         return 0

    def other_patch(self, bee_list, range_list):
        """Проверить находится ли пчела на том же участке, что и одна из пчел в bee_list.
        range_list - интервал изменения каждой из координат"""
        if len(bee_list) == 0:
            return True

        for curr_bee in bee_list:
            position = curr_bee.get_position()

            for n in range(len(self.position)):
                if abs(self.position[n] - position[n]) > range_list[n]:
                    return True

        return False

    def get_position(self):
        """Вернуть копию (!) своих координат"""
        return [val for val in self.position]

    def goto(self, other_pos, range_list):
        """Перелет в окрестность места, которое нашла другая пчела. Не в то же самое место! """

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
        """Скорректировать координаты пчелы, если они выходят за установленные пределы"""
        for n in range(len(self.position)):
            if self.position[n] < self.min_val[n]:
                self.position[n] = self.min_val[n]

            elif self.position[n] > self.max_val[n]:
                self.position[n] = self.max_val[n]


class Hive:
    """Улей. Управляет пчелами"""

    def __init__(self,
                 scout_bee_count,
                 selected_bee_count,
                 best_bee_count,
                 sel_sites_count,
                 best_sites_count,
                 range_list,
                 bee_type):
        """
        scout_bee_count - Количество пчел-разведчиков
        selected_bee_count - количество пчел, посылаемое на один из лучших участков
        best_bee_count - количество пчел, посылаемое на остальные выбранные участки

        sel_sites_count - количество выбранных участков
        best_sites_count - количество лучших участков среди выбранных
        bee_type - класс пчелы, производный от bee

        range_list - список диапазонов координат для одного участка
        """

        self.selected_bee_count = scout_bee_count
        self.selected_bee_count = selected_bee_count
        self.best_bee_count = best_bee_count

        self.sel_sites_count = sel_sites_count
        self.best_sites_count = best_sites_count

        self.bee_type = bee_type

        self.range = range_list

        # Лучшая на данный момент позиция
        self.best_position = None

        # Лучшее на данный момент здоровье пчелы (чем больше, тем лучше)
        self.best_fitness = -1.0e9

        # Начальное заполнение роя пчелами со случайными координатами
        bee_count = scout_bee_count + selected_bee_count * sel_sites_count + best_bee_count * best_sites_count
        self.swarm = [bee_type() for n in range(bee_count)]

        # Лучшие и выбранные места
        self.best_sites = []
        self.sel_sites = []

        self.swarm.sort(key=lambda bee: bee.fitness, reverse=True)
        self.best_position = self.swarm[0].get_position()
        self.best_fitness = self.swarm[0].fitness

    def send_bees(self, position, index, count):
        """ Послать пчел на позицию.
        Возвращает номер следующей пчелы для вылета """
        for n in range(count):
            # Чтобы не выйти за пределы улея
            if index == len(self.swarm):
                break

            curr_bee = self.swarm[index]

            if curr_bee not in self.best_sites and curr_bee not in self.sel_sites:
                # Пчела не на лучших или выбранных позициях
                curr_bee.goto(position, self.range)

            index += 1

        return index

    def next_step(self):
        """Новая итерация"""
        # Выбираем самые лучшие места и сохраняем ссылки на тех, кто их нашел
        self.best_sites = [self.swarm[0]]

        curr_index = 1
        for curr_bee in self.swarm[curr_index: -1]:
            # Если пчела находится в пределах уже отмеченного лучшего участка, то ее положение не считаем
            if curr_bee.other_patch(self.best_sites, self.range):
                self.best_sites.append(curr_bee)

                if len(self.best_sites) == self.best_sites_count:
                    break

            curr_index += 1

        self.sel_sites = []

        for curr_bee in self.swarm[curr_index: -1]:
            if curr_bee.other_patch(self.best_sites, self.range) and curr_bee.other_patch(self.sel_sites, self.range):
                self.sel_sites.append(curr_bee)

                if len(self.sel_sites) == self.sel_sites_count:
                    break

        # Отправляем пчел на задание :)
        # Отправляем сначала на лучшие места

        # Номер очередной отправляемой пчелы. 0-ую пчелу никуда не отправляем
        bee_index = 1

        for best_bee in self.best_sites:
            bee_index = self.send_bees(best_bee.get_position(), bee_index, self.best_bee_count)

        for sel_bee in self.sel_sites:
            bee_index = self.send_bees(sel_bee.get_position(), bee_index, self.selected_bee_count)

        # Оставшихся пчел пошлем куда попадет
        for curr_bee in self.swarm[bee_index: -1]:
            curr_bee.goto_random()

        self.swarm.sort(key=lambda bee: bee.fitness, reverse=True)
        self.best_position = self.swarm[0].get_position()
        self.best_fitness = self.swarm[0].fitness


class statistic:
    """ Класс для сбора статистики по запускам алгоритма"""

    def __init__(self):
        # Индекс каждого списка соответствует итерации.
        # В  элементе каждого списка хранится список значений для каждого запуска
        # Добавлять надо каждую итерацию

        # Значения целевой функции в зависимости от номера итерации
        self.fitness = []

        # Значения координат в зависимости от итерации
        self.positions = []

        # Размеры областей для поискарешения в зависимости от итерации
        self.range = []

    def add(self, run_number, curr_hive):
        range_vals = [val for val in curr_hive.range]
        fitness = curr_hive.best_fitness
        positions = curr_hive.swarm[0].get_position()

        assert (len(self.positions) == len(self.fitness))
        assert (len(self.range) == len(self.fitness))

        if run_number == len(self.fitness):
            self.fitness.append([fitness])
            self.positions.append([positions])
            self.range.append([range_vals])
        else:
            assert (run_number == len(self.fitness) - 1)

            self.fitness[run_number].append(fitness)
            self.positions[run_number].append(positions)
            self.range[run_number].append(range_vals)

    def format_fitness(self, run_number):
        """Сформировать таблицу целевой функции"""
        result = ""
        for n in range(len(self.fitness[run_number])):
            line = "%6.6d    %10f\n" % (n, self.fitness[run_number][n])
            result += line

        return result

    @staticmethod
    def format_columns(run_number, column):
        """Форматировать список списков items для вывода"""
        result = ""

        for n in range(len(column[run_number])):
            line = "%6.6d" % n

            for val in column[run_number][n]:
                line += "    %10f" % val

            line += "\n"
            result += line

        return result

    def format_pos(self, run_number):
        return self.format_columns(run_number, self.positions)

    def format_range(self, run_number):
        return self.format_columns(run_number, self.range)
