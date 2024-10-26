@app.route('/upload', methods=['POST'])
def upload():
    global product_name,product_description
    file = request.files['customer_dataset']
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_description = request.form['product_description']
    product_category = request.form['product_category']
    age_group = request.form['age_group']