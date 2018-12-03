FROM ubuntu:latest
MAINTAINER Sindre Sivertsen "sindrejohan1@gmail.com"
run apt-get update -y
run apt-get install -y python3-pip python-dev
copy ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 app.py
CMD ["python3 app.py"]
