from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from passlib.hash import bcrypt
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from utils.trading import simulate_trade, get_real_time_price, fetch_financial_news, get_top_performers
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from utils.predict import make_prediction
from datetime import datetime
from urllib.parse import urlparse
from flask_session import Session
main = Blueprint('main', __name__)
client = MongoClient('mongodb+srv://pandharkardeep35:7762Q0QmsBVhYqLF@deep.pfmz7xz.mongodb.net')
from flask_login import LoginManager

user_db = client['Users']
trade_db = client['Trades']
portfolio_db = client['portfolio_db']
portfolio_collection = portfolio_db['portfolio']
fmp_api_key = "3hm0DNDCC5NhmWRn1TDxIoHlDZnmLCLd"
@main.route('/')
def index():
    news = fetch_financial_news()
    return render_template('index.html', news=news)

@main.route('/login', methods=['GET', 'POST'])
def login():
   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = user_db.users.find_one({'username': username})
        print(user_data)
        if user_data:
            global user
            user = User(username=user_data['username'], email=user_data['email'], password=user_data['password_hash'])
            #print("Came till here", check_password_hash(password, user.password_hash))
            if password == user_data["password_hash"]:
                print(session)
                login_user(user, remember = True)
                print(session)
                print(f"User logged in successfully: {current_user.is_authenticated}")  # Debug print
            
            # Handle the 'next' parameter properly
                
                next_page = url_for('main.dashboard')
                return redirect(next_page)
        else:
            flash('Invalid username or password', 'danger')
            #print(session.get('_flashes'))
       

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username = username, email = email, password = password)
        user_db.users.insert_one({
            'username': new_user.username,
            'email': new_user.email,
            'password_hash': new_user.password_hash
        })
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

def get_user_shares(user_id, stock_symbol):
    """
    Fetch the number of shares a user owns for a specific stock from the portfolio.
    """
    portfolio_entry = portfolio_collection.find_one({"user_id": user_id, "stock_symbol": stock_symbol})
    print(portfolio_entry)
    return portfolio_entry["total_shares"] if portfolio_entry else 0

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print(session)
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect(url_for('main.login', next=request.url))
    stock_symbol = request.args.get('stock-symbol', 'AAPL')  # Default to 'AAPL' if no symbol is provided
    if request.method == 'POST':
        price_per_share = get_real_time_price([stock_symbol], fmp_api_key)
        (sym, price_per_share, *_) = price_per_share[0]
        stop_loss = request.form.get('stop_loss', 0)
        disclosed_quantity = int(request.form['quantity'])
        bulk_deal = request.form.get('bulk_deal', 'off') == 'on'
        total_amount = price_per_share * disclosed_quantity
        trade_type = request.form['trade_type']
          
        if trade_type == "buy":
            trade_db.trades.insert_one({
            'user_id' : current_user.get_id(),
            'stock_symbol': stock_symbol,
            'buying_price_per_share': price_per_share,
            'trade_type' : trade_type,
            'stop_loss': stop_loss if stop_loss else None,
            'disclosed_quantity': disclosed_quantity,
            'bulk_deal': bulk_deal,
            'total_amount': total_amount,
            'trade_date': datetime.utcnow()
            })
            flash(f'Bought {disclosed_quantity} shares of {stock_symbol} at ${price_per_share:.2f} each on {datetime.utcnow()}.', 'success')
            portfolio_collection.update_one(
                {"user_id": current_user.get_id(), "stock_symbol": stock_symbol},
                {"$inc": {"total_shares": disclosed_quantity}},  # Increment shares
                upsert=True  # Create entry if not exists
            )
        else:
            user_shares = get_user_shares(user_id=current_user.get_id(), stock_symbol=stock_symbol)
            print(f"User has {user_shares} shares of {stock_symbol}, trying to sell {disclosed_quantity}")
            
            if user_shares < disclosed_quantity:
                flash(f'You do not have enough shares to sell', 'danger')
                return redirect(url_for('main.dashboard'))  # Return before making any changes
            else:
            # Only update if the user has enough shares
                result = portfolio_collection.update_one(
                    {"user_id": current_user.get_id(), "stock_symbol": stock_symbol},
                    {"$inc": {"total_shares": -disclosed_quantity}}
                )
                trade_db.trades.insert_one({
                    'user_id' : current_user.get_id(),
                    'stock_symbol': stock_symbol,
                    'buying_price_per_share': price_per_share,
                    'trade_type' : trade_type,
                    'stop_loss': stop_loss if stop_loss else None,
                    'disclosed_quantity': disclosed_quantity,
                    'bulk_deal': bulk_deal,
                    'total_amount': total_amount,
                    'trade_date': datetime.utcnow()
                })
                print(f"Updated portfolio: Matched {result.matched_count}, Modified {result.modified_count}")

                flash(f'Sold {disclosed_quantity} shares of {stock_symbol} at ${price_per_share:.2f} each on {datetime.utcnow()}.', 'success')
    #indices = ['^GSPC', '^IXIC', '^DJI', '^VIX']  # S&P 500, Nasdaq, Dow Jones, Volatility Index
    stocks = ['AAPL', 'TSLA', 'NFLX', 'GOOGL', 'MSFT', 'DBRX', 'CRM'] 
    top_performers, bad_performers = get_top_performers(fmp_api_key)
    
    all_symbols = stocks
    trades = list(trade_db.trades.find({'user_id': current_user.get_id()}))
    portfolio = list(portfolio_collection.find({'user_id': current_user.get_id()}))
    real_time_price = get_real_time_price(all_symbols, fmp_api_key)
    
    news = fetch_financial_news()
    return render_template('dashboard.html', trades=trades, prices=real_time_price, top_performers = top_performers, bad_performers = bad_performers,  news=news, stock_symbol=stock_symbol, portfolio=portfolio)




@main.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    symbol = request.form['symbol']
    prediction = make_prediction(symbol)
    if prediction == -1:
        flash("Invalid stock symbol. Please enter a valid one.", "error")
        return redirect(url_for('main.dashboard'))
    result = "Will Make Profit" if prediction > 0 else "Won't Make any profit"
    return render_template('prediction_result.html', symbol=symbol, result=result)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

