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
    result = 5
    short = False
    if request.args.get('pgs'):
        pages = int(request.args.get('pgs'))
    if request.args.get('r'):
        result = int(request.args.get('r'))
    if request.args.get('short'):
        short = True
    br = brevis(query=query, lookAmt=pages, resultAmt=result, shortResult=short)
    results = br.main()
    return jsonify(results)