import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestRegressor
data = [{'sample': 0.01, 'lower_bound': 300, 'score': 4.77, 'time': 250.56195545196533},
{'sample': 0.01, 'lower_bound': 400, 'score': 4.79, 'time': 262.32014632225037},
{'sample': 0.01, 'lower_bound': 500, 'score': 4.78, 'time': 259.22157740592957},
{'sample': 0.01, 'lower_bound': 600, 'score': 4.74, 'time': 261.08715319633484},
{'sample': 0.01, 'lower_bound': 700, 'score': 4.79, 'time': 260.6836097240448},
{'sample': 0.01, 'lower_bound': 800, 'score': 4.79, 'time': 258.16564655303955},
{'sample': 0.01, 'lower_bound': 900, 'score': 4.76, 'time': 259.81779408454895},

{'sample': 0.05, 'lower_bound': 300, 'score': 4.76, 'time': 257.7449507713318},
{'sample': 0.05, 'lower_bound': 400, 'score': 4.78, 'time': 259.3352930545807},
{'sample': 0.05, 'lower_bound': 500, 'score': 4.75, 'time': 257.39712595939636},
{'sample': 0.05, 'lower_bound': 600, 'score': 4.81, 'time': 257.43964529037476},
{'sample': 0.05, 'lower_bound': 700, 'score': 4.74, 'time': 256.8101568222046},
{'sample': 0.05, 'lower_bound': 800, 'score': 4.74, 'time': 257.00703620910645},
{'sample': 0.05, 'lower_bound': 900, 'score': 4.78, 'time': 257.7362458705902},

{'sample': 0.1, 'lower_bound': 300, 'score': 4.75, 'time': 256.79678869247437},
{'sample': 0.1, 'lower_bound': 400, 'score': 4.77, 'time': 256.4346466064453},
{'sample': 0.1, 'lower_bound': 500, 'score': 4.76, 'time': 257.6855685710907},
{'sample': 0.1, 'lower_bound': 600, 'score': 4.77, 'time': 259.51310300827026},
{'sample': 0.1, 'lower_bound': 700, 'score': 4.77, 'time': 257.7303810119629},
{'sample': 0.1, 'lower_bound': 800, 'score': 4.77, 'time': 256.491840839386},
{'sample': 0.1, 'lower_bound': 900, 'score': 4.81, 'time': 258.831773519516},

{'sample': 0.2, 'lower_bound': 300, 'score': 4.79, 'time': 257.32952213287354},
{'sample': 0.2, 'lower_bound': 400, 'score': 4.74, 'time': 257.2199492454529},
{'sample': 0.2, 'lower_bound': 500, 'score': 4.78, 'time': 256.49737882614136},
{'sample': 0.2, 'lower_bound': 600, 'score': 4.75, 'time': 256.5583109855652},
{'sample': 0.2, 'lower_bound': 700, 'score': 4.75, 'time': 253.98967361450195},
{'sample': 0.2, 'lower_bound': 800, 'score': 4.81, 'time': 256.27025055885315},
{'sample': 0.2, 'lower_bound': 900, 'score': 4.77, 'time': 254.33030891418457},

{'sample': 0.3, 'lower_bound': 300, 'score': 4.77, 'time': 254.24397540092468},
{'sample': 0.3, 'lower_bound': 400, 'score': 4.78, 'time': 255.00421619415283},
{'sample': 0.3, 'lower_bound': 500, 'score': 4.75, 'time': 260.07699823379517},
{'sample': 0.3, 'lower_bound': 600, 'score': 4.8, 'time': 266.12309074401855},
{'sample': 0.3, 'lower_bound': 700, 'score': 4.75, 'time': 263.4785933494568},
{'sample': 0.3, 'lower_bound': 800, 'score': 4.81, 'time': 268.7733495235443},
{'sample': 0.3, 'lower_bound': 900, 'score': 4.76, 'time': 265.37500166893005},

{'sample': 0.4, 'lower_bound': 300, 'score': 4.78, 'time': 265.15859150886536},
{'sample': 0.4, 'lower_bound': 400, 'score': 4.76, 'time': 267.05470728874207},
{'sample': 0.4, 'lower_bound': 500, 'score': 4.75, 'time': 265.734947681427},
{'sample': 0.4, 'lower_bound': 600, 'score': 4.76, 'time': 266.1185004711151},
{'sample': 0.4, 'lower_bound': 700, 'score': 4.75, 'time': 265.402498960495},
{'sample': 0.4, 'lower_bound': 800, 'score': 4.77, 'time': 265.42645835876465},
{'sample': 0.4, 'lower_bound': 900, 'score': 4.75, 'time': 267.7906503677368},

{'sample': 0.5, 'lower_bound': 300, 'score': 4.77, 'time': 270.03368973731995},
{'sample': 0.5, 'lower_bound': 400, 'score': 4.77, 'time': 277.1805100440979},
{'sample': 0.5, 'lower_bound': 500, 'score': 4.8, 'time': 272.74782514572144},
{'sample': 0.5, 'lower_bound': 600, 'score': 4.79, 'time': 268.3822224140167},
{'sample': 0.5, 'lower_bound': 700, 'score': 4.77, 'time': 270.78865361213684},
{'sample': 0.5, 'lower_bound': 800, 'score': 4.73, 'time': 269.5309636592865},
{'sample': 0.5, 'lower_bound': 900, 'score': 4.75, 'time': 267.3947422504425},

{'sample': 0.6, 'lower_bound': 300, 'score': 4.81, 'time': 267.8988082408905},
{'sample': 0.6, 'lower_bound': 400, 'score': 4.74, 'time': 268.334664106369},
{'sample': 0.6, 'lower_bound': 500, 'score': 4.77, 'time': 270.46358919143677},
{'sample': 0.6, 'lower_bound': 600, 'score': 4.7, 'time': 268.28271555900574},
{'sample': 0.6, 'lower_bound': 700, 'score': 4.78, 'time': 272.61152172088623},
{'sample': 0.6, 'lower_bound': 800, 'score': 4.73, 'time': 266.53843426704407},
{'sample': 0.6, 'lower_bound': 900, 'score': 4.79, 'time': 269.77204990386963},

{'sample': 0.7, 'lower_bound': 300, 'score': 4.78, 'time': 269.4015564918518},
{'sample': 0.7, 'lower_bound': 400, 'score': 4.78, 'time': 269.481929063797},
{'sample': 0.7, 'lower_bound': 500, 'score': 4.75, 'time': 269.12932300567627},
{'sample': 0.7, 'lower_bound': 600, 'score': 4.76, 'time': 268.7834270000458},
{'sample': 0.7, 'lower_bound': 700, 'score': 4.79, 'time': 270.4876232147217},
{'sample': 0.7, 'lower_bound': 800, 'score': 4.79, 'time': 268.47736978530884},
{'sample': 0.7, 'lower_bound': 900, 'score': 4.75, 'time': 270.02819204330444},

{'sample': 0.8, 'lower_bound': 300, 'score': 4.81, 'time': 269.5380549430847},
{'sample': 0.8, 'lower_bound': 400, 'score': 4.76, 'time': 267.2695240974426},
{'sample': 0.8, 'lower_bound': 500, 'score': 4.8, 'time': 270.6505091190338},
{'sample': 0.8, 'lower_bound': 600, 'score': 4.74, 'time': 268.46295380592346},
{'sample': 0.8, 'lower_bound': 700, 'score': 4.74, 'time': 267.6710512638092},
{'sample': 0.8, 'lower_bound': 800, 'score': 4.76, 'time': 267.20979285240173},
{'sample': 0.8, 'lower_bound': 900, 'score': 4.74, 'time': 270.5145857334137},

{'sample': 0.9, 'lower_bound': 300, 'score': 4.78, 'time': 267.9156973361969},
{'sample': 0.9, 'lower_bound': 400, 'score': 4.75, 'time': 269.0197193622589},
{'sample': 0.9, 'lower_bound': 500, 'score': 4.75, 'time': 273.51514196395874},
{'sample': 0.9, 'lower_bound': 600, 'score': 4.78, 'time': 268.0191173553467},
{'sample': 0.9, 'lower_bound': 700, 'score': 4.79, 'time': 274.9988250732422},
{'sample': 0.9, 'lower_bound': 800, 'score': 4.75, 'time': 271.8913998603821},
{'sample': 0.9, 'lower_bound': 900, 'score': 4.79, 'time': 270.5533685684204}
]

