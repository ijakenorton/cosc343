import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

def update(num):
    with open("fitness.csv", "r") as file:
        numbers = file.read()
    fitnesses = [float(number.strip()) for number in numbers.split()]
    
    if len(fitnesses) == len(ax.lines[0].get_ydata()):
        # No update in data
        return
    
    smoothed_fitnesses = moving_average(fitnesses, periods=10)
    epochs = list(range(1, len(fitnesses)+1))
    smoothed_epochs = epochs[:len(smoothed_fitnesses)]
    
    # Update the data of the lines
    ax.lines[0].set_data(epochs, fitnesses)
    ax.lines[1].set_data(smoothed_epochs, smoothed_fitnesses)
    
    # Adjust the xlim to accommodate the new data points
    ax.set_xlim(0, len(fitnesses)+1)
    
    # Adjust ylim based on data
    min_fitness = min(min(fitnesses), min(smoothed_fitnesses))
    max_fitness = max(max(fitnesses), max(smoothed_fitnesses))
    margin = (max_fitness - min_fitness) * 0.1
    ax.set_ylim(min_fitness - margin, max_fitness + margin)
    max_fitness_value = max(fitnesses)
    max_fitness_epoch = epochs[fitnesses.index(max_fitness_value)]
    # Update the label with the maximum smoothed fitness value
    max_smoothed_value = max(smoothed_fitnesses)
    ax.lines[0].set_label(f'Average Fitness (Max: {max_fitness_value:.2f})')
    ax.lines[1].set_label(f'Trend (Moving Avg, Max: {max_smoothed_value:.2f})')
    
    # Update the legend
    ax.legend(loc='upper left')

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot([], [], label='Average Fitness', color='blue', alpha=0.3)
ax.plot([], [], label='Trend (Moving Average)', color='red', linewidth=2)

ax.set_title('Model Average Fitness Over Time')
ax.set_xlabel('Epoch')
ax.set_ylabel('Average Fitness')
ax.legend()
ax.grid(True)
plt.tight_layout()

ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)  # Updates every 1000ms
plt.show()
