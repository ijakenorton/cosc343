__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"


import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import time

fh_glbl = None
ph_glbl = None
hh_glbl = []

def load_and():
   """ Loads the AND dataset of 4 samples

   :return: (X,y) - a 2x4 data matrix and corresponding 4-dim vector of labels
   """
   X = np.array([[-1, -1],
                 [-1, 1],
                 [1, -1],
                 [1, 1]]).astype('float32')
   y = np.array([0,
                 0,
                 0,
                 1]).astype('uint8')

   return X, y


def load_xor():
   """ Loads the XOR dataset of 4 samples

   :return: (X,y) - a 2x4 data matrix and corresponding 4-dim vector of labels
   """
   X = np.array([[-1, -1],
                 [-1, 1],
                 [1, -1],
                 [1, 1]]).astype('float32')
   y = np.array([0,
                 1,
                 1,
                 0]).astype('uint8')

   return X, y


def load_iris(ver2D=False):
   """ Loads the iris dataset of 4 samples.

   :param ver2D: a boolean, if True loads the D=2 attribute
                 version of the dataset, otherwise loads
                 the D=4 attribute version
   :return: (X,y) - a 150xD data matrix and corresponding 150-dim vector of labels
   """

   # Load the dataset from sklearn
   iris = datasets.load_iris()
   X = iris.data

   if ver2D:
      # If 2D mode requested use PCA to cast
      # data from 4D to 2D
      from sklearn.decomposition import PCA
      X = PCA(n_components=2, random_state=0).fit_transform(X)

   y = iris.target.astype('uint8')

   return X, y


def load_iris2D():
   """ Loads the 2D version of iris dataset.

   :return: (X,y) - a 150x2 data matrix and corresponding 150-dim vector of labels
   """
   return load_iris(ver2D=True)


def load_digits():
   """ Loads the Sklearn's digits dataset of 8x8 grayscale images
       of digits.

   :return: (X,y) - a Nx64 data matrix and corresponding N-dim vector of labels
   """

   digits = datasets.load_digits()

   X = digits.data
   y = digits.target

   return X, y


def load_reg1dataset():
   # Define a uniformly spaced set of x values (n in total)
   n = 150
   x = np.linspace(-5, 5, n)

   w1_true = 0.7;
   w2_true = -2;
   w3_true = 1;
   w4_true = 0.8;  # True parameters of the function
   y = w1_true * np.cos(w2_true * x) + w3_true * np.sin(w4_true * x)

   rnd = np.random.RandomState(3)

   # add some Gaussian noise to each value of the true output
   y += rnd.randn(len(y)) * 0.1
   I = rnd.permutation(len(x))
   x = x[I]
   y = y[I]

   x /= 2.5*2
   X = np.expand_dims(x, axis=1)
   y = np.expand_dims(y, axis=1)

   return (X,y)

def load_spiral():

   N = 120

   X = np.zeros((N, 2))
   y = np.zeros((N)).astype('int64')

   for i in range(0, int(N / 2)):
      delta = np.pi / 8 + i * 0.2
      r = 2 * delta + 0.1
      X[i, 0] = r * np.sin(delta)
      X[i, 1] = r * np.cos(delta)
      y[i] = 0

   for i in range(0, int(N / 2)):
      delta = np.pi / 8 + i * 0.2
      r = -2 * delta - 0.1
      X[i + int(N / 2), 0] = r * np.sin(delta)
      X[i + int(N / 2), 1] = r * np.cos(delta)
      y[i + int(N / 2)] = 1

   X -= np.min(X)
   X /= np.max(X)

   return X,y

def load_mnist():
    import tensorflow as tf

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    X = np.concatenate((x_train, x_test),axis=0)
    y = np.concatenate((y_train, y_test), axis=0)
    return X, y

def load_california():
   california = datasets.fetch_california_housing()

   X = california.data
   y = california.target

   return X,y


def load_diabetes():
   diabetis = datasets.load_diabetes()

   X = diabetis.data
   y = diabetis.target

   return X,y

