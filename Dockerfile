
FROM python:3.12.5

WORKDIR /app

RUN groupadd -r selenium && useradd -g selenium selenium

RUN chown -R selenium:selenium /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --trusted-host pypy.python.org -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y wget unzip && \ 
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

RUN apt-get update && apt-get install -y curl jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN VERSION=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | jq -r '.channels.Stable.version') && \
        curl -O https://storage.googleapis.com/chrome-for-testing-public/$VERSION/linux64/chromedriver-linux64.zip && \
        unzip chromedriver-linux64.zip 'chromedriver-linux64/chromedriver' -d /usr/bin && \
        mv /usr/bin/chromedriver-linux64/chromedriver /usr/local/lib/python3.12/site-packages/seleniumbase/drivers/uc_driver && \
        rm -rf /usr/bin/chromedriver-linux64 && \
        rm chromedriver-linux64.zip


EXPOSE 8000

USER selenium

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]