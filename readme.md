# Running guide

    python -m venv venv
    pip install -r ./requirements.txt

## Define your .env

### Generate your AES key

    python3 -m src.utils.generate_key "your desired password"

### Example .env

    USER = random_user
    PASSWORD = random_password
    AES_KEY = 0000000000000000000000000000000000000000000000000000000000000000

### Authenticate

    python3 -m src.authenticate "linkedin"

## Install docker

    https://www.docker.com/

### run

    docker compose up --build
