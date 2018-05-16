"""Abstract Base Class for DatasetInput."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
from tf_trainer import types
from typing import Callable


class DatasetInput(abc.ABC):
  """Abstract Base Class for Dataset Input.

  Provides the input functions (referred to as input_fn in TF docs) to be used
  with Tensorflow Estimator's train, evaluate, and predict methods.
  """

  @abc.abstractmethod
  def train_input_fn(self) -> Callable[[], types.FeatureAndLabelTensors]:
    pass

  @abc.abstractmethod
  def validate_input_fn(self) -> Callable[[], types.FeatureAndLabelTensors]:
    pass
