from flask import Flask, render_template, jsonify, request, url_for
import json
import pandas as pd
from retrieve_definition import retrieve_definition


# Create Flask app
app = Flask(__name__)


# Creating the main route for the api page
@app.route('/', methods=['GET', 'POST'])
def home():
    """ Home page of site """
    message = "You are now home"
    return render_template('base.html', message=message)


# Creating a serach route to access retrieve_definition function
@app.route('/search', methods=['GET', 'POST'])
def wiki_search():
    """Accessing wikipedia's api with 
    retrieve_definition function"""
    searchword = request.args.get('word')
    data = retrieve_definition(searchword)
    return data


if __name__ == '__main__':
    app.run(debug=True)
