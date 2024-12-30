# Sets up the API before preventing root access to the alpine image
FROM python:3.13-alpine

WORKDIR /src

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./src/ /src/

RUN apk upgrade --no-cache &&\
    uv pip install --system -r /src/requirements/requirements.txt

RUN adduser -D nonroot
USER nonroot

EXPOSE 8000

ENTRYPOINT ["python", "-m"]
CMD ["fastapi", "run"]
