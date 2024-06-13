#first create a virtual environment > py -3 -m venv <name>
# use venv Scriptd python.exe for this project>view>command palete>python interprater>venv one
#lastly acvtivate.bat to use it in terminal
#now we are good for 

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware #for Cross Origion Resource Sharing


# Note: the module name is psycopg, not psycopg3
# import psycopg2 not in use here


from . import models
from .database import engine

#import the router created
from .routers import posts, users, auth, votes


#this line create schema table once the script runs
# models.Base.metadata.create_all(bind=engine)#// we are no depending on alembic to create the schema so this function may not be used again


app = FastAPI()

#specify the allowed domains to access your application here
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]


app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"], # for now let us allow all domains for testing purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}
# run the server => uvicorn main:app --reload

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)

