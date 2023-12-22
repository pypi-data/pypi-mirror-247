"""
authors: Pelin Kömürlüoğlu (pkoemuerlueo@uos.de)
         Deniz Gün (dguen@uos.de)

This module contains helper and test functions for Problemset 3
 of the course "Cognitive Modeling" at the University of Osnabrueck.
 This module exists in order to load certain functionality into the
 assignment notebooks without involuntarily giving students access to
 solutions.
"""

import numpy as np

class StroopNetwork:
    bias = -4
    class Weights:
        # Weights projecting from color input layer to color hidden layer
        scale_ci_ch = 2.0
        c_in_to_c_h = scale_ci_ch * np.array([[1, -1],
                                              [-1, 1]])
        # Weights projecting from color hidden layer to output layer
        scale_ch_co = 2.0
        c_h_to_out = scale_ch_co * np.array([[1, -1],
                                             [-1, 1]])
        # Weights projecting from word input layer to word hidden layer
        scale_wi_wh = 2.0
        w_in_to_w_h = scale_wi_wh * np.array([[1, -1],
                                              [-1, 1]])
        # Weights projecting from word hidden layer to output layer
        scale_wh_wo = 2.0
        w_h_to_out = scale_wh_wo * np.array([[1, -1],
                                            [-1, 1]])
        # Weights projecting from task layer to color hidden layer
        scale_ti_ch = 4.0
        t_in_to_c_h = scale_ti_ch * np.array([[1, 1],
                                             [0, 0]])
        # Weights projecting from task layer to word hidden layer
        scale_ti_wh = 4.0
        t_in_to_w_h = scale_ti_wh * np.array([[0, 0],
                                              [1, 1]])
    
    class TweakedWeights:
        # Weights projecting from color input layer to color hidden layer
        scale_ci_ch = 2.0
        c_in_to_c_h = scale_ci_ch * np.array([[1, -1],
                                              [-1, 1]])
        # Weights projecting from color hidden layer to output layer
        scale_ch_co = 2.0
        c_h_to_out = scale_ch_co * np.array([[1, -1],
                                             [-1, 1]])
        # Weights projecting from word input layer to word hidden layer
        scale_wi_wh = 2.0
        w_in_to_w_h = scale_wi_wh * np.array([[1, -1],
                                              [-1, 1]])
        # Weights projecting from word hidden layer to output layer
        scale_wh_wo = 2.0
        w_h_to_out = scale_wh_wo * np.array([[1, -1],
                                            [-1, 1]])
        # Weights projecting from task layer to color hidden layer
        scale_ti_ch = 4.0
        t_in_to_c_h = scale_ti_ch * np.array([[1, 1],
                                             [0, 0]])
        # Weights projecting from task layer to word hidden layer
        scale_ti_wh = 4.0
        t_in_to_w_h = scale_ti_wh * np.array([[0, 0],
                                              [1, 1]])

    ### Activation Functions ###
    def logistic(net_activation):
        return 1 / (1+np.exp(-v))
    
    def logistic_derivative(x):
        return x * (1-x)
        

    def softmax(activation):
        return np.exp(activation) / np.sum(np.exp(activation), axis=1)

    ### Layer activations ###
    def color_hidden_activation(color_input, task_input,
                                Weights, bias):
      net_activation =  np.dot(color_input, Weights.c_in_to_c_h)
      net_activation += np.dot(task_input, Weights.t_in_to_c_h)
      net_activation += bias
      activation = StroopNetwork.logistic(net_activation)
      return activation

    def word_hidden_activation(word_input, task_input,
                               Weights, bias):
        net_activation =  np.dot(word_input, Weights.w_in_to_w_h)
        net_activation += np.dot(task_input, Weights.t_in_to_w_h)
        net_activation += bias
        activation = StroopNetwork.logistic(net_activation)
    return activation

    def output_activation(color_hidden_activation,
                      word_hidden_activation,
                      Weights,
                      bias):

        net_activation =  np.dot(color_hidden_activation, Weights.c_h_to_out)
        net_activation += np.dot(word_hidden_activation, Weights.w_h_to_out)
        net_activation += bias

        activation = StroopNetwork.logistic(net_activation)
        return activation

    ### Forward Pass ###
    def forward(color_input, word_input,task_input, return_activations=False):
      """
      Accepts a single input pattern for the color, word and task input layers and produces a response probability at the output layer.

      Arguments:
        color_input (2D array): stores the color value (red vs. green)
        word_input (2D array): stores the word value (RED vs. GREEN)
        task_input (2D array): stores the task value (color naming vs. word reading)

      Returns:
        response_probability (float): probability distribution of the output activation.
      """

      Weights = StroopNetwork.Weights
      bias = StroopNetwork.bias

      # Compute activation of color hidden layer
      activation_ch = color_hidden_activation(color_input,task_input, Weights,bias)

      # Compute activation of word hidden layer
      activation_wh = word_hidden_activation(word_input, task_input, Weights, bias)

      # Compute activation of output layer
      activation_output = output_activation(activation_ch, activation_wh,Weights, bias)

      # Apply softmax function to convert the output activation for each unit (response) into a probability
      response_probabilities = StroopNetwork.softmax(activation_output)
      
      if return_activations:
        return {"color":activation_ch,
                "word":activation_wh,
                "out":activation,
                "response":response_probabilities}
      
      return response_probabilities
      
   
    ### WEIGHT UPDATES ####
    def compute_weight_updates_hidden_to_out(hidden_activation,
                                      output_activation,
                                      error):
        """ 
        This function calculates the weight update for the weights
        projecting from the hidden color units to the output units.
        
        Arguments:
            output_activation: activation at the output layer
            error:             discrepancy between output and target
            
        Returns:
            The weight update to be applied based on backprop
        """
        
        output_derivative = logistic_derivative(output_activation)
        
        weight_update = np.dot(hidden_activation.T,
                                error*output_derivative)
                                
        return weight_update


    def compute_weight_updates_in_to_hidden(input, weights_h_to_out,
                                            hidden_activation, error):
                                            
        """
        Arguments:
            input (2D Array):  e.g. [[1,0]]
            weights_h_to_out (2D Array):  e.g [[2,0],[0,-2]]
            hidden_activation (2D Array):  e.g. [[0.4],[0,9]]
            error (float):             discrepancy between output and target
            
        Returns:
            weight_update (float): Value which indicates how much the weights   between input and hidden units should change
            
        """
        # Derivative of error wrt hidden activation
        d_error_to_h = np.dot(error, weights_h_to_out.T)

        # Derivative of hidden activation wrt net activation
        d_h_act_to_h_net = logistic_derivative(hidden_activation)
        
        # Derivative of error wrt to hidden net activation
        d_error_to_h_net = d_error_to_h * d_h_act_to_h_net
        
        # Derivative of the error wrt to the weights 
        weight_update = np.dot(input.T, d_error_to_h_net * d_h_act_to_h_net)
        
        return weight_update

