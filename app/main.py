from fastapi import FastAPI
from app.routes import waste
from app.database import Base, engine  # this is where your error is

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(waste.router)

@app.get("/")
def root():
    return {"message": "WasteTracker API is live"}
