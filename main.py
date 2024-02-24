from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from uocalendar.uocalendar import UOCalendar
import logging

app = FastAPI()

uocalendar = UOCalendar()

@app.post("/uocalendar")
def generate_ics(file: UploadFile = File(...)):
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
    