# simple job scraper

## Create virtual enviroment

    python -m venv venv

## Activate virtual enviroment

    Windows:
    venv\Scripts\activate

    macOS/Linux:
    . venv/bin/activate

## Install requirements

    pip install -r ./requirements.txt

## Setup .env file

    USER = linkedin user to be used
    PASSWORD = password

## Install Chrome

    https://www.google.com/intl/pt-BR/chrome/

## Running

### the first argv is required

    python3 -m src.linkedin

### argv 1

    your search keyword ex: '"backend" AND "junior"'

### argv 2

    location ex: 'Brazil'

### argv 3

    timeframe linkedin format, r86400 means for example 24hrs = 86400 seconds

### argv 4

    Remote ex: 2 for only remote works
