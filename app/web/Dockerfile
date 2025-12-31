# ---------- Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---------- Runtime ----------
FROM python:3.11-slim

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

COPY --from=builder /root/.local /root/.local
COPY app/main.py ./main.py

EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
