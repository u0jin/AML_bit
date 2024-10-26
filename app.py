import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils import get_address_info, get_detailed_transactions, create_transaction_flow_visualization

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "your-secret-key-here"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL"
) or "sqlite:///local.db"  # Use local database for development
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database
db.init_app(app)

with app.app_context():
    import models
    db.create_all()

# Address information route
@app.route('/address/<string:address>')
def address_info(address):
    from models import SuspiciousAddress
    address_info = SuspiciousAddress.query.filter_by(address=address).first()  # address_info 변수는 정말 필요하지 않다면 제거하십시오
    if not address_info:
        return "Address not found", 404

    # API로부터 주소 정보를 가져옵니다
    address_data = get_address_info(address)
    transactions = get_detailed_transactions(address)
    transaction_viz = None
    if transactions:
        transaction_viz = create_transaction_flow_visualization(transactions, address)

    return render_template(
        'result.html',
        address=address,
        address_info=address_data,
        transaction_viz=transaction_viz,
        suspicious=address_info  # SuspiciousAddress 객체 자체를 전달
    )

# Check address route
@app.route('/check_address', methods=['POST'])
def check_address():
    address = request.form.get('address')
    return redirect(url_for('address_info', address=address))

# Report address route
@app.route('/report_address', methods=['GET', 'POST'])
def report_address():
    if request.method == 'POST':
        address = request.form.get('address')
        flash('Address reported successfully', 'success')
        return redirect(url_for('home'))
    return render_template('report.html')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)