FROM python:3.13-alpine

WORKDIR /app

RUN adduser -D nonroot
USER nonroot

COPY ./src/ /app/

RUN pip install --upgrade pip &&\
    pip install uv &&\
    uv pip install --user --no-cache-dir --upgrade -r /code/requirements/requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "-m"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
