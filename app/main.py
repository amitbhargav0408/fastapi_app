from fastapi import FastAPI
from app.routers import items, clock_in

app = FastAPI()

app.include_router(items.router)
app.include_router(clock_in.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}
