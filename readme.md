# Running guide

## Define your .env

### Generate your AES key

    python3 -m src.utils.generate_key "your desired password"

### Example .env

    USER = random_user
    PASSWORD = random_password
    AES_KEY = 0000000000000000000000000000000000000000000000000000000000000000

## Install docker

    https://www.docker.com/

### run

    docker compose up --build
