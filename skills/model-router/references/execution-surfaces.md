# Execution surfaces

This is a discovery workflow, not a static inventory of tools. Use the schema,
installed help, or documentation for the actual surface. Never infer a tool's
existence or writable fields from its name or another product's UI.

## Claude and Codex sessions

Inspect the active model and supported controls when exposed. In Claude Code,
consult [model configuration](https://code.claude.com/docs/en/model-config)
(verified 2026-09-06). In Codex, inspect available tool schemas or installed CLI
help; use official OpenAI documentation if local information is insufficient.
An API model list is not a list of models supported in every app.

A tool that sets a model for another task or worker does not change this session.
Do not edit global defaults for a request concerning one task. If no writable
control exists, explain that limitation and give a documented manual step.
If the installed UI cannot be verified, say so instead of inventing menu paths.

## Schedules and audits

Read the existing task definition and discover that scheduler's model/effort
controls. Do not assume Claude routines and Codex automations share fields or
that either always requires manual editing. Preserve schedule, prompt scope,
and notification preferences unless the request changes them. A schedule audit
is read-only unless changes were authorized.

Prioritize frequency, consequences, and observed failures. Record current and
proposed settings, why the change helps, required checks, and whether the change
is actionable through the available tool. Account for late/catch-up runs when
the task's correctness depends on timing.

## Workers and subagents

Discover installed offload skills or workers, such as a second Claude Code
session, a Codex offload, or a local-model runtime; these are examples, not
assertions of availability. Read only the selected workflow. A missing helper
does not authorize installing software or starting a paid service.

Respect the host's rules on delegation and task creation. Use only a supported
model/effort combination and the resources authorized for that worker. Preserve
file scope, data boundaries, acceptance checks, and progress/stop conditions.
A worker with a local working directory may still send all prompts remotely.

## Apply and verify

1. Resolve the exact target, allowed settings, and existing authorization.
2. Apply the smallest supported change; do not duplicate an existing worker or
   broaden a task-scoped change into persistent defaults.
3. Read effective settings from the result or state. Report applied versus
   recommended versus unverified separately. If the result is ambiguous, inspect
   before retrying. No success claim from a prompt line or a self-report alone.

When a new decision or authorization is necessary, ask only for that missing
piece. Existing permission persists; do not add a confirmation ceremony to an
already authorized switch.
