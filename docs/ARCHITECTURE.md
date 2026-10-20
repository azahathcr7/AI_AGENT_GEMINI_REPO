# System Architecture

## 1. Purpose

This document describes the current learning prototype's components, responsibilities, and request flow. The architecture is intentionally small and local-first.

## 2. Context diagram

```text
+-------------------+        prompt / answer        +----------------------+
| Human operator    | <---------------------------> | Python CLI           |
| PowerShell / CMD  |                               | agent.py             |
+-------------------+                               +----------+-----------+
                                                               |
                                                               | HTTPS API
                                                               v
                                                    +----------------------+
                                                    | Google Gemini API    |
                                                    | model inference      |
                                                    +----------------------+
                                                               |
                                                               | function-call request
                                                               v
                                                    +----------------------+
                                                    | Tool dispatcher      |
                                                    | explicit allowlist   |
                                                    +----------+-----------+
                                                               |
                                  +----------------------------+---------------------+
                                  |                            |                     |
                                  v                            v                     v
                         +----------------+          +----------------+   +------------------+
                         | Simulated       |          | Fixed local    |   | Local report     |
                         | server status   |          | demo log       |   | writer            |
                         +----------------+          +----------------+   +------------------+
```

## 3. Components

### CLI (`agent.py`)

- Reads user input.
- Handles local commands such as `/help`, `/status`, `/logs`, `/clear`, and `/quit`.
- Maintains bounded in-memory conversation history.
- Sends the current conversation and tool definitions to Gemini.
- Displays the final response.

### Gemini client

- Uses the `google-genai` Python SDK.
- Sends the selected model, prompt context, and function declarations.
- Receives either a text response or a function-call request.
- Model selection and fallback are configuration concerns; fallback behavior should be implemented in one shared function and tested independently.

### Tool dispatcher

- Maps model-requested function names to a fixed Python allowlist.
- Executes only registered functions.
- Sends tool results back to Gemini so it can produce a final answer.
- Enforces a per-turn tool-call limit.

### Demo tools

| Tool | Input | Effect | Boundary |
|---|---|---|---|
| `get_server_status` | None | Returns fixed sample metrics | No real server access |
| `read_application_logs` | None | Reads a predefined file | Must not accept arbitrary paths |
| `create_incident_report` | Title, findings, recommendations | Writes a text report | Output must remain under `reports/` |

### Configuration

- `.env` holds the local API key and model setting.
- `.gitignore` excludes `.env`, the virtual environment, and generated reports.
- `requirements.txt` declares runtime dependencies.

## 4. Main request sequence

1. User enters a message.
2. CLI adds it to the bounded conversation history.
3. Application sends the history, system instructions, tool definitions, and model ID to Gemini.
4. Gemini returns either a normal answer or one or more function-call requests.
5. Application validates each requested function name against the allowlist.
6. Application runs permitted tools and captures their results.
7. Tool results are appended to the model conversation in the SDK's expected function-response format.
8. The model is called again to interpret results.
9. The loop stops when the model returns a final answer or a safety/iteration limit is reached.
10. CLI prints the answer.

## 5. Trust boundaries

- **User input → model:** Treat input as untrusted.
- **External model output → local code:** Never evaluate model text as Python or shell commands.
- **Tool arguments → tool implementation:** Validate types, lengths, paths, and allowed values.
- **Local files → model:** Only send intended content; logs may contain secrets or prompt-injection text.
- **Application → Gemini API:** Prompts and tool results leave the machine and are subject to provider policies.
- **API key → process:** Load from environment/configuration; never print or commit it.

## 6. Failure handling

Expected failure categories include invalid credentials, unavailable model (503), quota/rate limit (429), permission errors (403), invalid model IDs (404), network timeouts, malformed/empty responses, and local file I/O failures.

Recommended behavior:

- Retry only transient failures, with bounded exponential backoff and jitter.
- Respect provider retry guidance and `Retry-After` where available.
- Switch models only for failures where fallback is appropriate; do not treat invalid credentials or exhausted project-wide quota as automatically solved by switching.
- Keep the number of model and tool calls bounded.
- Show a useful error without exposing API keys or sensitive request contents.
- Avoid unbounded retries.

## 7. Current scope and non-goals

Current scope:
- Local interactive CLI.
- General-purpose Q&A.
- Tool-assisted demo incident investigation.
- Local text report generation.

Non-goals:
- Production monitoring.
- Real infrastructure changes.
- Unrestricted shell access.
- Multi-user service.
- Persistent memory or audit-grade event storage.
- Guaranteed uptime or production incident response.

## 8. Evolution path

Potential next stages:

1. Add automated unit tests and structured logging.
2. Move model configuration and retry policy into a dedicated configuration module.
3. Add schema validation for tool arguments and outputs.
4. Add a read-only Prometheus or cloud monitoring connector.
5. Add a persistent incident store with retention rules.
6. Add human approval for any state-changing operation.
7. Add audit records, observability, and integration tests.
8. Only then evaluate narrowly scoped remediation actions.
