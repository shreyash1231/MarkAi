from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from model import train_model, predict_target_customers, store_target_customers_in_db
import os
import mysql.connector
from flask import session

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global product_name,product_description
    file = request.files['customer_dataset']
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_description = request.form['product_description']
    product_category = request.form['product_category']
    age_group = request.form['age_group']

    session['product_details'] = {
        'name': product_name,
        'description': product_description,
    }

    return redirect(url_for('results', filename='target_customers.csv'))
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Get target customers
    product_details = {
        'name': product_name,
        'price': product_price,
        'description': product_description,
        'category': product_category,
        'age_group': age_group
    }
    
    target_customers = predict_target_customers(file_path, product_details)

    # Store target customers in MySQL database
    store_target_customers_in_db(target_customers)

    # Save the target customers to a CSV file for displaying results
    target_customers_file = os.path.join(UPLOAD_FOLDER, 'target_customers.csv')
    target_customers.to_csv(target_customers_file, index=False)

    # Redirect to the results page with the filename
    return redirect(url_for('results', filename='target_customers.csv'))

@app.route('/next_page')
def next_page():
    return render_template('next.html')

@app.route('/results/<filename>')
def results(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if the file exists before processing it
    if not os.path.isfile(file_path):
        return f'File {filename} not found.'

    # Load the target customers from the CSV file
    target_customers = pd.read_csv(file_path)

    # Select specific columns you want to display
    specific_columns = target_customers[['CustomerID', 'Name', 'Gender', 'Email', 'PhoneNumber', 'State/UT']]

    # Convert to a list of dictionaries for easier rendering in the template
    customers_list = specific_columns.to_dict(orient='records')

    return render_template('results.html', customers=customers_list)

if __name__ == '__main__':
    app.run(debug=True)
