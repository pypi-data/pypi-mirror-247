import numpy as np
from nano_keras.layers import Layer, LayerWithParams
from nano_keras.activations import Activation, ACTIVATIONS
from nano_keras.optimizers import Optimizer
from nano_keras.regulizers import Regularizer
from nano_keras.initializers import Initializer, INITIALIZERS


class LSTM(LayerWithParams):
    def __init__(self, units: int, activation: Activation | str = "sigmoid", recurrent_activation: Activation | str = "tanh", weight_initalization: Initializer | str = "random_normal", recurrent_weight_initalization: Initializer | str = "random_normal", bias_initalization: Initializer | str = "zeros", return_sequences: bool = True, regulizer: Regularizer = None, name: str = "LSTM") -> None:
        self.units: int = units
        self.activation: Activation = activation if type(
            activation) == Activation else ACTIVATIONS[activation]
        self.recurrent_activation: Activation = recurrent_activation if type(
            recurrent_activation) == Activation else ACTIVATIONS[recurrent_activation]

        self.weight_initialization: Initializer = weight_initalization if type(
            weight_initalization) == Initializer else INITIALIZERS[weight_initalization]
        self.recurrent_weight_initalization: Initializer = recurrent_weight_initalization if type(
            recurrent_weight_initalization) == Initializer else INITIALIZERS[recurrent_weight_initalization]
        self.bias_initialization: Initializer = bias_initalization if type(
            bias_initalization) == Initializer else INITIALIZERS[bias_initalization]

        self.return_sequences: bool = return_sequences
        self.regulizer: Regularizer = regulizer
        self.name: str = name

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

        return f"{self.name} (LSTM){' ' * (28 - len(self.name) - 6)}{formatted_output}{' ' * (26 - len(formatted_output))}{self.input_weights.size + self.recurrent_weights.size + self.biases.size}\n"

    def generate_weights(self, layers: list[Layer], current_layer_index: int, weight_data_type: np.float_, bias_data_type: np.float_) -> None:
        input_shape = layers[current_layer_index -
                             1].output_shape(layers, current_layer_index-1)

        input_weights_shape = (input_shape[1], self.units)
        recurrent_weights_shape = (self.units, self.units)

        self.input_weights = np.random.randn(
            4, *input_weights_shape).astype(weight_data_type)
        self.recurrent_weights = np.random.randn(
            4, *recurrent_weights_shape).astype(weight_data_type)

        self.biases = np.random.randn(4, self.units)

        self.hidden_state = np.zeros((input_shape[0], self.units))
        self.cell_state = np.zeros((input_shape[0], self.units))

        self.output_shape_value = (
            input_shape[0], self.units) if self.return_sequences else self.units
        return

    def __call__(self, x: np.ndarray, is_training: bool = False) -> np.ndarray:
        self.inputs = x

        if len(x.shape) != 2:
            raise ValueError(
                f"Input shape in LSTM layer must be 2d, received: {x.shape}")

        extra_dim = np.zeros((1, self.hidden_state.shape[1]))

        self.hidden_state = np.vstack((extra_dim, self.hidden_state))
        self.cell_state = np.vstack((extra_dim, self.cell_state))

        self.forget_gate = np.ndarray((x.shape[0], self.units))
        self.input_gate = np.ndarray((x.shape[0], self.units))
        self.candidate_cell_state = np.zeros((x.shape[0] + 1, self.units))
        self.output_gate = np.ndarray((x.shape[0], self.units))

        for time_stamp in range(1, x.shape[0]+1):
            # Note that we are using [time_stamp - 1] in most cases as otherwise we'd get an index of -1 at the first iteration
            # And for elements like hidden state and cell state we assign it to the current timestamp and the remove the first element

            # fₜ = σ(Wᵢ₁xₜ + Wᵣ₁hₜ₋₁ + b₁)
            self.forget_gate[time_stamp-1] = self.activation.apply_activation(
                np.dot(self.input_weights[0].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[0], self.hidden_state[time_stamp-1]) + self.biases[0])

            # iₜ = σ(Wᵢ₂xₜ + Wᵣ₂hₜ₋₁ + b₂)
            self.input_gate[time_stamp-1] = self.activation.apply_activation(np.dot(
                self.input_weights[1].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[1], self.hidden_state[time_stamp-1]) + self.biases[1])

            # C'ₜ = tanh(Wᵢ₃xₜ + Wᵣ₃hₜ₋₁ + b₃)
            self.candidate_cell_state[time_stamp] = self.recurrent_activation.apply_activation(np.dot(
                self.input_weights[2].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[2], self.hidden_state[time_stamp-1]) + self.biases[2])

            # Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C'ₜ₋₁
            self.cell_state[time_stamp] = self.forget_gate[time_stamp-1] * self.cell_state[time_stamp-1] + \
                self.input_gate[time_stamp-1] * \
                self.candidate_cell_state[time_stamp-1]

            # oₜ = σ(Wᵢ₄xₜ + Wᵣ₄hₜ₋₁ + b₄)
            self.output_gate[time_stamp-1] = self.activation.apply_activation(np.dot(
                self.input_weights[3].T, x[time_stamp-1]) + np.dot(self.recurrent_weights[3], self.hidden_state[time_stamp-1]) + self.biases[3])

            # hₜ = oₜ ⊙ tanh(Cₜ)
            self.hidden_state[time_stamp] = self.output_gate[time_stamp-1] * \
                self.recurrent_activation.apply_activation(
                    self.cell_state[time_stamp])

        self.hidden_state = self.hidden_state[1:]
        self.cell_state = self.cell_state[1:]
        self.candidate_cell_state = self.candidate_cell_state[1:]

        if self.return_sequences:
            return self.hidden_state

        return self.hidden_state[-1]

    def backpropagate(self, gradient: np.ndarray, optimizer: Optimizer | list[Optimizer]) -> np.ndarray:
        if self.regulizer:
            gradient = self.regulizer.update_gradient(
                gradient, self.weights, self.biases)

        if len(gradient.shape) == 1:
            gradient = np.tile(gradient, (self.inputs.shape[0], 1))

        forget_gate_gradient = np.ndarray((gradient.shape[0], self.units))
        input_gate_gradient = np.ndarray((gradient.shape[0], self.units))
        candidate_cell_state_gradient = np.ndarray(
            (gradient.shape[0], self.units))
        output_gate_gradient = np.ndarray((gradient.shape[0], self.units))

        input_weights_gradient = np.ndarray(self.input_weights.shape)
        recurrent_weights_gradient = np.ndarray(
            self.recurrent_weights.shape)
        biases_gradient = np.ndarray(self.biases.shape)

        for time_stamp in range(gradient.shape[0]-1, -1, -1):
            output_gate_gradient[time_stamp] = gradient[time_stamp] * \
                self.recurrent_activation.apply_activation(
                    self.cell_state[time_stamp])

            forget_gate_gradient[time_stamp] = gradient[time_stamp] * \
                self.cell_state[time_stamp] * \
                self.forget_gate[time_stamp] * \
                (1 - self.forget_gate[time_stamp])

            input_gate_gradient[time_stamp] = gradient[time_stamp] * \
                self.candidate_cell_state[time_stamp] * \
                self.input_gate[time_stamp] * (1 - self.input_gate[time_stamp])

            candidate_cell_state_gradient[time_stamp] = gradient[time_stamp] * \
                self.input_gate[time_stamp] * \
                self.recurrent_activation.apply_activation(
                    self.candidate_cell_state[time_stamp]) * (1 - self.candidate_cell_state[time_stamp]**2)

            gate_gradients = [forget_gate_gradient[time_stamp], input_gate_gradient[time_stamp],
                              candidate_cell_state_gradient[time_stamp], output_gate_gradient[time_stamp]]

            for i, gate_gradient in enumerate(gate_gradients):
                input_weights_gradient[i] += np.outer(
                    self.inputs[time_stamp], gate_gradient)

                recurrent_weights_gradient[i] += np.outer(
                    self.hidden_state[time_stamp-1], gate_gradient)

                biases_gradient[i] += gate_gradient[i]

        self.input_weights, self.biases = optimizer[0].apply_gradients(
            input_weights_gradient, biases_gradient, self.input_weights, self.biases)
        self.recurrent_weights, _ = optimizer[0].apply_gradients(
            recurrent_weights_gradient, [], self.recurrent_weights, [], False)

        return np.dot(forget_gate_gradient, self.input_weights[0].T) + np.dot(input_gate_gradient, self.input_weights[1].T) + np.dot(candidate_cell_state_gradient, self.input_weights[2].T) + np.dot(output_gate_gradient, self.input_weights[3].T)
