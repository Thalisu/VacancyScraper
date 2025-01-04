FROM python:3.12.5

WORKDIR /app

# dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y wget unzip curl jq

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --trusted-host pypy.python.org -r requirements.txt

RUN cd /usr/local/lib/python3.12/site-packages/seleniumbase

RUN seleniumbase get chromedriver --path

RUN cd /app

COPY . .
