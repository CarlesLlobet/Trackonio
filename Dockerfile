FROM python:3.9-slim-buster

RUN apt-get update \
  && apt-get install -y \
    cron

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY trackonio.py .

RUN echo "${CRON_MINUTE:-0} ${CRON_HOUR:-9} * * * root python /app/trackonio.py $(date +%Y-%m-%d)" > /etc/cron.d/script-cron && \
    chmod 0644 /etc/cron.d/script-cron && \
    crontab /etc/cron.d/script-cron

# Run the command on container startup
CMD ["cron", "-f"]