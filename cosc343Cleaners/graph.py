import numpy as np
import matplotlib.pyplot as plt

# Function to compute moving average
def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

# Your average fitness values
 
numbers = "-25.36 -2.63375 1.9775000000000003 -0.8700000000000001 1.0612499999999998 -1.3212500000000005 -1.7274999999999998 1.8562499999999997 2.8137499999999998 3.21 1.32375 3.3287499999999994 -0.39750000000000013 3.0524999999999998 2.8 3.4675 1.2524999999999997 2.4 4.455 4.07625 4.84125 3.0975 2.6 2.9575 2.8225000000000002 1.6125 1.5987499999999997 -0.03500000000000014 3.5275 3.3449999999999998 3.6399999999999997 2.34 2.3625 4.595 3.9412499999999993 2.8899999999999997 3.2475 3.3287500000000003 4.0287500000000005 2.57 5.295 3.4387499999999998 3.9237499999999996 4.1125 2.60625 4.4875 4.6925 3.4537499999999994 "
# Extracting values from the numbers string
fitnesses = [float(number.strip()) for number in numbers.split()]

# Calculate the moving average
smoothed_fitnesses = moving_average(fitnesses, periods=10)  # adjust the period based on desired smoothness

# Create a list of epochs/timesteps based on the length of fitness values
epochs = list(range(1, len(fitnesses)+1))

# Create an adjusted epoch list for the smoothed data
smoothed_epochs = epochs[:len(smoothed_fitnesses)]

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(epochs, fitnesses, label='Average Fitness', color='blue', alpha=0.3)
plt.plot(smoothed_epochs, smoothed_fitnesses, label='Trend (Moving Average)', color='red', linewidth=2)

plt.title('Model Average Fitness Over Time')
plt.xlabel('Epoch')
plt.ylabel('Average Fitness')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Display the plot
plt.show()
