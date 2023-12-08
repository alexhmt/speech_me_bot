FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setup