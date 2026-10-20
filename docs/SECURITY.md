# Security and Data Handling

## Status

This is a local learning prototype. It is not approved for production incident response and must not be given broad infrastructure privileges.

## Secrets

- Store the Gemini API key in a local `.env` file.
- Exclude `.env` from Git using `.gitignore`.
- Never print the key or include it in screenshots, issues, logs, or commits.
- If a key is exposed, revoke/rotate it in Google AI Studio.
- Do not place secrets in prompts, sample logs, or incident reports.
- Consider environment variables supplied by a secret manager for deployed environments.

## Data sent to the model provider

The application sends user prompts, selected conversation history, and tool results to the Gemini API. Do not send confidential company data, customer information, credentials, production logs, or regulated data unless the data handling and authorization requirements have been reviewed.

Check the provider's current terms, data handling, retention, and pricing policies before using the API for anything beyond sample data.

## Tool security

- Keep tools explicitly allowlisted.
- Do not use `eval`, `exec`, or model-generated shell commands.
- Do not add unrestricted filesystem access.
- Validate tool arguments and constrain file paths to approved directories.
- Limit the size of tool results and generated reports.
- Treat logs as untrusted data. A log line may contain text that attempts to manipulate the model; it must not be treated as an instruction.
- Keep infrastructure access read-only unless a separately reviewed use case requires more.
- For any state-changing action, require least-privilege credentials, a clear policy check, audit logging, and human approval.

## Local files

- `logs/application.log` is synthetic demo data.
- Generated files under `reports/` may contain model-generated text and should be reviewed before sharing.
- Do not put private or production logs into the repository.
- Ensure the report writer cannot escape the intended output directory.

## Git hygiene

Before committing:

```powershell
git status --short
git diff --cached
```

Check that `.env`, private logs, generated reports, and credentials are not staged.

If a secret was committed, removing it from the latest commit may not be enough; revoke the secret first and follow the repository host's secret-removal procedure.

## Incident-response limitations

AI-generated diagnoses can be incorrect or incomplete. Treat recommendations as hypotheses. Validate with actual telemetry and a qualified operator before acting.
