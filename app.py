# app.py
from flask import Flask, request, render_template, redirect, url_for, session
import os
from em import generate_marketing_emails  # Import the function from em.py
from model import train_model, predict_target_customers, store_target_customers_in_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['customer_dataset']
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_description = request.form['product_description']
    product_category = request.form['product_category']
    age_group = request.form['age_group']

    # Store product details in session
    session['product_details'] = {
        'name': product_name,
        'description': product_description,
        'price': product_price
    }

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Pass product details and file path to model.py functions
    product_details = {
        'name': product_name,
        'price': product_price,
        'description': product_description,
        'category': product_category,
        'age_group': age_group
    }

    # Train the model and predict target customers
    train_model(file_path)  # Train the model with the uploaded dataset
    target_customers = predict_target_customers(file_path, product_details)

    # Store target customers in the database
    store_target_customers_in_db(target_customers)

    # Save target customers to a CSV for displaying results
    target_customers_file = os.path.join(UPLOAD_FOLDER, 'target_customers.csv')
    target_customers.to_csv(target_customers_file, index=False)

    # Generate marketing emails using em.py
    generate_marketing_emails(session['product_details'], file_path)

    # Redirect to the results page
    return redirect(url_for('results', filename='target_customers.csv'))

@app.route('/results/<filename>')
def results(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.isfile(file_path):
        return f'File {filename} not found.'

    # Load the target customers from the CSV file
    target_customers = pd.read_csv(file_path)
    customers_list = target_customers[['CustomerID', 'Name', 'Gender', 'Email', 'PhoneNumber', 'State/UT']].to_dict(orient='records')

    return render_template('results.html', customers=customers_list)

if __name__ == '__main__':
    app.run(debug=True)
