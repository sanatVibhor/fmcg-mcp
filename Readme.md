# FMCG Business Copilot

### Enterprise RAG + MCP + Agentic AI for FMCG Decision Intelligence

> A local-first enterprise AI system that combines **LLM reasoning, Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), structured business data, and controlled tool execution** to answer complex FMCG business questions and take governed actions.

---

## 1. Executive Summary

The **FMCG Business Copilot** is an enterprise-style AI decision-support system designed around a realistic FMCG business scenario.

The system allows a business user to ask questions such as:

> **"Why did Dove Shampoo sales decline in South India during Q3, and what should we do about it?"**

Unlike a conventional chatbot or document-based RAG application, the system does not rely on a single knowledge source.

Answering the question requires the AI to reason across:

- Sales data
- Inventory availability
- Pricing
- Promotions
- Competitor activity
- Market intelligence documents
- Business rules
- Potential operational actions

The project therefore demonstrates a more complete **Agentic AI architecture**:

```text
                         ┌──────────────────────┐
                         │      User / UI       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Agent Runtime    │
                         │                      │
                         │  Local LLM + Planner │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
              ┌─────────────┐              ┌─────────────┐
              │     RAG     │              │     MCP     │
              │             │              │             │
              │ Knowledge   │              │ Tool Layer  │
              │ Retrieval   │              │             │
              └──────┬──────┘              └──────┬──────┘
                     │                            │
                     ▼                     ┌──────┼─────────┐
              ┌─────────────┐              │      │         │
              │ Vector DB   │              ▼      ▼         ▼
              └─────────────┘             SQL    APIs    Business
                                                    Systems  Actions
```

The project is intentionally **local-first** and uses synthetic data so that the entire architecture can be developed, tested, and demonstrated without access to proprietary enterprise systems.

---

# 2. Problem Statement

Traditional enterprise chatbots generally fall into one of two categories.

### Document RAG

```text
User
 ↓
Question
 ↓
Vector Search
 ↓
Documents
 ↓
LLM
 ↓
Answer
```

This works well when the answer exists inside static documents.

However, FMCG decision-making frequently requires information that changes continuously.

For example:

> "Why did Dove Shampoo sales decline in South India?"

A market report might explain competitor behavior.

A sales database contains actual performance.

An inventory system contains availability.

A promotion system contains discounts.

A pricing system contains commercial information.

No individual source provides the complete answer.

---

# 3. The Core Problem

The system must answer business questions requiring **multi-source reasoning** across:

```text
Unstructured Knowledge
        +
Structured Data
        +
Operational Systems
        +
Business Context
        +
AI Reasoning
```

The objective is therefore not simply:

> "Build a chatbot."

The objective is:

> **Build an AI agent capable of understanding a business question, determining what information is required, retrieving information from appropriate sources, reasoning over the evidence, and executing controlled business actions when authorized.**

---

# 4. Example Business Scenario

Consider a fictional FMCG organization with products such as:

- Dove Shampoo
- Dove Conditioner
- Lux Soap
- Surf Excel
- Vaseline Body Lotion
- Axe Body Spray
- Pepsodent
- Horlicks

A business manager asks:

> **"Why did Dove Shampoo sales decline in South India during Q3, and what should we do?"**

The agent must investigate rather than immediately generate an answer.

### Investigation

```text
Question
   │
   ▼
Sales performance?
   │
   ├── Query sales
   │
   ▼
Inventory problem?
   │
   ├── Query inventory
   │
   ▼
Promotion change?
   │
   ├── Query promotions
   │
   ▼
Competitive pressure?
   │
   ├── Query competitor activity
   │
   ▼
Market context?
   │
   ├── Retrieve market intelligence
   │
   ▼
Synthesize evidence
   │
   ▼
Business recommendation
```

The resulting answer might identify:

```text
Sales decline              → ~19%

Promotion support          → 15% → 5%

Kerala inventory           → ~55–68% availability

Competitor activity        → 20% discount

Competitive intensity      → High
```

The agent can then explain the likely contributors and recommend actions.

---

# 5. Why MCP?

A major architectural objective of this project is to demonstrate the distinction between:

### RAG

RAG answers:

> "What does our knowledge base say?"

### MCP

MCP enables the AI application to interact with external tools and systems.

For example:

```text
get_sales()
get_inventory()
get_promotions()
get_competitor_activity()
search_market_reports()
create_inventory_alert()
```

The agent does not need direct unrestricted access to the underlying systems.

Instead:

