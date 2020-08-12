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
import gauge_plot
from retrieve_definition import retrieve_definition
from leitner import leitner_dates


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
    card_id : str
    isStarred : bool
    comfortLevel : int


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
@app.post('/gauge')
async def plot_gauge(request: Request, streaks: int):
    """Return the streaks gauge plot in encoded base64 string"""
    img_bytes = gauge_plot.gauge(streaks)
    # return templates.TemplateResponse('gauge.png', {"request": request})
    return img_bytes


# Create route to delete gauge plot
@app.delete('/delete_gauge')
async def delete_gauge():
    """deletes gauge.png file saved in server"""
    try:
        os.remove('gauge.png')
        return 'File deleted'
    except BaseException:
        return "File has already been deleted"


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


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
