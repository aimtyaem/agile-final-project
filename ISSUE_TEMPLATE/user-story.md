---
name: GenAI User Story
about: Standardized format for AI transformation tasks.
title: "[USE-CASE]: "
labels: ["Golden Use Case"]
assignees: ''
---

## 1. Problem Statement
To avoid "AI Distractions," define the specific friction point being solved.

As a **[Role]**  
I need **[Function/Capability]**  
So that **[Measurable Benefit/ROI]**

---

## 2. AI Risk Assessment Addendum (Mandatory)
Every GenAI feature must be evaluated for governance and safety before development.

- [ ] **Explainability**: Can the model's output be challenged, traced, or explained to a non-technical stakeholder?
- [ ] **Data Privacy**: Does this involve PII (Personally Identifiable Information), sensitive financial data, or trade secrets?
- [ ] **Hallucination Risk**: Is the output non-deterministic? Rate the risk: (Low / Medium / High).
- [ ] **Bias Audit**: Have potential biases in the training data or model output been identified?

---

## 3. Drill-Based Learning & Interaction
Use AI as a strategy partner during development to push beyond first-order thinking.

- [ ] **Consequence Analysis**: Have you asked Copilot/LLM to identify the potential negative consequences or edge cases of this design choice?
- [ ] **Adversarial Testing**: Has the prompt/logic been tested against at least 3 adversarial or "jailbreak" inputs?
- [ ] **Alternative Architectures**: Did you use GenAI to simulate at least one alternative technical approach?

---

## 4. Technical Feasibility & Viability
- [ ] **Token/Cost Estimate**: Estimated cost per 1,000 executions.
- [ ] **Latency Requirements**: Does the response time meet the defined User Experience (UX) threshold?
- [ ] **Model Selection**: Justification for the chosen model (e.g., Flash for speed vs. Pro for reasoning).

---

## 5. Definition of Done (GenAI Criteria)
- [ ] **Production Data Connectivity**: Feature is connected to live production data (No static CSVs or mockups).
- [ ] **Human-in-the-loop (HITL)**: Factual Consistency Score verified by a domain expert.
- [ ] **Prompt Library**: Optimized prompts and system instructions are archived in the `/prompts/` library.
- [ ] **Monitoring**: Evaluation metrics (LLM-as-a-judge or heuristic) are integrated into the dashboard.

---

## Strategic Risk/Reward Profile
- **Technical Risk**: High probability of "Model Drift" or non-deterministic behavior if the Factual Consistency Score is not monitored post-launch.
- **Market Reward**: Moving from PoC to a "Golden Use Case" reduces the cost of subsequent AI projects by creating a reusable agentic framework.