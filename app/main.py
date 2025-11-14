from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import router as api_router

app = FastAPI()

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")
