import os

import tensorflow as tf


def init_training(data_input_dir: str, model_output_dir: str):
    train_filename, test_filename = (
        f"{data_input_dir}/train.tfrecord",
        f"{data_input_dir}/test.tfrecord",
    )

    train = tf.data.TFRecordDataset(train_filename)
    test = tf.data.TFRecordDataset(test_filename)

    checkpoint_path = os.path.join(model_output_dir, "checkpoint/cp.ckpt")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path, save_weights_only=True, verbose=1
    )

    return train, test, cp_callback
