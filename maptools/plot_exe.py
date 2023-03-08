import pickle
from matplotlib import pyplot as plt

def plot_exe(range=None):
    file = './execu.pkl'
    with open(file, 'rb') as f_read:
        exe_dict = pickle.load(f_read)

    total = []
    for i, exe_list in enumerate(exe_dict.values()):
        total.append([])
        for j, d in enumerate(exe_list):
            if d != 0:
                if range is not None:
                    if j > range[0] and j < range[1]:
                        total[i].append((j, i))
                else:
                    total[i].append((j, i))

    for list in total:
        if len(list) == 0:
            continue
        x, y = zip(*list)
        plt.scatter(x, y, marker='|')

    plt.show()

if __name__ == "__main__":
    plot_exe(range=(49900,100000))