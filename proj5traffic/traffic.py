import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images, labels = [], []
    for i in range(NUM_CATEGORIES):
        directory = os.path.join(data_dir, str(i))
        for fil in os.listdir(directory):
            imagepath = os.path.join(directory, fil)
            image = cv2.imread(imagepath)
            images.append(cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT)))
            labels.append(i)

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    return get_final_model()

def get_example_model():
    """
    Color: RGB
    Convolution: 1 layer, 32 filters, (3x3) window
    Pooling: 1 layer max-pool (2x2)
    Dropout: 1 layer (.5)
    
    Layer description:
    - Convolution
    - MaxPooling
    - Flatten
    - Dense hidden layer with relu activation (32)
    - Dropout
    - Output layer with softmax activation

    Compile description:
    - optimizer: adam
    - loss: categorical_crossentropy
    - metrics: accuracy

    Performance w/ NUM_CATEGORIES = 10, EPOCHS = 10
    - 
    """
    
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        input_shape=( IMG_HEIGHT, IMG_WIDTH, 3)
    ))
    model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2)
    ))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    model.compile(
        optimizer = "adam",
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )
    return model
    
def get_model_0():
    """
    Color: RGB
    Convolution: None
    Pooling: None
    Dropout: None
    
    Layer description:
    - Dense hidden layer with relu activation (32)
    - Flatten
    - Output layer with sigmoid activation

    Compile description:
    - optimizer: adam
    - loss: categorical_crossentropy
    - metrics: accuracy

    Performance w/ NUM_CATEGORIES = 10, EPOCHS = 10
    - loss: 2.0077
    - accuracy: 0.7720
    """
    
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(
        32,
        input_shape =(IMG_HEIGHT, IMG_WIDTH, 3),
        activation = "relu")
    )
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid"))
    
    model.compile(
        optimizer = "adam",
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )
    
    return model

def get_model_1():
    """
    Color: RGB
    Convolution: None
    Pooling: None
    Dropout: None
    
    Layer description:
    - Dense hidden layer with relu activation (32)
    - Flatten
    - Output layer with softmax activation

    Compile description:
    - optimizer: adam
    - loss: categorical_crossentropy
    - metrics: accuracy

    Performance w/ NUM_CATEGORIES = 10, EPOCHS = 10
    - loss: 1.2170
    - accuracy: 0.8558
    """
    
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(
        32,
        input_shape =(IMG_HEIGHT, IMG_WIDTH, 3),
        activation = "relu")
    )
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    model.compile(
        optimizer = "adam",
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )
    return model

def get_model_2():
    """
    Color: RGB
    Convolution: None
    Pooling: None
    Dropout: None
    
    Layer description:
    - Flatten
    - Dense hidden layer with relu activation 
    - Output layer with softmax activation

    Compile description:
    - optimizer: adam
    - loss: categorical_crossentropy
    - metrics: accuracy

    Performance w/ NUM_CATEGORIES = 10, EPOCHS = 10
    - loss: 1.2170
    - accuracy: 0.8558
    """
    
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(tf.keras.layers.Dense(IMG_HEIGHT*32, activation = "relu")
    )

    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    model.compile(
        optimizer = "adam",
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )
    return model

def get_model_3():
    """
    Color: RGB
    Convolution: 1 Layer
    Pooling: None
    Dropout: None
    
    Layer description:
    - Convolution 2D 
    - Flatten
    - Dense hidden layer with relu activation 
    - Output layer with softmax activation

    Compile description:
    - optimizer: adam
    - loss: categorical_crossentropy
    - metrics: accuracy

    Performance w/ NUM_CATEGORIES = 10, EPOCHS = 10
    - loss: 0.7924
    - accuracy: 0.8914
    """
    
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(
        128,
        activation = "relu"
    ))

    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    model.compile(
        optimizer = "adam",
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )
    return model

def get_final_model():
    """
    Color: RGB
    Convolution: 2 layers, 32 filters, (3x3) window
    Pooling: 1 layer max-pool (2x2)
    Dropout: 1 layer (.5)
    
    Layer description:
    - Convolution
    - MaxPooling
    - Flatten
    - Dense hidden layer with relu activation (32)
    - Dropout
    - Output layer with softmax activation

    Compile description:
    - optimizer: adam
    - loss: categorical_crossentropy
    - metrics: accuracy

    Performance w/ NUM_CATEGORIES = 10, EPOCHS = 10
    - 
    """
    
    model = tf.keras.models.Sequential()
    
    # add convolutional layer
    model.add(tf.keras.layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    ))
    
    # add maxpooling layer
    model.add(tf.keras.layers.MaxPooling2D(
        pool_size=(3, 3)
    ))

    # Flatten
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dropout(0.25))

    # Add hidden layer with dropout
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES * 16, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.2))

    # Add hidden layer
    #model.add(tf.keras.layers.Dense(NUM_CATEGORIES * 16, activation="relu"))

    model.add(tf.keras.layers.Dense(NUM_CATEGORIES * 8, activation="relu"))
    
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    model.compile(
        optimizer = "adam",
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )

    return model
    

if __name__ == "__main__":
    main()
