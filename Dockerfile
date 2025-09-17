FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache
RUN uv remove opencv-contrib-python
RUN uv add opencv-python-headless

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "9999", "--host", "0.0.0.0"]