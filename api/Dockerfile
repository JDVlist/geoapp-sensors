FROM python:3.13-slim

WORKDIR /app

COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# uvicorn: Starts the web server used to run an ASGI application such as FastAPI.
# app.main:app: Imports the variable named app from app/main.py.
# --host 0.0.0.0: Accepts connections from outside the container. 
# --port 8000: Listens on port 8000 inside the container.