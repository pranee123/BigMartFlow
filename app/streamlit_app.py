import streamlit as st
import pandas as pd
import sqlite3
import time
import joblib

# Title
st.title("Top 10 Grocery Demand Predictions")

# Load model
model = joblib.load("ml/sales_model.joblib")

# Function to fetch data from SQLite database
def load_data():
    conn = sqlite3.connect('bigmart.db')
    query = "SELECT * FROM sales_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to make predictions based on the model
def predict_sales(df):
    features = ['Item_Identifier', 'Item_Weight', 'Item_Fat_Content', 'Item_Visibility',
                'Item_Type', 'Item_MRP', 'Outlet_Identifier', 'Outlet_Establishment_Year',
                'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
    
    # Ensure categorical variables are encoded
    df_encoded = pd.get_dummies(df[features])
    
    # Handle missing values (impute or drop rows with NaN values)
    df_encoded = df_encoded.fillna(df_encoded.mean())  # You can also use df_encoded.dropna() to drop rows with NaN

    # Align with model features
    X = df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)
    
    # Predict sales
    df['Predicted_Sales'] = model.predict(X)
    return df


# Display top 10 predictions
def display_top_10():
    # Load data from the database
    data = load_data()

    # Make predictions
    predictions = predict_sales(data)

    # Sort and select top 10
    top10 = predictions.sort_values(by='Predicted_Sales', ascending=False).head(10)

    # Display top 10 predictions as a table
    st.subheader("Top 10 Predicted Sales")
    st.table(top10[['Item_Identifier', 'Item_Type', 'Outlet_Identifier', 'Predicted_Sales']])

# Auto-refresh the data every 10 seconds manually
if st.button("Refresh Data"):
    display_top_10()
else:
    # Initially display the top 10
    display_top_10()

# Display message to indicate auto-refresh
st.info("Click 'Refresh Data' to manually refresh the top 10 predictions.")
