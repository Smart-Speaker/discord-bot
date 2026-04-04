FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY bot.py /app/bot.py
COPY ram_bot /app/ram_bot

CMD ["python", "/app/bot.py"]
