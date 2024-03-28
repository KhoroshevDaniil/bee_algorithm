from matplotlib import pyplot as plt

from bee import Hive, SimpleBee
import bee_examples
from bee_test_func import DynamicBeeScatterplot

if __name__ == "__main__":
    plt.ion()

    # bee_type = bee_examples.SphereBee

    # bee_type = bee_examples.GoldsteinBee
    bee_type: SimpleBee = bee_examples.HimmelblauBee
    # bee_type = bee_examples.RosenbrockBee

    # Количество пчел-разведчиков
    scout_bee_count = 300

    # Количество пчел, отправляемых на выбранные, но не лучшие участки
    selected_bee_count = 10

    # Количество пчел, отправляемые на лучшие участки
    best_bee_count = 30

    # Количество выбранных, но не лучших, участков
    selected_spots_count = 15

    # Количество лучших участков
    best_spots_count = 5

    # Количество запусков алгоритма
    run_count = 1

    # Максимальное количество итераций
    max_iteration = 2000

    # Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
    max_func_counter = 10

    # Во сколько раз будем уменьшать область поиска
    coefficient = bee_type.get_range_coefficient()

    ###################################################

    ax, bx, cx = None, None, None

    bee_scatter_plot = None

    for current_run in range(run_count):
        curr_hive = Hive(
            scout_bee_count=scout_bee_count,
            selected_bee_count=selected_bee_count,
            best_bee_count=best_bee_count,
            selected_spots_count=selected_spots_count,
            best_spots_count=best_spots_count,
            range_list=bee_type.get_start_range(),
            bee_type=bee_type
        )

        bee_scatter_plot = DynamicBeeScatterplot(curr_hive)

        # Начальное значение целевой функции
        best_func = -1.0e9

        # Количество итераций без улучшения целевой функции
        func_counter = 0

        for n in range(max_iteration):
            curr_hive.next_step()

            # Найдено место, где целевая функция лучше
            if curr_hive.best_fitness != best_func:
                best_func = curr_hive.best_fitness
                func_counter = 0

                # bee_scatter_plot.update(0, 1)
                bee_scatter_plot.update(0, 1)

                print(f"\n*** Run №{current_run + 1} | Iteration: {n}")
                print(f"Best position: {curr_hive.best_position}")
                print(f"Best fitness: {curr_hive.best_fitness}")
            else:
                func_counter += 1
                if func_counter == max_func_counter:
                    curr_hive.range = [curr_hive.range[i] * coefficient[i] for i in range(len(curr_hive.range))]
                    func_counter = 0

                    print(f"\n*** Run №{current_run + 1} | Iteration: {n} (new range)")
                    print(f"New range:{curr_hive.range}")
                    print(f"Best position: {curr_hive.best_position}")
                    print(f"Best fitness: {curr_hive.best_fitness}")

            if n % 10 == 0:
                # bee_scatter_plot.update(2, 3)
                bee_scatter_plot.update(0, 1)

        fig = bee_scatter_plot.get_figure()

        fig.savefig(f"{bee_type.__name__}_run_{current_run}.png")
