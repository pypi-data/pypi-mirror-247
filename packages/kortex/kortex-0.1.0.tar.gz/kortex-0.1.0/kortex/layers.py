import tensorflow as tf


class SpatialSoftargmax(tf.keras.layers.Layer):
    """Deep Spatial Autoencoders for Visuomotor Learning (Finn et al., 2015)"""

    def __init__(self):
        super(SpatialSoftargmax, self).__init__()

    def build(self, input_shape):
        _, height, width, channels = input_shape

        self.temperature = self.add_weight(name="temperature",
                                           shape=(),
                                           dtype=tf.float32,
                                           initializer=tf.keras.initializers.ones(),
                                           trainable=True)

        x_coords, y_coords = tf.meshgrid(
            tf.linspace(0., tf.cast(height - 1, tf.float32), num=height),
            tf.linspace(0., tf.cast(width - 1, tf.float32), num=width),
            indexing='ij')

        self.x_coords = tf.reshape(x_coords, [1, height * width, 1])
        self.y_coords = tf.reshape(y_coords, [1, height * width, 1])

        super(SpatialSoftargmax, self).build(input_shape)

    def call(self, x):
        input_shape = tf.shape(x)
        height = input_shape[1]
        width = input_shape[2]
        channels = input_shape[3]

        # add temperature coefficient
        x = x / self.temperature

        # Flatten the feature map
        flattened_map = tf.reshape(x, (-1, height * width, channels))

        # Apply softmax along the spatial dimensions
        softmax_map = tf.nn.softmax(flattened_map, axis=1)

        # Calculate the x-coordinate and y-coordinate separately
        x = tf.reduce_sum(softmax_map * self.x_coords, axis=1)
        y = tf.reduce_sum(softmax_map * self.y_coords, axis=1)

        # Normalize the coordinates to [0, 1]
        x /= tf.cast(width - 1, tf.float32)
        y /= tf.cast(height - 1, tf.float32)

        # Stack the x_y coordinates
        coordinates = tf.stack([x, y], axis=-1)
        coordinates = tf.reshape(coordinates, [-1, channels * 2])

        return coordinates

    # @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[3] * 2


if __name__ == '__main__':
    import numpy as np

    height, width, channels = 128, 128, 3
    data = np.zeros((2, height, width, channels), dtype=np.float32)  # batch size is 2
    true = [[], []]

    for i in range(2):
        for c in range(channels):
            x = np.random.randint(height)
            y = np.random.randint(width)

            data[i, x, y, c] = 100.
            true[i].append([x, y])

    true = np.array(true)
    pred = SpatialSoftargmax2()(data)

    # print
    print(true)
    print(tf.cast(pred * height, tf.int32))