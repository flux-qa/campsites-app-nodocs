# SentimentAnalyzer

## Background
SentimentAnalyzer is a sentiment analysis tool designed to analyze text data and determine the sentiment polarity (positive, negative, or neutral). It provides a simple yet powerful API for processing text and extracting sentiment insights.

## Technologies Used
Backend:
Python 3.9
FastAPI 0.68.0
NLTK 3.6.3
scikit-learn 0.24.2


Frontend:
Vue.js 3.2.4
Bootstrap 5.3.0


## Getting Started
Follow these instructions to set up and run SentimentAnalyzer on your local machine:


Install backend dependencies:
```bash
pip install -r requirements.txt
```

Install frontend dependencies:
```bash
cd frontend
npm install
```

Start the backend server:
```bash
uvicorn main:app --reload
```

In a separate terminal, start the frontend development server:
```bash
npm run serve
```
Open your web browser and navigate to http://localhost:8080 to access the SentimentAnalyzer interface.

## License
This project is licensed under the Apache License 2.0