from os import PathLike

import tensorflow as tf


def load_model(path_to_model: PathLike):
    return tf.saved_model.load(path_to_model)
