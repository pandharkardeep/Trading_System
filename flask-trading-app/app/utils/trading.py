from flask import current_app
import requests
import random

def simulate_trade(user_id, stock_symbol, buy_price, sell_price, quantity):
    buy_date = datetime.strptime(buy_date, '%Y-%m-%d')
    sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
    time_diff_years = (sell_date - buy_date).days / 365.25

    # Calculate the inflation factor
    inflation_rate = 0.06
    inflation_factor = (1 + inflation_rate) ** time_diff_years

    # Adjust the buy price for inflation
    adjusted_buy_price = buy_price * inflation_factor

    # Calculate profit or loss
    total_buy = adjusted_buy_price * quantity
    total_sell = sell_price * quantity
    profit_or_loss = total_sell - total_buy

    if profit_or_loss > 0:
        return f"User {user_id} made a profit of ${profit_or_loss:.2f} by selling {quantity} shares of {stock_symbol}."
    else:
        return f"User {user_id} incurred a loss of ${-profit_or_loss:.2f} by selling {quantity} shares of {stock_symbol}."


def fetch_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return [
            (stock["symbol"], stock["price"], stock["changesPercentage"], stock["change"])
            for stock in response.json()[:10]  # Get top 10
        ]
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []
        
def get_real_time_price(stock_symbols, api_key):
    """
    Fetches real-time prices for multiple stock symbols using Financial Modeling Prep API.
    :param stock_symbols: List of stock symbols (e.g., ['AAPL', 'TSLA', '^GSPC'])
    :param api_key: Your FMP API key
    :return: Dictionary of stock symbols and their prices (e.g., {'AAPL': 150.0, 'TSLA': 250.0})
    """
    # Convert list of symbols to a comma-separated string
    symbols = ",".join(stock_symbols)
   
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbols}"
    params = {"apikey": api_key}
    
    response = requests.get(url, params=params)
 
    return fetch_data(url, params)

def get_top_performers(api_key):
    gainers_url = "https://financialmodelingprep.com/api/v3/stock_market/gainers"
    losers_url = "https://financialmodelingprep.com/api/v3/stock_market/losers"
    
    params = {"apikey": api_key}

    

    top_performers = fetch_data(gainers_url, params)
    bad_performers = fetch_data(losers_url, params)

    return top_performers, bad_performers

def fetch_financial_news():
    # Placeholder for news fetching logic
    # This should use a web scraping tool or API
    api_key = "NEWS_API_KEY"
    response = requests.get(f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}")
    if response.status_code == 200:
        return response.json().get('articles')
    else:
        return []
