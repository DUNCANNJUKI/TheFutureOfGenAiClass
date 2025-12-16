# B-Smart Career Navigator — Scaffold

This folder contains the production system prompt and a JAC walker skeleton to implement a graph-first career intelligence engine.

Key files:
- `SYSTEM_PROMPT.md` — the strict production system prompt (must be used by orchestration layer)
- `jac/ontology.jac` — node/edge declarations for the domain model (skeleton)
- `jac/walkers.jac` — skeleton walkers: Profile Analyzer, Skill Gap Analyzer, Career Path Finder, Scoring Engine, Alternative Path Generator
- `schema/output_schema.json` — strict JSON schema for outputs

Developer notes:
- All career logic must be implemented in JAC walkers.
- LLMs are only allowed to parse user input into JSON and to articulate explanations based on walker output.
- Ensure all scores are deterministic and numeric per the weights in `SYSTEM_PROMPT.md`.

Next steps:
1. Implement the `walker` bodies in JAC with deterministic scoring functions.
2. Add tests using a small graph dataset and expected outputs conforming to `schema/output_schema.json`.
3. Wire an orchestration layer (Python/FastAPI) that:
   - Accepts user input
   - Uses an LLM only to extract JSON (no reasoning)
   - Updates the graph (Person node)
   - Executes walkers
   - Returns validated JSON output
