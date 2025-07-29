from fastapi import FastAPI
from app.routers import report

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Weekly Report Generator"}

app.include_router(report.router)
