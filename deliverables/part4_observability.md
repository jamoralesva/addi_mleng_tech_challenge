# Part 4 — Observability & Monitoring

---

## 4.2 — Monitoring Dashboard Design

_What panels/graphs would you include? Organize by: system health, business metrics, and LLM-specific metrics._

**Your answer:**

**System Health:**
- CPU and Memory Usage: Line graphs showing resource utilization across pods in the Kubernetes cluster for the chatbot API components (e.g., routers, adapters).
- Pod Health and Restarts: Status indicators and counters for pod restarts, focusing on adapters like chat_agent.py and routers like chat.py.
- Network I/O: Graphs for ingress/egress traffic to detect bottlenecks in API calls.

**Business Metrics:**
- API Request Rate: Time-series graph of requests per second to endpoints like /chat, correlating with user interactions.
- User Session Duration: Histogram of chat session lengths, derived from domain functions like handle_general.py.
- Error Rate by Endpoint: Bar chart showing 4xx/5xx errors per router (e.g., health.py vs. chat.py).

**LLM-Specific Metrics:**
- Model Response Time: Latency graphs for LLM calls in chains like general_chain.py.
- Token Usage: Counters for input/output tokens per request, to monitor cost efficiency.
- Model Accuracy/Quality: Custom metrics from adapters, such as response relevance scores based on knowledge base queries.

---

## 4.3 — Alert Rules

_Define at least 5 alerts. For each, specify: the metric, threshold, severity (warning/critical), and action._

| # | Metric | Threshold | Severity | Action |
|---|--------|-----------|----------|--------|
| 1 | API Error Rate | >5% over 5 minutes | Critical | Page on-call engineer; rollback deployment via Argo CD |
| 2 | Pod Restarts | >3 restarts per pod in 10 minutes | Warning | Investigate logs; scale pods if needed |
| 3 | LLM Latency | >2 seconds average over 5 minutes | Critical | Alert team; check model performance in adapters |
| 4 | Memory Usage | >85% sustained for 5 minutes | Warning | Scale resources; review memory leaks in domain functions |
| 5 | Token Cost Anomaly | >20% increase in daily token usage | Warning | Review usage patterns; optimize prompts in chains |

**Additional context for your alert design:**
Alerts are configured in Prometheus with PagerDuty integration for critical alerts. Thresholds are based on baseline metrics from production traffic, with auto-scaling rules in Kubernetes to handle warnings before escalation.

---

## 4.4 — LLM-Specific Monitoring

_How would you detect: model degradation, cost anomalies, latency degradation, prompt injection attempts?_

**Your answer:**

- **Model Degradation:** Monitor response quality via custom metrics in adapters (e.g., sentiment analysis or relevance scores from chat_agent.py). Use A/B testing with shadow deployments to compare outputs against a baseline model.
- **Cost Anomalies:** Track token usage per request in Prometheus, alerting on spikes. Integrate with LLM provider APIs (e.g., OpenAI) for real-time cost monitoring.
- **Latency Degradation:** Measure end-to-end latency for LLM calls in chains like general_chain.py. Set alerts for p95 latency exceeding thresholds.
- **Prompt Injection Attempts:** Log and analyze input prompts for suspicious patterns (e.g., via regex in data_filter.py). Use anomaly detection on prompt lengths or keywords, flagging for manual review.

---

## 4.5 — SLOs and SLIs

_Define at least 3 SLIs, their target SLOs, and your error budget policy._

| SLI | Target SLO | Measurement Method |
|-----|------------|-------------------|
| API Availability | 99.9% uptime | Percentage of successful requests (2xx status codes) over total requests, measured via Prometheus |
| API Latency | 95% of requests <500ms | P95 latency histogram from Istio or application metrics |
| Chat Response Quality | 90% user satisfaction | Custom metric from post-interaction surveys or automated quality checks in adapters |

**Error budget policy:**
The error budget is 0.1% per month (equivalent to ~43 minutes of downtime). If exceeded, halt feature releases and focus on reliability improvements. Track budget burn rate weekly, with automated alerts at 50% and 80% consumption.

---
