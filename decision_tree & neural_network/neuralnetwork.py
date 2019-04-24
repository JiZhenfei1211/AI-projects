import numpy as np
from numpy import argmax
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder


class NeuralNetwork:

    def __init__(self):
        self.label_encoder = LabelEncoder()
        dataset, self.labels = load_data('iris.data.txt')
        self.m = len(dataset)  # number of input examples
        self.n_x = len(dataset[0])   # number of features in one input example
        self.n_1 = len(set(self.labels))  # number of units in layer 1
        self.n_2 = len(set(self.labels))  # number of units in layer 2
        self.X = np.mat(dataset).T  # input examples
        self.Y = self.one_hot_encode(self.labels)  # oneHotEncoded real Y w.r.t X
        # initialize parameters
        self.W_1 = np.random.rand(self.n_1, self.n_x) * 0.01
        self.b_1 = np.zeros((self.n_1, 1))
        self.W_2 = np.random.rand(self.n_2, self.n_1) * 0.01
        self.b_2 = np.zeros((self.n_2, 1))
        self.alpha = 0.05  # learning rate

    def one_hot_encode(self, labels):
        self.label_encoder.fit(labels)
        encoded_Y = self.label_encoder.transform(labels)
        onehot_encoder = OneHotEncoder(sparse=False, categories='auto')
        encoded_Y = encoded_Y.reshape(len(encoded_Y), 1)
        onehot_encoded = onehot_encoder.fit_transform(encoded_Y)
        return onehot_encoded

    def learning(self):
        for i in range(1000):
            # forward propagation
            Z_1 = np.dot(self.W_1, self.X) + self.b_1
            A_1 = self.ReLU_activation_function(Z_1)
            Z_2 = np.dot(self.W_2, A_1) + self.b_2
            A_2 = self.Softmax_activation_function(Z_2)
            y = self.Y.argmax(axis=1).reshape(150, 1)
            # L = np.sum(-np.log(A_2[range(self.n_2), y])) / self.m
            L = np.sum(- np.dot(self.Y, np.log(A_2))) / self.m
            # print(L)
            # backward propagation
            dZ_2 = np.exp(Z_2) / (self.m * np.sum(np.exp(Z_2), axis=0))
            dZ_2[y, range(self.m)] -= (1.0 / self.m)
            Z_1_copy = Z_1.copy()
            Z_1_copy[Z_1_copy <= 0] = 0
            Z_1_copy[Z_1_copy > 0] = 1
            dZ_1 = np.multiply(np.dot(self.W_2.T, dZ_2), Z_1_copy)
            dW_2 = np.dot(dZ_2, A_1.T) / self.m
            db_2 = np.sum(dZ_2, axis=1) / self.m
            dW_1 = np.dot(dZ_1, self.X.T) / self.m
            db_1 = np.sum(dZ_1, axis=1) / self.m

            self.W_2 = self.W_2 - self.alpha * dW_2
            self.W_1 = self.W_1 - self.alpha * dW_1
            self.b_2 = self.b_2 - self.alpha * db_2
            self.b_1 = self.b_1 - self.alpha * db_1

    def loss_function(self, Y_pred):
        return - np.dot(self.Y, np.log(Y_pred))

    def ReLU_activation_function(self, Z):
        return np.maximum(0, Z)

    def Softmax_activation_function(self, Z):
        shift_Z = Z - np.max(Z)
        exps = np.exp(shift_Z)
        return exps / np.sum(exps, axis=0)

    def predict(self, test_input):
        test_input.reshape(self.n_x, 1)
        Z_1 = np.dot(self.W_1, test_input) + self.b_1
        A_1 = self.ReLU_activation_function(Z_1)
        Z_2 = np.dot(self.W_2, A_1) + self.b_2
        A_2 = self.Softmax_activation_function(Z_2)
        inverted = self.label_encoder.inverse_transform([argmax(A_2[0, :])])
        return inverted


def load_data(file_name):
    result = []
    labels = []
    with open(file_name, mode='r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) != 0:
                data = line.split(',')
                feature_data = list(map(float, data[:-1]))
                label = data[-1:][0]
                result.append(feature_data)
                labels.append(label)
    return result, labels


test = np.array([6.3, 3.3, 6.0, 2.5]).reshape(4, 1)
nn = NeuralNetwork()
nn.learning()
print(nn.predict(test))

