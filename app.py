# app.py

import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'm8GNb5y7h(GVX$fAACJSxfrX'

# Load combined dataset
combined_df = pd.read_csv('combined_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        filtered_df = combined_df[combined_df['Product_name'].str.contains(search_term, case=False, na=False)]
        session['search_results'] = filtered_df.to_dict(orient='records')
    else:
        session.pop('search_results', None)

    return render_template('index.html', products=session.get('search_results', []), shopping_cart=session.get('shopping_cart', []), total_price=session.get('total_price', 0.0))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'shopping_cart' not in session:
        session['shopping_cart'] = []
        session['total_price'] = 0.0

    product_name = request.form['product_name']
    product_price_str = request.form['product_price']
    quantity = int(request.form['quantity'])

    # Extract the numeric part of the price string (e.g., '₹24.00' -> '24.00')
    product_price_str = ''.join(filter(str.isdigit, product_price_str))

    # Convert the price string to a float (e.g., '24.00' -> 24.0)
    product_price = float(product_price_str)/100

    # Check if the product is already in the shopping cart
    for item in session['shopping_cart']:
        if item['product_name'] == product_name:
            item['quantity'] += quantity
            break
    else:
        session['shopping_cart'].append({
            'product_name': product_name,
            'product_price': product_price,
            'quantity': quantity
        })

    # Update the total price
    session['total_price'] = sum(item['product_price'] * item['quantity'] for item in session['shopping_cart'])

    return redirect(request.referrer)

@app.route('/edit_cart', methods=['POST'])
def edit_cart():
    new_quantities = {key: int(value) for key, value in request.form.items() if key.startswith('new_quantity_')}
    delete_product = request.form.get('delete_product')

    if delete_product:
        session['shopping_cart'] = [item for item in session['shopping_cart'] if item['product_name'] != delete_product]
    else:
        for item in session['shopping_cart']:
            if item['product_name'] in new_quantities:
                item['quantity'] = new_quantities[item['product_name']]

    # Update the total price
    session['total_price'] = round(sum(item['product_price'] * item['quantity'] for item in session['shopping_cart']), 2)

    return redirect(url_for('index'))

@app.route('/delete_cart/<product_name>', methods=['POST'])
def delete_cart(product_name):
    # Delete the item from the shopping cart based on the product_name
    session['shopping_cart'] = [item for item in session['shopping_cart'] if item['product_name'] != product_name]

    # Update the total price
    session['total_price'] = sum(item['product_price'] * item['quantity'] for item in session['shopping_cart'])

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
