FROM python:3.11-slim-bullseye

WORKDIR /src

COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN prisma generate
RUN prisma db push


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]