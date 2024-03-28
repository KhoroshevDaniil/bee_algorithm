from matplotlib import pyplot as plt

from models.hive import Hive


class DynamicBeeScatterplot:
    fig, ax = plt.subplots()

    hive: Hive = None

    current_bee_sc = None
    selected_bee_sc = None
    best_bee_sc = None

    def __init__(self, hive_instance: Hive):
        self.hive = hive_instance

    def update(self, x_index: int, y_index: int):
        x = []
        y = []

        x_best = []
        y_best = []

        x_selected = []
        y_selected = []

        for curr_bee in self.hive.swarm:
            if curr_bee in self.hive.best_spots:
                x_best.append(curr_bee.position[x_index])
                y_best.append(curr_bee.position[y_index])
            elif curr_bee in self.hive.selected_spots:
                x_selected.append(curr_bee.position[x_index])
                y_selected.append(curr_bee.position[y_index])
            else:
                x.append(curr_bee.position[x_index])
                y.append(curr_bee.position[y_index])

        self.ax.clear()
        self.current_bee_sc = self.ax.scatter(x, y, c='k', s=1, marker='o')

        if len(x_selected) != 0:
            self.selected_bee_sc = self.ax.scatter(x_selected, y_selected, c='y', s=20, marker='o')

        self.best_bee_sc = self.ax.scatter(x_best, y_best, c='r', s=30, marker='o')

        self.ax.grid(True)

        plt.pause(0.01)

    def get_figure(self):
        return self.fig