# sample_sizes = [d['sample'] for d in data]
# scores = [d['score'] for d in data ]

# plt.scatter(sample_sizes, scores)
# plt.xlabel('Sample Size')
# plt.ylabel('Score')
# plt.title('Sample Size vs Score')
# plt.show()

# df = pd.DataFrame(data)

# sns.pairplot(df)
# plt.show()

# Features (sample and lower_bound)
# X = np.array([[d['sample'], d['lower_bound']] for d in data])

# # Targets (score and time)
# y = np.array([[d['score'], d['time']] for d in data])

# # Create a Linear Regression model
# model = LinearRegression()

# # Fit the model to the data
# model.fit(X, y)

# # Now you can use the model to predict 'score' and 'time' based on 'sample' and 'lower_bound'
# # For example:
# sample = 0.4
# lower_bound = 500
# prediction = model.predict(np.array([[sample, lower_bound]]))

# print(f"Predicted score and time for sample={sample} and lower_bound={lower_bound}: {prediction}")



# fig = plt.figure(figsize=(12, 6))

# # Plot for Score
# ax1 = fig.add_subplot(121, projection='3d')
# ax1.scatter([d['sample'] for d in data], [d['lower_bound'] for d in data], [d['score'] for d in data])
# ax1.set_xlabel('Sample')
# ax1.set_ylabel('Lower Bound')
# ax1.set_zlabel('Score')
# ax1.set_title('Sample & Lower Bound vs Score')

