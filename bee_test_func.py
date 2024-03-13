# -*- coding: utf-8 -*-

# import plt
from matplotlib import pyplot as plt

plt.ion()


def plot_swarm(hive_inst, x_index, y_index):
    """Нарисовать рой с помощью plt"""

    x = []
    y = []

    x_best = []
    y_best = []

    x_sel = []
    y_sel = []

    for curr_bee in hive_inst.swarm:
        if curr_bee in hive_inst.best_sites:
            x_best.append(curr_bee.position[x_index])
            y_best.append(curr_bee.position[y_index])

        elif curr_bee in hive_inst.sel_sites:
            x_sel.append(curr_bee.position[x_index])
            y_sel.append(curr_bee.position[y_index])

        else:
            x.append(curr_bee.position[x_index])
            y.append(curr_bee.position[y_index])

    plt.clf()
    ax = plt.scatter(x, y, c='k', s=1, marker='o')
    bx = None

    if len(x_sel) != 0:
        bx = plt.scatter(x_sel, y_sel, c='y', s=20, marker='o')

    cx = plt.scatter(x_best, y_best, c='r', s=30, marker='o')

    plt.pause(0.1)

    # We must contain this values in main thread for interactive plot
    return ax, bx, cx


def plot_fitness(stat, run_number):
    """Вывести значение целевой функции в зависимости от номера итерации"""
    x = range(len(stat.fitness[run_number]))
    y = stat.fitness[run_number]

    plt.plot(x, y)
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.grid(True)


def plot_average_fitness(stat):
    """Вывести усредненное по всем запускам значение целевой функции в зависимости от номера итерации"""
    x = range(len(stat.fitness[0]))
    y = [val for val in stat.fitness[0]]

    for run_number in range(1, len(stat.fitness)):
        for iteration in range(len(stat.fitness[run_number])):
            y[iteration] += stat.fitness[run_number][iteration]

    y = [val / len(stat.fitness) for val in y]

    plt.plot(x, y)
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.grid(True)


def plot_positions(stat, run_number, pos_index):
    """Вывести график сходимости искомых величин"""
    x = range(len(stat.positions[run_number]))
    val_list = []

    for positions in stat.positions[run_number]:
        val_list.append(positions[pos_index])

    plt.plot(x, val_list)
    plt.xlabel("Iteration")
    plt.ylabel("Position %d" % pos_index)
    plt.grid(True)


def plot_range(stat, run_number, pos_index):
    """Вывести график уменьшения областей"""
    x = range(len(stat.range[run_number]))
    val_list = []

    for cur_range in stat.range[run_number]:
        val_list.append(cur_range[pos_index])

    plt.plot(x, val_list)
    plt.xlabel("Iteration")
    plt.ylabel("Range %d" % pos_index)
    plt.grid(True)


def plot_stat(stat):
    """Нарисовать статистику"""
    plt.ioff()

    # Вывести изменение целевой функции в зависимости от номера итерации
    plt.figure()
    plot_fitness(stat, 0)

    # Вывести усредненное по всем запускам изменение целевой функции в зависимости от номера итерации
    plt.figure()
    plot_average_fitness(stat)

    # Вывести сходимость положений лучшей точки в зависимости от номера итерации
    plt.figure()
    pos_count = len(stat.positions[0][0])

    for n in range(pos_count):
        plt.subplot(pos_count, 1, n + 1)
        plot_positions(stat, 0, n)

    # Вывести изменение размеров областей в зависимости от номера итерации
    plt.figure()
    range_count = len(stat.range[0][0])

    for n in range(range_count):
        plt.subplot(range_count, 1, n + 1)
        plot_range(stat, 0, n)

    plt.show()
