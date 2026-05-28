# LLM-Guard: Advanced AI Security & Red Teaming Framework

`LLM-Guard` is a comprehensive research project demonstrating the evolution of security architectures for LLM-based applications. It showcases the transition from basic filtering to a professional **Zero-Knowledge Tool-Gating** architecture.

---

## 🚀 Project Evolution: The Journey to v3.0

This repository documents a three-stage security hardening process, responding to real-world adversarial challenges and expert feedback.

### 🔹 v1.0: The Baseline (Legacy)

- **Defense:** Basic keyword filtering (Regex) and system prompt instructions.
- **Vulnerability:** Susceptible to advanced jailbreaking and context-steering.

### 🔹 v2.0: Semantic Defense (Watchdog Pattern)

- **Defense:** Implementation of a **Dual-LLM Architecture**.
- **Innovation:** Integrated `Llama Guard 3 (1B)` as a "Watchdog" to inspect user intent and model output.
- **Resource Optimization:** Engineered to run on local hardware using optimized 1B parameter models.

### 🔹 v3.0: Zero-Knowledge Architecture (Current)

- **Defense:** **Context Isolation & Tool-Gating**.
- **Innovation:** The sensitive "Secret" was removed from the LLM's context window.
- **Mechanism:** Implemented LangChain's **Tool-Calling framework**. The LLM acts as an orchestrator that must provide a valid Access Token to a Python-based "Vault" tool to retrieve sensitive data.
- **Security Gain:** Even a successful jailbreak cannot leak the secret, as the model does not "know" it until authorized.

---

## 🏗 Repository Structure

```text
LLM-Guard/
├── src/                    # Core Application Logic
│   ├── support_bot_v2.py   # Dual-LLM Watchdog implementation
│   └── support_bot_v3.py   # Tool-Gating & Context Isolation (Latest)
├── tests/                  # Red Teaming & Auditing
│   └── red_team_test_v2.py # Automated Multi-Turn Audit Runner
├── v1_basic/               # Legacy Baseline (v1.0)
├── reports/                # Generated Security Audit Reports (Markdown)
├── docs/                   # Technical Write-ups and Architecture Diagrams
├── requirements.txt        # Project Dependencies
└── .gitignore              # Environment and Report exclusions
```

---

## 🛠 Tech Stack

- **Framework:** LangChain (LCEL) & LangChain-Ollama
- **Models:** `llama3.2:1b` (Reasoning), `llama-guard3:1b` (Security)
- **Environment:** Local Inference via [Ollama](https://ollama.com/)

---

## 📋 Setup & Installation

1. **Pull the Models:**
  ```bash
   ollama pull llama3.2:1b
   ollama pull llama-guard3:1b
  ```
2. **Install Dependencies:**
  ```bash
   pip install -r requirements.txt
  ```
3. **Set Python Path (Crucial for Imports):**
  From the root directory (`LLM-Guard/`), run:
  ```bash
   export PYTHONPATH=$PYTHONPATH:.
  ```

---

## 🚀 Running the Security Audit

To validate the v3.0 architecture against multi-turn adversarial attacks:

```bash
python3 tests/red_team_test_v2.py
```

This will generate a professional **Audit Report** in the root directory, documenting:

- **Architectural Security Analysis**
- **Step-by-step Conversation Logs**
- **Pass/Fail status for each Jailbreak Scenario**

---

## 📊 Security Evidence

The framework produces timestamped Markdown reports. Below is an example of a successful defense in v3.0, where the model refuses access without a valid token:

Audit Report Screenshot

![](docs/images/Screenshot%202026-05-28%2010.41.48%20AM.png)
*Figure 1: v3.0 Audit Report showing successful Context Isolation.*

---

## ⚠️ Disclaimer

This project is for **educational and portfolio purposes**. It illustrates advanced LLM security patterns. Before production use, further hardening (e.g., encrypted secret management, rate limiting, and PII masking) is required.

---

**Author:** Manuela Schrittwieser  
**Focus:** AI Security Engineering | Adversarial ML | LLM Hardening
