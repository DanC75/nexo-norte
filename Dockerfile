FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system django && adduser --system --ingroup django django

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN chmod +x /app/docker/entrypoint.sh \
    && python manage.py collectstatic --noinput \
    && chown -R django:django /app

USER django

EXPOSE 8000
ENTRYPOINT ["/app/docker/entrypoint.sh"]
