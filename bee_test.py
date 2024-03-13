# -*- coding: utf-8 -*-
import random
import math

# import pylab
from matplotlib import pyplot as plt

from bee import Hive, statistic
import bee_examples
import bee_test_func

if __name__ == "__main__":
    # try:
    #     import psyco
    #
    #     psyco.full()
    # except Exception as ex:
    #     print("Psyco not found")
    #     print(ex)

    # Включаем интерактивный режим
    plt.ion()

    # Будем сохранять статистику
    stat = statistic()

    # Имя файла для сохранения статистики
    stat_fname = "stat/beestat_%s.txt"

    ###################################################
    ##                     Параметры алгоритма
    ###################################################

    # Класс пчел, который будет использоваться в алгоритме

    bee_type = bee_examples.SphereBee
    # bee_type = beeexamples.dejongbee
    # bee_type = beeexamples.goldsteinbee
    # bee_type = beeexamples.rosenbrockbee
    # bee_type = beeexamples.testbee
    # bee_type = beeexamples.funcbee

    # Количество пчел-разведчиков
    scout_bee_count = 300

    # Количество пчел, отправляемых на выбранные, но не лучшие участки
    selected_bee_count = 10

    # Количество пчел, отправляемые на лучшие участки
    best_bee_count = 30

    # Количество выбранных, но не лучших, участков
    sel_sites_count = 15

    # Количество лучших участков
    best_sites_count = 5

    # Количество запусков алгоритма
    run_count = 1

    # Максимальное количество итераций
    max_iteration = 2000

    # Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
    max_func_counter = 10

    # Во столько раз будем уменьшать область поиска
    koeff = bee_type.get_range_koeff()

    ###################################################

    ax, bx, cx = None, None, None

    for run_number in range(run_count):
        # fig = plt.figure()
        # ax = fig.add_subplot(111)

        # Рисуем белый канвас
        # fig.canvas.draw()
        # plt.show(block=False)

        curr_hive = Hive(scout_bee_count, selected_bee_count, best_bee_count,
                         sel_sites_count, best_sites_count,
                         bee_type.get_start_range(), bee_type)

        # Начальное значение целевой функции
        best_func = -1.0e9

        # Количество итераций без улучшения целевой функции
        func_counter = 0

        stat.add(run_number, curr_hive)

        for n in range(max_iteration):
            curr_hive.next_step()

            stat.add(run_number, curr_hive)

            if curr_hive.best_fitness != best_func:
                # Найдено место, где целевая функция лучше
                best_func = curr_hive.best_fitness
                func_counter = 0

                # Обновим рисунок роя пчел
                ax, bx, cx = bee_test_func.plot_swarm(curr_hive, 0, 1)

                print(f"\n*** iteration {run_number + 1} / {n}")
                print(f"Best position: {curr_hive.best_position}")
                print(f"Best fitness: {curr_hive.best_fitness}")
            else:
                func_counter += 1
                if func_counter == max_func_counter:
                    # Уменьшим размеры участков
                    curr_hive.range = [curr_hive.range[m] * koeff[m] for m in range(len(curr_hive.range))]
                    func_counter = 0

                    print(f"\n*** iteration {run_number + 1} / {n} (new range)")
                    print(f"New range:{curr_hive.range}")
                    print(f"Best position: {curr_hive.best_position}")
                    print(f"Best fitness: {curr_hive.best_fitness}")

            if n % 10 == 0:
                ax, bx, cx = bee_test_func.plot_swarm(curr_hive, 2, 3)

        # Сохраним значения целевой функции
        fname = stat_fname % (("%4.4d" % run_number) + "_fitness")
        file = open(fname, "w")
        file.write(stat.format_fitness(run_number))
        file.close()

        # Сохраним значения координат
        fname = stat_fname % (("%4.4d" % run_number) + "_pos")
        file = open(fname, "w")
        file.write(stat.format_pos(run_number))
        file.close()

        # Сохраним значения интервалов
        fname = stat_fname % (("%4.4d" % run_number) + "_range")
        file = open(fname, "w")
        file.write(stat.format_range(run_number))
        file.close()

    bee_test_func.plot_stat(stat)
