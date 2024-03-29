FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PORT 5000
EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
