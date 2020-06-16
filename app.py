import calendar_heatmap
from flask import Flask, render_template, jsonify, request, url_for
import json
import os
import pandas as pd
from retrieve_definition import retrieve_definition
import gauge_plot


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

# Create a route to return heatmap
@app.route('/heatmap', methods=['GET', 'POST'])
def calender_heatmap():
    """Returning the plotly visual in html form"""
    month = int(request.args.get('month'))
    year = int(request.args.get('year'))

    # Uses the default values in function if no value is inputted
    if month:
        calendar_heatmap.get_viz(month, year)
    else:
        calendar_heatmap.get_viz()

    return render_template('heatmap.html')

# Create route to delete heatmap
@app.route('/delete_map')
def delete():
    os.remove('templates/heatmap.html')
    return 'File deleted'

# Create route to return gauge plot
@app.route('/gauge')
def plot_gauge():
    streaks = int(request.args.get('streaks'))
    gauge_plot.gauge(streaks)
    return render_template('gauge.html')

# Create route to delete gauge plot
@app.route('/delete_gauge')
def delete_gauge():
    os.remove('templates/gauge.html')
    return 'File deleted'


if __name__ == '__main__':
    app.run(debug=True)
