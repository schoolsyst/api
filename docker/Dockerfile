FROM python:3.7
WORKDIR /api

RUN apt update \
    && apt-get install -y pandoc git curl tree \
    && git clone https://github.com/schoolsyst/api . \
    && pip install poetry==1.0.5 \
    && poetry config virtualenvs.create false \
    && poetry install


ENTRYPOINT ["docker/run.sh"]
