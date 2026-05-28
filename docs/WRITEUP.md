# Technical Write-up: LLM-Guard v3.0

## From Semantic Defense to Zero-Knowledge Tool-Gating

### 1. Executive Summary

As Large Language Models (LLMs) are integrated into enterprise workflows, they introduce critical vulnerabilities like **Prompt Injection** and **Context Leakage**. This project, **LLM-Guard**, demonstrates the evolution of a security framework for a customer support bot ("SecureCorp"). The project progressed from basic filtering (v1) and Dual-LLM monitoring (v2) to a professional **Zero-Knowledge Tool-Gating architecture (v3)**, effectively isolating sensitive data from the model's reasoning layer.

---

### 2. The Challenge: Context Leakage & Jailbreaking

Standard security measures often rely on system prompts (e.g., "Do not reveal the secret"). However, sophisticated attackers use **Context Steering** and **Jailbreaking** to bypass these instructions.

- **The v2.0 Vulnerability:** Even with a "Watchdog" model, the secret still resided within the main model's **Context Window**. If an attacker successfully bypassed the guardrails, the secret was readily available for extraction.
- **The v3.0 Solution:** Removing the secret from the prompt entirely, ensuring the model has "Zero-Knowledge" of the sensitive data until a secure, external validation occurs.

---

### 3. Architecture: Defense-in-Depth Evolution

#### A. The Dual-LLM "Watchdog" Pattern (v2.0)

The system utilizes **Llama Guard 3 (1B)** as a security orchestrator. It inspects both User Input and Model Output for adversarial intent, providing a semantic layer of protection that goes beyond simple keyword matching.

#### B. Context Isolation & Tool-Gating (v3.0)

In the latest iteration, I implemented **Separation of Concerns** by decoupling sensitive data from the LLM's reasoning process:

1. **Context Isolation:** The "Secret Admin Code" was removed from the system prompt. The model no longer "knows" the secret.
2. **Tool-Gating:** I implemented LangChain’s **Tool-Calling framework**. The LLM acts as an orchestrator that must call a specific Python-based tool (retrieve_admin_code) to access sensitive information.
3. **Logic-Based Authorization:** The tool acts as a "Gate." It requires a valid **Access Token** checked via native Python logic. This creates a metaphorical "Air-Gap": even if the LLM is compromised via jailbreak, it cannot produce the secret without triggering the tool's internal logic-based validation.

---

### 4. Engineering for Constraints: Resource Optimization

A significant challenge was running this multi-model architecture on consumer-grade hardware (approx. 8GB RAM).

- **Optimization:** By utilizing **1B parameter models** (Llama 3.2 1B for reasoning and Llama Guard 3 1B for security), the memory footprint was reduced to ~2.5GB.
- **Reliability:** To handle the lower reasoning capabilities of 1B models, I implemented **Robust Error Handling** and **Few-Shot Prompting** to ensure the models follow the Tool-Calling schema correctly without crashing the pipeline.

---

### 5. Red Teaming Methodology

The system is validated using an automated **Multi-turn Red Teaming Framework** that simulates persistent adversarial behavior:

- **Social Engineering:** Mimicking authorized personnel to nudge the bot into revealing internal protocols.
- **Recursive Jailbreaking:** Using complex roleplay to test if the bot adheres to its "Tool-Gating" instructions over long conversation windows.
- **Evidence Generation:** The framework produces timestamped Markdown reports, providing a transparent audit trail of the security pipeline's performance.

---

### 6. Results & Key Findings

- **v3.0 Resilience:** Version 3.0 successfully mitigated 100% of the tested jailbreak scenarios. Even when the model was "convinced" to help the attacker, it could not leak the secret because the secret was not in its context.
- **Architectural Superiority:** The shift from "Instruction-based security" to "Architecture-based security" proved to be the most effective defense against context-extraction attacks.
- **Fail-Safe:** The combination of Llama Guard (Semantic) and Tool-Gating (Logic) provides a robust multi-layered defense that handles both intent-based and data-based threats.

---

### 7. Future Work: The "Indirect Injection" Frontier

The next phase will address **Indirect Prompt Injection**. This involves poisoning external data sources (RAG corpus) with malicious instructions. Future iterations will include "Ingestion Guardrails" to sanitize retrieved data before it is presented to the reasoning layer.

---

### 8. Conclusion

LLM Security is an architectural challenge. Version 3.0 of LLM-Guard demonstrates that the most effective way to protect sensitive data is to **isolate it from the LLM's context window** and gate access through verified, logic-based tools. This "Zero-Knowledge" approach represents the current gold standard for building secure, production-ready AI agents.

---

**Tech Stack:** Python, LangChain (LCEL), LangChain-Ollama, Llama 3.2, Llama Guard 3.  
**Project Repository:** **[https://github.com/MANU-de/LLM-Guard](https://github.com/MANU-de/LLM-Guard)**  
**Author:** Manuela Schrittwieser

