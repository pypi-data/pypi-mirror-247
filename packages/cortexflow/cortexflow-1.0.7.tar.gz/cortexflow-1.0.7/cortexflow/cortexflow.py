import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

def cross_validator(X, y, model, n_splits):
    kf = KFold(n_splits=n_splits)
    mse_scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        mse_scores.append(mse)

    average_mse = np.mean(mse_scores)
    return average_mse
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score

def classifier(x, y):
    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Initialize and fit classification models
    models = {
        "Logistic Regression": LogisticRegression(),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Support Vector Machine": SVC(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "AdaBoost": AdaBoostClassifier(),
        "Gaussian Naive Bayes": GaussianNB(),
        "Neural Network": MLPClassifier(),
        "Linear Discriminant Analysis": LinearDiscriminantAnalysis(),
        "Quadratic Discriminant Analysis": QuadraticDiscriminantAnalysis()
    }

    for name, model in models.items():
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        
        acc = accuracy_score(y_test, y_pred)
        
        print(f"Model: {name}")
        print(f"Accuracy: {acc:.2f}")
        print("=" * 40)

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import (
    LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor, PassiveAggressiveRegressor,
    BayesianRidge, ARDRegression, TweedieRegressor, PoissonRegressor
)
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor,
    BaggingRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor
)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import Lars, OrthogonalMatchingPursuit, RANSACRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import xgboost as xgb
import lightgbm as lgb

def regressor(x, y):
    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Initialize and fit regression models
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(),
        "ElasticNet Regression": ElasticNet(),
        "Huber Regressor": HuberRegressor(),
        "Passive Aggressive Regressor": PassiveAggressiveRegressor(),
        "Bayesian Ridge Regression": BayesianRidge(),
        "ARD Regression": ARDRegression(),
        "Tweedie Regressor": TweedieRegressor(),
        "Poisson Regressor": PoissonRegressor(),
        "Support Vector Regression": SVR(),
        "Decision Tree Regression": DecisionTreeRegressor(),
        "Random Forest Regression": RandomForestRegressor(),
        "Gradient Boosting Regression": GradientBoostingRegressor(),
        "AdaBoost Regression": AdaBoostRegressor(),
        "Bagging Regressor": BaggingRegressor(),
        "Extra Trees Regressor": ExtraTreesRegressor(),
        "HistGradient Boosting Regressor": HistGradientBoostingRegressor(),
        "K-Nearest Neighbors Regression": KNeighborsRegressor(),
        "Gaussian Process Regression": GaussianProcessRegressor(),
        "LARS (Least Angle Regression)": Lars(),
        "Orthogonal Matching Pursuit": OrthogonalMatchingPursuit(),
        "RANSAC Regressor": RANSACRegressor(),
        "Kernel Ridge Regression": KernelRidge(),
        "Neural Network Regression": MLPRegressor(),
        "XGBoost Regression": xgb.XGBRegressor(),
        "LightGBM Regression": lgb.LGBMRegressor()
    }

    for name, model in models.items():
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)  # Compute RMSE
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Model: {name}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"Root Mean Squared Error: {rmse:.2f}")
        print(f"Mean Absolute Error: {mae:.2f}")
        print(f"R-squared: {r2:.2f}")
        print("=" * 40)

# Call the regression function with your data (x and y)
# regression(x_data, y_data)

import warnings
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam, Adadelta, Adagrad, Adamax, Nadam, Ftrl
warnings.filterwarnings('ignore')
logger = logging.getLogger('tensorflow')
logger.setLevel(logging.ERROR)
def neural_classification_evaluation(X, y, input_shape, problem='binary', activation=None, optimizer_class=Adam, hidden_layers=2, neurons_per_hidden=100):
    def test_model(X_train, y_train, X_val, y_val, X_test, y_test, activation):
        optimizer = optimizer_class()

        model = Sequential()
        model.add(Dense(neurons_per_hidden, input_shape=input_shape))
        model.add(Activation(activation))

        for _ in range(hidden_layers - 1):
            model.add(Dense(neurons_per_hidden))
            model.add(Activation(activation))

        model.add(Dense(1 if problem == 'binary' else len(np.unique(y_train))))

        if problem == 'binary':
            model.add(Activation('sigmoid'))
            model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        else:
            model.add(Activation('softmax'))
            model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        history = model.fit(
            X_train, y_train,
            epochs=10, batch_size=32,
            validation_data=(X_val, y_val),
            verbose=0
        )

        evaluation = model.evaluate(X_test, y_test, verbose=0)
        return {'Activation Function': activation, 'Test Score': evaluation[1], 'History': history}

    if activation is None:
        activation = 'relu'

    if activation == 'all':
        activations = ['relu', 'elu', 'selu', 'sigmoid','LeakyReLU', 'tanh', 'softmax', 'softplus', 'softsign']
    else:
        activations = [activation]

    results = []
    X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)

    for act_func in activations:
        result = test_model(X_train, y_train, X_val, y_val, X_test, y_test, act_func)
        results.append(result)

    results_df = pd.DataFrame(results)
    print(results_df[['Activation Function', 'Test Score']])

    for result in results:
        print(f"Activation Function: {result['Activation Function']}")
        plt.figure(figsize=(8, 3))

        plt.subplot(1, 2, 1)
        plt.plot(result['History'].history['accuracy'], label='Training Accuracy')
        plt.plot(result['History'].history['val_accuracy'], label='Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(result['History'].history['loss'], label='Training Loss')
        plt.plot(result['History'].history['val_loss'], label='Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        plt.tight_layout()
        plt.show()

def neural_regression_evaluation(X, y, input_shape, activation=None, optimizer_class=Adam, hidden_layers=2, neurons_per_hidden=100):
    def test_model_regression(X_train, y_train, X_val, y_val, X_test, y_test, activation):
        optimizer = optimizer_class()

        model = Sequential()
        model.add(Dense(neurons_per_hidden, input_shape=input_shape))
        model.add(Activation(activation))

        for _ in range(hidden_layers - 1):
            model.add(Dense(neurons_per_hidden))
            model.add(Activation(activation))

        model.add(Dense(1))

        model.compile(optimizer=optimizer, loss='mean_squared_error')

        history = model.fit(
            X_train, y_train,
            epochs=10, batch_size=32,
            validation_data=(X_val, y_val),
            verbose=0
        )

        evaluation = model.evaluate(X_test, y_test, verbose=0)
        predictions = model.predict(X_test,verbose=0)
        mean_absolute_error = np.mean(np.abs(predictions - y_test))
        return {
            'Activation Function': activation,
            'Mean Squared Error': evaluation,
            'Mean Absolute Error': mean_absolute_error
        }

    if activation is None:
        activation = 'relu'

    if activation == 'all':
        activations = ['relu', 'elu', 'selu', 'sigmoid', 'tanh', 'softmax', 'softplus', 'softsign']
    else:
        activations = [activation]

    results = []

    X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)

    for act_func in activations:
        result = test_model_regression(X_train, y_train, X_val, y_val, X_test, y_test, act_func)
        results.append(result)

    results_df = pd.DataFrame(results)
    return results_df
