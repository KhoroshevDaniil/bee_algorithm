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


class Hive:
    def __init__(self,
                 scout_bee_count,
                 selected_bee_count,
                 best_bee_count,
                 selected_spots_count,
                 best_spots_count,
                 range_list,
                 bee_type):
        """
        scout_bee_count - Количество пчел-разведчиков
        selected_bee_count - количество пчел, посылаемое на один из лучших участков
        best_bee_count - количество пчел, посылаемое на остальные выбранные участки

        selected_spots_count - количество выбранных участков
        best_spots_count - количество лучших участков среди выбранных
        bee_type - класс пчелы, производный от bee

        range_list - список диапазонов координат для одного участка
        """

        self.scout_bee_count = scout_bee_count
        self.selected_bee_count = selected_bee_count
        self.best_bee_count = best_bee_count

        self.selected_spots_count = selected_spots_count
        self.best_spots_count = best_spots_count

        self.bee_type = bee_type

        self.range = range_list

        # Лучшая на данный момент позиция
        self.best_position = None

        # Лучшее на данный значение целевой функции
        self.best_fitness = -1.0e9

        # Начальное заполнение роя пчелами со случайными координатами
        bee_count = scout_bee_count + selected_bee_count * selected_spots_count + best_bee_count * best_spots_count
        self.swarm = [bee_type() for n in range(bee_count)]

        # Лучшие и выбранные места
        self.best_spots = []
        self.selected_spots = []

        self.swarm.sort(key=lambda bee: bee.fitness, reverse=True)
        self.best_position = self.swarm[0].get_position()
        self.best_fitness = self.swarm[0].fitness

    def send_bees(self, position, index, count):
        """
        Послать пчел на позицию.
        Возвращает номер следующей пчелы для вылета
        """
        for n in range(count):
            # Чтобы не выйти за пределы улея
            if index == len(self.swarm):
                break

            curr_bee = self.swarm[index]

            # Пчела не на лучших или выбранных позициях
            if (curr_bee not in self.best_spots) and (curr_bee not in self.selected_spots):
                curr_bee.goto(position, self.range)

            index += 1

        return index

    def next_step(self):
        """
        Новая итерация
        """

        # Выбираем самые лучшие места и сохраняем ссылки на тех, кто их нашел
        self.best_spots = [self.swarm[0]]

        curr_index = 1
        for curr_bee in self.swarm[curr_index: -1]:
            # Если пчела находится в пределах уже отмеченного лучшего участка, то ее положение не считаем
            if curr_bee.check_other_patch(self.best_spots, self.range):
                self.best_spots.append(curr_bee)

                if len(self.best_spots) == self.best_spots_count:
                    break

            curr_index += 1

        self.selected_spots = []

        for curr_bee in self.swarm[curr_index: -1]:
            if curr_bee.check_other_patch(self.best_spots, self.range) and curr_bee.check_other_patch(self.selected_spots, self.range):
                self.selected_spots.append(curr_bee)

                if len(self.selected_spots) == self.selected_spots_count:
                    break

        # Отправляем пчел на задание

        # Номер очередной отправляемой пчелы. 0-ую пчелу никуда не отправляем
        bee_index = 1

        # Сначала отправляем на лучшие места
        for best_bee in self.best_spots:
            bee_index = self.send_bees(best_bee.get_position(), bee_index, self.best_bee_count)

        # Затем на остальные выбранные места
        for sel_bee in self.selected_spots:
            bee_index = self.send_bees(sel_bee.get_position(), bee_index, self.selected_bee_count)

        # Остальные пчёлы летят куда глаза глядят
        for curr_bee in self.swarm[bee_index: -1]:
            curr_bee.goto_random()

        self.swarm.sort(key=lambda bee: bee.fitness, reverse=True)
        self.best_position = self.swarm[0].get_position()
        self.best_fitness = self.swarm[0].fitness


class Statistic:
    """ Класс для сбора статистики по запускам алгоритма"""

    def __init__(self):
        # Индекс каждого списка соответствует итерации.
        # В элементе каждого списка хранится список значений для каждого запуска
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
