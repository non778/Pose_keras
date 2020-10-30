import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
import os

label = -1
label_list = []
data_list = []

def make_numpy():
    global resultData
    global trainData

    trainData = np.array(data_list)
    resultData = np.array(label_list)

    print(trainData.shape)
    print(resultData.shape)

def read_file(path):
    global label
    global label_list
    global data_list

    with open(path) as json_file:
        json_data = json.load(json_file)

    label = json_data[-1]

    for idx in json_data[0:-1]:
        label_list.append(label)
        data_list.append(idx)

def learning():
    global model

    model = keras.models.Sequential([
        keras.layers.Flatten(input_shape=(1, 34)),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(4, activation='softmax'),
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(trainData, resultData, epochs=70)

def learn_save(path):
    global model

    model.save_weights("Action_model.h5")
    model_json = model.to_json()
    with open(path, "w") as json_file:
        json_file.write(model_json)

    print("Save Complete!")

def make_path(path):
    file_list = os.listdir(path)
    path_list = []
    
    for f in file_list:
        path_list.append(os.path.join(path, f))

    return path_list

paths = make_path("C:\\Users\\zmzmd\\Desktop\\test\\Train\\")
for f in paths:
    read_file(f)

make_numpy()
learning()
learn_save("C:\\Users\\zmzmd\\Desktop\\test\\model.json")