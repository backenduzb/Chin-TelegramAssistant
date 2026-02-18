FROM python:3.13-alpine3.21

WORKDIR /bot

COPY . .

RUN pip install --no-cache-dir -r /bot/requirements.txt

EXPOSE 7400

ENTRYPOINT [ "sh", "/bot/entrypoint.sh" ]