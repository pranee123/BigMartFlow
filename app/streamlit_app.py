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
    conn = sqlite3.connect(r"C:\Users\SUMANTH GOUD\OneDrive\Documents\OneDrive\Desktop\PGP\Kafka__Project\bigmart.db")
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales_data'")
    table_exists = cursor.fetchone()

    if not table_exists:
        conn.close()
        return pd.DataFrame()  # return empty DataFrame if table doesn't exist

    # Load data from existing table
    query = "SELECT * FROM sales_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to make predictions based on the model
def predict_sales(df):
    if df.empty:
        return df

    features = ['Item_Identifier', 'Item_Weight', 'Item_Fat_Content', 'Item_Visibility',
                'Item_Type', 'Item_MRP', 'Outlet_Identifier', 'Outlet_Establishment_Year',
                'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']

    df_encoded = pd.get_dummies(df[features])
    df_encoded = df_encoded.fillna(df_encoded.mean())
    X = df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)
    df['Predicted_Sales'] = model.predict(X)
    return df



# Display top 10 predictions
def display_top_10():
    data = load_data()

    if data.empty:
        st.warning("No data available yet. Please wait for data to be consumed.")
        return

    predictions = predict_sales(data)
    top10 = predictions.sort_values(by='Predicted_Sales', ascending=False).head(10)
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
