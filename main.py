from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

import os
from fastapi.responses import JSONResponse
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get("/blob", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    blob_url = os.environ.get("AzureWebJobsStorage__blobServiceUri")
    blob_client = BlobServiceClient(account_url=blob_url, credential=DefaultAzureCredential()).get_container_client("files")
    container_properties = blob_client.get_container_properties()
    container_properties

@app.get("/queue", response_class=HTMLResponse)
async def index(request: Request):
    queue_url = os.environ.get("AzureWebJobsStorage__queueServiceUri")
    queue_client = QueueServiceClient(account_url=queue_url, credential=DefaultAzureCredential()).get_queue_client("jobs")
    #queue_client.peek_messages(max_messages=1)
    properties=queue_client.get_service_properties()
    properties

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print('Request for hello page received with name=%s' % name)
        return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
