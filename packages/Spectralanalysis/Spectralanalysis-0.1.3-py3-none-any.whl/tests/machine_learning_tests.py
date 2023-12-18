import unittest
import pandas as pd
import  numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from data_module import DataIO as data_io

def train_model(X_train, y_train):
    """
    Trains a random forest classifier model using the training data.
    Inputs: 
        X_train: Pandas dataframe containing the training data
        y_train: Pandas series containing the training labels
    Outputs:
        model: Trained random forest classifier model
    """
    if not isinstance(X_train, pd.DataFrame):
        raise TypeError('X_train must be a pandas dataframe')
    if not isinstance(y_train, pd.Series):
        raise TypeError('y_train must be a pandas series')
    model = RandomForestClassifier(random_state=107)      
    if y_train.empty or X_train.empty:
        raise ValueError('Training data must not be empty')
    model.fit(X_train, y_train) 
    return model

def make_predictions(model, X):
    """
    Makes predictions using the trained model.
    Inputs:
        model: Trained random forest classifier model
        X: Pandas dataframe containing the data to make predictions on
    Outputs:
        predictions: List of predictions
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError('X must be a pandas dataframe')
    if X.empty:
        raise ValueError('Data to make predictions on must not be empty')
    if not isinstance(model, RandomForestClassifier):
        raise TypeError('Model must first be trained on training data')
    predictions = model.predict(X)
    return predictions

class TestMachineLearningModule(unittest.TestCase):
    def setUp(self):
        # sample spectral data in a CSV format
        self.sample_data = {
            'wavelength_1': [0.1, 0.2, 0.3, 0.4],
            'wavelength_2': [0.5, 0.6, 0.7, 0.8],
            'class_label': [1, 0, 1, 0]
        }
        self.csv_filename = 'sample_data.csv'
        pd.DataFrame(self.sample_data).to_csv(self.csv_filename, index=False)

    # Test training the model
    def test_train_model(self):
        data = pd.read_csv(self.csv_filename)
        X = data.drop('class_label', axis=1)
        y = data['class_label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=107)

        model = train_model(X_train, y_train)

        # Model should be a random forest classifier
        self.assertIsInstance(model, RandomForestClassifier) 
        accuracy = model.score(X_test, y_test)

        # Accuracy should be between 0 and 1
        self.assertGreaterEqual(accuracy, 0)
        self.assertLessEqual(accuracy, 1)

    def test_model_training_with_empty_data(self):
        X_train = pd.DataFrame()
        y_train = pd.Series()

        # Model should raise a ValueError if training data is empty
        self.assertRaises(ValueError, train_model, X_train, y_train)

    def test_model_training_with_incorrect_data_type(self):
        X_train = np.array([1, 2, 3])
        y_train = np.array([1, 2, 3])

        # Model should raise a TypeError if training data is not a pandas dataframe
        self.assertRaises(TypeError, train_model, X_train, y_train)

    # Test making predictions using the trained model
    def test_make_predictions(self):
        data = pd.read_csv(self.csv_filename)
        X = data.drop('class_label', axis=1)
        y = data['class_label']

        model = RandomForestClassifier(random_state=42) 
        model.fit(X, y) 

        predictions = make_predictions(model, X)
        self.assertEqual(len(predictions), len(y))  

    def test_no_trained_module(self):
        fake_model = pd.DataFrame([1, 2, 3])
        X = pd.DataFrame([1, 2, 3])

        # Model should raise a TypeError if model is not a random forest classifier
        self.assertRaises(TypeError, make_predictions, fake_model, X)

    def test_make_predictions_with_empty_data(self):
        data = pd.read_csv(self.csv_filename)
        X = data.drop('class_label', axis=1)
        y = data['class_label']
    
        model = train_model(X, y)

        empty = pd.DataFrame()

        # Model should raise a ValueError if data to make predictions on is empty
        self.assertRaises(ValueError, make_predictions, model, empty)


if __name__ == '__main__':
    unittest.main()