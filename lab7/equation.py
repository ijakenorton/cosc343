import numpy as np
import matplotlib .pyplot as plt

    
def learn():
    X = np.array([[-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]).astype('float32')
    y = np.array([0,
                0,
                0,
                1]).astype('uint8')
    N, D = np.shape(X)
    K = 1
    Y = np.expand_dims(y, axis=1)
    max_iter = 100
    learning_rate = 0.1
    W = np.random.randn(D, K)
    b = np.random.randn(K)
    for i in range(0, max_iter):
        y_hat = (np.dot(X, W) + b)
        y_hat[y_hat <= 0] = 0
        y_hat[y_hat > 0] = 1
        E = Y - y_hat
        delta_W = np.dot(X.T, E)
        delta_b = np.sum(E, axis=0)
        W = W + ((learning_rate/N) * delta_W)
        b = b + ((learning_rate/N) * delta_b)
        error = np.sum(E != 0)
        print(error)
        if error == 0:
            print("finished")
            break

    plt.scatter(X[:3 ,0] ,X[:3 ,1] ,c='red')
    plt.scatter(X[3,0],X[3,1],c='blue')
    plt.xlabel('x 1 ')
    plt.ylabel('x 2 ')
    plt.show ()
learn()
