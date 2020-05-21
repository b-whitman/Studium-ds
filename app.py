from flask import Flask, render_template, jsonify, request, url_for
import json
import pandas as pd
import retrieve_definition
from retrieve_definition import retrieve_definition


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Home page of site """
    message = "You are now home"
    return render_template('base.html', message=message)


@app.route('/search', methods=['GET', 'POST'])
def wiki_search():
    searchword = request.args.get('word')
    data = retrieve_definition(searchword)
    return data


if __name__ == '__main__':
    app.run(debug=True)
