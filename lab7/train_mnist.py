import helper
import numpy as np
from Perceptron import Perceptron
X, y = helper.load_digits()
num_samples = len(X)
num_train_samples = 1000
num_test_samples = num_samples-num_train_samples
print("Training on %d samples." % num_train_samples )
print("Testing on %d samples." % num_test_samples )

random_indices = np.random.permutation ( num_samples )
test_sample_indices = random_indices [: num_test_samples ]
train_sample_indices = random_indices [ num_test_samples :]

X = np.array(X, dtype=list)
y = np.array(y, dtype=str)
X_train = X[ train_sample_indices ]
y_train = y[ train_sample_indices ]
X_test = X[ test_sample_indices ]
y_test = y[ test_sample_indices ]
model = Perceptron ( learning_rate =0.1 , max_iter=1, verbose=False)
for epoch in range(200):
    model.fit(X_train,y_train)
model.plot_classified_images( X_test[:16])