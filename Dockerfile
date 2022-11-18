FROM python:3.10-slim

ARG HOME="/app"
ENV HOME=${HOME}

ADD . ${HOME}
WORKDIR ${HOME}

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
