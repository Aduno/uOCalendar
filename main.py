from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from uocalendar.uocalendar import UOCalendar
import logging
from fastapi.middleware.cors import CORSMiddleware
import uuid;
from pathlib import Path 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.post("/uocalendar")
def generate_ics(file: UploadFile = File(...)):
    uocalendar = UOCalendar()

    logging.basicConfig(level=logging.INFO)
    if not file:
        raise HTTPException(status_code=400, detail="No upload file sent")
    # Check if file is an htm file
    elif not file.filename.endswith('.htm') and not file.filename.endswith('.html'):
        raise HTTPException(status_code=400, detail="File is not an htm file") 
    try:
        contents = file.file.read()
        ics = uocalendar.run(contents.decode('utf-8'))
        return StreamingResponse(ics, media_type="text/calendar", headers={"Content-Disposition": "attachment; filename=My Schedule.ics"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occured: {str(e)}")

@app.post("/errors")
def log_error(file: UploadFile = File(...)):
    contents = file.file.read()
    if len(contents) > 1000000:
        return {"message": "File is too large"}
    else:
        file = Path("logs/"+str(uuid.uuid4()))
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(contents)
        return {"message": "File sucessfully received for investigation"}