```text
Agent
  │
  │ MCP
  ▼
MCP Server
  │
  ├── PostgreSQL
  ├── Internal APIs
  ├── Knowledge systems
  └── Controlled business actions
```

This creates a clear separation between:

**Reasoning**

and

**System access.**

---

# 6. MCP vs RAG

These technologies solve different problems.

| Capability | RAG | MCP |
|---|---|---|
| Retrieve documents | Yes | Possible through tools |
| Semantic search | Yes | Not inherently |
| Query structured data | Possible | Yes, through tools |
| Execute business actions | No | Yes |
| Tool discovery | No | Yes |
| Connect enterprise systems | Indirectly | Yes |
| Provide contextual knowledge | Yes | Can expose resources |
| Replace the LLM | No | No |
| Replace a database | No | No |
| Replace RAG | No | No |

The architecture intentionally uses both.

```text
                 AI Agent
                    │
           ┌────────┴────────┐
           │                 │
          RAG               MCP
           │                 │
      Knowledge          Tools / Systems
           │                 │
     Vector Database      PostgreSQL
                          APIs
                          Actions
```

---

# 7. Project Goals

The project is designed to demonstrate the following engineering capabilities.

### AI Engineering

- Local LLM inference
- Prompt engineering
- Tool calling
- Agent orchestration
- Structured output
- Context management
- Hallucination reduction

### RAG Engineering

- Document ingestion
- Chunking
- Embeddings
- Vector retrieval
- Metadata filtering
- Retrieval evaluation
- Context construction
- Grounded generation

### Agentic AI

- Tool selection
- Multi-step reasoning
- Tool execution
- Observation → reasoning → action loops
- Controlled actions
- Failure handling
- Agent traces

### Backend Engineering

- FastAPI
- PostgreSQL
- Supabase
- MCP server
- API design
- Authentication and authorization

### AI System Design

- Separation of concerns
- Tool isolation
- Least-privilege access
- Auditability
- Observability
- Evaluation
- Failure recovery

---

# 8. Architecture

## High-Level Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                        USER / BUSINESS                       │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                         WEB APPLICATION                      │
│                           React UI                           │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                         API / GATEWAY                        │
│                           FastAPI                            │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       AGENT RUNTIME                          │
│                                                              │
│  Local LLM                                                   │
│  ├── Intent understanding                                    │
│  ├── Tool selection                                          │
│  ├── Retrieval decisions                                     │
│  ├── Evidence synthesis                                      │
│  └── Action planning                                         │
└───────────────┬──────────────────────────┬───────────────────┘
                │                          │
                ▼                          ▼
       ┌────────────────┐         ┌────────────────────┐
       │      RAG       │         │        MCP         │
       │    Pipeline    │         │      Server       │
       └───────┬────────┘         └─────────┬──────────┘
               │                            │
               ▼                            ▼
       ┌────────────────┐       ┌──────────────────────┐
       │   Vector DB    │       │ Structured Systems   │
       │                │       │                      │
       │ Market Reports │       │ PostgreSQL           │
       │ Strategy Docs  │       │ Sales                │
       │ Research       │       │ Inventory            │
       └────────────────┘       │ Promotions           │
                                │ Pricing              │
                                │ Competitors          │
                                └──────────────────────┘
```

---

# 9. Data Architecture

The project uses synthetic FMCG data designed to represent a realistic enterprise data environment.

### Current datasets

```text
products.csv
stores.csv
sales.csv
inventory.csv
promotions.csv
competitor_activity.csv
pricing.csv
```

### Planned PostgreSQL schema

```text
products
   │
   ├──────── sales
   │
   ├──────── inventory
   │
   ├──────── promotions
   │
   └──────── pricing

stores
   │
   └──────── sales
              │
              └── region / state / channel
```

The CSV files serve as the reproducible source dataset.

Supabase PostgreSQL will serve as the operational structured-data layer.

---

# 10. Synthetic Data Philosophy

The data is intentionally **not purely random**.

A completely random dataset would make the AI system difficult to evaluate because there would be no meaningful underlying business narrative.

Instead, the dataset contains controlled signals.

For example:

### Dove Shampoo

South India:

```text
Q2 → stronger performance

Q3 → ~19% decline
```

### Promotion

```text
Q2 → 15%
Q3 → 5%
```

### Kerala inventory

```text
Normal availability → ~80–100%

Q3 scenario → ~55–68%
```

### Competitor

```text
Competitor:
L'Oreal

South India:
20% discount

