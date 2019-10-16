
# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

import numpy as np
import os
import re
import struct
import functools
import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf
import keras

import pickle

import aes_internals as aise
import dwdb_reader

def shuffle_batch(X, y, batch_size):
    rnd_idx = np.random.permutation(len(X))
    n_batches = len(X) // batch_size
    for batch_idx in np.array_split(rnd_idx, n_batches):
        X_batch, y_batch = X[batch_idx], y[batch_idx]
        yield X_batch, y_batch
        
print(tf.__version__)
print(keras.__version__)

RANDOM_SEED = 42

# Where to save the figures and get the traces
PROJECT_ROOT_DIR="/home/ubuntu/data/unmasked-8-bit-aes-olimex"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images")
os.makedirs(IMAGES_PATH, exist_ok=True)

LOG_DIR = os.path.join(PROJECT_ROOT_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)

DWDB_DIR = PROJECT_ROOT_DIR # os.path.join(PROJECT_ROOT_DIR, "dwdb")
DWDB_LOCATION = os.path.join(DWDB_DIR, "log.dwdb")

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

# Set these values for the particular dataset
strt_pt = 8848
stop_pt = 10768    

with open(DWDB_LOCATION) as file:
    content = file.readlines()
    
meta = []
for line in content:
    meta.append(dwdb_reader.parse_metadata_line(line))

print(meta[0])

i=0
X=[]
y=[]
while i < len(meta):
    X.append(dwdb_reader.read_trace(os.path.join(DWDB_DIR, meta[i]['filename']), start=strt_pt, stop=stop_pt))
    y.append(meta[i]['other'].strip('[]'))
    i=i+1

X_np = np.array(X, dtype=np.int32)

means = X_np.mean(axis=0, keepdims=True)
stds = X_np.std(axis=0, keepdims=True) + 1e-10
X_scaled = (X_np - means) / stds

X_test, X_valid, X_train = X_scaled[:5000], X_scaled[5000:10000], X_scaled[10000:]

print(X_train.shape)

# parameters
learning_rate = 0.001
alpha = 0.01
dropout_rate = 0.05
activation_type = "relu"
optimizer = "sgd"

model = keras.models.Sequential([
    keras.layers.Dropout(rate=dropout_rate, input_shape=X_train.shape[1:]),
    keras.layers.Dense(256, use_bias=False),
#    keras.layers.BatchNormalization(),
    keras.layers.Activation(activation_type),
    keras.layers.Dropout(rate=dropout_rate),
    keras.layers.Dense(256, use_bias=False),
#    keras.layers.BatchNormalization(),
    keras.layers.Activation(activation_type),
    keras.layers.Dropout(rate=dropout_rate),
    keras.layers.Dense(256, use_bias=False),
#    keras.layers.BatchNormalization(),
    keras.layers.Activation(activation_type),
    keras.layers.Dropout(rate=dropout_rate),
    keras.layers.Dense(2, activation="softmax")
])

def selection_function(p, k):
    myaes = aise.AES(k)
    allresults = myaes.encrypt(p)
    return (allresults['sbox1'][0] & 1)

key = 'FEDCBA98765432100123456789ABCDEF'
k = bytes.fromhex(key)

epochs=50

i=0
while (i<256):
    nk = bytes.fromhex("{:02X}".format(i) + key[2:32])
    sel=[]
    for plaintext in y:
        p = bytes.fromhex(plaintext)
        sel.append(selection_function(p, nk))

    y_np = np.array(sel, dtype=np.int32)
    y_test, y_valid, y_train = y_np[:5000], y_np[5000:10000], y_np[10000:]
    
    model.compile(loss="sparse_categorical_crossentropy",
              optimizer=optimizer,
              metrics=["accuracy"])

    model.build()
    
    history = model.fit(X_train, y_train, epochs=epochs,
                    validation_data=(X_valid, y_valid))
    
    FILE_OUT=os.path.join(LOG_DIR, "history."+format(i, '03d')+".p")
    pickle.dump(history.history, open(FILE_OUT, "wb"))

    i=i+1

