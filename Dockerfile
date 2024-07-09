FROM python:3

RUN "pip3 install -r requirements.txt"

CMD  ["fastapi", "dev", "app/main.py"]