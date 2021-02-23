import numpy as np
import pandas as pd
import random
# Tensorflow
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
print('Tensorflow Version:',tf.__version__)

# Variables 
W_PATH = 'weights/'
W_NAME = 'weights_v01.hdf5'
DF_PATH = 'weights/'
DF_NAME = 'pd_weights_v01'

class GNN():
    def __init__(self, weights=None, input_size=16, output_size=4):
        self.layers = [16,16]
        self.fitness = -999
        self.weights_idx = []
        self.input_size = input_size
        self.output_size = output_size
        self.network = Sequential()
        if weights is None:
            # First Layer with Input
            self.network.add(Dense(units=self.layers[0], activation='swish', input_dim=self.input_size))
            for i in range(1,len(self.layers)):
                # Other Hidden layers
                self.network.add(Dense(units=self.layers[i], activation='swish'))
            # Output Layer    
            self.network.add(Dense(units=output_size, activation='softmax'))
        else:
            # First Layer with Input
            self.network.add(Dense(units=self.layers[0], activation='swish', input_dim=self.input_size, 
                                   weights=[weights[0], np.zeros(self.layers[0])]))
            for i in range(1,len(self.layers)):
                # Other Hidden layers
                self.network.add(Dense(units=self.layers[i], activation='swish', 
                                   weights=[weights[i], np.zeros(self.layers[i])]))
            # Output Layer        
            self.network.add(Dense(units=output_size, activation='softmax',weights=[weights[-1], np.zeros(output_size)])) 

        # Index all the weights
        for layer_idx, layer in enumerate(self.network.layers):
            arr = layer.get_weights()[0]
            for line_idx, line in enumerate(arr):
                for col_idx, col in enumerate(line):
                    self.weights_idx.append([layer_idx, line_idx, col_idx])    

        self.episilon_mut = len(self.weights_idx) # Episilon to reduce the number of mutations according to the number of generations
            
    def select_action(self, state):
        input_state = np.array([state])
        prediction = self.network(input_state, training=False)
        action = np.argmax(prediction)
        return action
        
    def crossover(self, net2):
        p1 = []
        p2 = []
        w1 = []
        w2 = []
        
        for idx, layer in enumerate(self.network.layers):
            p1.append(layer.get_weights()[0])
        for idx, layer in enumerate(net2.network.layers):
            p2.append(layer.get_weights()[0])
        
        # Crossover parents
        for i in range(0, len(p1)): # all layers
            split = random.randint(0, np.shape(p1[i])[1]-1) # All neurons for lines
            for j in range(split, np.shape(p1[i])[1]-1):
                gene1 = p1[i][:, j]
                gene2 = p1[i][:, j]
                p1[i][:, j] = gene2 # for all lines, update the selected neuron
                p2[i][:, j] = gene1 # for all lines, update the selected neuron

            w1.append(p1[i])
            w2.append(p2[i])
        
        # Mutation
        w1 = self.mutation_small(w1)
        w2 = self.mutation_small(w2)
        ch1 = GNN(weights=w1, input_size=self.input_size, output_size=self.output_size)
        ch2 = GNN(weights=w2, input_size=self.input_size, output_size=self.output_size)

        return ch1, ch2

    def mutation_small(self, weights):
        for layer, layer_val in enumerate(weights):
            for col, col_val in enumerate(layer_val):
                if random.random() <= 0.15: # about 15% of chance
                    new_gene = random.uniform(-0.5,0.5) # small mutation for good childs
                    weights[layer][col] += new_gene
        return weights

    def save_weights(self, id=0):
        path = ''.join([W_PATH,str(id),'_', W_NAME])
        self.network.save(path)

    def save_history(self, df):
        df.to_csv(DF_PATH+DF_NAME+'.zip', 
                index = False,
                header=True, 
                sep=';', 
                compression=dict(method='zip',archive_name=DF_NAME+'.csv'))

    def load_weights(self, id=0):
        path = ''.join([W_PATH,str(id),'_', W_NAME])
        self.network = tf.keras.models.load_model(path)
        print("Model Loaded!")

    def ProbList(self, population):
        total_fit = sum([pop[1] for pop in population])
        rel_fitness = [f[1]/total_fit for f in population]
        return rel_fitness

    def FChoices(self, population, relative_fitness, number):
        return random.choices(population, weights = relative_fitness, k = number)