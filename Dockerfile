FROM python:2.7
COPY . /app/build
RUN pip install -r /app/build/requirements.txt
WORKDIR /app/src