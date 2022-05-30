ARG PYTHON_VERSION=3.9


FROM python:${PYTHON_VERSION}-alpine AS poetry

RUN apk add --no-cache \
        curl \
        gcc \
        g++ \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile=minimal && \
    source $HOME/.cargo/env && \
    pip install -U --no-cache-dir pip==22.1.1 && \
    pip install --no-cache-dir poetry==1.1.12

ENTRYPOINT ["poetry"]


FROM poetry AS development

WORKDIR /src/

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY src/ ./src/
COPY tests ./tests/

CMD ["run", "pytest"]
