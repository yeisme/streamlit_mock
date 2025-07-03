ARG BASE_IMAGE=python:3.13-slim
FROM ${BASE_IMAGE}

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Create a virtual environment
RUN python -m venv .venv

# Install uv into the virtual environment and then sync dependencies
RUN /app/.venv/bin/python -m pip install uv && /app/.venv/bin/uv sync

# Copy the rest of the application code
COPY . .

EXPOSE 8501

# Use the python executable from the virtual environment
CMD ["/app/.venv/bin/python", "-m", "streamlit", "run", "src/main.py"]
