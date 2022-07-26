from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os

import downloader

app = FastAPI()

if not os.path.exists("assets"):
    os.mkdir("assets")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, err: str):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}
    )


@app.post("/download")
async def download_file(request: Request):
    form_data = await request.form()
    url = form_data.get("url")
    filepath = downloader.download(url)
    return FileResponse(
        f"assets/{filepath}.mp3",
        media_type="application/octet-stream",
        filename=f"{filepath}.mp3",
    )


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
