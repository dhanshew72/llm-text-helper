from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import const
from models.query_model import QueryModel
from service.upload_service import UploadService
from service.query_service import QueryService
import os

app = FastAPI()

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/converted", exist_ok=True)

os.environ["OPENAI_API_KEY"] = const.CREDENTIALS["OPENAI_API_KEY"]


@app.post("/upload")
async def upload(user: str, start: int, end: int, file: UploadFile = File(...)):
    if end <= start:
        raise HTTPException(status_code=400, detail="Start cannot be larger than or equal to end")
    if start - end > const.MAX_PAGES:
        raise HTTPException(status_code=400, detail="Creator of this app is lazy/poor, no more than 20 pages")
    file_path = _write(file, user)
    UploadService(start=start, end=end, user=user).upload(file_path)
    return JSONResponse(content={"result": "successfully uploaded"})


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


@app.post("/query")
async def query(query_body: QueryModel):
    answer = QueryService(user=query_body.user).answer(query_body.question)
    return JSONResponse(content={"result": answer})
