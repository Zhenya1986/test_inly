FROM python:3.11

RUN mkdir /test_task_InlyIT

WORKDIR /test_task_InlyIT

COPY pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000
