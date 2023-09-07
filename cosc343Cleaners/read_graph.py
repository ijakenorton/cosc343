import matplotlib.pyplot as plt
import numpy as np

def read_data_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("------"):
                continue
            if not any(char.isalpha() for char in line):  # check if the line contains any alphabetic characters
                data = [float(i) for i in line.split()]
                return data
    return []

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

def plot_data(y):
    x = list(range(1, len(y) + 1))
    ma = moving_average(y)

    # Adjust the x values for the moving average to align with data
    ma_x = x[len(x) - len(ma):]

    plt.plot(x, y, '-o', label='Data')
    plt.plot(ma_x, ma, '-r', linewidth=2, label='Trend (Moving Average)')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Plot from data file with Trendline')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    y_data = read_data_from_file("averages.txt")
    plot_data(y_data)

if __name__ == "__main__":
    main()
