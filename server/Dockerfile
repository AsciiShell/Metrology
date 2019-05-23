FROM python:3.7.3-slim

WORKDIR /usr/src/app

COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]