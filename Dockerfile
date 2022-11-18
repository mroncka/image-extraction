FROM python:3.10-slim as runtime

ARG HOME="/app"
ENV HOME=${HOME}

ADD . ${HOME}
WORKDIR ${HOME}

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

FROM runtime as test
WORKDIR ${HOME}

RUN pip install -r test_requirements.txt
RUN pip install -e .

ENTRYPOINT ["pytest", "tests"]
