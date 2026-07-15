FROM python:3.14-slim@sha256:d3400aa122fa42cf0af0dbe8ec3091b047eac5c8f7e3539f7135e86d855dc015 AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN addgroup --system django && adduser --system --ingroup django django

COPY requirements.txt .
RUN python -m venv "$VIRTUAL_ENV" \
    && python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .
RUN chmod +x /app/docker/entrypoint.sh \
    && python manage.py collectstatic --noinput \
    && chown -R django:django /app

USER django

EXPOSE 8000
ENTRYPOINT ["/app/docker/entrypoint.sh"]
