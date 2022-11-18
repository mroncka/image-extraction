FROM python:3.10-slim as build

ARG HOME="/app"
ENV HOME=${HOME}

ADD . ${HOME}
WORKDIR ${HOME}

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

FROM build as test
WORKDIR ${HOME}

RUN pip install -r test_requirements.txt
RUN pip install -e .

ENTRYPOINT ["pytest", "tests"]

FROM test as dev
WORKDIR ${HOME}

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r dev_requirements.txt
RUN pip install -e .

ENTRYPOINT ["/bin/bash"]
