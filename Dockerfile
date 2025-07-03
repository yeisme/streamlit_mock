ARG BASE_IMAGE=python:3.13-slim
FROM ${BASE_IMAGE}

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

COPY . .
EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "src/main.py"]
