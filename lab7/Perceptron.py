__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"
__modified_by__ = "<your name>"

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import time
import sys


class Perceptron:
    """
           Sklearn-like model for perceptron.

           ...

           Attributes
           ----------
           learning_rate : float
               the learning rate parameter
           max_iter : int
               maximum number of epochs to train for in the fit method
           verbose : bool
               if set to True, prints information while training inside
               the fit method
           trained : bool
               indicates if fit method has been invoked
           W: numpy array
               a DxK matrix of Perpectron weights
           b: numpy array
               a K-dim vector of Perceptorn biases

           Methods
           -------
            fit(X, y):
               Trains the Perceptron on set of points in X with
               corresponding labels in y

           predict(X)
               Returns the predictions of the perceptron for set of
               points in X

          get_params()
               Returns the W matrix and b vector of the
               perceptron parameters

          set_params(**params)
               Allows setting of the W and b parameters of the
               perceptron

         plot_classified_regions(X, y, titleStr)
               Visualisation of classified regions (works only
               if input size of the perceptron is D=2)

         plot_classified_images(X)
               Visualisation of data in X interpreted as
               images

         _one_hot(y)
               Converts N-dim label vector to one-hot encoded
               matrix of labels NxD, where D is the number of
               unique labels in y

           """

    def __init__(self, learning_rate=0.01, max_iter=100, verbose=False):
        """
        Initialisation

        :param learning_rate: the learning rate of the perceptron learning rule
        :param max_iter: max number of epochs to train for in the fit method
        :param verbose: verbosity of the fit method
        """

        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.verbose = verbose

        # Set the Perceptron parameters to None - they will
        # be initialised to random values the first time the fit method
        # is invoked (where the number of inputs and output will be
        # inferred from the data)
        self.W = None
        self.b = None

        # Set the class_labels to None - will be inferred from
        # the training data in the fit method
        self.class_labels = None

        self._trained = False

    def fit(self, X, y):
        """
        Implementation of the perceptron learning rule

        :param X: numpy array
            An NxD matrix of N samples of D attributes

        :param y: numpy array
            An N-dim vector of labels

        """

        # Infer the number of training samples and
        # dimensionality of input from X.
        N, D = X.shape

        # If this is the first time the fit method has
        # been invoked, initialise the perceptron parameters.
        if self.W is None:
            # How many unique entries in y?
            self.class_labels = np.unique(y)

            if len(self.class_labels) > 2:
                # Set the number of output equal to
                # the number of unique labels, if the
                # latter is larger than 2
                K = len(self.class_labels)
            else:
                # If only 2 labels in y, one perceptron output
                # is sufficient
                K = 1

            # Initialise the weight matrix and bias vector
            # of the perceptron with random, normally distributed
            # values
            self.W = np.random.randn(D,K)
            self.b = np.random.randn(K)

        # Convert the vector of labels to one-hot encoding
        Y = Perceptron._one_hot(y)

        # Iterate over max_iters each time computing errors based on the output
        # of the perceptron and updating the weights and bias
        for i in range(self.max_iter):
            y_hat = (np.dot(X, self.W) + self.b)
            y_hat[y_hat <= 0] = 0
            y_hat[y_hat > 0] = 1
            E = Y - y_hat
            delta_W = np.dot(X.T, E)
            delta_b = np.sum(E, axis=0)
            self.W = self.W + ((self.learning_rate/N) * delta_W)
            self.b = self.b + ((self.learning_rate/N) * delta_b)
            error = np.sum(E != 0)
            if self.verbose:
                print(error)            
            if error == 0:
                print("finished")
                break

        self._trained = True

    def predict(self, X):
        """
        Computes perceptron output Yhat = hardlim(X*self.W + self.b).

        :param X: numpy array
            An NxD matrix of N samples of D attributes

        :returns: numpy array
            An N-dim vector of labels as predicted by the
            perceptron from the input

        """

        if not self._trained:
            raise RuntimeError("Model needs training first.")

        # Calculate the weighted sum of inputs + bias
        Yhat = np.dot(X, self.W) + self.b

        # Apply the hardlimiting activation function
        Yhat[Yhat > 0] = 1
        Yhat[Yhat < 0] = 0

        # Convert one-hot encoded output to indices of
        # the labels
        yhat = np.argmax(Yhat, axis=1)

        # Return the predicted labels
        return self.class_labels[yhat]

    def get_params(self):
        """
        Getter of the Perceptron parameters

        :returns: dictionary
            with perceptron weights under key 'W'
            and biases under key 'b'.

        """

        return {'W': self.W, 'b': self.b}

    def set_params(self, **params):
        """
        Setter of the Perceptron parameters

        :param params: dictionary
            with perceptron weights under key 'W'
            and biases under key 'b'.

        """

        for key in params:
            if key != 'W' and key != 'b':
                print("Warning! Unrecognised parameter type '%s'" % key)

        if 'W' in params:
            self.W = params['W']

        if 'b' in params:
            self.b = params['b']

    def plot_classified_regions(self, X=None, y=None, titleStr=None):
        """
        Plots classification regions for 2-attribute input Perceptron

        :param X: numpy array
            Data points to plot

        :param y: numpy array
            Labels of the datapoint to plot

        :param titleStr: string
            The string to put as the title of the matplotlib plot

        """

        D, K = self.W.shape

        if D != 2:
            raise RuntimeError("Cannot visualise classification regions on %d-dimensional input Perceptron." % D)

        if K == 1:
            colours = ['blue']
        elif K == 3:
            colours = ['red', 'green', 'blue']
        else:
            return

        if not hasattr(self, 'fh'):
            # Create a new (empty) figure
            self.fh = plt.figure()
            self.ph = []
            plt.ion()
            plt.show()

            if X is not None and y is not None:
                Y = Perceptron._one_hot(y)

                if K == 1:
                    I = np.where(Y == 0)[0]
                    plt.plot(X[I, 0], X[I, 1], 'r.')

                    I = np.where(Y == 1)[0]
                    plt.plot(X[I, 0], X[I, 1], 'b.')
                else:
                    for k in range(K):
                        # Get indices of points labelled as 0
                        I = np.where(Y[:, k] == 1)[0]
                        plt.plot(X[I, 0], X[I, 1], '%s.' % colours[k][0])

            plt.xlabel('x_1')
            plt.ylabel('x_2')

        for ph in self.ph:
            ph.remove()

        self.ph = []

        if X is not None:
            xmins = np.min(X, axis=0)
            xmaxs = np.max(X, axis=0)
        else:
            xmins = np.ones((2))*-1
            xmaxs = np.ones((2))

        xrange = xmaxs - xmins

        xmins -= xrange * 0.2
        xmaxs += xrange * 0.2

        xedges = np.array([[xmins[0], xmins[1]],
                           [xmins[0], xmaxs[1]],
                           [xmaxs[0], xmins[1]],
                           [xmaxs[0], xmaxs[1]]])

        v = np.max(np.dot(xedges, self.W) + self.b, axis=0)

        for k in range(K):
            x1s = np.array([xmins[0], xmaxs[0]])
            x2s = (-self.b[k] - self.W[0, k] * x1s) / self.W[1, k]
            x_neg = (v[k] - self.b[k] - self.W[0, k] * x1s) / self.W[1, k]

            ph, = plt.plot(x1s, x2s, 'k-')
            self.ph.append(ph)
            ph = plt.fill_between(x1s, x2s, x_neg, facecolor=colours[k], alpha=0.5)
            self.ph.append(ph)

        plt.xlim([xmins[0], xmaxs[0]])
        plt.ylim([xmins[1], xmaxs[1]])

        if titleStr is not None:
            plt.title(titleStr)

        plt.pause(0.1)
        time.sleep(0.1)

    def plot_classified_images(self, X):
        """
        Plots classification regions for 2-attribute input Perceptron

        :param X: numpy array
            Data points to plot

        :param y: numpy array
            Labels of the datapoint to plot

        :param titleStr: string
            The string to put as the title of the matplotlib plot

        """

        N, D = X.shape

        im_height = int(np.sqrt(D))
        im_width = int(D / im_height)

        if im_height != im_width or im_height <= 2:
            return

        yhat = self.predict(X)

        # Create a new (empty) figure
        self.fh = plt.figure(figsize=(10, 8))
        plt.ion()
        plt.show()

        n = 0
        self.ph = []
        R = int(np.floor(np.sqrt(N)))
        C = int(np.ceil(N / R))

        for r in range(R):
            for c in range(C):
                if n >= N:
                    continue

                im = X[n, :].reshape(im_height, im_width)
                titleStr = str(yhat[n])
                n += 1
                ph = self.fh.add_subplot(R, C, n)
                self.ph.append(ph)
                ph.imshow(im, cmap='gray')
                ph.xaxis.set_visible(False)
                ph.yaxis.set_visible(False)
                ph.set_title(titleStr)

            if n >= N:
                break

            plt.pause(0.01)
            time.sleep(0.01)

        plt.ioff()
        plt.show()

    @staticmethod
    def _one_hot(y):
        """
        Converts vector of labels to one-hot encoding

        :param y: numpy array
            N-dim vector of labels

        :returns: numpy array
            A NxD matrix of one hot encoded labels, where
            D is the number of unique labels in y
        """

        # Convert (N,)-shape array to (N,1)-shape
        y = np.expand_dims(y, axis=1)

        # Use Sklearn's OnHotEncoder to convert
        # digits to one-hot encoding
        enc = preprocessing.OneHotEncoder()
        enc.fit(y)
        Y = enc.transform(y).toarray()

        # If only have 2 labels, return only
        # single output
        if Y.shape[1] == 2:
            Y = Y[:, 1:]

        return Y