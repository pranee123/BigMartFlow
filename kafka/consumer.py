from kafka import KafkaConsumer
import sqlite3
import json

# SQLite DB setup
conn = sqlite3.connect('bigmart.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_data (
    Item_Identifier TEXT,
    Item_Weight REAL,
    Item_Fat_Content TEXT,
    Item_Visibility REAL,
    Item_Type TEXT,
    Item_MRP REAL,
    Outlet_Identifier TEXT,
    Outlet_Establishment_Year INTEGER,
    Outlet_Size TEXT,
    Outlet_Location_Type TEXT,
    Outlet_Type TEXT,
    Item_Outlet_Sales REAL,
    Profit REAL
)
''')
conn.commit()

# Kafka Consumer setup
consumer = KafkaConsumer(
    'bigmart_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    print("Received:", data)

    # Check if data matches the expected schema
    expected_columns = ['Item_Identifier', 'Item_Weight', 'Item_Fat_Content', 'Item_Visibility',
                        'Item_Type', 'Item_MRP', 'Outlet_Identifier', 'Outlet_Establishment_Year',
                        'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type', 'Item_Outlet_Sales', 'Profit']
    
    # Ensure the data matches the expected columns, otherwise skip this entry
    if not all(col in data for col in expected_columns):
        print("Invalid data structure, skipping:", data)
        continue
    
    # Handle missing values if needed
    data = {key: (value if value is not None else 0) for key, value in data.items()}

    # Prepare placeholders for SQL query
    placeholders = ', '.join('?' * len(data))
    
    try:
        # Insert data into the sales_data table
        cursor.execute(f'''
            INSERT INTO sales_data ({', '.join(expected_columns)}) VALUES ({placeholders})
        ''', list(data.values()))
        
        # Commit the transaction after each insert
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        continue

# Close the connection when done
conn.close()
