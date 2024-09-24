FROM python:3.10
WORKDIR /web_app
COPY requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
