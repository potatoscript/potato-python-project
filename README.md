
# 🥔 Potato Python Project (PotatoGPT)

A **local, private AI chatbot** built with **Streamlit + LangChain + RAG + Ollama**, fully containerized with **Docker**.

This project lets you:

* Chat with a local LLM (via Ollama)
* Ask questions about your own PDFs (RAG)
* Run everything reproducibly using Docker
* Persist embeddings across restarts

---

## ✨ Features

* 🧠 **Local LLM** using Ollama (no cloud, no API keys)
* 📄 **RAG (Retrieval-Augmented Generation)** over PDFs
* 💬 **Conversation memory** (chat history aware)
* 🖥 **Streamlit UI**
* 🐳 **Dockerized** for easy setup
* 💾 **Persistent ChromaDB**

---

## 🗂 Project Structure

```
potato-python-project/
├── app/
│   ├── main.py          # Streamlit entrypoint
│   ├── agent.py         # LangChain agent + memory
│   ├── rag.py           # PDF loading + embeddings + Chroma
│   ├── __init__.py
│   ├── data/
│   │   ├── pdfs/         # 📄 Put your PDFs here
│   │   └── chroma/       # 💾 Persistent vector store
│   └── web/
│       └── Dockerfile    # App Dockerfile
├── docker-compose.yml    # (optional) Compose setup
├── requirements.txt
├── tests/
├── .github/workflows/    # CI (optional)
└── README.md
```

---

## 🧠 Architecture Overview

```
Browser
  ↓ (8501)
Streamlit UI (main.py)
  ↓
LangChain Agent (agent.py)
  ↓
Retriever (rag.py)
  ↓
ChromaDB (embeddings)
  ↓
Ollama (LLM + Embeddings)
```

---

## 🚀 Quick Start

### 1️⃣ Install Ollama (host machine)

👉 [https://ollama.com/download](https://ollama.com/download)

Then pull required models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

Make sure Ollama is running:

```bash
ollama list
```

---

### 2️⃣ Add your PDFs

Put at least **one PDF** into:

```
app/data/pdfs/
```

---

### 3️⃣ Build Docker Image

From project root:

```bash
docker build --no-cache -t potatogpt .
```

---

### 4️⃣ Run the App

```bash
docker run -p 8501:8501 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --name potatogpt-app \
  potatogpt
```

Open your browser:

👉 [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: "3.9"
services:
  app:
    image: potatogpt
    container_name: potatogpt-app
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    volumes:
      - ./app/data/pdfs:/app/data/pdfs
      - ./app/data/chroma:/app/data/chroma
    restart: unless-stopped
```

Run:

```bash
docker compose up --build
```

---

## 🔄 Auto‑Reload PDFs (No Rebuild Needed)

* PDFs are **mounted as volumes**
* Add / replace PDFs in `app/data/pdfs`
* Restart container:

```bash
docker restart potatogpt-app
```

Embeddings are reused if Chroma already exists.

---

## 💾 Persistent ChromaDB

Chroma is stored at:

```
app/data/chroma/
```

Because it is mounted as a volume:

* Restarting Docker **does NOT delete embeddings**
* Rebuilding the image keeps your vector DB

---

## 🧪 Development (Optional)

Run locally without Docker:

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

Set Ollama URL if needed:

```bash
export OLLAMA_BASE_URL=http://localhost:11434
```

---

## ❓ Common Issues

### ❌ Ollama connection error

Make sure:

* Ollama is running on host
* `OLLAMA_BASE_URL` is set correctly

For Docker on Windows/macOS:

```
http://host.docker.internal:11434
```

---

### ❌ No PDFs found

Ensure:

```
app/data/pdfs/*.pdf
```

At least one valid PDF is required.

---

## 🔐 Privacy

* No cloud APIs
* No data leaves your machine
* Fully offline after model download

---

## 📌 Tech Stack

* Python 3.11
* Streamlit
* LangChain
* ChromaDB
* Ollama
* Docker

---

## 🧭 Roadmap

* [ ] GPU support
* [ ] Auth & multi-user
* [ ] PDF upload via UI
* [ ] LangGraph workflows
* [ ] Cloud deployment templates

---

## 🥔 Final Words

This project is a **production-grade local AI system**, not a toy.

You now have:

* Real RAG
* Real containers
* Real AI infra skills
