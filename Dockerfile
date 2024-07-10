FROM python:3.9

WORKDIR /home/florentin/fastapi

RUN pip3 install requirements.txt

CMD ["fastapi", "dev", "app/main.py"]