Activity:
High
```

These signals allow the agent to perform a meaningful investigation.

The dataset therefore acts as a **controlled experimental environment** for evaluating agent behavior.

---

# 11. MCP Tool Layer

The MCP server will expose business-level operations rather than arbitrary database access.

### Planned tools

```text
get_sales()
```

Returns sales performance based on product, region, state, channel, and period.

```text
get_inventory()
```

Returns inventory availability and stock information.

```text
get_promotions()
```

Returns active and historical promotional activity.

```text
get_competitor_activity()
```

Returns competitor campaigns and pricing pressure.

```text
search_market_reports()
```

Provides access to relevant market intelligence.

```text
create_inventory_alert()
```

Creates an operational alert after appropriate authorization.

---

# 12. Why Business-Level Tools?

The MCP layer should not expose:

```text
execute_arbitrary_sql()
```

to the LLM.

Instead, expose constrained operations:

```text
get_sales(
    product_id,
    region,
    quarter
)
```

This provides:

- Smaller attack surface
- Better validation
- Predictable behavior
- Easier authorization
- Better observability
- Easier testing
- Lower risk of unintended data access

The principle is:

> **Expose capabilities, not infrastructure.**

---

# 13. Agent Execution Example

User:

> "Why did Dove Shampoo sales decline in South India during Q3?"

The agent might generate an execution trace:

```text
USER_QUERY
    ↓
INTENT_ANALYSIS
    ↓
get_sales()
    ↓
OBSERVATION
    ↓
get_inventory()
    ↓
OBSERVATION
    ↓
get_promotions()
    ↓
OBSERVATION
    ↓
get_competitor_activity()
    ↓
OBSERVATION
    ↓
search_market_reports()
    ↓
EVIDENCE_SYNTHESIS
    ↓
BUSINESS_RECOMMENDATION
```

The final response should be based on retrieved evidence rather than unsupported model knowledge.

---

# 14. Example Agent Response

```text
Dove Shampoo sales declined approximately 19% in South India
during Q3 compared with the previous quarter.

The strongest contributing factors identified were:

1. Reduced promotional support
   Q2 promotion: 15%
   Q3 promotion: 5%

2. Inventory availability
   Kerala availability fell to approximately 55–68%.

3. Competitive pressure
   L'Oreal launched a high-intensity South India campaign
   with approximately 20% discounting.

Recommended actions:

• Restore targeted promotional support.
• Prioritize Kerala inventory replenishment.
• Monitor competitor pricing weekly.
• Evaluate retailer-level promotion effectiveness.

Confidence:
High for observed correlations.
Further causal analysis would be required before claiming
that any individual factor independently caused the decline.
```

That final distinction is intentional.

The system should differentiate **observed evidence** from **causal claims**.

---

# 15. RAG Layer

The RAG layer will contain synthetic enterprise documents such as:

```text
documents/
├── south_india_market_report_q3.pdf
├── competitor_analysis_q3.pdf
├── dove_category_strategy.pdf
├── retail_market_report.pdf
├── promotional_strategy.pdf
└── inventory_strategy.pdf
```

Pipeline:

```text
Documents
    ↓
Parsing
    ↓
Cleaning
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Database
    ↓
Retriever
    ↓
Context Construction
    ↓
LLM
```

Future iterations may include:

- Hybrid retrieval
- BM25
- Dense retrieval
- Reranking
- Query rewriting
- Metadata filtering
- Context compression
- Retrieval evaluation

---

# 16. Local-First Design

The project is intentionally designed to run locally wherever practical.

### Planned stack

| Layer | Technology |
|---|---|
| UI | React |
| API | FastAPI |
| LLM | Local open-weight model |
| LLM Runtime | Ollama / equivalent |
| Embeddings | Local embedding model |
| RAG | Python |
| Vector DB | Chroma / equivalent |
| Database | PostgreSQL |
| Managed DB | Supabase |
| Agent Tool Protocol | MCP |
| Containerization | Docker |
| Orchestration | Kubernetes — future |
| Observability | Structured logs / traces |

The architecture is designed so that individual components can later be replaced without redesigning the entire system.

---

# 17. Security Principles

Even though the data is synthetic, the architecture follows enterprise security principles.

### Database access

The LLM should never receive raw database credentials.

```text
LLM
 ↓
MCP
 ↓
Authorized service
 ↓
