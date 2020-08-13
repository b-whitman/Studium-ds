import pandas as pd
import datetime
from datetime import timedelta

pd.set_option('mode.chained_assignment', None)

# replace this code with actual access to user data
test_data = pd.read_csv(
    'https://raw.githubusercontent.com/Lambda-School-Labs/Studium-ds/viz-session-quality/test_data/mean_cards_test.csv')


def get_session_length(row):
    """ Calculate length of session in seconds"""
    time_delta = row['session_end'] - row['session_start']
    session_length = time_delta.total_seconds()
    return session_length


def get_cards_per_min(row):
    """Calculate cards viewed per minute"""
    row['session_length'] = get_session_length(row)
    cards_per_min = (row['total_looked_at'] / row['session_length']) * 60
    return cards_per_min


def convert_to_datetime(df):
    """Convert seconds since epoch timestamp to pandas datetime object"""
    df['session_start'] = pd.to_datetime(df['session_start'], unit='s')
    df['session_end'] = pd.to_datetime(df['session_end'], unit='s')
    return df


def convert_to_datetime_test_data(df):
    """Convert datetime strings to pandas datetime object"""
    df['session_start'] = pd.to_datetime(df['session_start'])
    df['session_end'] = pd.to_datetime(df['session_end'])
    return df


def daily_cards_min_comparison(df):
    """Function to compare today's avg cards per minute to yesterday's. Returns a string consisting of the absolute value of the
    difference and the unicode for an upward (positive) or downward (negative) arrow, and a hex color code (red for
    negative, green for positive), today's average, and yesterday's average  """
    df = convert_to_datetime_test_data(df)
    # IMPORTANT!
    # FIX THIS LINE BEFORE SENDING TO HEROKU!
    today = datetime.date.today()
    yesterday = today - timedelta(days=1)
    todays_per_min = []
    yesterday_per_min = []
    # this iterates over each row in the dataframe, applying the logic and adding the cards_per_min value to the
    # appropriate list
    for index, row in df.iterrows():
        if row['session_start'].date() == today:
            per_min = get_cards_per_min(row)
            todays_per_min.append(per_min)
        if row['session_start'].date() == yesterday:
            per_min = get_cards_per_min(row)
            yesterday_per_min.append(per_min)
    if len(todays_per_min) > 0 and len(yesterday_per_min) > 0:
        # if both days have data, then calculate the average of the list
        today_average = sum(todays_per_min) / len(todays_per_min)
        yesterday_average = sum(yesterday_per_min) / len(yesterday_per_min)
    elif len(todays_per_min) == 0:
        # if no cards viewed today, cards per min average is 0
        today_average = 0
    elif len(yesterday_per_min) == 0:
        yesterday_average = 0
    if today_average > yesterday_average:
        color_code = "09B109"
        # hex color code for green
        arrow = u"\u2191"
        # unicode for upward arrow
    elif today_average < yesterday_average:
        color_code = "CE2929"
        # hex color code for red
        arrow = u"\u2193"
        # unicode for downward arrow
    else:
        color_code = "000000"
        # hex color code for black
        arrow = u"\u003D"
        # unicode for equal sign
    try:
        difference = abs((today_average - yesterday_average) / yesterday_average * 100)
    except ZeroDivisionError:
        # if no cards viewed yesterday, cards per min up 100% today
        # if both averages are zero, this will display 100% = in black
        difference = 100
    s = f"{difference:.2f}% {arrow}"
    return s, color_code, today_average,


