"""Model class for a single layer CNN"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Embedding
from keras.layers import Flatten
from keras.layers import Input
from keras.layers import MaxPooling1D
from keras.layers import Activation
from keras.layers import Concatenate
from keras.models import Model
from keras_trainer import base_model
from keras_trainer.custom_metrics import auc_roc


class SingleLayerCnn(base_model.BaseModel):
  """Single Layer Based CNN

  hparams:
    embedding_dim
    vocab_size
    sequence_length
    dropout_rate
    train_embedding
  """

  def __init__(self, embeddings_matrix, hparams, labels):
    self.embeddings_matrix = embeddings_matrix
    self.hparams = hparams
    self.labels = labels
    self.num_labels = len(labels)

  def get_model(self) -> Model:
    I = Input(shape=(self.hparams.sequence_length,), dtype='float32')
    E = Embedding(
        self.hparams.vocab_size,
        self.hparams.embedding_dim,
        weights=[self.embeddings_matrix],
        input_length=self.hparams.sequence_length,
        trainable=self.hparams.train_embedding)(
            I)
    X5 = Conv1D(128, 5, activation='relu', padding='same')(E)
    X5 = MaxPooling1D(self.hparams.sequence_length, padding='same')(X5)
    X4 = Conv1D(128, 4, activation='relu', padding='same')(E)
    X4 = MaxPooling1D(self.hparams.sequence_length, padding='same')(X4)
    X3 = Conv1D(128, 3, activation='relu', padding='same')(E)
    X3 = MaxPooling1D(self.hparams.sequence_length, padding='same')(X3)
    X = Concatenate(axis=-1)([X5, X4, X3])
    X = Flatten()(X)
    X = Dropout(self.hparams.dropout_rate)(X)
    X = Dense(128, activation='relu')(X)
    X = Dropout(self.hparams.dropout_rate)(X)
    Output = Dense(self.num_labels, activation='sigmoid', name='outputs')(X)

    model = Model(inputs=I, outputs=Output)
    model.compile(
        optimizer='rmsprop',
        loss='binary_crossentropy',
        metrics=['accuracy', auc_roc])
    print(model.summary())
    return model
