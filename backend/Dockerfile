FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir --require-hashes -r requirements.lock
RUN useradd --create-home --uid 10001 aml
COPY . .
USER aml
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
