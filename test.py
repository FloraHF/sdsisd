import matplotlib.pyplot as plt
from vecgram import *\

if __name__ == '__main__':
    fig, ax = plt.subplots()
    draw_vecgram(fig, ax, 3.5, 2.2)
    plt.show()