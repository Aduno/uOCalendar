from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from uocalendar import UOCalendar
import logging
from fastapi.middleware.cors import CORSMiddleware
import uuid;

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
        return {"message": "No upload file sent"}
    # Check if file is an htm file
    elif not file.filename.endswith('.htm'):
        return {"message": "File is not an htm file"}
    try:
        contents = file.file.read()
        ics = uocalendar.run(contents.decode('utf-8'))
        return StreamingResponse(ics, media_type="text/calendar", headers={"Content-Disposition": "attachment; filename=My Schedule.ics"})
    except Exception as e:
        return {"message": f"An error occured: {str(e)}"}

@app.post("/errors")
def log_error(file: UploadFile = File(...)):
    contents = file.file.read()
    if len(contents) > 1000000:
        return {"message": "File is too large"}
    else:
        with open(f'logs/'+uuid.uuid4(), 'wb') as f:
            f.write(contents)
        return {"message": "File sucessfully received for investigation"}
