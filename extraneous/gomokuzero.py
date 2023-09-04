import tensorflow as tf
import pandas as pd 
import numpy as np
from ast import literal_eval
#import keras_tuner as kt

data = pd.read_csv('data.csv')

#data['state'] = data['state'].apply(lambda x: eval(x))


print(data.head())

data_features = data
#data_labels = data_features.pop(data_features.columns[169:171])
data_labels = pd.concat([data_features.pop(data_features.columns[x]) for x in [-3, -2, -1]], axis=1)
data_features = np.array(data_features)

test_features = data_features[-100:-1]
test_labels = data_labels[-100:-1]

model_con = tf.keras.Sequential([
  #tf.keras.layers.Dense(169, activation=tf.nn.relu),
  tf.keras.layers.Reshape((13, 13, 1), input_shape=(169,)),
  tf.keras.layers.Conv2D(2, 5, input_shape=(13, 13, 1)),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(81, activation=tf.nn.relu),
  tf.keras.layers.Dense(250),
  tf.keras.layers.Dense(3)
])

model = tf.keras.Sequential([
  tf.keras.layers.Dense(169),
  tf.keras.layers.Dense(85, activation=tf.nn.relu),
  tf.keras.layers.Dense(42),
  tf.keras.layers.Dense(21, activation=tf.nn.relu),
  tf.keras.layers.Dense(3)
])

#earlystopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", mode="min", patience=5, restore_best_weights=True)

model.compile(loss = tf.keras.losses.CategoricalCrossentropy(), optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.0000025), metrics=['categorical_accuracy'])
model.fit(data_features, data_labels, epochs=10)
model.evaluate(test_features,  test_labels, verbose=2)


path = "/Users/gage/Documents/Code/Gomoku_Challenge/models/"
#model.save("models/nn_0.3.1")
#model.load_weights(path)

#latest = tf.train.latest_checkpoint(path)

#model.load_weights(latest)

#predictions = model(data_features[:1]).numpy()

#print(predictions)
#print(tf.nn.softmax(predictions).numpy())


#test = pd.DataFrame(pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
#test = np.array(pd.DataFrame([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).T)
#print(res := model(test).numpy())
#print(tf.nn.softmax(res).numpy())



#model.save(path)