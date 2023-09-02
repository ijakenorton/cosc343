import helper
from Perceptron import Perceptron
# X, y = helper.load_and()
# X, y = helper.load_xor ()
X, y = helper.load_iris2D()

model = Perceptron ( learning_rate =0.1 , max_iter=1, verbose=False)
for epoch in range(200):
    model.fit(X,y)
    model. plot_classified_regions (X,y,titleStr="Epoch %d" % (epoch +1))