### END OF CLASS ### 

### Functions and Test Functions ###
def logistic(v):
    return 1 / (1+np.exp(-v))
    
    
def test_logistic(student_function):
  test_values = np.arange(10)
  for v in test_values:
    v = np.array([v])
    if not np.array_equal(student_function(v), logistics(v)):
      print("Your Logistic Function produces incorrect ouputs")
      return
  print("Your Logistic function produces correct outputs.")
  return


def test_color_hidden_activation(student_function, weights):
  c_ins = [[0,1],[1,0]]
  t_ins = [[0,1],[1,0]]
  bias = -3
  for ci in c_ins:
    for ti in t_ins:
      answer = student_function(ci,ti,weights,bias)
      correct = StroopNetwork.color_hidden_activation(ci,ti,weights,bias)
      if not np.array_equal(answer, correct):
        print("Your color_hidden_activation produces wrong outputs.")
        return
  print("Your color_hidden_activation produces correct ouputs")
  return

def test_word_hidden_activation(student_function, weights):
  c_ins = [[0,1],[1,0]]
  t_ins = [[0,1],[1,0]]
  bias = -3
  for ci in c_ins:
    for ti in t_ins:
      answer = student_function(ci,ti,weights,bias)
      correct = StroopNetwork.word_hidden_activation(ci,ti,weights,bias)
      if not np.array_equal(answer, correct):
        print("Your color_hidden_activation produces wrong outputs.")
        return

  print("Your word_hidden_activation produces correct ouputs")
  return


def test_output_activation(student_function, weights):
  c_ins = [[0,1],[1,0]]
  t_ins = [[0,1],[1,0]]
  bias = -3
  for ci in c_ins:
    for ti in t_ins:
      answer = student_function(ci,ti,weights,bias)
      correct = StroopNetwork.output_activation(ci,ti,weights,bias)
      if not np.array_equal(answer, correct):
        print("Your output_activation produces wrong outputs.")
        return

  print("Your output_activation produces correct ouputs")
  return



def act_func(x):

    return 1 / (1 + np.exp(-x))
def act_func_der(x):

    return x * (1-x)
