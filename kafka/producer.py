from kafka import KafkaProducer
import pandas as pd
import json
import time

# Load and inspect the dataset
df = pd.read_csv('bigmartsales.csv')

# STEP 1: Drop duplicates
df.drop_duplicates(inplace=True)

# STEP 2: Handle null values
# Fill Item_Weight nulls with mean
df['Item_Weight'].fillna(df['Item_Weight'].mean(), inplace=True)

# Fill Outlet_Size nulls with mode
df['Outlet_Size'].fillna(df['Outlet_Size'].mode()[0], inplace=True)

# Drop any remaining nulls (if any critical ones are left)
df.dropna(inplace=True)

# STEP 3: Fix categorical inconsistencies
df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
    'LF': 'Low Fat',
    'low fat': 'Low Fat',
    'reg': 'Regular'
})

# STEP 4: Drop columns you don't need (optional)
# df.drop(columns=['Some_Column'], inplace=True)

# STEP 5: Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# STEP 6: Stream the cleaned data
for _, row in df.iterrows():
    data = row.to_dict()
    producer.send('bigmart_topic', value=data)
    print("Sent:", data)
    time.sleep(1)  # simulate real-time stream

producer.flush()
