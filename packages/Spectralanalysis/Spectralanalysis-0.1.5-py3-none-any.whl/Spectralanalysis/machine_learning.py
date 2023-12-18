import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class MachineLearning:
    """
    A class for machine learning functionalities in the Spectralysis library.
    """

    def __init__(self):
        """
        Initializes the MachineLearning class.
        """
        pass

    @staticmethod
    def train_model(data, labels):
        """
        Trains a random forest classifier model using the provided data and labels.
        Args:
            data (pd.DataFrame): The training data.
            labels (pd.Series): The labels for the training data.
        Returns:
            RandomForestClassifier: The trained model.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        if not isinstance(labels, pd.Series):
            raise TypeError("labels must be a pandas Series")

        if data.empty or labels.empty:
            raise ValueError("Training data and labels must not be empty")

        model = RandomForestClassifier(random_state=107)
        model.fit(data, labels)
        return model

    @staticmethod
    def predict_spectrum(model, data):
        """
        Makes predictions using the provided model on new data.
        Args:
            model (RandomForestClassifier): The trained machine learning model.
            data (pd.DataFrame): New data on which to make predictions.
        Returns:
            np.ndarray: Predictions made by the model.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        if data.empty:
            raise ValueError("Data to make predictions on must not be empty")
        if not isinstance(model, RandomForestClassifier):
            raise TypeError("Model must be a trained RandomForestClassifier")

        predictions = model.predict(data)
        return predictions


# Example usage

# Sample data
#data = pd.read_csv("path/to/data.csv")
#labels = data["target_column"]
#features = data.drop("target_column", axis=1)

# Splitting data into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
#)

# Machine Learning
#ml = MachineLearning()

# Training the model
#model = ml.train_model(X_train, y_train)

# Making predictions
#predictions = ml.predict_spectrum(model, X_test)
