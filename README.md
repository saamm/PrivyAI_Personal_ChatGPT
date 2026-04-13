# PrivyAI_Personal_ChatGPT

# 🚀 ConvoPro – Local Multi-Model ChatGPT Clone

---

## 🧠 Overview

**ConvoPro** is a local, multi-model AI chat application that allows users to interact with different large language models (LLMs) through a unified interface.

Unlike typical chatbot apps, ConvoPro enables **dynamic model selection**, persistent conversation memory, and GPU-accelerated inference — all deployed on a cloud environment.

---

## 🎯 Key Features

* 🤖 **Multi-Model Support**
  Switch between multiple local LLMs (e.g., `gemma2:2b`, `mistral:7b`, `llama3`) in real-time

* 💬 **Persistent Conversations**
  Chat history stored using MongoDB with retrieval and session continuity

* ⚡ **GPU-Accelerated Inference**
  Models served via Ollama using NVIDIA GPU on AWS EC2

* 🧠 **Automatic Chat Title Generation**
  Generates concise titles for conversations using LLM prompts

* 🔄 **Model Caching System**
  Efficient reuse of LLM instances to reduce latency

* 🌐 **Interactive UI**
  Built with Streamlit for real-time conversational experience

---

## 🏗 System Architecture

```
User (Streamlit UI)
        ↓
Model Selector (Dynamic)
        ↓
LLM Factory (Cached Instances)
        ↓
Ollama (Local Model Server)
        ↓
GPU (AWS EC2 - g5.xlarge)
        ↓
Response → UI
        ↓
MongoDB (Conversation Storage)
```

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **LLM Orchestration:** LlamaIndex
* **Model Serving:** Ollama
* **Database:** MongoDB
* **Containerization:** Docker
* **Cloud:** AWS EC2 (GPU-enabled instance)
* **Environment Management:** Python venv

---

## ☁️ Cloud Deployment (AWS EC2)

The application is deployed on a GPU-enabled EC2 instance:

* Instance Type: `g5.xlarge` (NVIDIA A10G GPU)
* OS: Ubuntu (Deep Learning AMI)
* Docker used for containerized services:

  * Ollama (LLM inference)
  * MongoDB (data persistence)

### Key Setup Steps

```bash
# Enable GPU support in Docker
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Run Ollama with GPU
docker run -d --gpus all -p 11434:11434 ollama/ollama

# Run MongoDB
docker run -d -p 27017:27017 mongo

# Start application
streamlit run main.py --server.address 0.0.0.0 --server.port 8501
```

---

## 🧪 Supported Models

Configured via `.env`:

```
OLLAMA_MODELS=gemma2:2b,mistral:7b,llama3:latest
```

Users can dynamically select models at runtime via UI.

---

## 📂 Project Structure

```
.
├── db/                     # MongoDB interaction (conversation storage)
├── llm_factory/            # LLM initialization and caching
├── services/               # Chat logic, title generation, utilities
├── config/                 # Environment settings
├── main.py                 # Streamlit application entry point
├── requirements.txt
└── .env
```

---

## 🧠 How It Works

1. User selects a model from the UI
2. Query is sent to LLM via Ollama
3. Response is generated using GPU acceleration
4. Chat is stored in MongoDB
5. Future interactions maintain context

---

## 🚀 Key Engineering Highlights

* Designed a **multi-model inference system** with runtime model switching
* Implemented **LLM instance caching** to optimize performance
* Deployed **GPU-backed LLM serving pipeline on AWS EC2**
* Built a **persistent conversational system** with database integration
* Managed **containerized services (Docker)** for reproducibility

---

## 💡 Future Improvements

* 🔄 Model routing (auto-select best model per query)
* 🧠 Agentic reasoning workflows (LangGraph)
* 📊 Monitoring & logging system
* 🔐 Authentication & secure DB access

---

## 📌 Notes

* First response from larger models may be slower due to model warmup
* GPU acceleration significantly improves inference speed
* Instance should be stopped when not in use to reduce cost

---

## ⭐ Why This Project Matters

This project demonstrates:

* Real-world LLM system design
* Cloud deployment with GPU infrastructure
* Integration of multiple AI models in a single application
* End-to-end ML system engineering

---

## 🙌 Acknowledgements

Built as part of hands-on exploration into **LLM systems, agentic AI, and scalable ML infrastructure**.