def weekly_per_min_comparison(df):
    """Function to compare this week's avg cards per minute to last week's. Returns a string consisting of the absolute value of the
    difference and the unicode for an upward (positive) or downward (negative) arrow, and a hex color code (red for
    negative, green for positive), this week's average, and last week's average """
    df = convert_to_datetime_test_data(df)
    # FIX THIS LINE
    today = datetime.date.today()
    this_week_start = today - timedelta(days=7)
    last_week_start = today - timedelta(days=14)
    week_per_min = []
    lastweek_per_min = []
    for index, row in df.iterrows():
        if row['session_start'].date() >= this_week_start:
            per_min = get_cards_per_min(row)
            week_per_min.append(per_min)
        if last_week_start <= row['session_start'].date() < this_week_start:
            per_min = get_cards_per_min(row)
            lastweek_per_min.append(per_min)
    if len(week_per_min) > 0 and len(lastweek_per_min) > 0:
        week_average = sum(week_per_min) / len(week_per_min)
        lastweek_average = sum(lastweek_per_min) / len(lastweek_per_min)
    elif len(week_per_min) == 0:
        week_average = 0
    elif len(lastweek_per_min) == 0:
        lastweek_average = 0
    if week_average > lastweek_average:
        color_code = "09B109"
        arrow = u"\u2191"
    elif week_average < lastweek_average:
        color_code = "CE2929"
        arrow = u"\u2193"
    else:
        color_code = "000000"
        arrow = u"\u003D"
    try:
        difference = abs((week_average - lastweek_average) / lastweek_average * 100)
    except ZeroDivisionError:
        difference = 100
    s = f"{difference:.2f}% {arrow}"
    return s, color_code, week_average


def monthly_per_min_comparison(df):
    """Function to compare today's stats to yesterday's. Returns a string consisting of the absolute value of the
    difference and the unicode for an upward (positive) or downward (negative) arrow, and a hex color code (red for
    negative, green for positive) """
    df = convert_to_datetime_test_data(df)
    # FIX THIS LINE
    today = datetime.date.today()
    this_month_start = today - timedelta(days=30)
    last_month_start = today - timedelta(days=60)
    month_per_min = []
    lastmonth_per_min = []
    for index, row in df.iterrows():
        if row['session_start'].date() >= this_month_start:
            per_min = get_cards_per_min(row)
            month_per_min.append(per_min)
        if last_month_start <= row['session_start'].date() < this_month_start:
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
    try:
        difference = abs((month_average - lastmonth_average) / lastmonth_average * 100)
    except ZeroDivisionError:
        difference = 100
    s = f"{difference:.2f}% {arrow}"
    return s, color_code, month_average


def best_session_length(df):
    """Takes in dataframe of user session data and returns best session length in minutes (best session being session
    with highest cards per minute """
    if len(df) == 0:
        best_length = 0
        # if no data in dataframe, return 0
    else:
        df = convert_to_datetime_test_data(df)
        # FIX TO NON-TEST FUNCTION
        df = df.reindex(columns=df.columns.tolist() + ['cards_per_min', 'session_length'])
        # adds necessary columns to dataframe
        for index, row in df.iterrows():
            df['session_length'].loc[index] = get_session_length(row)
            df['cards_per_min'].loc[index] = get_cards_per_min(row)
        df = df.sort_values(by=['cards_per_min'], ascending=False)
        # sorts dataframe and puts highest cards per minute at the top
        best_length = (df['session_length'].iloc[0] / 60)
        # converts session length in seconds to minutes
    return best_length


def best_session_daily(df):
    """Function to determine the best session length in minutes for today and yesterday. Takes in a
    user session dataframe and returns today's best session length as an integer,
    a string of the difference in percent and the unicode for up arrow or down arrow, and a color code"""
    df = convert_to_datetime_test_data(df)
    today = datetime.date.today()
    yesterday = today - timedelta(days=1)
    today_card_ids = []
    yesterday_card_ids = []
    for index, row in df.iterrows():
        if row['session_start'].date() == today:
            today_card_ids.append(row['id'])
        elif row['session_start'].date() == yesterday:
            yesterday_card_ids.append(row['id'])
    today = df[df['id'].isin(today_card_ids)]
    yesterday = df[df['id'].isin(yesterday_card_ids)]
    today_best_session = best_session_length(today)
    yesterday_best_session = best_session_length(yesterday)
    if today_best_session > yesterday_best_session:
        color_code = "09B109"
        arrow = u"\u2191"
    elif today_best_session < yesterday_best_session:
        color_code = "CE2929"
        arrow = u"\u2193"
    else:
        color_code = "000000"
        arrow = u"\u003D"
    try:
        difference = abs((today_best_session - yesterday_best_session) / yesterday_best_session * 100)
    except ZeroDivisionError:
        # if no sessions yesterday, best session is up 100%
        difference = 100
    s = f"{difference:.2f}% {arrow}"
    return today_best_session, s, color_code


