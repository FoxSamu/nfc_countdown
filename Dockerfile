FROM python:3.12.0-alpine

WORKDIR /usr/src/app

RUN apk add -u zlib-dev jpeg-dev gcc musl-dev krb5-dev freetype-dev
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 3000

COPY . .
# CMD ["sh", "/usr/src/app/server.sh"]