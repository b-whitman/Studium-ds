import os
from datetime import datetime
import json
import pandas as pd
from typing import List
import uvicorn

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from autogenerate_decks import autogenerate
from comparative_metrics import *
from retrieve_definition import retrieve_definition
from leitner import leitner_dates
from viz_leitner import leitner_bar


# Creating FastApi
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining the templating directeroy
templates = Jinja2Templates(directory="templates")


# A Pydantic model to parse through JSON data
class Card(BaseModel):
    id : str
    is_starred : bool
    comfort_level : int

class User(BaseModel):
    id : str
    total_looked_at : int
    session_start : int
    session_end : int


@app.get("/")
async def root():
    """
    Verifies the API is deployed, and links to the docs
    """
    return HTMLResponse("""
    <h1>Studium DS API</h1>
    <p>Go to <a href="/docs">/docs</a> for documentation.</p>
    """)


# Creating a serach route to access retrieve_definition function
@app.get('/search')
async def wiki_search(word: str):
    """Accessing wikipedia's api and returns
    first 300 characters for a given term"""
    data = retrieve_definition(word)
    if isinstance(data, str):
        json = {"msg": data}
        data_json = jsonable_encoder(json)
        return data_json
    else:
        return data


# Create route to return gauge plot
@app.post('/leitner_bar')
async def plot_gauge(comfort_level : list = []):
    """Takes a list of comfort levels as integers 
    and returns the lietner levels plot in plotly json object"""
    lietner_img = leitner_bar(comfort_level)
    return lietner_img


@app.get('/autogenerate_deck')
async def autogenerate_search(word: str):
    """Function to generate a set of extracts from a 
    single user-entered term using the Wikipedia API"""
    data = autogenerate(word)
    data_json = jsonable_encoder(data)
    return data_json


@app.post('/leitner')
async def leitner_system(user: List[Card]):
    """Function to analyze card-by-card user data after a study session
    and apply leitner system spaced repetition to it """
    df = pd.DataFrame([dict(card) for card in user])
    df_modified = df.apply(leitner_dates, axis=1)
    data_json = df_modified.to_json(orient='records', indent=2)
    return Response(data_json)


@app.post('/metrics')
async def get_metrics(user_data: List[User]):
    """Function to get all user metrics needed. Returns an array of objects [daily, weekle, monthly] 
    cards per minute and best sessions including percentage difference, 
    unicode for the (up/down/equal) sign, and a color code"""
    df = pd.DataFrame([dict(x) for x in user_data])

    # saving each function's result into a variable
    daily_cards = daily_cards_min_comparison(df)
    weekly_cards = weekly_per_min_comparison(df)
    monthly_cards = monthly_per_min_comparison(df)

    best_daily = best_session_daily(df)
    best_weekly = best_session_weekly(df)
    best_monthly = best_session_monthly(df)

    daily_viewed_card = daily_viewed(df)
    weekly_viewed_card = weekly_viewed(df)
    monthly_viewed_card = monthly_viewed(df)


    # return all metrics data as an array of JSON objects
    metrics_data = [daily_cards, weekly_cards, monthly_cards,
                    best_daily, best_weekly, best_monthly,
                    daily_viewed_card, weekly_viewed_card, monthly_viewed_card]
    print(metrics_data)
    
    return metrics_data



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
