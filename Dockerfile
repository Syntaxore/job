FROM python:3.10
WORKDIR /web_app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]