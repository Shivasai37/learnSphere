# Required Libraries
# numpy, pandas, scikit-learn

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Define a function to create a random forest classifier
def create_random_forest(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize a random forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the classifier using the training data
    clf.fit(X_train, y_train)
    
    # Use the trained classifier to make predictions on the test data
    y_pred = clf.predict(X_test)
    
    # Calculate the accuracy of the classifier
    accuracy = accuracy_score(y_test, y_pred)
    
    # Print the accuracy and a classification report
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return clf

# Main execution block
if __name__ == "__main__":
    # Create a sample dataset
    np.random.seed(42)
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    
    # Create a pandas dataframe from the dataset
    df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
    df['target'] = y
    
    # Split the dataframe into features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Create and train a random forest classifier
    clf = create_random_forest(X, y)
    
    # Print the feature importances
    print("Feature Importances:")
    for feature, importance in zip(X.columns, clf.feature_importances_):
        print(f"{feature}: {importance}")