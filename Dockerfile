FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
