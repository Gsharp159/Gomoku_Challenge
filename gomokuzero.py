import gomoku as gm
import tensorflow as tf
from tensorflow import keras
import numpy as np

#[[1, 2, 3], [4, 5, 6]] = (2, 3)
#first value = number of datasets in batch, input shape is per each single set
test_features = np.zeros((5, 169))

#[3, 6] = (2)
#idek know why but 5 works because thats how many sets are in features
test_labels = np.ones((5, 169))

model = keras.Sequential([
    keras.layers.Dense(169, activation=tf.nn.relu, input_shape=(169,)),
    keras.layers.Dense(250, activation=tf.nn.relu),
    keras.layers.Dense(169)
])

#print(tf.nn.softmax((model(test_features))))


#LOSS


loss_object = tf.keras.losses.MeanSquaredError()

def loss(model, x, y, training):
  # training=training is needed only if there are layers with different
  # behavior during training versus inference (e.g. Dropout).
  y_ = model(x, training=training)

  return loss_object(y_true=y, y_pred=y_)

l = loss(model, test_features, test_labels, training=False)
print("Loss test: {}".format(l))


#GRADIENTS


def grad(model, inputs, targets):
  with tf.GradientTape() as tape:
    loss_value = loss(model, inputs, targets, training=True)
  return loss_value, tape.gradient(loss_value, model.trainable_variables)


#OPTIMIZER

optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

loss_value, grads = grad(model, test_features, test_labels)

print("Step: {}, Initial Loss: {}".format(optimizer.iterations.numpy(),
                                          loss_value.numpy()))

optimizer.apply_gradients(zip(grads, model.trainable_variables))

print("Step: {},         Loss: {}".format(optimizer.iterations.numpy(),
                                          loss(model, test_features, test_labels, training=True).numpy()))





for i in range (whatever):
    #play game of gomoku
    #if lose, do thing
    #update gradients
    #loop
    pass







#TRAINING LOOP


## Note: Rerunning this cell uses the same model parameters

'''
#Keep results for plotting
train_loss_results = []
train_accuracy_results = []

num_epochs = 201

for epoch in range(num_epochs):
  epoch_loss_avg = tf.keras.metrics.Mean()
  epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

  # Training loop - using batches of 32

  #x, y = features and labels
  for x, y in ds_train_batch:
    # Optimize the model
    loss_value, grads = grad(model, x, y)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))

    # Track progress
    epoch_loss_avg.update_state(loss_value)  # Add current batch loss
    # Compare predicted label to actual label
    # training=True is needed only if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    epoch_accuracy.update_state(y, model(x, training=True))

  # End epoch
  train_loss_results.append(epoch_loss_avg.result())
  train_accuracy_results.append(epoch_accuracy.result())

  if epoch % 50 == 0:
    print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                epoch_loss_avg.result(),
                                                                epoch_accuracy.result()))
'''
