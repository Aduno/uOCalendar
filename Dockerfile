from python:3.11

WORKDIR /app

COPY  ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app
COPY uocalendar /app/uocalendar
COPY Dockerfile /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "52310"]
# For using nginx 
# CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "52310"]