# # Plot for Time
# ax2 = fig.add_subplot(122, projection='3d')
# ax2.scatter([d['sample'] for d in data], [d['lower_bound'] for d in data], [d['time'] for d in data])
# ax2.set_xlabel('Sample')
# ax2.set_ylabel('Lower Bound')
# ax2.set_zlabel('Time')
# ax2.set_title('Sample & Lower Bound vs Time')

# plt.show()
# Features and Targets
X = np.array([[d['sample'], d['lower_bound']] for d in data])
y = np.array([d['score'] for d in data])  # Let's just consider 'score' for this example

# Create a Random Forest Regressor model and fit it to the data
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Create a grid of 'sample' and 'lower_bound' values
sample_values = np.linspace(min([d['sample'] for d in data]), max([d['sample'] for d in data]), num=100)
lower_bound_values = np.linspace(min([d['lower_bound'] for d in data]), max([d['lower_bound'] for d in data]), num=100)

sample_values, lower_bound_values = np.meshgrid(sample_values, lower_bound_values)
X_grid = np.c_[sample_values.ravel(), lower_bound_values.ravel()]

# Predict 'score' for each pair of 'sample' and 'lower_bound' in the grid
predicted_scores = model.predict(X_grid).reshape(sample_values.shape)

# Create a 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(sample_values, lower_bound_values, predicted_scores, alpha=0.3, color='none')

# Also plot the original data for comparison
ax.scatter([d['sample'] for d in data], [d['lower_bound'] for d in data], [d['score'] for d in data], c='r', marker='o')

ax.set_xlabel('Sample')
ax.set_ylabel('Lower Bound')
ax.set_zlabel('Score')
ax.set_title('Random Forest Regression - Sample & Lower Bound vs Score')



# Features and Targets
X = np.array([[d['sample'], d['lower_bound']] for d in data])
y = np.array([d['time'] for d in data])  # Now we consider 'time'

# Create a Random Forest Regressor model and fit it to the data
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Create a grid of 'sample' and 'lower_bound' values
sample_values = np.linspace(min([d['sample'] for d in data]), max([d['sample'] for d in data]), num=100)
lower_bound_values = np.linspace(min([d['lower_bound'] for d in data]), max([d['lower_bound'] for d in data]), num=100)

sample_values, lower_bound_values = np.meshgrid(sample_values, lower_bound_values)
X_grid = np.c_[sample_values.ravel(), lower_bound_values.ravel()]

# Predict 'time' for each pair of 'sample' and 'lower_bound' in the grid
predicted_times = model.predict(X_grid).reshape(sample_values.shape)

# Create a 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(sample_values, lower_bound_values, predicted_times, alpha=0.3, color='none')

# Also plot the original data for comparison
ax.scatter([d['sample'] for d in data], [d['lower_bound'] for d in data], [d['time'] for d in data], c='r', marker='o')

ax.set_xlabel('Sample')
ax.set_ylabel('Lower Bound')
ax.set_zlabel('Time')
ax.set_title('Random Forest Regression - Sample & Lower Bound vs Time')

plt.show()