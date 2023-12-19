# CortexFlow

Welcome to CortexFlow, a Python library designed for efficient neural network evaluation, regression analysis, and optimization tasks. This library simplifies the process of evaluating and optimizing neural network models, making it accessible to beginners and experienced data scientists. CortexFlow is equipped with a variety of tools for analysis and optimization, providing accurate insights into your data.
##Features
1.Evaluate neural network models for both classification and regression tasks.
2.Analyze the impact of various activation functions and model configurations.
3.Perform regression analysis on datasets.

## Installation

You can install CortexFlow using pip:

```shell
pip install cortexflow

```
# Usage
## Neural Network Evaluation
CortexFlow simplifies neural network evaluation for both classification and regression tasks. Example usage:
```shell
from cortexflow import neural_classification_evaluation, neural_regression_evaluation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam, Adadelta, Adagrad, Adamax, Nadam, Ftrl


# Example data
X_data = ...
y_labels = ...

# Classification evaluation
neural_classification_evaluation(X_data, y_labels, input_shape=(num_features,),
                                 problem='binary/multiclass', activation='all'/'single_activation',
                                 optimizer_class=Adam, hidden_layers=2, neurons_per_hidden=100)

# Single_activation=['relu', 'elu', 'selu', 'sigmoid','LeakyReLU', 'tanh', 'softmax', 'softplus', 'softsign'] From this you can choose any of this
# optimizer_class=any of you choice SGD, RMSprop, Adam, Adadelta, Adagrad, Adamax, Nadam, Ftrl

# Regression evaluation
X_iris = ...
y_regression = ...
neural_regression_evaluation(X_iris, y_regression, input_shape=(4,), activation='all',
                             optimizer_class=Adam, hidden_layers=2, neurons_per_hidden=100)

```

