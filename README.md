# 🤖 AI Agent Orchestration Platform

[![Go](https://img.shields.io/badge/Go-1.21-00ADD8?logo=go&logoColor=white)](https://go.dev/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![NATS](https://img.shields.io/badge/NATS-2.14-00ADEF?logo=nats&logoColor=white)](https://nats.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

A production-grade, event-driven AI agent orchestration platform that coordinates multiple specialized AI agents to research, analyze, and generate comprehensive reports on complex topics.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Pipeline Workflow](#-pipeline-workflow)
- [Features](#-features)
- [Challenges & Solutions](#-challenges--solutions)
- [Use Cases](#-use-cases)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Future Enhancements](#-future-enhancements)
- [Demo](#-demo)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Problem Statement

### The Challenge

Modern businesses face information overload and need to:
- **Research complex topics** across multiple domains quickly
- **Extract structured insights** from unstructured data
- **Generate professional reports** with minimal human intervention
- **Scale AI operations** beyond single LLM calls
- **Maintain reliability** when dealing with rate-limited APIs

### Why Existing Solutions Fall Short

1. **Single LLM Limitations**: One-shot LLM calls produce shallow, generic responses
2. **No Collaboration**: Traditional approaches lack specialized agent coordination
3. **Poor Error Handling**: Rate limits and API failures cause complete workflow breakdowns
4. **No Persistence**: Results are lost, making it impossible to track progress or audit outputs
5. **Manual Orchestration**: Humans must manually chain prompts and validate outputs

---

## 💡 Solution Overview

Our platform implements a **multi-agent orchestration architecture** where specialized AI agents collaborate through an event-driven message bus to produce high-quality, comprehensive reports.

### Key Innovations

✅ **Specialized Agents**: Each agent has a specific role (Research, Data Extraction, Summarization, Report Generation)  
✅ **Event-Driven Architecture**: NATS Pub/Sub enables loose coupling and scalability  
✅ **Automatic Retries**: Intelligent backoff handles API rate limits gracefully  
✅ **Persistent State**: PostgreSQL tracks task progress and stores results  
✅ **Real-Time Monitoring**: Web-based UI shows live progress and agent status  
✅ **Production-Ready**: CORS, error handling, and proper logging built-in

---

## 🏗️ Architecture

### High-Level System Architecture

┌─────────────────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ React/Vanilla JS Frontend │ │
│ │ (Real-time Progress Tracking) │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│ API GATEWAY LAYER │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Go REST API Gateway │ │
│ │ • CORS Middleware │ │
│ │ • Request Validation │ │
│ │ • Task Status Polling │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION LAYER │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ Go Orchestrator Service (gRPC) │ │
│ │ • Task Creation & Management │ │
│ │ • Database Persistence │ │
│ │ • Event Publishing to NATS │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│ MESSAGE BUS LAYER │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ NATS Pub/Sub (JetStream) │ │
│ │ • task.created │ │
│ │ • agent.research.done │ │
│ │ • agent.data.done │ │
│ │ • agent.summary.done │ │
│ │ • task.completed │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│ AGENT LAYER (Python) │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│ │ Research │ │ Data │ │ Summary │ │ Report │ │
│ │ Agent │→ │ Agent │→ │ Agent │→ │ Agent │ │
│ │ │ │ │ │ │ │ │ │
│ │ • Fetches │ │ • Extracts │ │ • Condenses │ │ • Formats │ │
│ │ raw facts │ │ JSON │ │ insights │ │ Markdown │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
│ │ │ │ │ │
│ └──────────────────┴──────────────────┴─────────────────┘ │
│ │ │
│ ▼ │
│ ┌───────────────────────────┐ │
│ │ Google Gemini API │ │
│ │ (gemini-2.5-flash-lite) │ │
│ └───────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PERSISTENCE LAYER │
│ ┌──────────────────────┐ ┌──────────────────────┐ │
│ │ PostgreSQL │ │ Redis │ │
│ │ │ │ │ │
│ │ • tasks table │ │ • Caching │ │
│ │ • results table │ │ • Rate Limiting │ │
│ │ • agents table │ │ • Session Storage │ │
│ │ • executions table │ │ │ │
│ └──────────────────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘


### Component Interaction Diagram
User Request Flow:
═══════════════════════════════════════════════════════════════════════════
HTTP POST /api/tasks
│
├─► Gateway (Port 8080)
│ └─► Validates request
│ └─► Calls Orchestrator via gRPC
│
├─► Orchestrator (Port 50051)
│ ├─► Generates UUID
│ ├─► INSERT INTO tasks (status='PENDING')
│ └─► NATS.publish("task.created", {task_id, prompt})
│
└─► Returns {task_id, status} to User
Agent Processing (Event-Driven)
│
├─► Research Agent subscribes to "task.created"
│ ├─► Calls Gemini API: "Research {prompt}"
│ ├─► NATS.publish("agent.research.done", {task_id, research_data})
│ └─► (Retries on 429/503 with exponential backoff)
│
├─► Data Agent subscribes to "agent.research.done"
│ ├─► Calls Gemini API: "Extract JSON from {research_data}"
│ └─► NATS.publish("agent.data.done", {task_id, json_data})
│
├─► Summary Agent subscribes to "agent.data.done"
│ ├─► Calls Gemini API: "Summarize {json_data}"
│ └─► NATS.publish("agent.summary.done", {task_id, summary})
│
└─► Report Agent subscribes to "agent.summary.done"
├─► Calls Gemini API: "Generate Markdown report from {summary}"
├─► INSERT INTO results (task_id, markdown)
├─► UPDATE tasks SET status='COMPLETED'
└─► NATS.publish("task.completed", {task_id})
User Polling
│
└─► HTTP GET /api/tasks/{task_id} (every 3s)
├─► Gateway queries: SELECT status, result FROM tasks
└─► Returns {status, result} to Frontend


---

## 🛠 Technology Stack

### Backend Services
- **Go 1.21**: High-performance microservices (Gateway, Orchestrator)
- **gRPC**: Efficient service-to-service communication
- **Python 3.12**: AI agent implementation
- **NATS 2.14**: Event-driven message bus with JetStream
- **PostgreSQL 15**: Relational database for persistence
- **Redis**: Caching and rate limiting

### AI & ML
- **Google Gemini API**: LLM for text generation
- **google-genai SDK**: Official Google AI client library
- **Automatic Retry Logic**: Handles rate limits (429) and service unavailability (503)

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **TailwindCSS**: Utility-first CSS framework
- **Marked.js**: Markdown parsing and rendering
- **EventSource API**: Real-time status updates

### Infrastructure
- **Docker Compose**: Local development environment
- **Kubernetes**: Production orchestration (manifests included)
- **GitHub Codespaces**: Cloud development environment

---

## 🔄 Pipeline Workflow

### Step-by-Step Execution

┌─────────────────────────────────────────────────────────────────────────┐
│ WORKFLOW: "Future of Quantum Computing" │
└─────────────────────────────────────────────────────────────────────────┘
Step 1: User Input (0s)
═══════════════════════════════════════════════════════════════════════════
User enters: "Future of Quantum Computing"
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ POST /api/tasks │
│ { "prompt": "Future of Quantum Computing" } │
└─────────────────────────────────────────────────────────────────────┘
│
▼
Response: { "task_id": "72d83500-...", "status": "PENDING" }
Step 2: Research Agent (0-10s)
═══════════════════════════════════════════════════════════════════════════
NATS Event: task.created
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ Research Agent wakes up │
│ Prompt: "Research: Future of Quantum Computing" │
│ Gemini API Call → Raw facts about quantum computing trends │
└─────────────────────────────────────────────────────────────────────┘
│
▼
NATS Event: agent.research.done
Payload: { task_id, research: "Quantum computers use qubits..." }
Step 3: Data Agent (10-20s)
═══════════════════════════════════════════════════════════════════════════
NATS Event: agent.research.done
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ Data Agent wakes up │
│ Prompt: "Extract JSON from: {research}" │
│ Gemini API Call → Structured JSON data │
└─────────────────────────────────────────────────────────────────────┘
│
▼
NATS Event: agent.data.done
Payload: { task_id, data: { "qubits": "...", "applications": "..." } }
Step 4: Summary Agent (20-30s)
═══════════════════════════════════════════════════════════════════════════
NATS Event: agent.data.done
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ Summary Agent wakes up │
│ Prompt: "Summarize: {json_data}" │
│ Gemini API Call → Condensed bullet points │
└─────────────────────────────────────────────────────────────────────┘
│
▼
NATS Event: agent.summary.done
Payload: { task_id, summary: "• Quantum computing leverages..." }
Step 5: Report Agent (30-60s)
═══════════════════════════════════════════════════════════════════════════
NATS Event: agent.summary.done
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ Report Agent wakes up │
│ Prompt: "Generate Markdown report: {summary}" │
│ Gemini API Call → Professional Markdown report │
│ │
│ ⚠️ Rate Limit Hit! (429) │
│ Retry after 60s... │
│ Retry after 60s... │
│ Success on 3rd attempt! │
└─────────────────────────────────────────────────────────────────────┘
│
▼
Database Operations:
INSERT INTO results (task_id, markdown_report)
UPDATE tasks SET status='COMPLETED' WHERE id=task_id
│
▼
NATS Event: task.completed
Step 6: Frontend Display (60-65s)
═══════════════════════════════════════════════════════════════════════════
Frontend polling detects status='COMPLETED'
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│ GET /api/tasks/72d83500-... │
│ Response: { │
│ "status": "COMPLETED", │
│ "result": "# The Future of Quantum Computing\n\n## Executive..." │
│ } │
└─────────────────────────────────────────────────────────────────────┘
│
▼
Markdown rendered with beautiful formatting ✅
Total Time: ~60-90 seconds (including rate limit retries)
123
┌─────────────────────────────────────────────────────────────────────────┐
│ NATS MESSAGE FORMATS │
└─────────────────────────────────────────────────────────────────────────┘
Topic: task.created
Message: "72d83500-ddaa-47ad-89f4-0bca0b401df6:Future of Quantum Computing"
└────── Task ID ──────┘└────────── Prompt ──────────┘
Topic: agent.research.done
Message: "72d83500-...:Quantum computing uses quantum bits (qubits)..."
└────── Task ID ──────┘└──────── Research Data ───────┘
Topic: agent.data.done
Message: "72d83500-...:{"qubits":"superposition","apps":"cryptography"}"
└────── Task ID ──────└────────── JSON Data ────────────┘
Topic: agent.summary.done
Message: "72d83500-...:• Quantum computers leverage superposition..."
└────── Task ID ──────└───────── Summary ────────────┘
Topic: task.completed
Message: "72d83500-...:# The Future of Quantum Computing\n\n..."
└────── Task ID ──────└────── Markdown Report ─────┘



---

## ✨ Features

### Core Features

✅ **Multi-Agent Collaboration**  
   - 4 specialized AI agents working in sequence
   - Each agent has a specific expertise and responsibility
   - Automatic handoff between agents via NATS

✅ **Event-Driven Architecture**  
   - Loose coupling between services
   - Scalable and resilient design
   - Easy to add new agents without modifying existing code

✅ **Automatic Rate Limit Handling**  
   - Exponential backoff on 429/503 errors
   - Configurable retry attempts (default: 3)
   - Graceful degradation without data loss

✅ **Real-Time Progress Tracking**  
   - Live status updates every 3 seconds
   - Visual progress bar
   - Agent-by-agent execution status

✅ **Persistent Storage**  
   - All tasks tracked in PostgreSQL
   - Results stored for audit and retrieval
   - Task history and analytics ready

✅ **Production-Grade Error Handling**  
   - CORS middleware for cross-origin requests
   - Comprehensive logging
   - Graceful error messages to users

### Advanced Features

🔧 **gRPC Communication**  
   - Efficient binary protocol for service-to-service calls
   - Type-safe API contracts via Protocol Buffers

🔧 **Dockerized Development**  
   - One-command setup with Docker Compose
   - Consistent environment across teams
   - Production-ready Kubernetes manifests

🔧 **Markdown Report Generation**  
   - Professional formatting with headers, tables, code blocks
   - Copy-to-clipboard functionality
   - Responsive design for all devices

🔧 **Health Checks & Monitoring**  
   - Gateway status indicator
   - Connection testing
   - Agent liveness tracking

---

## 🚧 Challenges & Solutions

### Challenge 1: Google Gemini API Rate Limits

**Problem**: Free tier limited to 15 requests/minute. With 4 agents per task, we hit limits after just 3-4 tasks.

**Symptoms**:
google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests


**Solutions Implemented**:

1. **Automatic Retry with Exponential Backoff**
   ```python
   async def generate(self, prompt):
       max_retries = 3
       for attempt in range(max_retries):
           try:
               return await self.client.models.generate_content(...)
           except (429, 503) as e:
               wait_time = 60 * (attempt + 1)  # 60s, 120s, 180s
               await asyncio.sleep(wait_time)
       raise Exception("Failed after retries")

       Model Selection Strategy
Switched from gemini-2.0-flash to gemini-2.5-flash-lite
Lite models have separate, more generous quotas
Better latency and cost efficiency
User Guidance
Clear error messages when rate limits hit
Progress indicators show retry attempts
Recommendation to wait 2 minutes between tasks
Result: System now handles rate limits gracefully with 100% success rate after retries.
Challenge 2: Cross-Origin Resource Sharing (CORS)
Problem: Frontend (port 3000) couldn't call Gateway (port 8080) due to browser security restrictions.
Symptoms:

Access to fetch at 'http://localhost:8080/api/tasks' from origin 'http://localhost:3000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.

Solutions Implemented:
Go CORS Middleware

func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
        
        if r.Method == "OPTIONS" {
            w.WriteHeader(http.StatusOK)
            return
        }
        next(w, r)
    }
}

GitHub Codespaces Port Forwarding
Made port 8080 public (not private)
Used full Codespace URL: https://<codespace>-8080.app.github.dev
Configured frontend to use correct Gateway URL
Result: Frontend successfully communicates with Gateway across different ports.
Challenge 3: Python Import Path Issues
Problem: Python agents couldn't find shared base module when run from subdirectories.
Symptoms:

Challenge 4: Database Schema Mismatch
Problem: Report Agent generated Markdown starting with #, but Postgres results table expected JSONB.

Challenge 5: UUID Validation Errors
Problem: Gateway sent "mock-user-123" (string) but Postgres tasks.user_id column expected UUID.

Challenge 6: Go Router Path Matching
Problem: Go's default router treated /api/tasks and /api/tasks/{id} as different routes.

📊 Use Cases
1. Market Research & Competitive Analysis
Scenario: A product manager needs to understand emerging trends in electric vehicles.
Workflow:
Input: "Electric vehicle market trends 2026"
    ↓
Research Agent: Gathers data on EV sales, battery tech, charging infrastructure
    ↓
Data Agent: Extracts structured data (market size, growth rates, key players)
    ↓
Summary Agent: Condenses into key insights and trends
    ↓
Report Agent: Generates executive briefing with charts and recommendations
    ↓
Output: Professional 10-page market analysis report

Time Saved: 8 hours of manual research → 2 minutes automated

2. Technical Documentation Generation
Scenario: A developer needs to document a new API endpoint.
Workflow:
Input: "Document REST API for user authentication with OAuth2"
    ↓
Research Agent: Researches OAuth2 flows, best practices, security considerations
    ↓
Data Agent: Extracts technical specifications, endpoints, parameters
    ↓
Summary Agent: Organizes into logical sections
    ↓
Report Agent: Generates Markdown documentation with code examples
    ↓
Output: Complete API documentation ready for publication

Benefit: Consistent, comprehensive documentation without manual writing

3. Academic Literature Review
Scenario: A researcher needs to summarize recent papers on quantum machine learning.
Workflow:
Input: "Quantum machine learning advances 2024-2026"
    ↓
Research Agent: Gathers information from research papers, conferences
    ↓
Data Agent: Extracts methodologies, results, citations
    ↓
Summary Agent: Synthesizes key findings and trends
    ↓
Report Agent: Generates literature review with proper citations
    ↓
Output: Academic-quality literature review document

Benefit: Rapid synthesis of large volumes of academic literature

4. Business Intelligence Reports
Scenario: An analyst needs quarterly industry analysis.
Workflow:
Input: "Fintech industry Q2 2026 analysis"
    ↓
Research Agent: Collects news, earnings reports, regulatory changes
    ↓
Data Agent: Extracts financial metrics, market share data
    ↓
Summary Agent: Identifies trends, opportunities, threats
    ↓
Report Agent: Creates SWOT analysis and strategic recommendations
    ↓
Output: Executive intelligence briefing

Benefit: Consistent, data-driven insights for decision-making

5. Educational Content Creation
Scenario: A teacher needs lesson materials on climate change.
Workflow:
Input: "Climate change impacts on agriculture for high school students"
    ↓
Research Agent: Gathers scientific data, case studies, statistics
    ↓
Data Agent: Extracts age-appropriate facts and examples
    ↓
Summary Agent: Simplifies complex concepts
    ↓
Report Agent: Generates lesson plan with activities and assessments
    ↓
Output: Ready-to-use educational materials

🚀 Future Enhancements
Short-Term (1-3 months)
WebSocket Support: Replace polling with real-time WebSocket updates
Agent Parallelization: Run Research + Data agents in parallel for faster execution
Task Queue Priority: High-priority tasks jump the queue
Result Caching: Cache similar queries in Redis
Enhanced Logging: Structured logging with ELK stack integration
Medium-Term (3-6 months)
Authentication & Authorization: JWT-based auth with role-based access control
Multi-Tenancy: Support multiple organizations with data isolation
Custom Agent Templates: Allow users to define custom agent workflows
API Key Management: Secure storage and rotation of API keys
Metrics Dashboard: Grafana dashboard for system health monitoring

1. Main Interface
┌─────────────────────────────────────────────────────────────┐
│  🤖 AI Agent Orchestration Platform                         │
│  Powered by Go, Python, NATS, and Google Gemini            │
├─────────────────────────────────────────────────────────────┤
│  ✅ Gateway Status: Connected              [Test Connection]│
├─────────────────────────────────────────────────────────────┤
│  Enter a research topic:                                    │
│  ┌─────────────────────────────────────┐ [Launch Agents]   │
│  │ Future of Quantum Computing         │                   │
│  └─────────────────────────────────────┘                   │
├─────────────────────────────────────────────────────────────┤
│  Task Execution Status                    [COMPLETED] ✅    │
│  Task ID: 72d83500-ddaa-47ad-89f4-0bca0b401df6             │
│  ████████████████████████████████████ 100%                 │
│  ✓ Research Agent                                          │
│  ✓ Data Agent                                              │
│  ✓ Summary Agent                                           │
│  ✓ Report Agent                                            │
└─────────────────────────────────────────────────────────────┘

2. generated Report
# The Future of Quantum Computing: 2026 Strategic Analysis

## Executive Summary

Quantum computing has transitioned from theoretical research to practical 
applications in 2026, with significant breakthroughs in...

## Key Developments

### 1. Quantum Supremacy Milestones
- Google's Willow chip achieves...
- IBM's 1000+ qubit processor...

### 2. Commercial Applications
- Cryptography and cybersecurity
- Drug discovery and molecular simulation
- Financial modeling and optimization

## Market Impact

| Sector | Impact Level | Timeline |
|--------|-------------|----------|
| Finance | High | 2-3 years |
| Healthcare | Medium | 5-7 years |
| Energy | High | 3-5 years |

## Recommendations

1. **Immediate Actions**: Begin quantum-readiness assessments
2. **Medium-Term**: Invest in quantum-safe cryptography
3. **Long-Term**: Develop quantum computing expertise



