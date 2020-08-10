#attempting to create measurements of comparative metrics
#for daily show comparison of today to previous day, weekly for previous week, and monthly for previous month
#will need to recalculate all the stats each time to compare
#then return either a positive or negative integer, the appropriate arrow, and a hex code for color
#up arrow = u"\u2191"
#down arrow = u"\u2193"
#green = 09B109
#red = CE2929

import pandas as pd
import datetime
from datetime import timedelta
import numpy as np

##replace this code with actual access to user data
test_data = pd.read_csv('https://raw.githubusercontent.com/Lambda-School-Labs/Studium-ds/viz-session-quality/test_data/mean_cards_test.csv')

def get_session_length(df):
    ''' Calculate length of session in seconds'''
    df['session_start'] = pd.to_datetime(df['session_start'])
    df['session_end'] = pd.to_datetime(df['session_end'])
    time_deltas = df['session_end'] - df['session_start']
    session_length = []
    for d in time_deltas:
        session_length.append(d.total_seconds())
    return session_length

def get_start_hour(df):
    '''Isolate start hour from datetime object'''
    start_hour = []
    for t in df['session_start']:
        start_hour.append(t.hour)
    return start_hour


def get_cards_per_min(df):
    '''Calculate cards viewed per minute'''
    cards_per_min = (df['total_looked_at'] / df['session_length']) * 60
    return cards_per_min

def daily_cards_min_comparison(df):
    today = datetime.date.today()
    yesterday = today - timedelta(days=1)
    todays_per_min = []
    yesterday_per_min = []
    for row in df:
        if row['session_start'].date() == today:
            per_min = get_cards_per_min(row)
            todays_per_min.append(per_min)
        if row['session_start'].date() == yesterday:
            per_min = get_cards_per_min(row)
            yesterday_per_min.append(per_min)
    if len(todays_per_min) > 0 and len(yesterday_per_min) > 0:
        today_average = sum(todays_per_min) / len(todays_per_min)
        yesterday_average = sum(yesterday_per_min) / len(yesterday_per_min)
    elif len(todays_per_min) == 0:
        today_average = 0
    elif len(yesterday_per_min) == 0:
        yesterday_average = 0
    if today_average > yesterday_average:
        color_code = "09B109"
        arrow = u"\u2191"
    elif today_average < yesterday_average:
        color_code = "CE2929"
        arrow = u"\u2193"
    else:
        color_code = "000000"
        arrow = u"\u003D"
    difference = (today_average - yesterday_average) / yesterday_average * 100
    s = f"{difference}% {arrow}"
    return s, color_code

def monthly_per_min_comparison(df):
    month = datetime.datetime.now().month
    last_month = month - timedelta(month=1)
    year = datetime.datetime.now().year
    month_per_min = []
    lastmonth_per_min = []
    for row in df:
        if row['session_start'].date().month == month and row['session_start'].date().year == year:
            per_min = get_cards_per_min(row)
            month_per_min.append(per_min)
        if row['session_start'].date().month == last_month and row['session_start'].date().year == year:
            per_min = get_cards_per_min(row)
            lastmonth_per_min.append(per_min)
    if len(month_per_min) > 0 and len(lastmonth_per_min) > 0:
        month_average = sum(month_per_min) / len(month_per_min)
        lastmonth_average = sum(lastmonth_per_min) / len(lastmonth_per_min)
    elif len(month_per_min) == 0:
        month_average = 0
    elif len(lastmonth_per_min) == 0:
        lastmonth_average = 0
    if month_average > lastmonth_average:
        color_code = "09B109"
        arrow = u"\u2191"
    elif month_average < lastmonth_average:
        color_code = "CE2929"
        arrow = u"\u2193"
    else:
        color_code = "000000"
        arrow = u"\u003D"
    difference = (month_average - lastmonth_average) / lastmonth_average * 100
    s = f"{difference}% {arrow}"
    return s, color_code
