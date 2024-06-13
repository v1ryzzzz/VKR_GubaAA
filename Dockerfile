FROM python:3.12

WORKDIR /application

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/requirements.txt /application/requirements/
RUN pip install -r requirements/requirements.txt

COPY . .

WORKDIR /application/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000