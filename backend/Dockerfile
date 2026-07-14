ARG PYTHON_VERSION=3.14.6
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

COPY . .
RUN chmod +x entrypoint.sh
USER appuser

EXPOSE 8000

# Run the application.
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["/app/.venv/bin/python", "-m", "app"]
