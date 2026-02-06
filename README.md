# ShopSmart – AI Powered E-Commerce Platform

ShopSmart is a full-scale, production-ready e-commerce web application built using Flask, SQLAlchemy, and Bootstrap 5. The platform integrates an AI-powered chatbot using Google Gemini and a product recommendation system based on the Apriori algorithm to enhance user engagement and improve shopping experience.

The project simulates a real-world e-commerce system similar to Amazon or Flipkart and is designed with modular architecture, secure authentication, and deployment readiness.

---

## Features

- Responsive storefront with featured products and category-based listings
- Product browsing with search, filter, sort, and pagination
- Secure user authentication with login and registration
- Role-based access control for Users and Admins
- Shopping cart functionality with checkout simulation
- Order management and order history
- Admin dashboard for managing products and viewing analytics
- AI chatbot powered by Google Gemini for intelligent product queries
- “Frequently Bought Together” recommendations using Apriori algorithm
- Modular Flask architecture using Blueprints

---

## Tech Stack

Backend:
- Python (Flask)
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-Migrate

Frontend:
- HTML5
- Bootstrap 5
- JavaScript

Database:
- SQLite (default)
- MySQL (optional and configurable)

AI and Machine Learning:
- Google Generative AI (Gemini)
- mlxtend (Apriori Algorithm)
- pandas
- numpy

---

## Setup and Installation

Prerequisites:
- Python 3.9 or higher
- Google Gemini API Key

Steps:
1. Clone the repository or extract the project files.
2. Create and activate a virtual environment:
   
   python -m venv venv  
   source venv/bin/activate    (Linux / Mac)  
   venv\Scripts\activate       (Windows)

3. Install dependencies:

   pip install -r requirements.txt

4. Configure environment variables:
   - Review `config.py`
   - Set the `GEMINI_API_KEY` using environment variables or a `.env` file

---

## Running the Application

Local Development:
- Start the application using:

  python run.py

- The application will be available at:
  
  http://127.0.0.1:5000

Production Deployment:
- In production environments such as Render, the application is started using Gunicorn:

  gunicorn run:app

- Access the application using the deployment URL provided by the hosting platform.

---

## Admin Access

Admin registration is not public.

Steps to create an admin user:
1. Register a normal user through the application.
2. Update the user role to `admin` directly in the database.

Example using Flask shell:

from app import create_app, db  
from app.models import User  

app = create_app()  
with app.app_context():  
    user = User.query.first()  
    user.role = 'admin'  
    db.session.commit()

---

## API Endpoints

- POST /api/chatbot  
  Handles chatbot queries and returns AI-generated responses.

- GET /api/recommendations/<product_id>  
  Returns recommended products based on Apriori association rules.

---

## Deployment

The project is deployment-ready and supports cloud hosting.

Render Deployment:
- GitHub-integrated CI/CD
- Gunicorn used as the production WSGI server
- Environment variables managed through Render Dashboard

Docker Support (Optional):

docker build -t shopsmart .  
docker run -p 5000:5000 shopsmart

---

## Project Highlights

- Clean and scalable Flask project structure
- Secure authentication and authorization
- Real-world AI and ML integration in e-commerce
- Cloud deployment compatible
- Suitable for academic projects, demos, and presentations

---

## License

This project is developed for academic and learning purposes only.