def load_bcancer():
   bcancer = datasets.load_breast_cancer()


   X = bcancer.data
   y = bcancer.target

   return X,y

def load_fashion_mnist():
    import tensorflow as tf

    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()

    X = np.concatenate((train_images, test_images),axis=0)
    y = np.concatenate((train_labels, test_labels), axis=0)

    return X, y

def load_olivetti():
   olivetti = datasets.fetch_olivetti_faces()
   X = olivetti.data
   y = olivetti.target

   return X,y


def load_cifar10():
    import tensorflow as tf

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    X = np.concatenate((x_train, x_test),axis=0)
    y = np.concatenate((y_train, y_test), axis=0)
    return X, y

def plot_function(model, X, y, titleStr=None, blocking = True):

    global fh_glbl, ph_glbl, hh_glbl

    N, D = X.shape

    if D != 1:
        raise RuntimeError("Cannot plot funciton on %d-dimensional input." % D)


    xmin = np.min(X)
    xmax = np.max(X)
    xtest = np.linspace(xmin, xmax, 200)
    Xtest = np.expand_dims(xtest, axis=1)
    yhat = model.predict(Xtest)

    if fh_glbl is None:
        fh_glbl = plt.figure()
        ph_glbl = fh_glbl.add_subplot(1, 1, 1)

        ph_glbl.set_xlabel('x')
        ph_glbl.set_ylabel('y')

        h = ph_glbl.scatter(X, y, c='b')

    for h in hh_glbl:
        h.remove()

    hh_glbl = []


    h = ph_glbl.plot(xtest, yhat, c='r')
    hh_glbl.append(h[0])

    if titleStr is not None:
        plt.title(titleStr)

    if not blocking:
        plt.ion()
        plt.show()

        plt.pause(0.01)
        time.sleep(0.01)
    else:
        plt.ioff()
        plt.show()

    plt.show()


def plot_classified_regions(model, X, y, titleStr=None, blocking = True):
     """
     Plots classification regions for 2-attribute input

     :param X: numpy array
         Data points to plot

     :param y: numpy array
         Labels of the datapoint to plot

     :param titleStr: string
         The string to put as the title of the matplotlib plot

     """
     global fh_glbl, ph_glbl, hh_glbl


     N, D = X.shape
     class_labels = np.unique(y)
     K = len(class_labels)

     if K==2:
        K = 1

     if D != 2:
         raise RuntimeError("Cannot visualise classification regions on %d-dimensional input." % D)

     if fh_glbl is None:
         fh_glbl = plt.figure()
         ph_glbl = fh_glbl.add_subplot(1,1,1)

         ph_glbl.set_xlabel('x_1')
         ph_glbl.set_ylabel('x_2')

     xmins = np.min(X, axis=0)
     xmaxs = np.max(X, axis=0)

     xrange = xmaxs - xmins

     xmins -= xrange * 0.2
     xmaxs += xrange * 0.2

     F = 500
     xrange1 = np.linspace(xmins[0], xmaxs[0], F)
     xrange2 = np.linspace(xmins[1], xmaxs[1], F)

     x1, x2 = np.meshgrid(xrange1, xrange2)

     x = np.concatenate([np.reshape(x1, (-1, 1)), np.reshape(x2, (-1, 1))], axis=1)

     yhat = model.predict(x)

     yc = np.zeros((len(x), 3)).astype('uint8')
     if K == 1:
         #yhat = yhat[:, 0]
         yc[yhat == 0, :] = [255, 255, 255]
         yc[yhat == 1, :] = [0, 0, 255]
     elif K == 3:
         yc[yhat == class_labels[0], :] = [255, 0, 0]
         yc[yhat == class_labels[1], :] = [0, 255, 0]
         yc[yhat == class_labels[2], :] = [0, 0, 255]
     else:
         return

     w, h = np.shape(x1)
     yc = np.reshape(yc, (w, h, 3))
     yc = yc[::-1, :, :]

     for h in hh_glbl:
         h.remove()

     hh_glbl = []

     h = ph_glbl.imshow(yc, alpha=0.5)
     hh_glbl.append(h)

     for i in range(len(X)):
         x = X[i]
         x0 = np.argmin(np.abs(xrange1-x[0]))
         x1 = np.argmin(np.abs(xrange2[::-1]-x[1]))

         if K == 1:
             if y[i] == class_labels[0]:
                 c = 'r'
             else:
                 c = 'b'
         elif K==3:
             if y[i] == class_labels[0]:
                 c = 'r'
             elif y[i] == class_labels[1]:
                 c = 'g'
             else:
                 c = 'b'

         h = plt.scatter(x0, x1, c=c, s=20)
         hh_glbl.append(h)

     ph_glbl.set_xticks([])
     ph_glbl.set_yticks([])

     if titleStr is not None:
         plt.title(titleStr)

     if not blocking:
        plt.ion()
        plt.show()

        plt.pause(0.01)
        time.sleep(0.01)
     else:
         plt.ioff()
         plt.show()

