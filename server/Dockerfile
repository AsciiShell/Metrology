FROM python:3.7.3-slim

WORKDIR /usr/src/app

COPY requirements.txt index.html server.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./server.py" ]