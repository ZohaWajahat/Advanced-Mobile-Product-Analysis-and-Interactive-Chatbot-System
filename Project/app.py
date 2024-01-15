from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)

# Load data from the Excel file
df = pd.read_excel('bushogai.xlsx') 

@app.route("/")
def homepage():
    return render_template("chatbot1.html")

@app.route("/ask", methods=["POST"])
def ask_bot():
    user_message = request.form["message"]

    # Search for user query in the loaded DataFrame
    #response = "I'm sorry, I don't have information on that. Is there anything else I can assist you with?"

    # General Question Handling
    if user_message.lower() == "best phones":
        best_phones = df.sort_values(by='Product Price', ascending=False).head(5)  # Get the top 5 highest rated phones
        response = f"The best phones based on ratings are:\n{best_phones['Product Name'].to_string(index=False)}"

    # In-between Questions
    elif "between" in user_message.lower() and "and" in user_message.lower():
        # Logic for range queries
        price_range = [int(s) for s in user_message.split() if s.isdigit()]
        if len(price_range) == 2:
            min_price, max_price = price_range
            phones_in_range = df[(df['Product Price'] >= min_price) & (df['Product Price'] <= max_price)]
            response = f"Phones between {min_price} and {max_price} are:\n{phones_in_range['Product Name'].to_string(index=False)}"
    # Spec-based Queries
    elif "64GB RAM" in user_message and "48MP camera" in user_message:
        spec_phones = df[df['Additional Information'].str.contains("64GB RAM") & df['Additional Information'].str.contains("48MP camera")]
        if not spec_phones.empty:
            response = f"Phones with 64GB RAM and 48MP camera are:\n{spec_phones['Product Name'].to_string(index=False)}"

    # Specific Phones Search
    else:
        matched_product = df[df['Product Name'].str.contains(user_message, case=False)]
        if not matched_product.empty:
            product_details = matched_product[['Product Name', 'Product Price', 'Additional Information', 'Reviews']]
            response = f"Details for '{user_message}':\n{product_details.to_string(index=False)}"

    return response
@app.route('/dashboard')
def dashboard():
    # Clean and convert 'Product Price' column to numeric
    df['Product Price'] = df['Product Price'].replace('[^\d.]', '', regex=True).astype(float)

    # Calculate average price
    avg_price = df['Product Price'].mean()

    # Passing product details and average price to the template
    return render_template('dashboard.html', product_details=None, avg_price=avg_price)



if __name__ == "__main__":
    app.run(debug=True)
