Build a production-style Multi-Agent Research Assistant using Python, FastAPI, Gemini API and Docker.

Architecture:

User Query
→ Orchestrator Agent
→ Research Agent
→ Analysis Agent
→ Summary Agent
→ Final Response

Requirements:

1. Create separate agent classes:

* ResearchAgent
* AnalysisAgent
* SummaryAgent
* OrchestratorAgent

2. FastAPI backend

Endpoints:

* POST /research
* GET /health

3. Request Flow:

* User submits a research topic
* ResearchAgent gathers detailed information
* AnalysisAgent extracts key insights and trends
* SummaryAgent generates a concise report
* Orchestrator coordinates the workflow

4. Use Gemini API through environment variables.

5. Project structure:

agents/
services/
api/
models/

6. Include:

* Pydantic schemas
* Error handling
* Logging
* requirements.txt
* Dockerfile
* README.md

7. Generate all files with production-ready code.

8. Add comments explaining the role of each agent.

9. Make the project runnable with:
   uvicorn main:app --reload

Generate the entire project structure and code.



Explain the architecture of this project in detail.

Excellent project to study — it follows a clean layered architecture with a workflow-orchestrated multi-agent core plus provider-level LLM failover.

High-Level Architecture
Request path is:

Client calls POST /research
API layer validates input and resolves dependencies
OrchestratorAgent runs sequential workflow:
ResearchAgent
AnalysisAgent
SummaryAgent
Each agent delegates generation to LLMService
LLMService selects provider order (gemini first or groq first)
Provider service (GeminiService or GroqService) calls external API
Output is assembled into typed response model and returned
Layer-by-Layer Breakdown
1) App Bootstrap Layer
main.py initializes FastAPI and logging, and mounts routes.

setup_logging() is called at startup.
app.include_router(research_router) registers endpoint handlers.
This keeps app startup minimal and pushes logic into dedicated modules.

2) API Layer (Transport + HTTP error mapping)
api/routes.py exposes:

GET /health -> lightweight service status
POST /research -> primary workflow entrypoint
Responsibilities in this layer:

Accept ResearchRequest body
Inject orchestrator via FastAPI dependency injection
Translate domain/service exceptions into HTTP responses:
ConfigurationError -> 500
GeminiServiceError / AgentExecutionError -> 502
unknown -> 500
So this layer is intentionally thin: no business logic, only transport concerns.

3) Dependency Composition Layer
services/dependencies.py builds the object graph per request:

LLMService
ResearchAgent
AnalysisAgent
SummaryAgent
OrchestratorAgent
This gives you clean inversion of control and easy future testing/mocking.

4) Orchestration Layer
agents/orchestrator_agent.py is the workflow engine.

It enforces strict sequence:

research notes -> analysis report -> summary report
It also centralizes lifecycle logging (starting / completed) and wraps any downstream failure in AgentExecutionError.

This is the “process manager” of your multi-agent design.

5) Specialized Agent Layer
Each agent has one job and one prompt contract:

ResearchAgent (agents/research_agent.py): gathers broad factual research
AnalysisAgent (agents/analysis_agent.py): extracts insights/trends/risks/actions
SummaryAgent (agents/summary_agent.py): converts analysis to executive summary
All three depend only on LLMService.generate(), so they are provider-agnostic.

This separation is the strongest part of your architecture: prompt specialization + pipeline composition.

6) LLM Abstraction + Provider Failover
services/llm_service.py is the provider router/fallback controller.

Reads LLM_PRIMARY_PROVIDER
Initializes provider clients if keys exist
Chooses provider order:
primary groq -> ["groq", "gemini"]
else default -> ["gemini", "groq"]
If first provider fails, logs and tries next
If all fail, raises GeminiServiceError("All configured LLM providers failed.")
This is effectively a resilience gateway for model providers.

7) Provider Adapter Layer
services/gemini_service.py
Uses google-genai client
Has internal Gemini-model fallback chain:
configured model
gemini-2.0-flash
gemini-1.5-flash-8b
Retries transient 503/unavailable conditions per model (up to 3 attempts)
Handles timeout and API failures consistently
So Gemini has both intra-provider retries/fallback and outer cross-provider fallback via LLMService.

services/groq_service.py
Uses Groq chat completion endpoint
Applies configured model + timeout + temperature
Returns first choice content
Converts provider failures to unified app error type
8) Configuration Layer
services/config.py uses pydantic-settings with cached settings (@lru_cache).

It centralizes runtime knobs:

app/log config
provider selection
Gemini key/model/temp
Groq key/model/temp
request timeout
This keeps env-driven behavior clean and avoids hard-coded runtime decisions.

9) Data Contract Layer
models/schemas.py defines all request/response DTOs:

ResearchRequest(topic)
AgentOutputs(research_notes, analysis_report, summary_report)
ResearchResponse(topic, result)
HealthResponse(status, service)
This gives you strict input validation and predictable output shape for clients.

10) Error Taxonomy + Logging
services/exceptions.py defines app-specific exceptions:

ConfigurationError
GeminiServiceError (now used as generalized provider failure signal)
AgentExecutionError
services/logger.py configures structured logs:

timestamp, level, logger name, message
This makes runtime diagnosis straightforward (you’ve already seen useful provider-failure traces in logs).

Architectural Strengths
Clear separation of concerns by layer
Strong workflow composition via orchestrator
Provider-agnostic agents through shared LLM interface
Multi-level resilience:
internal Gemini retry/fallback
cross-provider Gemini <-> Groq failover
Typed API contracts with Pydantic
Centralized config + logging + error mapping
One subtle design note
GeminiServiceError is now used for both Gemini and Groq failures (naming mismatch vs usage).
It works functionally, but semantically it’s become a generic LLM failure type. If you later refactor, you may want a provider-neutral error class name.




