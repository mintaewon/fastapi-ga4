FROM python:3.9.21-alpine3.21

WORKDIR /home/foresys

COPY . ./app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./app/requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=./app/secret/he-dashboard-580f85880e99.json

CMD ["uvicorn", "app.wsgi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
