# Design Document

## 1. Goals

- Provide an understandable CLI interface to a Gemini-powered assistant.
- Demonstrate the agent pattern: reason, request a tool, receive evidence, and respond.
- Allow general-purpose questions without forcing every request through DevOps tools.
- Keep the initial implementation safe, easy to run locally, and inexpensive to experiment with.
- Keep provider-specific configuration separate from the tool implementations where practical.

## 2. Design principles

1. **Least privilege:** Tools expose only the capabilities the application needs.
2. **Explicit tool allowlist:** The model may request a named tool, but cannot invent executable Python functions.
3. **Safe defaults:** Demonstration tools do not modify infrastructure.
4. **Bounded work:** Limit history size, tool calls per turn, retries, and response time where supported.
5. **Configuration outside source:** API keys and model choices are not hard-coded.
6. **Observable behavior:** Log which tool is called, without logging secrets or unnecessary sensitive payloads.
7. **Fail safely:** Errors stop or return control to the user rather than triggering destructive fallback behavior.
8. **Evidence-based responses:** The agent should distinguish observed facts from hypotheses.
9. **Provider-aware fallback:** A fallback model must be available to the project and support the needed features.
10. **Small components:** Keep CLI, provider calls, tool logic, and configuration separable as the project grows.

## 3. Functional requirements

- FR-1: The user can submit a natural-language prompt from the terminal.
- FR-2: The application can return a Gemini-generated answer.
- FR-3: The application can preserve a bounded conversation history during a process session.
- FR-4: The model can request one of the registered tools.
- FR-5: The application validates requested tool names before execution.
- FR-6: The application returns tool results to the model.
- FR-7: The application can return simulated server status and read the fixed sample log.
- FR-8: The application can create a text report only when requested.
- FR-9: The CLI provides help, status, logs, clear, and exit commands.
- FR-10: The application handles expected API and local I/O errors without exposing the API key.

## 4. Non-functional requirements

- **Security:** No hard-coded secrets; no unrestricted shell execution.
- **Reliability:** Bounded retries and bounded tool execution loop.
- **Maintainability:** Clear names, small functions, dependency pinning when the project stabilizes, and tests.
- **Portability:** Support a documented Python version and standard virtual-environment workflow.
- **Cost control:** Keep prompt history bounded, cap tool calls, and monitor provider quotas.
- **Usability:** Explain startup, commands, errors, and limitations in the README.

## 5. Tool contract design

Each tool should have a narrow purpose and a predictable return structure.

Recommended contract:

```python
def tool_name(validated_argument: str) -> dict:
    return {
        "status": "ok",
        "data": {},
        "error": None,
    }
```

The current prototype may use simpler dictionaries, but a consistent structure makes future testing and error handling easier.

Tool requirements:
- Validate all inputs.
- Limit string lengths and returned data volume.
- Restrict file paths to an expected base directory.
- Avoid shell interpolation and dynamic code evaluation.
- Return structured errors instead of leaking stack traces to the model.
- Be idempotent where practical.
- Mark whether an operation is read-only or state-changing.
- Require human confirmation for consequential changes.

## 6. Conversation and function-calling loop

The agent loop should:
1. Send the current user conversation and tool definitions to the model.
2. Inspect the response for function calls.
3. Reject unregistered tool names.
4. Validate arguments before invoking a tool.
5. Execute only approved tools.
6. Send each result back using the SDK's supported function-response structure.
7. Repeat until a final text answer is returned or the turn's call limit is reached.

Implementation note: function-calling response formats can change across SDK versions. Follow the installed `google-genai` SDK documentation and include tests for the exact SDK version used.

## 7. Model fallback policy

Fallback is intended for temporary model availability or model-specific access problems, not as a universal solution to every error.

Recommended policy:
- Configure a primary model and a short, reviewed list of fallback models.
- Verify each model is currently available to the API project.
- Retry transient errors a small number of times with exponential backoff and jitter.
- Switch models on appropriate transient/model-specific errors.
- Do not blindly retry invalid keys, malformed requests, or permission failures.
- Treat 429 separately: inspect whether the error is rate limiting, a daily quota, or project-level exhaustion.
- Display which model succeeded, but never display credentials.
- Test fallback behavior with mocked errors rather than depending on live outages.

## 8. Security decisions

- The first version uses simulated data.
- The log tool reads one predefined file.
- The report writer writes beneath `reports/`.
- The application does not provide a general-purpose shell tool.
- The API key is stored in `.env`, excluded from version control.
- Tool output and log content are treated as untrusted data.
- The application must not claim it inspected or changed a real system when it did not.

See [SECURITY.md](SECURITY.md).

## 9. Acceptance criteria

A change is acceptable when relevant checks pass:

- A general question returns a response without calling tools unnecessarily.
- A request to inspect the demo incident can call the status/log tools.
- Unknown tool names are rejected.
- The tool-call limit terminates a runaway loop.
- Missing API key produces a clear startup error.
- API errors are surfaced without revealing the key.
- Report creation writes only within the reports directory.
- `/clear` clears the current in-memory conversation.
- `/quit` exits cleanly.
- `.env` and generated/private data are not included in Git commits.

## 10. Known design debt

- Conversation history may be truncated at message boundaries without summarization.
- Tool schemas and function responses should be tested against the exact SDK version.
- Retry/fallback behavior should use typed SDK exceptions where possible instead of matching error-message strings.
- A wall-clock timeout and token budget should be added.
- Unit tests and automated lint/type checks should be added.
- Report filenames should account for collisions and filesystem edge cases.
- Model-generated findings need explicit confidence/evidence formatting for incident workflows.
