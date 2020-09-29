FROM python:3.8 as base
COPY requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt
FROM python:3.8
COPY --from=base /wheels /wheels
COPY --from=base requirements.txt .

ENV PYTHONBUFFERED=1

RUN pip install --no-cache /wheels/*
WORKDIR /app
COPY ./esports /app/esports
COPY ./scripts /app/scripts
COPY ./swagger_template /app/swagger_template
COPY .env /app

RUN mv ../requirements.txt .
RUN useradd esports_dev
RUN chown -R esports_dev:esports_dev /app
RUN chmod +x /app/scripts/start_esports.sh /app/scripts/patch_swagger_template.sh
RUN chown -R esports_dev:esports_dev /app

RUN /app/scripts/patch_swagger_template.sh

USER esports_dev

CMD ["/app/scripts/start_esports.sh"]
