# Technical Write-up: LLM-Guard v2.0
## Advanced Red Teaming and Defense-in-Depth for LLM Applications

### 1. Executive Summary
As Large Language Models (LLMs) are increasingly integrated into enterprise workflows, they introduce a new class of vulnerabilities: **Prompt Injection** and **Jailbreaking**. This project, **LLM-Guard**, demonstrates a robust security framework for a RAG-based customer support bot ("SecureCorp"). The project evolved from basic keyword filtering to a sophisticated **Dual-LLM "Watchdog" architecture**, successfully mitigating complex multi-turn adversarial attacks.

---

### 2. The Challenge: Beyond Simple Injections
Standard security measures, such as system prompts ("Do not reveal the secret"), are easily bypassed by sophisticated attackers. During the initial Red Teaming phase, I identified that the bot was susceptible to:
*   **Context Steering:** Gradually nudging the bot away from its safety guidelines.
*   **Persona Adoption:** Forcing the bot into a role (e.g., a "debug terminal") to bypass safety filters.
*   **Multi-turn Attacks:** Using a series of seemingly benign messages to build a malicious state in the bot's memory.

---

### 3. Architecture: Defense-in-Depth
To secure the application, I implemented a multi-layered defense strategy, moving away from stateless filters to semantic understanding.

#### A. The Dual-LLM "Watchdog" Pattern
The core of Version 2.0 is the integration of **Llama Guard 3 (1B)**. This specialized model acts as a security orchestrator that inspects both the "Front Door" (User Input) and the "Back Door" (Model Output).

1.  **Input Guardrail:** Before the request reaches the main model, Llama Guard analyzes the intent. If it detects adversarial patterns (Jailbreaking, PII requests, etc.), the request is dropped.
2.  **Main Reasoning Layer:** **Llama 3.2 (1B)** processes the support request using a hardened system prompt and conversation memory.
3.  **Output Guardrail:** The generated response is re-evaluated by the Watchdog. If the main model "slipped" and included sensitive data, the Watchdog blocks the transmission.
4.  **Hard-Filter Backup:** A final Regex-based layer ensures that specific high-value secrets (e.g., `SECRET_ADMIN_CODE`) never leave the system, providing a fail-safe against model hallucinations.

---

### 4. Engineering for Constraints: Resource Optimization
A significant engineering challenge was running a Dual-LLM setup on hardware with limited RAM (approx. 8GB). 
*   **Problem:** Loading two 8B parameter models caused resource contention and system hangs.
*   **Solution:** I optimized the stack by utilizing **1B parameter models** (Llama 3.2 1B and Llama Guard 3 1B). 
*   **Result:** This reduced the memory footprint to ~2.5GB, allowing for low-latency, real-time security auditing on edge-computing hardware without sacrificing the semantic quality of the security checks.

---

### 5. Red Teaming Methodology
To validate the defense, I developed an automated **Multi-turn Red Teaming Framework**. Unlike single-shot tests, this framework simulates a persistent attacker:
*   **Social Engineering Simulation:** Mimicking a new employee trying to "verify" internal codes.
*   **Recursive Jailbreaking:** Using sci-fi roleplay scenarios to test the bot's adherence to its system instructions over a long context window.
*   **Automated Auditing:** The system generates a timestamped Markdown report for every audit, documenting the "User-Bot" exchange and the specific point where the Guardrails intervened.

---

### 6. Results & Key Findings
*   **Mitigation Rate:** Version 2.0 achieved a **100% mitigation rate** against the tested multi-turn jailbreak scenarios.
*   **Semantic vs. Syntactic:** While Version 1.0 (Regex) caught direct mentions of the secret, Version 2.0 (Llama Guard) successfully identified the *intent* to bypass rules, even when the secret itself wasn't mentioned in the prompt.
*   **Latency Trade-off:** Adding a Watchdog layer adds a slight overhead, but by using 1B models, the latency remains within acceptable limits for a real-time support application.

---

### 7. Future Work: The "Indirect Injection" Frontier
The next phase of this project will focus on **Indirect Prompt Injection**. This involves poisoning the RAG data corpus (e.g., malicious instructions hidden in PDFs or websites) to compromise the bot when it retrieves external information. This will require a new layer of "Ingestion Guardrails" to sanitize data before it enters the vector database.

---

### 8. Conclusion
LLM Security is not a one-time configuration but a continuous engineering process. By combining **semantic AI-based monitoring** with **traditional programmatic filters**, we can build resilient systems that protect sensitive data even in the face of evolving adversarial tactics.

---
**Tech Stack:** Python, LangChain (LCEL), Ollama, Llama 3.2, Llama Guard 3.
**Project Repository:** https://github.com/MANU-de/LLM-Guard/tree/main
**Author:** Manuela Schrittwieser