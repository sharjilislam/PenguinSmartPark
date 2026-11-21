from fastapi import FastAPI

app = FastAPI(
    title="Penguin SmartPark",
    description="Smart parking recommendation system for Youngstown State University",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "project": "Penguin SmartPark",
        "message": "Welcome to Penguin SmartPark!",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Penguin SmartPark Backend"
    }
