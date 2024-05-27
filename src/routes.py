from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import const
from service.upload_service import UploadService
from service.query_service import QueryService
import os

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/converted", exist_ok=True)

os.environ["OPENAI_API_KEY"] = const.CREDENTIALS["OPENAI_API_KEY"]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, user: str = Form(...), start: int = Form(...), end: int = Form(...), file: UploadFile = File(...)):
    if end <= start:
        raise HTTPException(status_code=400, detail="Start cannot be larger than or equal to end")
    if start - end > const.MAX_PAGES:
        raise HTTPException(status_code=400, detail="Creator of this app is lazy/poor, no more than 20 pages")
    file_path = _write(file, user)
    UploadService(start=start, end=end, user=user).upload(file_path)
    return templates.TemplateResponse(
        "query.html",
        {
            "request": request,
            "data": {"answer": "", "question": ""},
            "context": {"user": user, "start": start, "end": end}
        },
    )


def _write(file, user):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
    try:
        contents = file.file.read()
        file_path = 'data/raw/{}.pdf'.format(user)
        with open(file_path, 'wb') as raw_file:
            raw_file.write(contents)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid PDF file. Error msg: {}".format(exc))
    return file_path


@app.post("/query", response_class=HTMLResponse)
async def query(request: Request, user: str = Form(...), question: str = Form(...)):
    answer = QueryService(user=user).answer(question)
    return templates.TemplateResponse(
        "query.html",
        {"request": request, "data": {"answer": answer, "question": question}}
    )

