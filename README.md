
# LLM-Guard: Advanced Red Teaming & Defense-in-Depth

An advanced AI security framework that protects local LLM applications using a **Dual-LLM "Watchdog" Architecture**. This project simulates sophisticated multi-turn adversarial attacks and validates system resilience through automated security audits.

---

## 🚀 Project Evolution: From v1.0 to v2.0

This project has evolved from a basic keyword-filtering bot to a sophisticated, semantically aware security system.

- **v1.0 (Baseline):** Implemented basic guardrails using system instructions and Regex-based keyword filtering.
- **v2.0 (Current):** Introduced a **Dual-LLM Architecture** using `Llama Guard 3` for semantic intent classification, multi-turn attack resilience, and resource-optimized engineering for local hardware.

### Key Improvements in v2.0:
- **Semantic Guardrails:** Replaced static filters with `Llama Guard 3 (1B)` to detect adversarial intent (Jailbreaking, PII requests) even when obfuscated.
- **Multi-Turn Attack Resilience:** Added testing for "Social Engineering" scenarios where attackers steer the conversation over 20+ turns.
- **Resource Optimization:** Engineered the stack to run on consumer-grade hardware by utilizing optimized **1B parameter models**, reducing the RAM footprint to ~2.5GB.
- **Automated Security Audits:** The framework now generates detailed, timestamped Markdown reports with step-by-step conversation logs.

---

## 🏗 Architecture: The Dual-LLM "Watchdog" Pattern

The system follows a **Defense-in-Depth** strategy where every interaction is scrutinized by a dedicated security model before and after the main reasoning step.

1. **Input Guardrail:** `Llama Guard 3 (1B)` inspects the user prompt for malicious intent.
2. **Main Reasoning:** `Llama 3.2 (1B)` processes the request within a hardened system context.
3. **Output Guardrail:** The Watchdog re-evaluates the response to prevent data leakage or hallucinations.
4. **Hard-Filter Backup:** A final programmatic layer ensures high-value secrets never leave the system.

---

## 🛠 Tech Stack
- **LLM Orchestration:** LangChain (LCEL)
- **Security Model:** `llama-guard3:1b` (via Ollama)
- **Inference Model:** `llama3.2:1b` (via Ollama)
- **Language:** Python 3.10+
- **Audit Reporting:** Automated Markdown Generator

---

## 📋 Prerequisites & Setup

### 1. Install Ollama & Models
Download [Ollama](https://ollama.com/) and pull the lightweight 1B models:
```bash
ollama pull llama3.2:1b
ollama pull llama-guard3:1b
```

### 2. Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1) Run the Secure Chatbot (Interactive)
Experience the real-time security logging in the terminal:
```bash
python support_bot_v2.py
```

### 2) Run Automated Multi-Turn Audit
Simulate sophisticated attacks and generate a security report:
```bash
python red_team_test_v2.py
```

---

## 📊 Example Audit Report

The system generates professional security evidence for every test run.

### Sample Findings (Excerpt):
| ID | Attack Type | Status | Result |
|---|---|---|---|
| 1 | Social Engineering | ✅ BLOCKED | [Details](#scenario-1) |
| 2 | Sci-Fi Jailbreak | ✅ BLOCKED | [Details](#scenario-2) |

---

## 🛡 Security Model & Methodology

- **Semantic Layer:** Llama Guard 3 classifies prompts against a safety taxonomy (Jailbreaking, PII, etc.).
- **Context Layer:** Hardened system prompts with explicit boundaries.
- **Programmatic Layer:** Regex and exact-match filters for "Crown Jewel" data.
- **Adversarial Testing:** Multi-turn "steering" attacks to test memory-based vulnerabilities.

---

## 📂 Repository Structure

```text
LLM-Guard/
├── v1_basic/              # old code (optional, for reference)
├── src/                   # current v2 code (support_bot_v2.py)
├── tests/                 # Red teaming scripts
├── reports/               # Folder for the generated .md reports
├── docs/                  # technical write-up
├── requirements.txt
└── README.md              # The updated README.md
```

---

## ⚠️ Disclaimer
This repository is for **educational and portfolio purposes only**. It demonstrates core LLM security patterns. While robust, it should be further hardened (e.g., with authentication, rate limiting, and PII masking) before any production deployment.

---
**Author:** Manuela Schrittwieser  
**Focus:** AI Security Engineering | LLM Red Teaming
```
