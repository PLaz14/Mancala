import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

def testai():
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(10, activation="softmax"))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    model.fit(x_train, y_train, epochs=6)

    # plt.imshow(x_train[0], cmap = plt.cm.binary)
    # plt.show()
    # print(x_train[0])
    predictions = model.predict([x_train])
    print(np.argmax(predictions[0]))
    plt.imshow(x_train[0])
    plt.show()

if __name__ == "__main__":
    testai()