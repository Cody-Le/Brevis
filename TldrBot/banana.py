from flask import Flask, request, jsonify
from flask_cors import CORS
from brevis import brevis
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'hello'



@app.route('/main')
def main():
    query = request.args.get('q')
    pages = 15
    if request.args.get('pgs'):
        pages = int(request.args.get('pgs'))
    br = brevis(query=query, lookAmt=pages)
    results = br.main()
    return jsonify(results)