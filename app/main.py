# app/main.py

from fastapi import FastAPI
from app.api.endpoints import auth, users
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Add more routes and application logic here

app.include_router(users.router,prefix="/api",tags=["users"])
app.include_router(auth.router, tags=["authentication"])