def best_session_weekly(df):
    """Function to determine the best session length in minutes for this week and last week. Takes in a
    user session dataframe and returns this week's best session length as an integer,
    a string of the difference in percent and the unicode for up arrow or down arrow, and a color code"""
    df = convert_to_datetime_test_data(df)
    # FIX THIS LINE
    today = datetime.date.today()
    this_week_start = today - timedelta(days=7)
    last_week_start = today - timedelta(days=14)
    this_week_card_ids = []
    lastweek_card_ids = []
    for index, row in df.iterrows():
        if row['session_start'].date() >= this_week_start:
            this_week_card_ids.append(row[id])
        elif last_week_start <= row['session_start'].date() < this_week_start:
            lastweek_card_ids.append(row[id])
    thisweek = df[df['id'].isin(this_week_card_ids)]
    lastweek = df[df['id'].isin(lastweek_card_ids)]
    thisweek_best_session = best_session_length(thisweek)
    lastweek_best_session = best_session_length(lastweek)
    if thisweek_best_session > lastweek_best_session:
        color_code = "09B109"
        arrow = u"\u2191"
    elif thisweek_best_session < lastweek_best_session:
        color_code = "CE2929"
        arrow = u"\u2193"
    else:
        color_code = "000000"
        arrow = u"\u003D"
    try:
        difference = abs((thisweek_best_session - lastweek_best_session) / lastweek_best_session * 100)
    except ZeroDivisionError:
        # if no sessions last week, best session is up 100%
        difference = 100
    s = f"{difference:.2f}% {arrow}"
    return thisweek_best_session, s, color_code


def best_session_monthly(df):
    """Function to determine the best session length in minutes for this month and last month. Takes in a
    user session dataframe and returns this month's best session length as an integer,
    a string of the difference in percent and the unicode for up arrow or down arrow, and a color code"""
    df = convert_to_datetime_test_data(df)
    # FIX THIS LINE
    today = datetime.date.today()
    this_month_start = today - timedelta(days=30)
    last_month_start = today - timedelta(days=60)
    this_month_card_ids = []
    lastmonth_card_ids = []
    for index, row in df.iterrows():
        if row['session_start'].date() >= this_month_start:
            this_month_card_ids.append(row[id])
        elif last_month_start <= row['session_start'].date() < this_month_start:
            lastmonth_card_ids.append(row[id])
    thismonth = df[df['id'].isin(this_month_card_ids)]
    lastmonth = df[df['id'].isin(lastmonth_card_ids)]
    thismonth_best_session = best_session_length(thismonth)
    lastmonth_best_session = best_session_length(lastmonth)
    if thismonth_best_session > lastmonth_best_session:
        color_code = "09B109"
        arrow = u"\u2191"
    elif thismonth_best_session < lastmonth_best_session:
        color_code = "CE2929"
        arrow = u"\u2193"
    else:
        color_code = "000000"
        arrow = u"\u003D"
    try:
        difference = abs((thismonth_best_session - lastmonth_best_session) / lastmonth_best_session * 100)
    except ZeroDivisionError:
        # if last month has no sessions, the difference is up 100%
        difference = 100
    s = f"{difference:.2f}% {arrow}"
    return thismonth_best_session, s, color_code
