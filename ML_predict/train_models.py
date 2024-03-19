import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint

# Load the dataset (replace 'dataset.csv' with your actual dataset file)
data = pd.read_csv('dataset.csv')

# Data preprocessing
# Assuming 'YearsExperience', 'Salary', 'Education', and 'RetentionYears' are columns in your dataset
X = data[['YearsExperience', 'Salary', 'Education']].values
# Modify the target variable to represent the number of years the employee will stay
y = data['RetentionYears'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert X_train to a DataFrame
X_train_df = pd.DataFrame(X_train, columns=['YearsExperience', 'Salary', 'Education'])

# Save X_train as a CSV file
X_train_df.to_csv('X_train.csv', index=False)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define a list to store models
models = []

# Train a separate model for each retention year
for year in np.unique(y_train):
    # Create a binary target variable indicating whether the employee will stay for 'year' years or not
    y_train_binary = (y_train >= year).astype(int)

    # For each retention year, a neural network model is defined using the Keras Sequential API. 
    # The model consists of densely connected (fully connected) layers with ReLU activation functions, 
    # which are commonly used in neural networks for introducing non-linearity.   

    # The model is compiled with the Adam optimizer and binary cross-entropy loss function, suitable for binary classification tasks.
     
    # Define the neural network model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # During training, a portion of the training data is used for validation to monitor the model's performance and prevent overfitting. 
    # Model weights are saved using ModelCheckpoint to keep the best-performing weights.
    
    # Define a checkpoint to save the best model weights during training
    checkpoint_filepath = f"model_weights_{year}_year.h5"
    model_checkpoint_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_loss',
        mode='min',
        save_best_only=True)
    
    # Train the model
    model.fit(X_train_scaled, y_train_binary, epochs=10, batch_size=32, validation_split=0.2, callbacks=[model_checkpoint_callback], verbose=1)
    
    # Store the trained model
    models.append(model)