Database
```

### Least privilege

Each MCP tool should have only the permissions it requires.

### Input validation

Tool parameters should be validated before execution.

### Output validation

Tool results should conform to predictable schemas.

### No arbitrary SQL

The LLM should not receive unrestricted SQL execution capabilities.

### Audit logging

Each tool invocation should be traceable:

```text
user
timestamp
tool
arguments
result
execution_time
success/failure
```

### Action confirmation

High-impact operations should require explicit user confirmation.

---

# 18. Observability

An enterprise AI system should not be a black box.

The system will maintain traces such as:

```text
Request ID
    │
    ├── Agent decision
    │
    ├── RAG retrieval
    │     ├── documents retrieved
    │     └── relevance scores
    │
    ├── MCP invocation
    │     ├── tool
    │     ├── arguments
    │     ├── latency
    │     └── result
    │
    └── Final response
```

This allows investigation of questions such as:

> Why did the agent choose this tool?

> Why did retrieval fail?

> Which source influenced the answer?

> How long did the database query take?

> Did the model hallucinate a business metric?

---

# 19. Evaluation Strategy

The system will not be evaluated only on whether the final answer "sounds good."

Evaluation will happen at multiple layers.

### Retrieval evaluation

Metrics:

- Precision
- Recall
- MRR
- Hit Rate

### Tool selection

Measure:

```text
Correct tool selected?
Correct parameters?
Unnecessary tool calls?
Missing required tool?
```

### Data accuracy

Compare generated answers against ground-truth SQL calculations.

### Groundedness

Check whether claims are supported by retrieved evidence.

### Hallucination

Identify claims that cannot be supported by:

- Structured data
- Retrieved documents
- Tool outputs

### Agent efficiency

Track:

```text
Number of tool calls
Latency
Token usage
Repeated calls
Failed calls
```

---

# 20. Ground Truth

Because this project uses synthetic data, we can create deterministic ground truth.

For example:

```text
Expected:

South India Q3 Dove Shampoo decline ≈ 19%

Promotion:
15% → 5%

Kerala inventory:
55–68%

Competitor:
L'Oreal

Competitor discount:
20%
```

This makes the project useful not just as a demonstration, but as a controlled environment for **agent evaluation**.

---

# 21. Failure Scenarios

A serious agent system must handle failure.

The project will eventually test:

### MCP unavailable

```text
Agent
 ↓
MCP
 ↓
TIMEOUT
```

Expected behavior:

> Clearly state that live business data could not be retrieved rather than fabricating an answer.

### Database unavailable

The system should fail gracefully.

### Missing data

If no inventory data exists:

> "Inventory information is unavailable for the requested period."

Not:

> "Inventory was normal."

### Ambiguous question

For:

> "Why did Dove perform badly?"

the agent should request clarification:

```text
Which geography and time period would you like me
to analyze?
```

### Tool returns invalid data

The agent should validate and reject malformed responses.

---

# 22. Project Development Phases

## Phase 1 — Synthetic Data

- Generate FMCG master data
- Generate sales
- Generate inventory
- Generate promotions
- Generate pricing
- Generate competitor activity

## Phase 2 — Database

- PostgreSQL schema
- Supabase deployment
- Indexing
- Constraints
- Relationships

## Phase 3 — RAG

- Document generation
- Ingestion
- Chunking
- Embeddings
- Vector search
- Retrieval evaluation

## Phase 4 — MCP

- MCP server
- Tool definitions
- Parameter validation
- Database integration
- Tool error handling

## Phase 5 — Agent

- Local LLM
- Tool calling
- RAG integration
- Multi-step execution
- Structured responses

## Phase 6 — Application

- React interface
- Streaming responses
- Tool execution visualization
- Evidence panel
- Business recommendations

## Phase 7 — Production Engineering

- Authentication
- Authorization
- Rate limiting
- Audit logs
- Observability
- Evaluation framework
- Dockerization

## Phase 8 — Scale

Future work:

- Kubernetes
- Horizontal scaling
- Queue-based tool execution
- Caching
- Model gateway
- Distributed tracing
- Production vector database
- Enterprise identity
- Secrets management

---

# 23. Repository Structure

Target repository:

```text
FMCG-MCP/
│
├── README.md
│
├── data/
│   ├── products.csv
│   ├── stores.csv
│   ├── sales.csv
│   ├── inventory.csv
│   ├── promotions.csv
│   ├── competitor_activity.csv
│   └── pricing.csv
│
├── scripts/
│   └── generate_data.py
│
├── backend/
│   ├── api/
│   ├── agent/
│   ├── rag/
│   └── services/
│
├── mcp_server/
│   ├── server.py
│   ├── tools/
│   │   ├── sales.py
│   │   ├── inventory.py
│   │   ├── promotions.py
│   │   └── competitors.py
│   └── schemas/
│
├── database/
│   ├── schema.sql
│   ├── migrations/
│   └── seed/
│
├── documents/
│   └── synthetic_reports/
│
├── evaluation/
│   ├── datasets/
│   ├── ground_truth/
│   └── evaluation.py
│
├── frontend/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│
├── docker/
│
├── .env.example
├── .gitignore
└── requirements.txt
```

The current implementation will be smaller than this structure. The repository structure represents the intended evolution of the system.

---

# 24. Engineering Principles

The project follows several principles.

### 1. Evidence before generation

The model should retrieve evidence before making business claims.

### 2. Capability over unrestricted access

Expose controlled tools instead of arbitrary infrastructure access.

### 3. Deterministic systems around probabilistic systems

Use databases, schemas, validation, and business rules to constrain LLM behavior.

### 4. Explicit uncertainty

The system should distinguish:

```text
Observed
Inferred
Recommended
Unknown
```

### 5. Reproducibility

Synthetic data generation should be deterministic through seeded generation.

### 6. Observability by design

Agent behavior should be traceable.

### 7. Evaluation before optimization

The system should have measurable correctness before introducing unnecessary complexity.

---

# 25. What This Project Demonstrates

This project goes beyond:

> "I built a chatbot using LangChain."

It demonstrates an understanding of an enterprise AI system as a collection of interacting layers:

```text
                 ┌───────────────────┐
                 │    Experience     │
                 └─────────┬─────────┘
                           │
                 ┌─────────▼─────────┐
                 │      Agent        │
                 └─────────┬─────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
        ┌─────▼─────┐             ┌─────▼─────┐
        │    RAG    │             │    MCP    │
        └─────┬─────┘             └─────┬─────┘
              │                         │
        ┌─────▼─────┐             ┌─────▼─────┐
        │ Knowledge │             │ Enterprise │
        │   Layer   │             │   Tools    │
        └───────────┘             └─────┬──────┘
                                        │
                              ┌─────────▼─────────┐
                              │ Structured Data   │
                              │ APIs / Systems    │
                              └───────────────────┘
