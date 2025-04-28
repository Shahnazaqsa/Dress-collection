from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample product data for abayas
products = [
    {
        'id': 1,
        'name': 'Elegant Black Abaya',
        'price': 120.00,
        'image': 'pictures/fashion-model-black-trenchcoat-beige-handbag.jpg',
        'description': 'Elegant black abaya with intricate embroidery.'
    },
    {
        'id': 2,
        'name': 'Pink Floral Abaya',
        'price': 150.00,
        'image': 'pictures/full-shot-woman-posing-with-pink-hijab.jpg',
        'description': 'Beautiful green floral abaya perfect for special occasions.'
    },
    {
        'id': 3,
        'name': 'Off White Classic Abaya',
        'price': 130.00,
        'image': 'pictures/beautiful-woman-wearing-hijab.jpg',
        'description': 'Classic off white abaya with modern design.'
    },
    {
        'id': 4,
        'name': 'Stylish Abaya 1',
        'price': 140.00,
        'image': 'pictures/1cbafed2-2e58-43ad-b9f6-ea4b5ece76b8.jpg',
        'description': 'Stylish abaya with modern design.'
    },
    {
        'id': 5,
        'name': 'Stylish Abaya 2',
        'price': 110.00,
        'image': 'pictures/2937.jpg',
        'description': 'Elegant abaya with classic touch.'
    },
     {
        'id': 6,
        'name': 'woman-long-dress-headscarf',
        'price': 210.00,
        'image': 'pictures/woman-long-dress-headscarf.jpg',
        'description': 'Elegant abaya with pink touch.'
    }
    
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart_items.items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            total += item_total
            items.append({'product': product, 'quantity': quantity, 'total': item_total})
    return render_template('cart.html', items=items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # For simplicity, just clear the cart and show a thank you message
        session.pop('cart', None)
        return render_template('checkout.html', success=True)
    return render_template('checkout.html', success=False)

@app.route('/faq')
def faq():
    faqs = [
        {
            'question': 'What is the return policy?',
            'answer': 'You can return any item within 30 days of purchase for a full refund.'
        },
        {
            'question': 'Do you offer international shipping?',
            'answer': 'Yes, we ship worldwide. Shipping fees and times vary by location.'
        },
        {
            'question': 'How can I track my order?',
            'answer': 'Once your order ships, you will receive a tracking number via email.'
        },
        {
            'question': 'Can I change or cancel my order?',
            'answer': 'Orders can be changed or canceled within 24 hours of placement.'
        }
    ]
    return render_template('faq.html', faqs=faqs)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )
