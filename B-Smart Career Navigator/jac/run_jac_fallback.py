"""
JAC fallback runner

This module provides a small bridge that treats the Python walkers as the
executable equivalent of the JAC walkers so you can test the end-to-end
flow before deploying a real JAC runtime.

Usage:
  from run_jac_fallback import run_recommendation
  out = run_recommendation(person_json)

The output conforms to schema/output_schema.json
"""
from typing import Dict, Any
import os
import json

# import the Python walkers/orchestrator components
from backend.sample_graph import build_sample_graph
from backend.walkers import profile_analyzer, scoring_and_ranking, alternative_path_generator, build_learning_plan
from backend.walkers import deterministic_score

BASE = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(os.path.dirname(BASE), "schema", "output_schema.json")
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    OUTPUT_SCHEMA = json.load(f)

from jsonschema import validate


def run_recommendation(person_json: Dict[str, Any]) -> Dict[str, Any]:
    """Run the Python walkers pipeline to simulate JAC execution and return validated output."""
    graph = build_sample_graph()
    # Profile analyzer
    pa = profile_analyzer(person_json, graph)
    person_id = pa["person"]
    # Scoring
    ranked = scoring_and_ranking(person_id, person_json, graph)
    if not ranked:
        raise RuntimeError("No candidate roles found")
    top = ranked[0]
    role_id = top["role"]
    missing = top.get("missing_skills", [])
    learning_plan = build_learning_plan(missing, graph)
    alternatives = alternative_path_generator(person_id, role_id, graph)

    out = {
        "recommended_role": graph.get_node(role_id).props.get("title", role_id),
        "confidence_score": float(top["score"]),
        "why_this_role": [
            f"Role requires skills: {', '.join([r.split(':',1)[1] for r in [e.dst for e in graph.adj.get(role_id, []) if e.type=='REQUIRES_SKILL']])}"
        ],
        "missing_skills": [s.split(":",1)[1] for s in missing],
        "learning_plan": [{"course_id": item["course"], "title": item["title"], "teaches": item["teaches"]} for item in learning_plan],
        "time_estimate_months": int(len(missing) * 3),
        "cost_estimate": int(len(learning_plan) * 200),
        "alternative_paths": [{"role": graph.get_node(a["role"]).props.get("title", a["role"])} for a in alternatives]
    }

    # Validate
    validate(instance=out, schema=OUTPUT_SCHEMA)
    return out


if __name__ == '__main__':
    # quick demo
    demo = {"id": "person:demo", "name": "Demo", "skills": ["python","sql"], "interests": ["data"], "location": "ny"}
    print(json.dumps(run_recommendation(demo), indent=2))
