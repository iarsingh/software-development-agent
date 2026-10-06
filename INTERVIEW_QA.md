# Software Development Agent: interview questions and answers

Answers describe this repository's current implementation. Suggested production changes are explicitly labeled as future work.

## 1. Does this agent generate or apply a patch?

The planner is deterministic and returns test, implementation, verification, and review steps. The goal selects an API-handler or implementation focus; validated relative file paths and acceptance checks describe scope. It does not generate a diff, call a model, read files, execute tools, or apply changes.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 2. Which goals are refused?

A case-insensitive word-boundary scan rejects goals containing `git push`, `apply`, or `merge`. For example, `git push origin main` returns `refused: true` and an empty tools list. This is a coarse phrase check, not a complete command policy.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 3. How is an empty goal handled?

A missing, non-string, or whitespace-only goal raises `InputError`; the HTTP handler translates it to status 422.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 4. What happens to the payload?

The handler passes `body.get("payload") or body`. The planner validates an optional list of at most 50 workspace-relative paths, rejects traversal and absolute paths, and returns deduplicated scope. It does not open or modify these paths.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 5. How would you demonstrate the current behavior?

Send `{"goal":"add a healthz test"}` to `/agent/run`. The response contains a goal-aware deterministic plan and `wrote: false`, `applied: false`. Then demonstrate a refused goal; do not describe the first response as a generated patch.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 6. Is the tools field evidence that tools ran?

No. `TOOLS` is a constant label list. There are no function calls that execute those tools. Execution traces would need actual tool inputs, outputs, errors, and durations.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 7. What is the main limitation of the refusal scan?

Word-boundary matching avoids some substring false positives but can still miss other descriptions of mutations. Keep real execution permissions separate from natural-language checks before adding tool execution.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 8. What would a useful next iteration add?

Extend the current scope and acceptance-check output with read-only source inspection and concrete proposed diffs. Keep execution behind an explicit permission boundary and isolated workspace.

Source: [src/devagent/agent.py](src/devagent/agent.py).

## 9. How are the domain API and ops plane connected?

The app registers the ops router under `/v1`, alongside the domain endpoint. Creating or approving a job updates ops records; it does not call the domain function. There is no background worker or job executor.

Source: [src/devagent/main.py](src/devagent/main.py).

## 10. Does X-Tenant-Id authenticate a user?

No. It is a caller-supplied header defaulting to `default`. Workspace and job reads filter by that value, but a caller can choose another value. Real identity and authorization would need to precede this lab tenant selector.

Source: [src/devagent/ops.py](src/devagent/ops.py).

## 11. What survives a process restart?

Nothing in the ops dictionaries or audit list is persisted. Multiple server workers would also have separate state. Durable storage, transactions, and a shared job queue are future changes.

Source: [src/devagent/ops.py](src/devagent/ops.py).

## 12. What happens when a production job is approved?

Targets are trimmed and normalized to lowercase before policy checks. `prod` and `production`, including case/padding variants, create a `pending_approval` job and approval returns HTTP 403. Repeated lab approval is idempotent; approval changes a record only, without executing a workload.

Source: [src/devagent/ops.py](src/devagent/ops.py).

## 13. Are audit and metrics equally tenant-scoped?

Audit results filter events by the tenant and its workspace/job identifiers. `/v1/metrics` returns process-wide counters without tenant filtering, so it is not a tenant-specific dashboard. Domain requests are not automatically audited.

Source: [src/devagent/ops.py](src/devagent/ops.py).

## 14. What would you prioritize before a customer deployment?

Define authenticated identities and permission checks, durable state, typed domain inputs, bounded requests, concurrency behavior, and observable execution semantics. Use the existing tests as a baseline, then test failure and access boundaries rather than claiming the lab is production-ready.

Source: [src/devagent/ops.py](src/devagent/ops.py).
