# Part 3 — Release Strategy

Answer each section with specific, practical details. Reference the Emporyum Tech bot architecture where relevant.

---

## 3.1 — Canary Release

_Describe step-by-step how you would perform a canary release for a new version of the chatbot API._

**Your answer:**

To perform a canary release for a new version of the Emporyum Tech chatbot API in a Kubernetes cluster using Argo CD, follow these steps:

1. **Prepare the New Version**: Build and tag the new Docker image for the chatbot API (e.g., `emporyum/chatbot-api:v2.0`). Ensure the image includes all necessary components like adapters (e.g., chat_agent.py), routers (e.g., chat.py, health.py), and domain logic (e.g., handle_general.py).

2. **Update Kubernetes Manifests**: Modify the Kubernetes deployment YAML to reference the new image tag. Use a canary deployment strategy by creating a separate deployment for the canary version alongside the stable one. For example:
   - Stable deployment: `emporyum-chatbot-stable` with image `v1.0`
   - Canary deployment: `emporyum-chatbot-canary` with image `v2.0`
   - Both deployments should use the same Service to route traffic.

3. **Configure Argo CD Application**: In Argo CD, ensure the application is set up to sync with the Git repository containing the Kubernetes manifests. Use Argo CD's sync policies to automate deployment.

4. **Implement Traffic Splitting**: Use a Kubernetes Ingress controller (e.g., NGINX Ingress) or a service mesh like Istio to route a small percentage of traffic (e.g., 5-10%) to the canary deployment. For Istio, configure VirtualService with traffic policies:
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: chatbot-api
   spec:
     http:
     - route:
       - destination:
           host: emporyum-chatbot-stable
         weight: 90
       - destination:
           host: emporyum-chatbot-canary
         weight: 10
   ```

5. **Deploy via Argo CD**: Commit the updated manifests to the Git repository. Argo CD will detect the changes and sync the cluster, deploying the canary version.

6. **Monitor and Validate**: Use monitoring tools like Prometheus and Grafana to track metrics such as error rates, latency, and user interactions specific to the chatbot API (e.g., chat completion success rates). Monitor logs from the adapters and routers for any anomalies.

7. **Gradual Rollout**: If metrics are positive, gradually increase traffic to the canary (e.g., 20%, 50%, 100%) by updating the traffic weights in the VirtualService.

8. **Full Promotion or Rollback**: Once confident, promote the canary to stable by updating the stable deployment's image and removing the canary deployment.

---

## 3.2 — Rollback Strategy

_How would you implement instant rollback? How do you handle state/data consistency during rollback?_

**Your answer:**

For instant rollback in a Kubernetes cluster using Argo CD:

1. **Argo CD Rollback**: Argo CD maintains deployment history. To rollback instantly, use the Argo CD CLI or UI to revert to a previous sync revision. For example: `argocd app rollback emporyum-chatbot --revision <previous-revision>`.

2. **Kubernetes Deployment Rollback**: If using standard Kubernetes deployments, rollback via `kubectl rollout undo deployment/emporyum-chatbot`. For canary setups, scale down the canary deployment to 0 replicas and scale up the stable one.

3. **Blue-Green or Rolling Updates**: Implement a blue-green strategy where the previous version remains running. Switch traffic back using the Ingress/Service mesh configuration.

For state/data consistency during rollback:
- **Stateless Design**: The Emporyum Tech bot architecture uses adapters and domain functions that are stateless, relying on external services for data (e.g., knowledge base via knowledge_base.py). Rollback doesn't affect in-memory state.
- **External State**: If using databases or caches (e.g., for user data via fetch_user_data.py), ensure schema migrations are backward-compatible. Use database versioning tools like Flyway to handle rollbacks.
- **Session Handling**: For ongoing user chats, implement session affinity or use distributed caches (e.g., Redis) that persist across deployments. During rollback, ensure active sessions are gracefully handled by draining connections before scaling down.
- **Data Validation**: Post-rollback, run automated tests (e.g., via the tests/ directory) to verify data integrity and API responses.

---

## 3.3 — Incident Response

_Scenario: You deploy a new version at 2:00 PM Tuesday. By 2:30 PM, error rate spikes from 0.1% to 15%. Walk us through your response._

**Your answer:**

1. **Detection (2:30 PM)**: Monitoring alerts (e.g., from Prometheus) notify the team of the error rate spike. Check dashboards for affected components, such as the chat router or adapters in the Emporyum Tech bot.

2. **Initial Assessment (2:31 PM)**: Review logs in Kubernetes (via `kubectl logs`) and Argo CD for deployment issues. Check if the spike correlates with the new version rollout.

3. **Isolate Traffic (2:32 PM)**: If using canary deployment, immediately reduce canary traffic to 0% via Argo CD/Istio to prevent further impact.

4. **Rollback (2:33 PM)**: Trigger instant rollback using Argo CD: `argocd app rollback emporyum-chatbot`. Scale back to the previous stable version.

5. **Verify Rollback (2:35 PM)**: Monitor metrics to confirm error rate returns to baseline. Run health checks on the API endpoints (e.g., /health via health.py).

6. **Root Cause Analysis (2:40 PM)**: Form a war room. Analyze code changes, especially in adapters/chains (e.g., general_chain.py) or domain functions. Check for compatibility issues with external dependencies.

7. **Communication (Ongoing)**: Notify stakeholders via Slack/email. Update incident tracking (e.g., in Jira).

8. **Post-Incident (3:00 PM+)**: Document findings, implement fixes, and plan a controlled redeploy. Enhance monitoring for similar issues, such as adding more granular metrics for chatbot interactions.

---
