"""
Implementations of walkers in Python that mimic deterministic JAC walkers.
Each walker returns explicit structured outputs so the orchestrator can combine them.
"""
from typing import Dict, Any, List, Tuple
from .graph import Graph

# Scoring weights (deterministic)
WEIGHTS = {
    "skill_match": 0.40,
    "interest_match": 0.20,
    "market_demand": 0.20,
    "learning_cost": 0.10,
    "time_to_entry": 0.10
}

def profile_analyzer(person_json: Dict[str, Any], graph: Graph) -> Dict[str, Any]:
    # Person JSON: {"id": "person:1", "skills": ["python","sql"], "interests": ["data"] , "location": "ny"}
    pid = person_json.get("id", "person:anonymous")
    # Create Person node in graph if not present (idempotent)
    if pid not in graph.nodes:
        graph.add_node(pid, "Person", {"name": person_json.get("name","anon")})
    # Attach HAS_SKILL edges
    for s in person_json.get("skills", []):
        sid = f"skill:{s}"
        if sid in graph.nodes:
            graph.add_edge(pid, sid, "HAS_SKILL")
    # Attach location
    loc = person_json.get("location")
    if loc:
        graph.add_node(f"location:{loc}", "Location", {"id": loc})
        graph.add_edge(pid, f"location:{loc}", "LOCATED_IN")
    return {"person": pid}


def skill_gap_analyzer(person_id: str, role_id: str, graph: Graph) -> List[str]:
    # Return list of missing skill ids (strings like 'skill:sql')
    required = [e.dst for e in graph.adj.get(role_id, []) if e.type == "REQUIRES_SKILL"]
    have = [e.dst for e in graph.adj.get(person_id, []) if e.type == "HAS_SKILL"]
    missing = [r for r in required if r not in have]
    return missing


def career_path_finder(person_id: str, graph: Graph, max_depth: int=3) -> List[Dict[str, Any]]:
    # Enumerate candidate roles reachable via LEADS_TO or TRANSITIONS_TO starting from available roles or broad search
    candidates = []
    # We'll consider all Role nodes in the graph as candidates (small sample graph)
    for nid, node in graph.nodes.items():
        if node.type == "Role":
            # compute missing skills for this role
            missing = skill_gap_analyzer(person_id, nid, graph)
            candidates.append({"role": nid, "missing": missing})
    return candidates


def deterministic_score(person_id: str, role_id: str, missing_skills: List[str], person_interest: List[str], graph: Graph) -> float:
    # Skill match score: percent of required skills the person has
    required = [e.dst for e in graph.adj.get(role_id, []) if e.type == "REQUIRES_SKILL"]
    if not required:
        skill_match = 0.0
    else:
        skill_match = max(0.0, 1.0 - (len(missing_skills) / len(required)))
    # Interest match: basic deterministic check if any interest token matches role title tokens
    role_title = graph.get_node(role_id).props.get("title","").lower()
    interest_match = 0.0
    for it in person_interest:
        if it.lower() in role_title:
            interest_match = 1.0
            break
    # Market demand: simple deterministic lookup (presence in AVAILABLE_IN for a sample location implies demand)
    market_demand = 0.5
    # learning cost/time: proportional to missing skills
    learning_cost = min(1.0, 0.2 * len(missing_skills))
    time_to_entry = min(1.0, 3 * len(missing_skills) / 12.0)  # normalized

    score = (
        WEIGHTS["skill_match"] * skill_match +
        WEIGHTS["interest_match"] * interest_match +
        WEIGHTS["market_demand"] * market_demand +
        WEIGHTS["learning_cost"] * (1.0 - learning_cost) +
        WEIGHTS["time_to_entry"] * (1.0 - time_to_entry)
    )
    # Deterministic numeric score between 0 and 1
    return round(float(score), 4)


def scoring_and_ranking(person_id: str, person_json: Dict[str, Any], graph: Graph) -> List[Dict[str, Any]]:
    # Produce ranked list of candidate roles with scores and details
    person_interest = person_json.get("interests", [])
    candidates = career_path_finder(person_id, graph)
    scored = []
    for c in candidates:
        role = c["role"]
        missing = c["missing"]
        score = deterministic_score(person_id, role, missing, person_interest, graph)
        scored.append({"role": role, "score": score, "missing_skills": missing})
    # Sort descending by score deterministic tie-breaker by role id
    scored.sort(key=lambda x: (x["score"], x["role"]), reverse=True)
    return scored


def alternative_path_generator(person_id: str, top_role: str, graph: Graph, limit: int=3) -> List[Dict[str, Any]]:
    # Suggest roles connected via TRANSITIONS_TO or GROWS_INTO from top_role
    alternatives = []
    for e in graph.adj.get(top_role, []):
        if e.type in ("TRANSITIONS_TO", "GROWS_INTO"):
            alternatives.append({"role": e.dst})
    return alternatives


def build_learning_plan(missing_skills: List[str], graph: Graph) -> List[Dict[str, Any]]:
    # For each missing skill, find courses that LEARNS_FROM that skill
    plan = []
    for ms in missing_skills:
        # find courses where there's an edge course -> skill with LEARNS_FROM
        for nid, node in graph.nodes.items():
            if node.type == "Course":
                for e in graph.adj.get(nid, []):
                    if e.type == "LEARNS_FROM" and e.dst == ms:
                        plan.append({"course": nid, "title": node.props.get("title","unknown"), "teaches": ms})
    return plan
