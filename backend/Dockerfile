FROM python:3.12-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y gcc redis-server postgresql-client curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000



# Start the application with dependency check, migration, and then start FastAPI
CMD ["/bin/sh", "-c", " \
  while ! PGPASSWORD=$APP_CONFIG__DATABASE__DB_PASSWORD psql -h \"$APP_CONFIG__DATABASE__DB_HOST\" -U \"$APP_CONFIG__DATABASE__DB_USER\" -d \"$APP_CONFIG__DATABASE__DB_NAME\" -c '\\q' > /dev/null 2>&1; do \
    >&2 echo 'Postgres is unavailable - sleeping'; \
    sleep 1; \
  done; \
  ls; \
  >&2 echo 'Postgres is up - executing command'; \
  poetry install; \
  cd app; \
  poetry run alembic upgrade head; \
  cd ..; \
  poetry run python ./app/main.py"]