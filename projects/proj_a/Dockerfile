FROM python:3.11 as requirements-stage
WORKDIR /work
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes --output requirements.txt --only proj_a

FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /work
RUN pip install --no-cache-dir --upgrade pip

COPY --from=requirements-stage /work/requirements.txt requirements.txt
COPY libs/lib_hello libs/lib_hello
RUN pip install --no-cache-dir -r requirements.txt

COPY projects/proj_a projects/proj_a
WORKDIR /work/projects/proj_a

CMD exec uvicorn --port $PORT --host 0.0.0.0 app.main:app
