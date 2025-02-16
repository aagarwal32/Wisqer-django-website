FROM python:3.9.13-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

RUN python3 -m venv /opt/djangoenv && \
    /opt/djangoenv/bin/pip install --upgrade pip && \
    /opt/djangoenv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

EXPOSE ${PORT}
CMD ["/app/entrypoint.sh"]
