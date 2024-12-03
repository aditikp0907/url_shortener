from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///short_links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class URL(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    short_url = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<URL {self.original_url}>"

# Function to Generate Short URL
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Route to Handle Shortening and Display
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            long_url = request.form['long_url']
            company_name = request.form['company_name']
            alias = request.form['alias']

            # Validate URL format
            if not long_url.startswith('http://') and not long_url.startswith('https://'):
                return render_template('index.html', error="Invalid URL. Make sure it starts with http:// or https://")

            # If alias is provided, use it; otherwise, generate one
            if alias:
                short_url = f"{company_name}/{alias}"
            else:
                short_url = f"{company_name}/{generate_short_url()}"

            # Check if the short URL already exists
            if URL.query.filter_by(short_url=short_url).first():
                return render_template('index.html', error="Short URL already exists. Please try a different alias.")

            # Insert the new URL into the database
            new_url = URL(original_url=long_url, company_name=company_name, short_url=short_url)
            db.session.add(new_url)
            db.session.commit()

            # Return the generated short URL and show it on the same page
            short_url_link = f"http://127.0.0.1:5000/{short_url}"  # Update this when hosting online
            return render_template('index.html', short_url=short_url_link)
        
        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {e}")

    return render_template('index.html')


@app.route('/<company_name>/<short_url>')
def redirect_to_url(company_name, short_url):
    # Find the URL by its short URL and company name
    url_data = URL.query.filter_by(short_url=f"{company_name}/{short_url}").first()

    # If URL not found, display an error
    if not url_data:
        return render_template('index.html', error="Short URL not found!")

    # Redirect to the original URL
    return redirect(url_data.original_url)

# Create the database tables when the app starts
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
