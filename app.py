from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
data = pd.read_csv("Minor Project 2\cosmetic_pre.csv")

# Mapping of skin concerns to skincare ingredients
concern_solution = {
    'acne': 'salicylic acid',
    'dryness': 'hyaluronic acid',
    'hyperpigmentation': 'vitamin c',
    'wrinkles': 'retinol',
    'dark spots': 'niacinamide',
    'uneven texture': 'glycolic acid',
    'dullness': 'vitamin C + E acid'
}

# Define route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Define route for recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    # name = int(input("Enter your name: "))
    # age = int(input("Enter your age: "))
    skin_type = request.form['skin_type']
    price_range = int(request.form['price_range'])
    skin_concern1 = request.form['skin_concern1'].lower()
    skin_concern2 = request.form['skin_concern2'].lower()

    solution1 = concern_solution.get(skin_concern1, '')
    solution2 = concern_solution.get(skin_concern2, '')

    # Logic to recommend skincare products based on user input
    options = data[data[skin_type] == 1][data['price'] <= price_range]
    options = options.sort_values(by='rank', ascending=False)
    options = options[['Label', 'brand', 'name', 'price', 'rank', 'ingredients', 'URL']]
    options = options[options['ingredients'].str.contains(solution1, case=False) | options['ingredients'].str.contains(solution2, case=False)]

    # Filter products by category
    recommended_products = {}
    categories = ['Cleanser', 'Face Mask', 'Treatment', 'Eye cream', 'Moisturizer', 'Sun protect']
    for category in categories:
        recommended_products[category] = options[options['Label'] == category].to_dict(orient='records')

    return jsonify(recommended_products)

if __name__ == '__main__':
    app.run(debug=True)
