FROM python:3.8

WORKDIR /
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app app
CMD python3 -m app.main
