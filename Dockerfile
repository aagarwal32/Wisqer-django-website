FROM python:3.9.13-slim-buster

ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app

# Install necessary dependencies, including certificates
RUN apt-get update && apt-get install -y \
    ca-certificates && \
    update-ca-certificates

RUN python3 -m venv /opt/djangoenv

RUN /opt/djangoenv/bin/pip install pip --upgrade && \
    /opt/djangoenv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]