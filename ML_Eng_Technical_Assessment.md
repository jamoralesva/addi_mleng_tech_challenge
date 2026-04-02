# ML Engineering Technical Assessment

## Addi — AI & ML Ops Team

---

## General Instructions

Welcome to the ML Engineering Technical Assessment for **Addi**. This assessment is designed for the **ML Engineer** position within the AI & ML Ops team.

### What You Need to Do

Complete the **ML Ops Challenge** in the `ml_ops_challenge/` folder. The challenge is structured in 6 parts that cover the full lifecycle of taking an AI service to production: API design, containerization, A/B testing, release strategy, observability, production readiness, and architecture reasoning.

You will receive a **working chatbot** built with LangGraph and OpenAI. Your job is **not** to improve the bot's AI quality — your job is to make it production-ready.

### Timeline

You have **5 calendar days** from the date you receive this assessment to submit your work. If you need additional time, please let us know in advance.

### Submission

- Fork or clone the repository you received along with this document.
- Work on the challenge in the `ml_ops_challenge/` folder.
- Push your completed work to a GitHub repository (public or private — if private, grant access to the reviewers we specify).
- Send us the repository link by the deadline.

### AI Tools — Required

We **expect you to use AI tools** during this assessment. Tools like ChatGPT, GitHub Copilot, Claude, Cursor, and others are part of how modern engineers work, and we want to see how you work with them. **AI maturity is part of what we evaluate** — how effectively you leverage these tools, how you validate their output, and how you integrate them into your workflow.

Include a short note with each deliverable mentioning which tools you used and how (e.g., "Used Copilot for Dockerfile boilerplate" or "Asked Claude about Kubernetes canary patterns, then adapted to our context"). This is not a formality — we genuinely want to understand your AI workflow.

The key thing is: **make sure you can explain and defend every part of your solution.** Using AI effectively is a skill we value. However, if any part of your submission was AI-generated and you can't walk us through the reasoning behind it, that will work against you. The best candidates use AI to move faster and think deeper — not to skip the thinking.

### Follow-Up

After submission, we will schedule a **technical conversation** where you will walk us through your solutions — the architecture decisions, the trade-offs, and the reasoning behind your approach. You must be able to explain and defend every part of your work.

### Questions?

If you have any questions about the assessment, setup, or expectations, please don't hesitate to reach out. We'd rather answer a question than have you spend time on a wrong assumption.

---

<div class="page-break"></div>

## Challenge — ML Ops: Emporyum Tech Assistant (Production)

**Folder:** `ml_ops_challenge/`

### Overview

You receive a working chatbot for **Emporyum Tech**, a Colombian e-commerce platform. The bot is built with LangGraph (state graph) and OpenAI (GPT-4o-mini). It answers customer questions about orders, payments, products, returns, and account issues using a Knowledge Base and personalized user data.

Your task is to take this bot from a development prototype to a production-ready service.

### Time Estimate

