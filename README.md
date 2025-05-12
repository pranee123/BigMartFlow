# BigMartFlow
🛒 BigMart Real-Time Sales Prediction Dashboard

🚀 Overview

This project showcases a real-time data pipeline and machine learning system for predicting retail sales demand using Apache Kafka, Python, and Streamlit. It simulates a dynamic retail environment where sales data is continuously streamed, processed, and visualized.

The system consists of a Kafka producer that feeds new sales records, a Kafka consumer that stores the data in a database, a trained ML model that predicts future demand, and a Streamlit dashboard that displays the top 10 latest entries with predictions in real time.

📦 Tech Stack

Apache Kafka – for real-time data streaming

Python – for scripting, data processing, and ML

scikit-learn – for building the predictive model

SQLite (bigmart.db) – for storing incoming data

Pandas & NumPy – for data manipulation

Streamlit – for creating a web-based dashboard

Docker – (optional) for containerized deployment

🔄 Workflow

Kafka Producer

Reads from bigmartsales.csv line-by-line

Sends records to a Kafka topic every few seconds

Kafka Consumer

Listens to the topic

Writes the data into bigmart.db SQLite database

ML Model

A regression model (e.g., Linear Regression) is trained on historical sales data

Predicts Item_Outlet_Sales for each new record

Streamlit Dashboard

Fetches the top 10 most recent records from the database

Displays actual and predicted sales dynamically with refresh capability

📁 Project Structure

.
├── app
│   └── streamlit_app.py         # Streamlit UI logic
├── consumer.py                  # Kafka consumer script
├── producer.py                  # Kafka producer script
├── model.pkl                    # Trained ML model
├── bigmart.db                   # SQLite database storing new data
├── bigmartsalws.csv             # Sample data used by the producer
├── requirements.txt             # Dependencies for the project
└── README.md                    # Project documentation

💻 How to Run Locally

1. Start Kafka and Zookeeper

Use Docker or local Kafka setup to start Zookeeper and Kafka broker.

2. Start Producer and Consumer

python producer.py
python consumer.py

3. Launch the Dashboard

streamlit run app/streamlit_app.py

📊 Output Preview

Top 10 latest sales records

Real-time updates every few seconds

Actual vs Predicted sales

🌐 Deployment

Deployed using Streamlit Cloud. Visit the live app here: https://bigmartflow.streamlit.app

✨ Highlights

Real-time data streaming & visualization

End-to-end ML integration

Lightweight and scalable design

🤝 Contributions

Feel free to fork the repo, raise issues, or submit PRs. Suggestions to improve real-time accuracy, visualization, or deployment are welcome!

📧 Contact

Developed by Praneeth Goud📬 Email: praneethgoud2510@gmail.com 🔗 GitHub: pranee123
