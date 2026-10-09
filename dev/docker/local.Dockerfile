FROM python:3.14-slim

# Set up a safe working directory to put the code in
WORKDIR /root/work

# Do not copy anything other than reqs because this is a dev container and so we are using Docker volumes instead.
COPY pyproject.toml .
COPY uv.lock .
# NOTE: this is a dev container so we should use a docker volume mount instead of copying in files

RUN apt-get update && \
    apt-get install -y gcc git libc-dev libpq-dev curl

ENV UV_INSTALL_DIR=/usr/local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install python deps, both dev and regular
RUN uv sync

EXPOSE 8000

# We are using the same thing as PROD here but with the --reload option enabled, so it can be used as a dev server.
CMD ["uv", "run", "uvicorn", "to_do_api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
