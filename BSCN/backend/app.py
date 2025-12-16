from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
from jsonschema import validate, ValidationError

from .sample_graph import build_sample_graph
from .walkers import profile_analyzer, scoring_and_ranking, alternative_path_generator, build_learning_plan

BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(os.path.dirname(BASE_DIR), "schema", "output_schema.json")
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    OUTPUT_SCHEMA = json.load(f)

app = FastAPI(title="B-Smart Career Navigator - Orchestrator")

class ExtractedInput(BaseModel):
    # This endpoint expects the LLM to have already returned structured JSON
    id: str
    name: str = ""
    skills: List[str] = []
    interests: List[str] = []
    location: str = ""

@app.post("/recommend")
async def recommend(payload: ExtractedInput):
    # Load graph
    graph = build_sample_graph()
    person_json = payload.dict()
    person_json["id"] = payload.id
    # 1) Profile Analyzer
    pa = profile_analyzer(person_json, graph)
    person_id = pa["person"]
    # 2) Scoring & Ranking
    ranked = scoring_and_ranking(person_id, person_json, graph)
    if not ranked:
        raise HTTPException(status_code=400, detail="No candidate roles found")
    top = ranked[0]
    role_id = top["role"]
    # 3) Skill Gap
    missing_skills = top.get("missing_skills", [])
    # 4) Learning plan
    learning_plan = build_learning_plan(missing_skills, graph)
    # 5) Alternatives
    alternatives = alternative_path_generator(person_id, role_id, graph)
    # Compose output following strict schema
    out = {
        "recommended_role": graph.get_node(role_id).props.get("title", role_id),
        "confidence_score": float(top["score"]),
        "why_this_role": [
            f"Role aligns with skills: {', '.join([s.split(':',1)[1] for s in graph.incoming(role_id) if s.startswith('skill:')])}" if graph.incoming(role_id) else "Role matches candidate profile"
        ],
        "missing_skills": [s.split(":",1)[1] for s in missing_skills],
        "learning_plan": [{"course_id": item["course"], "title": item["title"], "teaches": item["teaches"}] for item in learning_plan],
        "time_estimate_months": int(len(missing_skills) * 3),
        "cost_estimate": int(len(learning_plan) * 200),
        "alternative_paths": [{"role": graph.get_node(a["role"]).props.get("title", a["role"])} for a in alternatives]
    }
    # Validate output strictly
    try:
        validate(instance=out, schema=OUTPUT_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Output validation error: {e.message}")
    return out

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
