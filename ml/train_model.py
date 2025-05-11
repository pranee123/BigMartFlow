import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.preprocessing import LabelEncoder

# Step 1: Load CSV file into SQLite database
def load_csv_to_sqlite():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('bigmartsales.csv')

    # Connect to SQLite database (it will create if it doesn't exist)
    conn = sqlite3.connect('bigmart.db')

    # Write the DataFrame to SQLite (create a new table called 'sales_data')
    df.to_sql('sales_data', conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

# Step 2: Query the data from SQLite
def load_data_from_sqlite():
    # Connect to the SQLite database
    conn = sqlite3.connect('bigmart.db')

    # Query the data
    df = pd.read_sql_query("SELECT * FROM sales_data", conn)

    # Close the connection
    conn.close()
    return df

# Step 3: Preprocess data
def preprocess_data(df):
    # Handle missing values (only for numeric columns)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    # Encoding categorical columns (if any)
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le
    
    return df, label_encoders


# Step 4: Train a machine learning model (Random Forest Regressor)
def train_model(df):
    # Define feature columns and target column
    feature_columns = df.columns[df.columns != 'Sales']
    X = df[feature_columns]
    y = df['Item_Outlet_Sales']

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the RandomForest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    return model

# Step 5: Save the trained model
def save_model(model):
    joblib.dump(model, 'sales_model.joblib')
    print("Model saved as 'sales_model.joblib'")

if __name__ == "__main__":
    # Load CSV to SQLite (run only once)
    load_csv_to_sqlite()

    # Load data from SQLite
    df = load_data_from_sqlite()

    # Preprocess data
    df, label_encoders = preprocess_data(df)

    # Train model
    model = train_model(df)

    # Save model
    save_model(model)
