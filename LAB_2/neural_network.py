import numpy as np

NUM_NEURONS = 4

class NeuralNetwork():


    def __init__(self, inputs, layers, outputs):
        """Constructor de la clase
        Args:
            inputs (int): Número de entradas de la red neuronal.
            layers (int): Número de capas de la red neuronal, 
            No se incluyen la input/output layer, solo las hidden
            Cada capa tendra 8 neuronas.
            outputs (int): Número de outputs de la red neuronal.
        """
        self.num_inputs = inputs
        self.num_layers = layers
        self.num_outputs = outputs
        self.weights = []
        self.layer_nodes = []
        self.learning_rate = 0.1


    def build_layers(self):
        """Función que nos construye capas
        """
        # Capa oculta justo despues de la input
        self.weights.append(np.random.rand(self.num_inputs, NUM_NEURONS))

        # Capas ocultas
        for i in range(self.num_layers-1):
            self.weights.append(np.random.rand(NUM_NEURONS, NUM_NEURONS))

        # Capa oculta justo antes de la output
        self.weights.append(np.random.rand(NUM_NEURONS, self.num_outputs))

    
    def propagate(self, inputs):
        """Función para propagar valores en la red neuronal
        Args:
            inputs (int): Valores a propagar
        """
        self.layer_nodes.clear()

        # input->hidden layer
        layer = self.sigmoid(np.dot(inputs, self.weights[0]))
        self.layer_nodes.append(layer)

        # Hidden layers
        for i in range(self.num_layers-1):
            layer = self.sigmoid(np.dot(layer, self.weights[i+1]))
            self.layer_nodes.append(layer)
        
        # hidden->output layer
        output = self.sigmoid(np.dot(layer, self.weights[-1]))
        self.layer_nodes.append(output)
        return output


    def backpropagation(self, inputs, expected_output):
        """Función que corregira valores de los pesos
        Args:
            inputs (np.array): Input
            expected_output (np.array): Output esperada
        """
        # Calculating the error
        layer_error = self.layer_nodes[-1] - expected_output 
        layer = self.layer_nodes[-1]

        i = -1
        while i > -self.num_layers-2:
            # Calculating the gradient
            layer_delta = layer_error\
                        * self.sigmoid_derivative(layer)

            # Calculating the error of the previous layer
            layer_error = np.dot(layer_delta, self.weights[i].T)

            # Weights update
            layer = self.layer_nodes[i-1] if len(self.layer_nodes) >= (i-1)*-1 else inputs
            weight_update = np.dot(layer.T, layer_delta)
            self.weights[i] = self.weights[i] - self.learning_rate * weight_update
            i-=1
            

    def sigmoid(self, value):
        """Función para calcular el sigmoide de un valor
        Args:
            value (float/int): Valor a calcular
        Returns:
            float: Valor de la función
        """
        return 1 / (1 + np.exp(-value))


    def sigmoid_derivative(self, value):
        """Función para calcular la derivada de la sigmoide
        de un valor
        Args:
            value (int/float): Valor a calcular
        Returns:
            float: Valor
        """
        return value * (1 - value)


"""# MAIN DE PRUEBA
n = NeuralNetwork(5, 1, 2)
n.build_layers()
set_ = {'inputs': [], 'outputs': []}
set_['inputs'].append([[1,1,0,0,0]])
set_['outputs'].append([[0]])
set_['inputs'].append([[1,1,0,0,1]])
set_['outputs'].append([[0]])
set_['inputs'].append([[1,1,0,1,0]])
set_['outputs'].append([[1,0]])
set_['inputs'].append([[1,1,0,1,1]])
set_['outputs'].append([[1,1]])
set_['inputs'].append([[1,1,1,0,0]])
set_['outputs'].append([[1,0]])
set_['inputs'].append([[1,1,1,0,1]])
set_['outputs'].append([[1,1]])
set_['inputs'].append([[1,1,1,1,0]])
set_['outputs'].append([[1,0]])
set_['inputs'].append([[1,1,1,1,1]])
set_['outputs'].append([[1,1]])
for i in range(100):
    for k in range(8):
        output = n.propagate(np.array(set_['inputs'][k]))
        n.backpropagation(np.array(set_['inputs'][k]), np.array(set_['outputs'][k]))
print(n.propagate([[1,1,0,0,0]]))
print(n.propagate([[1,1,0,1,0]]))
print(n.propagate([[1,1,0,1,1]]))
print(n.propagate([[1,1,1,0,0]]))
print(n.propagate([[1,1,1,0,1]]))
print(n.propagate([[1,1,1,1,1]]))
"""