ARG BASE_IMAGE=python:3.13-slim
FROM ${BASE_IMAGE}

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Create a virtual environment, install uv, sync dependencies, and clean up
RUN python -m venv .venv && \
    /app/.venv/bin/python -m pip install uv && \
    /app/.venv/bin/uv sync && \
    /app/.venv/bin/uv clean && \
    rm -rf /root/.cache/pip # Clean pip cache

# Copy the rest of the application code
COPY . .

EXPOSE 8501

# Use the python executable from the virtual environment
CMD ["/app/.venv/bin/python", "-m", "streamlit", "run", "src/main.py"]
