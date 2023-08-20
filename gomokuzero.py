import tensorflow as tf
import pandas as pd 
import numpy as np
from ast import literal_eval

data = pd.read_csv('data.csv', names=['state', 'outcome'], delimiter=';')
print(data.head())

data['state'] = data['state'].apply(lambda x: eval(x))

data_features = data
data_labels = data_features.pop('outcome')

data_features = np.array(data_features)
print(data_features[0:2])

model = tf.keras.Sequential([
  tf.keras.layers.Dense(169),
  tf.keras.layers.Dense(1)
])

model.compile(loss = tf.keras.losses.MeanSquaredError(), optimizer = tf.keras.optimizers.legacy.Adam())

model.fit(data_features, data_labels, epochs=10)