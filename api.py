from flask import Flask, request, jsonify, send_from_directory
from db import connect_db
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

db = connect_db()
collection = db["articles"]

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/articles', methods=['GET'])
def get_articles():
    category = request.args.get('category')
    author = request.args.get('author')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    title_contains = request.args.get('title_contains')

    query = {}
    if category:
        query['tag'] = category
    if author:
        query['author'] = author
    if start_date and end_date:
        query['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        query['date'] = {'$gte': start_date}
    elif end_date:
        query['date'] = {'$lte': end_date}
    if title_contains:
        query['title'] = {'$regex': title_contains, '$options': 'i'}

    articles = list(collection.find(query))
    for article in articles:
        article['_id'] = str(article['_id'])

    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
