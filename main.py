import matplotlib.pyplot as plt
import numpy as np

F = lambda x: np.sin(2 * x)

plt.ion()
x = np.linspace(0, 1, 200)
li, = plt.plot(x, F(x))

for i in range(100):
    # if 'ax' in globals(): ax.remove()
    new_x = np.random.choice(x, size=10)
    ax = plt.scatter(new_x, F(new_x))
    plt.pause(1)

plt.ioff()
plt.show()