```

The goal is to understand **how these layers interact**, where their responsibilities begin and end, and how to make the overall system reliable.

---

# 26. Current Status

### Completed

- [x] Project definition
- [x] FMCG business scenario
- [x] Synthetic data generation
- [x] Products dataset
- [x] Stores dataset
- [x] Sales dataset
- [x] Inventory dataset
- [x] Promotions dataset
- [x] Competitor activity dataset
- [x] Pricing dataset

### In Progress

- [ ] Supabase PostgreSQL schema
- [ ] Data ingestion
- [ ] Synthetic market intelligence documents
- [ ] RAG pipeline
- [ ] MCP server
- [ ] MCP tools
- [ ] Local LLM
- [ ] Agent runtime
- [ ] React UI

### Planned

- [ ] Tool-call tracing
- [ ] Evaluation framework
- [ ] Security controls
- [ ] Docker
- [ ] Integration tests
- [ ] Production-style observability
- [ ] Kubernetes deployment

---

# 27. Success Criteria

The project will be considered successful when a user can ask:

> **"Why did Dove Shampoo sales decline in South India during Q3?"**

and the system can independently:

1. Understand the business question.
2. Identify the required information.
3. Query structured sales data through MCP.
4. Inspect inventory through MCP.
5. Inspect promotional activity through MCP.
6. Inspect competitor activity through MCP.
7. Retrieve relevant market intelligence through RAG.
8. Combine the evidence.
9. Clearly separate facts from inference.
10. Generate a business recommendation.
11. Explain the evidence behind the recommendation.
12. Log the agent's execution trace.

The final system should therefore demonstrate not merely **LLM generation**, but **controlled enterprise decision intelligence**.

---

# 28. Long-Term Vision

The long-term objective is to evolve this prototype toward a production-style **Enterprise AI Decision Agent**.

Potential future capabilities include:

```text
Sales Analytics
      +
Demand Forecasting
      +
Inventory Intelligence
      +
Promotion Optimization
      +
Competitor Intelligence
      +
Market Research
      +
Agentic Workflows
      +
Human Approval
      +
Enterprise Governance
```

Ultimately:

> **The system should function less like a chatbot and more like an AI analyst operating within a governed enterprise environment.**

---

## Disclaimer

This project uses entirely synthetic business data and does not represent actual data, systems, performance, strategy, or internal processes of Unilever or any other real organization.

The FMCG scenario is used solely as a realistic domain context for demonstrating enterprise AI architecture.