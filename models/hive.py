
class Hive:
    def __init__(
            self,
            scout_bee_count,
            selected_bee_count,
            best_bee_count,
            selected_spots_count,
            best_spots_count,
            range_list,
            bee_type
    ):
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
            if curr_bee.check_other_patch(self.best_spots, self.range) and curr_bee.check_other_patch \
                    (self.selected_spots, self.range):
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