def sizeStr(x):
   if not isinstance(x, np.ndarray):
      raise RuntimeError("This method works only for Numpy arrays")

   bytes = x.nbytes
   if bytes > 1024*1024:
      return "%.2fMB" % (bytes/(1024*1024))
   elif bytes > 1024:
      return "%.2fKB" % (bytes/(1024))
   else:
      return "%.2fB" % bytes

def plot_images(X,imsize, X2=None,imsize2=None):

        N1 = len(X)

        if len(imsize)==2:
           im_height1, im_width1 = imsize
           colours1 = 1
        elif len (imsize)==3:
           im_height1, im_width1, colours1 = imsize
        else:
           raise RuntimeError("imsize must be a (H,W) or (HxWxC) tuple, and X must be a corresponding Nx(H*W) or Nx(H*W*C) Numpy array")

        if X2 is None:
           N2 = 0
        else:
           N2 = len(X2)

           if len(imsize2) == 2:
               im_height2, im_width2 = imsize2
               colours2 = 1
           elif len(imsize2) == 3:
              im_height2, im_width2, colours2 = imsize2
           else:
               raise RuntimeError(
                   "imsize2 must be a (H,W) or (HxWxC) tuple, and X2 must be a corresponding Nx(H*W) or Nx(H*W*C) Numpy array")

        # Create a new (empty) figure
        fh = plt.figure(figsize=(10, 8))
        plt.ion()
        plt.show()

        R1 = int(np.floor(np.sqrt(N1)))
        C1 = int(np.ceil(N1 / R1))

        if N2!=0:
           R2 = int(np.floor(np.sqrt(N2)))
           C2 = int(np.ceil(N2 / R2))

        n = 0
        for r in range(R1):
            for c in range(C1):
                if n >= N1:
                    continue

                im = X[n, :].reshape(im_height1, im_width1, colours1)
                if N2==0:
                   ph = fh.add_subplot(R1, C1, n+1)
                else:
                   ph = fh.add_subplot(R1, C1+C2, n//(C1)*(C1+C2)+n%C1+1)
                n += 1


                if colours1 == 1:
                   ph.imshow(im[:,:,0], cmap='gray')
                else:
                   ph.imshow(im)
                ph.xaxis.set_visible(False)
                ph.yaxis.set_visible(False)

                plt.pause(0.01)
                time.sleep(0.01)


            if n >= N1:
                break

        if N2>0:
           n = 0
           for r in range(R2):
              for c in range(C2):
                 if n >= N2:
                    continue

                 im = X2[n, :].reshape(im_height2, im_width2, colours2)
                 ph = fh.add_subplot(R2, C1 + C2, n // (C2) * (C1 + C2) + n % C2 + 1 + C1)
                 n += 1

                 if colours2 == 1:
                    ph.imshow(im[:, :, 0], cmap='gray')
                 else:
                    ph.imshow(im)
                 ph.xaxis.set_visible(False)
                 ph.yaxis.set_visible(False)

                 plt.pause(0.01)
                 time.sleep(0.01)

              if n >= N2:
                 break


        #plt.ioff()
        #plt.show()