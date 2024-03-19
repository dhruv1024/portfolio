import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Define a function to preprocess the user input
def preprocess_input(years_exp, salary, education):
    input_data = np.array([[years_exp, salary, education]])
    input_data_scaled = scaler.transform(input_data)
    return input_data_scaled

# Load X_train data from CSV
X_train_df = pd.read_csv('X_train.csv')
X_train = X_train_df.values

# Load the trained models
models = []
#for i in range(1, 6):  # Assuming we trained models for up to 5 years of retention
for i in (0, 1, 3):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(3,)),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.load_weights(f'model_weights_{i}_year.h5')  # Load model weights for each year
    models.append(model)

# Load the fitted scaler
scaler = StandardScaler()
scaler.fit(X_train)  # Fit the scaler on the training data

# Accept user input
years_exp = float(input("Enter years of experience: "))
salary = float(input("Enter salary: "))
education = float(input("Enter education level: "))

# Preprocess the user input
input_data_scaled = preprocess_input(years_exp, salary, education)

# Make predictions
for i, model in enumerate(models):
    prediction = model.predict(input_data_scaled)[0][0]
    print(f'Probability of retaining the employee for {i+1} year(s): {prediction:.4f}')
