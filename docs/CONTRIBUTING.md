# Contributing

Thanks for helping improve the Gemini CLI agent.

## Development setup

1. Install a supported Python version.
2. Create a virtual environment.
3. Install the dependencies from `requirements.txt`.
4. Create a local `.env` file with a valid Gemini API key and a supported model.
5. Use only synthetic data during development.

Example PowerShell setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If activation is blocked by PowerShell policy, follow the environment-specific instructions in the README. Do not bypass organization policy.

## Coding guidelines

- Prefer small, single-purpose functions.
- Add type hints to new functions where practical.
- Keep API keys and other secrets out of source code.
- Use explicit tool allowlists; do not add arbitrary shell execution.
- Validate tool inputs and limit tool output.
- Handle expected errors with clear, non-sensitive messages.
- Keep model retries bounded and limited to appropriate transient errors.
- Document new configuration variables and tools.
- Update architecture/design/security docs when behavior or trust boundaries change.

## Testing checklist

Before submitting a change:

- [ ] Run syntax checks: `python -m compileall agent.py`.
- [ ] Run any available unit tests.
- [ ] Verify general Q&A works.
- [ ] Verify expected tool calls work with demo data.
- [ ] Verify unknown tool names are rejected.
- [ ] Verify API errors do not reveal credentials.
- [ ] Verify reports are written only to the expected directory.
- [ ] Check `git status` and staged diffs for secrets or personal data.
- [ ] Update documentation for behavior changes.

Do not make tests depend on a live API outage. Mock API failures when testing retry and fallback logic.

## Pull requests

A useful change description includes:
- Problem and motivation.
- Summary of behavior changes.
- How the change was tested.
- Any configuration or documentation changes.
- Security, privacy, and cost implications.