**~20 hours** across 5 calendar days. You do not need to finish every single detail — a well-designed partial solution with clear documentation is better than a rushed complete one.

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [Docker](https://docs.docker.com/get-docker/) installed
- An LLM API key — we will contact you to provide one. You may also use your own if you prefer (GPT-4o-mini is sufficient and cost-effective).

### Quick Start

Run the bot first. See it work. Understand the code.

```bash
# 1. Install dependencies
poetry install

# 2. Create your .env file and add the LLM API key we provide (or your own)
cp .env.example .env

# 3. Run the assistant interactively
poetry run python tests/inline.py
```

> **Having trouble setting up your local environment?** Don't hesitate to reach out to us — we're happy to help you get up and running so you can focus on the challenge itself.

Try a few conversations and then read the source code — especially `graph.py`, `handle_general.py`, and `general_chain.py`. Understanding the architecture is critical for Parts 2 and 6.

### The 6 Parts

| Part | Focus | Type |
|------|-------|------|
| 1. API, Containerization & CI/CD | Serve the bot, Dockerize it, automate builds | Hands-on |
| 2. A/B Testing | Split an agent into two versions, implement feature toggle | Hands-on + design |
| 3. Release Strategy | Canary release, rollback, incident response | Written |
| 4. Observability & Monitoring | Structured logging, alerts, SLOs | Hands-on + written |
| 5. Production Readiness | State management, security, cost, scaling | Written |
| 6. Architecture Reasoning | Latency analysis, operational trade-offs, optimization | Written + design |

### Project Structure

```
ml_ops_challenge/
|
|-- README.md                            # Detailed instructions for each part
|-- pyproject.toml                       # Project dependencies
|-- .env.example                         # Template for your API key
|
|-- source/
|   |-- application/
|   |   |-- state.py                     # GraphState TypedDict
|   |   |-- graph.py                     # LangGraph workflow definition
|   |
|   |-- domain/
|   |   |-- fetch_user_data.py           # Fetches user data from mock profiles
|   |   |-- handle_general.py            # Generic agent handler (key file for Part 2)
|   |
|   |-- adapters/
|       |-- chains/
|       |   |-- general_chain.py         # LLM chain with system prompt (OpenAI)
|       |-- utils/
|           |-- mock_data.py             # 8 mock user profiles
|           |-- data_filter.py           # Utility to filter user data
|           |-- knowledge_base.py        # Knowledge Base definitions
|
|-- tests/
|   |-- inline.py                        # Interactive testing script
|
|-- deliverables/                        # >>> YOUR WORK GOES HERE <<<
    |-- part1_api_and_containerization/  # API, Docker, CI/CD, tests
    |-- part2_ab_testing/               # Agent split, feature toggle, measurement plan
    |-- part3_release_strategy.md       # Canary, rollback, incident response
    |-- part4_observability.md          # Monitoring, alerts, SLOs
    |-- part5_production_readiness.md   # State, security, cost, scaling
    |-- part6_architecture_reasoning.md # Cognitive architecture & latency analysis
```

### Deliverables

1. **A production-ready API** — FastAPI wrapping the chatbot, with Dockerfile, docker-compose, and a CI/CD pipeline definition. Working tests.

2. **A/B testing implementation** — Two agent versions with a feature toggle mechanism and a written measurement plan.

3. **Release strategy** — Written canary release plan, rollback strategy, and incident response walkthrough.

4. **Observability** — Structured logging (hands-on) and a written monitoring/alerting design with SLOs.

5. **Production readiness answers** — Written answers on state management, security, cost, and scaling.

6. **Architecture reasoning** — Written analysis of latency trade-offs, operational implications of multi-agent routing, and a concrete optimization proposal.

### Evaluation Criteria

What we value, roughly in order of importance:

- **API, containerization & CI/CD** — Working API, clean Dockerfile, sensible CI/CD pipeline. Can you build a deployable service?
- **A/B testing implementation** — Deterministic traffic split, configurable without redeployment, clean code, practical measurement plan.
- **Observability & monitoring** — Structured logging in code, practical alert design, well-defined SLOs. Do you know what to watch in production?
- **Release strategy & incident response** — Practical canary/rollback plan, realistic incident walkthrough. Can you deploy safely?
- **Architecture reasoning** — Shows understanding of latency/quality trade-offs in multi-agent LLM systems, practical optimization proposal.
- **Production readiness** — State management, security, scaling. Shows real production experience.
- **Code quality & documentation** — Clean code, clear docs, reproducible setup.

### Tips

1. **Run the bot first** — verify it works before wrapping it in anything.
2. **Read the source code** — especially `graph.py`, `handle_general.py`, and `general_chain.py`. Understanding the architecture is critical for Parts 2 and 6.
3. **Start with Part 1** — everything else builds on having a working API.
4. **Working code > perfect documentation.** But good documentation on top of working code is ideal.
5. **Be practical.** We want production-tested approaches, not theoretical designs.
6. **Simple and working is better than complex and broken.**

Full details, instructions, and deliverable templates are in `ml_ops_challenge/README.md`.

---

Good luck — we look forward to reviewing your work!
