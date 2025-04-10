# Real Time Trading App

## Overview
The Flask Trading App is a web application designed to simulate real-time trading, display financial charts, and provide users with the latest finance news. The application leverages deep learning models to recommend stocks and uses web scraping to gather news from finance websites.

## Features
- Simulate real-time trades
- Display charts of real-time prices using trading APIs
- User authentication (login and registration)
- Trading dashboard with real-time trade simulations
- Deep learning model recommendations for stock performance
- LLM integration to explain stock recommendations
- Latest finance news aggregation

## Project Structure
```
flask-trading-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── scripts.js
│   │   └── images
│   └── utils
│       └── trading.py
├── config.py
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-trading-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the configuration in `config.py` as needed.

4. Run the application:
   ```
   python application.py
   ```

## Usage
- Access the application in your web browser at `http://127.0.0.1:5000`.
- Register a new account or log in to access the trading dashboard.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
