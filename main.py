from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from uocalendar.uocalendar import UOCalendar
import logging
app = FastAPI()

# One concern is that since UOCalendar is intiantiated once, it will be shared across all requests.
# so there will be bottleneck if there are many requests.

uocalendar = UOCalendar()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uocalendar")
def generate_ics(file: UploadFile = File(...)):
    logging.basicConfig(level=logging.DEBUG)
    if not file:
        return {"message": "No upload file sent"}
    # Check if file is an htm file
    if not file.filename.endswith('.htm'):
        return {"message": "File is not an htm file"}
    try:
        contents = file.file.read()
        ics = uocalendar.run(contents.decode('utf-8'))
        return StreamingResponse(ics, media_type="text/calendar", headers={"Content-Disposition": "attachment; filename=My Schedule.ics"})
    except Exception as e:
        return {"message": f"An error occured: {str(e)}"}
    