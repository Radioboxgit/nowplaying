from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from services import get_song_title

app= FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get('/')
def docs():
    # redirect to project documentation
    return RedirectResponse(url='/docs')


@app.get('/title')
def get_title(stream_url:str):
    title=get_song_title(stream_url)
    return title
