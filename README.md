Inventra - AI-Powered Inventory & Business Management System

Inventra is an AI-powered inventory and business management system designed to help businesses manage products, billing, suppliers, sales, and inventory while using machine learning for demand forecasting and stock-level recommendations.

Features

- Inventory management
- Product management
- Billing and sales management
- Supplier management
- Sales analytics
- Inventory stock-level monitoring
- Demand forecasting
- AI/ML-based stock recommendations
- Persistent data storage using Supabase
- Interactive web interface using Streamlit

Machine Learning

Inventra uses machine learning to support inventory decision-making.

Demand Forecasting

The system analyzes historical sales data to predict future product demand.

Stock Recommendations

Predicted demand is used to provide stock-level recommendations, helping identify products that may require restocking.

Tech Stack

Programming

- Python

Machine Learning

- Scikit-learn
- Regression
- Data preprocessing
- Model evaluation

Data & Libraries

- Pandas
- NumPy

Application

- Streamlit

Database

- Supabase

Project Architecture

Inventra
│
├── Dashboard
├── Billing
├── Inventory Management
├── Supplier Management
├── Sales Dashboard
├── Product Recommendations
└── Demand Forecasting

How to Run

1. Clone the repository

git clone https://github.com/DilpreetSingh-rgb/Inventra.git
cd Inventra

2. Install dependencies

pip install -r requirements.txt

3. Configure Supabase

Create a Supabase project and configure the required credentials using Streamlit secrets.

Example:

SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"

Never commit your actual credentials to GitHub.

4. Run the application

streamlit run app.py

The application will open in your browser.

Project Highlights

- Built a full-stack inventory and business management application.
- Integrated machine learning for demand prediction.
- Implemented automated stock-level recommendations.
- Integrated Supabase for persistent data storage.
- Developed interactive dashboards and business analytics using Streamlit.

Author

Dilpreet Singh

B.Tech CSE - Artificial Intelligence & Machine Learning

GitHub: https://github.com/DilpreetSingh-rgb

LinkedIn: https://linkedin.com/in/dilpreet-singh-45170628a/

License

This project is developed for educational and portfolio purposes.
