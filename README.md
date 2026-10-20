<<<<<<< HEAD
# AI_AGENT_GEMINI_REPO
ai chat agent created using gemini api key for testing - run via terminal and local host 
=======
# Gemini DevOps AI Agent

A local command-line AI assistant built with Python and Google's Gemini API. The project demonstrates a simple agent loop: accept a user request, ask Gemini to reason about it, execute explicitly allowlisted Python tools when requested, and return the tool results to Gemini for a final response.

> **Project status:** Learning / prototype. The included infrastructure data is simulated. This project does not connect to or modify real servers, Kubernetes clusters, or cloud accounts.

## Features

- Interactive command-line chat.
- Gemini API integration using Google's `google-genai` SDK.
- Configurable primary model and model fallback candidates.
- In-session conversation history.
- Function/tool calling with an explicit Python allowlist.
- Demo tools to inspect simulated server status and read a local sample log.
- Optional creation of local incident-report text files.
- Basic tool-call and conversation-history limits.

## Architecture at a glance

```text
User in terminal
      |
      v
Python CLI (agent.py)
      |
      v
Agent loop / prompt / bounded conversation history
      |
      v
Gemini API  <-------------------------------+
      |                                      |
      | final text                           | tool results
      v                                      |
CLI output                                   |
                                             |
Gemini requests a function                   |
      |                                      |
      v                                      |
Python allowlist and tool dispatcher --------+
      |
      +--> get_server_status() [simulated data]
      +--> read_application_logs() [fixed local demo log]
      +--> create_incident_report() [writes under reports/]
```

See [Architecture](docs/ARCHITECTURE.md) and [Design](docs/DESIGN.md) for details.

## Requirements

- Windows 10/11, PowerShell, or another supported Python environment.
- A supported Python 3 version compatible with the installed `google-genai` SDK.
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/api-keys).
- Network access to the Gemini API.

Free-tier availability, model access, and quotas depend on the Google AI Studio project and selected model. See Google's current [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) and [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits).

## Quick start (Windows PowerShell)

Run these commands from the project directory:

```powershell
python -m venv .venv
```

If PowerShell blocks activation, either use the temporary process-only policy described below or call the virtual environment's Python directly.

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If this repository does not yet contain `requirements.txt`, create it with:

```text
google-genai
python-dotenv
```

Create a local `.env` file in the repository root:

```dotenv
GEMINI_API_KEY=replace_with_your_key
GEMINI_MODEL=replace_with_a_model_available_to_your_project
```

Choose a model that is currently available to your project and free tier, if you intend to stay within the free tier. Do not commit `.env`.

Create the demo log:

```powershell
New-Item -ItemType Directory -Force logs | Out-Null
notepad logs\application.log
```

Example contents:

```text
2026-10-20 10:00:00 INFO Application started
2026-10-20 10:00:05 INFO Database connection successful
2026-10-20 10:02:10 WARNING Memory usage reached 85%
2026-10-20 10:02:30 ERROR Database connection timeout
2026-10-20 10:02:45 ERROR HTTP 500 returned by /api/orders
2026-10-20 10:03:00 ERROR Database connection timeout
2026-10-20 10:03:15 WARNING Application response time exceeded threshold
```

Test the API connection (if `test_gemini.py` is present):

```powershell
python test_gemini.py
```

Run the agent:

```powershell
python agent.py
```

### PowerShell activation is blocked

If your organization's policy permits it, a process-only workaround is:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
```

This applies only to the current PowerShell process. Alternatively, avoid activation and run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe agent.py
```

Do not change execution policy on a managed device without following your organization's IT policy.

## Commands

When the agent is running:

| Command | Purpose |
|---|---|
| `/help` | Display usage guidance |
| `/status` | Print the simulated server status directly |
| `/logs` | Print the local sample log directly |
| `/clear` | Clear in-memory conversation history |
| `/quit` or `/exit` | Exit the application |

Example prompts:

```text
What is Git?
Explain the difference between git add, git commit, and git push.
Investigate the demo incident using the server status and sample logs.
Create an incident report for the database timeout.
```

The agent can answer general questions. Its tools are domain-specific and should only be called when useful.

## Repository layout

```text
.
├── agent.py                 # CLI, Gemini requests, tool dispatch loop
├── test_gemini.py           # Simple API connectivity check (if included)
├── test_git.py              # Model/fallback test prompt (if included)
├── requirements.txt         # Python dependencies
├── .env                     # Local API key; never commit
├── .gitignore
├── logs/
│   └── application.log      # Synthetic sample log; not production data
├── reports/                 # Generated local reports; normally ignored by Git
└── docs/
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    ├── SECURITY.md
    ├── CONTRIBUTING.md
    └── CHANGELOG.md
```

The files marked “if included” reflect the development steps in this project; adjust this list if your repository differs.

## Security and privacy

- Never commit API keys, `.env`, tokens, credentials, or private logs.
- Treat prompts, model output, logs, and tool arguments as untrusted.
- Only expose tools through a fixed allowlist; do not add unrestricted shell execution.
- Keep tools read-only by default. Require explicit authorization and human approval for consequential actions.
- The demo status function returns hard-coded values; it does not monitor a real server.
- The log reader is restricted to a predefined project file.
- The report tool writes only within the project's `reports/` directory.
- Requests and relevant context are sent to Google's API. Do not send sensitive company, customer, or production data to a learning project.
- Review Google's current API terms, data handling, pricing, and quota policies before use.

See [Security](docs/SECURITY.md).

## Known limitations

- No real monitoring integration.
- No direct shell, cloud, Docker, or Kubernetes execution.
- Conversation history is in memory and is not persistent across runs.
- Model availability and free-tier quotas can change.
- Model fallback only helps when an alternative model is available and permitted for the API project.
- AI-generated diagnoses are hypotheses and require verification.
- This is not a production incident-response system.

## Troubleshooting

| Symptom | Checks |
|---|---|
| `GEMINI_API_KEY` missing | Confirm `.env` is in the project root and the variable name is exact. |
| Invalid API key / 403 | Check key, project, API access, and restrictions in AI Studio. |
| `404 NOT_FOUND` | Confirm the model ID is currently available to the project. |
| `429 RESOURCE_EXHAUSTED` | Check quota, rate limits, and billing/free-tier eligibility. |
| `503 UNAVAILABLE` | Retry with backoff and try an available fallback model. |
| Python cannot import `google.genai` | Activate the correct virtual environment and install requirements there. |
| PowerShell blocks activation | Use the process-only workaround above if permitted, or run the virtual-environment Python directly. |

## Development and validation

Before submitting changes:

1. Confirm `.env` and private data are excluded from Git.
2. Run the API connectivity script, if present.
3. Run the CLI and test `/help`, `/status`, `/logs`, `/clear`, and `/quit`.
4. Test a general question that should not call a tool.
5. Test an incident question that should use demo tools.
6. Test report creation and verify the output is under `reports/`.
7. Test error handling with an unavailable model or quota error when practical.

See [Contributing](docs/CONTRIBUTING.md).

## License

No license has been selected for this project. Add a `LICENSE` file only after deciding how you want the code to be reused.
>>>>>>> master
