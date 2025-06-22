FROM python:3.10-slim

WORKDIR /app
ENV PIP_ROOT_USER_ACTION=ignore
COPY . /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

VOLUME ["/watched"]

CMD ["python", "Bot.py"] 