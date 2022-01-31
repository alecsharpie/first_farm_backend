from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]  # This will eventually be changed to only the origins you will use once it's deployed, to secure the app a bit more.

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get('/')
def get_root():
    return {"Ping": "Pong"}
