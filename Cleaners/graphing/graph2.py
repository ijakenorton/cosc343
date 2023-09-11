import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

def update(num):
    all_fitnesses = []  # Store all fitness values for all models
    all_smoothed = []  # Store all smoothed fitness values for all models
    max_epoch_length = 0  # Track the largest epoch value across models

    for i, filename in enumerate(filenames):
        with open(filename, "r") as file:
            numbers = file.read()
        fitnesses = [float(number.strip()) for number in numbers.split()]
        smoothed_fitnesses = moving_average(fitnesses, periods=10)

        all_fitnesses.extend(fitnesses)
        all_smoothed.extend(smoothed_fitnesses)

        epochs = list(range(1, len(fitnesses) + 1))
        smoothed_epochs = epochs[:len(smoothed_fitnesses)]

        max_epoch_length = max(max_epoch_length, len(fitnesses))  # Update max_epoch_length

        # Update the data of the lines
        ax.lines[2*i].set_data(epochs, fitnesses)
        ax.lines[2*i + 1].set_data(smoothed_epochs, smoothed_fitnesses)

    # Adjust the xlim and ylim dynamically
    ax.set_xlim(0, max_epoch_length + 1)
    min_fitness = min(all_fitnesses + all_smoothed)
    max_fitness = max(all_fitnesses + all_smoothed)
    margin = (max_fitness - min_fitness) * 0.1
    ax.set_ylim(min_fitness - margin, max_fitness + margin)


# Define your filenames here
filenames = ["0", "1", "2", "3", "4"]

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# For each file, initialize two lines (one for raw data, one for moving average)
for i in range(len(filenames)):
    ax.plot([], [], label=f'Model {i+1} Average Fitness', alpha=0.3)
    ax.plot([], [], label=f'Model {i+1} Trend (Moving Average)', linewidth=2)

ax.set_title('Models Average Fitness Over Time')
ax.set_xlabel('Epoch')
ax.set_ylabel('Average Fitness')
ax.legend()
ax.grid(True)
plt.tight_layout()

ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)  # Updates every 1000ms
plt.show()
