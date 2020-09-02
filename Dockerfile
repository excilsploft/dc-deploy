FROM python:3.7.8-slim-buster
RUN apt update -y
COPY . /
RUN pip install -r requirements.txt
ENTRYPOINT ["/entrypoint.sh"]
