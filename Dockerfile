FROM python:3.6-alpine

RUN adduser -D visualdata

RUN pip install --upgrade pip

WORKDIR /Users/vladtihomirov/Usersstats/staf

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


COPY all.csv app.py ./

USER root

EXPOSE 3000

CMD python app.py