FROM ghcr.io/astral-sh/uv:0.6.17-python3.12-bookworm-slim

WORKDIR /app

RUN uv venv

COPY requirements.txt .

RUN uv pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uv", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
