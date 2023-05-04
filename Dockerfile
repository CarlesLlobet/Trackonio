FROM python:3.9-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY trackonio.py .

ARG CRON_HOUR
ARG CRON_MINUTE

RUN echo "${CRON_MINUTE:-0} ${CRON_HOUR:-9} * * 1-5 /usr/local/bin/python /app/trackonio.py $(date +%Y-%m-%d) >> /var/log/cron.log 2>&1" > /etc/cron.d/script-cron
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/script-cron
RUN crontab /etc/cron.d/script-cron

# Run the command on container startup
CMD printenv > /etc/environment && cron && tail -f /var/log/cron.log