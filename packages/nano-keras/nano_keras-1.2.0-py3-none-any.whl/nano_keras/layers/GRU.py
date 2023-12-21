import numpy as np
from nano_keras.activations import Activation, ACTIVATIONS
from nano_keras.initializers import Initializer, INITIALIZERS
from nano_keras.layers import Layer, LayerWithParams
from nano_keras.optimizers import Optimizer
from nano_keras.regulizers import Regularizer


class GRU(LayerWithParams):
    def __init__(self, units: int, activation: Activation | str = "tanh", recurrent_actvation: Activation | str = "sigmoid", weight_initialization: Initializer | str = "random_normal", recurrent_weight_initialization: Initializer | str = "random_normal", bias_initalization: Initializer | str = "zeros", return_sequences: bool = True, regulizer: Regularizer = None, name: str = "GRU") -> None:
        self.units: int = units
        self.activation: Activation = activation if type(
            activation) == Activation else ACTIVATIONS[activation]
        self.recurrent_activation: Activation = recurrent_actvation if type(
            recurrent_actvation) == Activation else ACTIVATIONS[recurrent_actvation]

        self.weight_initialization: Initializer = weight_initialization if type(
            weight_initialization) == Initializer else INITIALIZERS[weight_initialization]
        self.recurrent_weight_initialization: Initializer = recurrent_weight_initialization if type(
            recurrent_weight_initialization) == Initializer else INITIALIZERS[recurrent_weight_initialization]
        self.bias_initialization: Initializer = bias_initalization if type(
            bias_initalization) == Initializer else INITIALIZERS[bias_initalization]

        self.return_sequences: bool = return_sequences
        self.regulizer: Regularizer = regulizer
        self.name: str = name

        self.hidden_state: np.ndarray = np.array([])

    def output_shape(self, layers: list[Layer], current_layer_index: int) -> tuple:
        input_shape = layers[current_layer_index -
                             1].output_shape(layers, current_layer_index-1)

        self.output_shape_value = (
            input_shape[0], self.units) if self.return_sequences else self.units

        return self.output_shape_value

    def __repr__(self) -> str:
        formatted_output = f"(None, {self.output_shape_value})"
        if type(self.output_shape_value) == tuple:
            formatted_output = f'(None, {", ".join(map(str, self.output_shape_value))})'

        return f"{self.name} (GRU){' ' * (28 - len(self.name) - 5)}{formatted_output}{' ' * (26 - len(formatted_output))}{self.input_weights.size + self.recurrent_weights.size + self.biases.size}\n"

    def generate_weights(self, layers: list[Layer], current_layer_index: int, weight_data_type: np.float_, bias_data_type: np.float_) -> None:
        input_shape = layers[current_layer_index -
                             1].output_shape(layers, current_layer_index-1)

        input_weights_shape = (input_shape[1], self.units)
        recurrent_weights_shape = (self.units, self.units)

        self.input_weights = np.random.randn(
            3, *input_weights_shape).astype(weight_data_type)
        self.recurrent_weights = np.random.randn(
            3, *recurrent_weights_shape).astype(weight_data_type)

        self.biases = np.random.randn(2, 3, self.units)

        self.hidden_state = np.zeros((input_shape[0], self.units))

        self.output_shape_value = (
            input_shape[0], self.units) if self.return_sequences else self.units

    def __call__(self, x: np.ndarray, is_training: bool = False) -> np.ndarray:
        if len(x.shape) != 2:
            raise ValueError(
                f"Input shape in GRU layer must be 2d, received: {x.shape}")

        self.inputs = x

        extra_dim = np.zeros((1, self.hidden_state.shape[1]))

        self.hidden_state = np.vstack((extra_dim, self.hidden_state))

        self.update_gate = np.ndarray((x.shape[0], self.units))
        self.reset_gate = np.ndarray((x.shape[0], self.units))
        self.current_memory_content = np.zeros((x.shape[0] + 1, self.units))

        for time_stamp in range(1, x.shape[0]+1):
            self.update_gate[time_stamp-1] = self.recurrent_activation.apply_activation(
                np.dot(self.input_weights[0].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[0],
                                                                          self.hidden_state[time_stamp-1]) + self.biases[0, 0] + self.biases[1, 0])

            self.reset_gate[time_stamp-1] = self.recurrent_activation.apply_activation(
                np.dot(self.input_weights[0].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[0],
                                                                          self.hidden_state[time_stamp-1]) + self.biases[0, 0] + self.biases[1, 0])

            self.current_memory_content[time_stamp] = self.activation.apply_activation(
                np.dot(self.input_weights[2].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[2],
                                                                          (self.hidden_state[time_stamp-1] * self.reset_gate[time_stamp-1])) + self.biases[0, 2] + self.biases[1, 2])

            self.hidden_state[time_stamp] = self.update_gate[time_stamp-1] * self.hidden_state[time_stamp - 1] + (
                1 - self.update_gate[time_stamp-1]) * self.current_memory_content[time_stamp]

        self.hidden_state = self.hidden_state[1:]
        self.current_memory_content = self.current_memory_content[1:]

        if self.return_sequences:
            return self.hidden_state

        return self.hidden_state[-1]

    def backpropagate(self, gradient: np.ndarray, optimizer: Optimizer | list[Optimizer]) -> np.ndarray:
        if self.regulizer:
            gradient = self.regulizer.update_gradient(
                gradient, self.weights, self.biases)

        if len(gradient.shape) == 1:
            gradient = np.tile(gradient, (self.inputs.shape[0], 1))

        update_gate_gradient = np.ndarray((gradient.shape[0], self.units))
        reset_gate_gradient = np.ndarray((gradient.shape[0], self.units))
        current_memory_content_gradient = np.ndarray(
            (gradient.shape[0], self.units))

        input_weights_gradient = np.ndarray(self.input_weights.shape)
        recurrent_weights_gradient = np.ndarray(
            self.recurrent_weights.shape)
        biases_gradient = np.ndarray(self.biases.shape)

        for time_stamp in range(gradient.shape[0]-1, -1, -1):
            update_gate_gradient[time_stamp] = gradient[time_stamp] * (
                self.current_memory_content[time_stamp] - self.hidden_state[time_stamp])

            current_memory_content_gradient[time_stamp] = gradient[time_stamp] * \
                self.update_gate[time_stamp]

            reset_gate_gradient[time_stamp] = gradient[time_stamp] * \
                self.hidden_state[time_stamp] * \
                self.current_memory_content[time_stamp]

            gate_gradients = [update_gate_gradient[time_stamp], reset_gate_gradient[time_stamp],
                              current_memory_content_gradient[time_stamp]]

            for i, gate_gradient in enumerate(gate_gradients):
                input_weights_gradient[i] += np.outer(
                    self.inputs[time_stamp], gate_gradient)

                recurrent_weights_gradient[i] += np.outer(
                    self.hidden_state[time_stamp-1], gate_gradient)

                biases_gradient[:, i] += gate_gradient[i]

        # Input weights and biases
        self.input_weights, self.biases[0] = optimizer[0].apply_gradients(
            input_weights_gradient, biases_gradient[0], self.input_weights, self.biases[0])

        self.recurrent_weights, self.biases[1] = optimizer[0].apply_gradients(
            recurrent_weights_gradient, biases_gradient[1], self.recurrent_weights, self.biases[1])

        return np.dot(update_gate_gradient, self.input_weights[0].T) + np.dot(reset_gate_gradient, self.input_weights[1].T) + np.dot(current_memory_content_gradient, self.input_weights[2].T)
