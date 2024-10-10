FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY flask_app ./flask_app

EXPOSE 5000

ENV FLASK_APP flask_app

CMD ["flask", "run", "--debug", "--host", "0.0.0.0"]
