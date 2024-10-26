import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import joblib
import mysql.connector

def train_model(file_path, model_path='svm_model.pkl'):
    # Load dataset
    data = pd.read_csv(file_path)

    # Convert 'LastPurchaseDate' to datetime and calculate 'DaysSinceLastPurchase'
    data['LastPurchaseDate'] = pd.to_datetime(data['LastPurchaseDate'], format='%d-%m-%Y')
    data['DaysSinceLastPurchase'] = (pd.Timestamp.now() - data['LastPurchaseDate']).dt.days

    # Handle missing values by dropping them or filling with appropriate values
    data.dropna(inplace=True)  # This will drop rows with any missing values

    # Create target labels based on engagement and purchase amount quantiles
    data['Target'] = ((data['EngagementScore'] > data['EngagementScore'].quantile(0.7)) & 
                      (data['PurchaseAmount'] > data['PurchaseAmount'].quantile(0.7))).astype(int)

    # Select features for prediction
    X = data[['Age', 'Gender', 'PurchaseAmount', 'DaysSinceLastPurchase', 'EngagementScore', 'State/UT', 'ProductCategory']]
    y = data['Target']

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['Age', 'PurchaseAmount', 'DaysSinceLastPurchase', 'EngagementScore']),
            ('cat', OneHotEncoder(), ['Gender', 'State/UT', 'ProductCategory'])
        ]
    )

    # Create SVM model pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', SVC())])

    # Train the SVM model
    pipeline.fit(X, y)

    # Save the trained model to a pickle file
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

def predict_target_customers(file_path, product_details):
    # Load the trained model
    model = joblib.load('svm_model.pkl')

    # Load dataset
    data = pd.read_csv(file_path)

    # Convert 'LastPurchaseDate' to datetime and calculate 'DaysSinceLastPurchase'
    data['LastPurchaseDate'] = pd.to_datetime(data['LastPurchaseDate'], format='%d-%m-%Y')
    data['DaysSinceLastPurchase'] = (pd.Timestamp.now() - data['LastPurchaseDate']).dt.days

    # Handle missing values
    data.dropna(inplace=True)

    # Prepare features for prediction
    X_pred = data[['Age', 'Gender', 'PurchaseAmount', 'DaysSinceLastPurchase', 'EngagementScore', 'State/UT', 'ProductCategory']]

    # Predict target customers
    target_predictions = model.predict(X_pred)

    # Filter potential target customers
    data['Target'] = target_predictions
    target_customers = data[data['Target'] == 1]

    # Optionally, select specific columns to return
    target_customers_filtered = target_customers[['CustomerID', 'Name', 'Age', 'Gender', 'Email', 'PhoneNumber', 
                                                  'PurchaseAmount', 'LastPurchaseDate', 'EngagementScore', 
                                                  'State/UT', 'ProductCategory', 'DaysSinceLastPurchase']]

    return target_customers_filtered

def store_target_customers_in_db(target_customers):
    # MySQL connection setup
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='customer'
    )
    cursor = conn.cursor()

    # SQL query to insert data
    insert_query = """
    INSERT INTO target_customers (
    CustomerID, Name, Age, Gender, Email, PhoneNumber, PurchaseAmount,
    LastPurchaseDate, EngagementScore, State_UT, ProductCategory, 
    DaysSinceLastPurchase, Target
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

    """

    # Insert each target customer into the database
    for _, row in target_customers.iterrows():
        try:
            cursor.execute(insert_query, tuple(row))
        except mysql.connector.Error as err:
            print(f"Error inserting row: {row}")
            print(f"Error: {err}")

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Target customers stored in MySQL database.")
def train_model(file_path, model_path='svm_model.pkl'):
    data = pd.read_csv(file_path)
    data['LastPurchaseDate'] = pd.to_datetime(data['LastPurchaseDate'], format='%d-%m-%Y')
    data['DaysSinceLastPurchase'] = (pd.Timestamp.now() - data['LastPurchaseDate']).dt.days
    data.dropna(inplace=True)

    data['Target'] = ((data['EngagementScore'] > data['EngagementScore'].quantile(0.7)) &
                      (data['PurchaseAmount'] > data['PurchaseAmount'].quantile(0.7))).astype(int)

    X = data[['Age', 'Gender', 'PurchaseAmount', 'DaysSinceLastPurchase', 'EngagementScore', 'State/UT', 'ProductCategory']]
    y = data['Target']

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), ['Age', 'PurchaseAmount', 'DaysSinceLastPurchase', 'EngagementScore']),
        ('cat', OneHotEncoder(), ['Gender', 'State/UT', 'ProductCategory'])
    ])

    pipeline = Pipeline([('preprocessor', preprocessor), ('classifier', SVC())])
    pipeline.fit(X, y)
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")
