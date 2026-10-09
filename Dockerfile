FROM python:3.12-slim

WORKDIR /app

# Copy project definition and source code first
COPY pyproject.toml .
COPY src/ ./src/

# Install the application package
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "url_shortener.app:app", "--host", "0.0.0.0", "--port", "8000"]