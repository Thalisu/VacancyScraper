FROM python:3.12.5

WORKDIR /app

# dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y wget unzip curl jq

# Install Chrome
ARG ChromeUrl=https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN wget $ChromeUrl && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --trusted-host pypy.python.org -r requirements.txt

RUN cd /usr/local/lib/python3.12/site-packages/seleniumbase

RUN seleniumbase get chromedriver --path

RUN cd /app

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
