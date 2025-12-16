/*
JAC walker implementations (translation of Python walkers)

This file provides deterministic walker logic for:
- profile_analyzer
- skill_gap_analyzer
- career_path_finder
- scoring_engine
- alternative_paths

These walkers operate using the canonical node and edge labels defined in
`ontology.jac`. They are intentionally written to be deterministic and to
return structured outputs that an orchestrator can consume.
*/

walker profile_analyzer(person_json) {
  # person_json is a map: { id: "person:1", skills: ["python","sql"], interests: ["data"], location: "ny" }
  let pid = person_json.id;
  if (!node_exists(pid)) {
    node(pid, "Person", { name: person_json.name });
  }
  # attach HAS_SKILL edges for known skills
  foreach (s in person_json.skills) {
    let sid = concat("skill:", s);
    if (node_exists(sid)) {
      add_edge(pid, sid, { type: "HAS_SKILL" });
    }
  }
  # attach location
  if (person_json.location) {
    let lid = concat("location:", person_json.location);
    if (!node_exists(lid)) { node(lid, "Location", { id: person_json.location }); }
    add_edge(pid, lid, { type: "LOCATED_IN" });
  }
  return { person: pid };
}

walker skill_gap_analyzer(person_id, role_id) {
  # returns a list of missing skill node ids for role_id
  let required = [];
  foreach (e in out_edges(role_id)) {
    if (e.props.type == "REQUIRES_SKILL") { required.push(e.dst); }
  }
  let have = [];
  foreach (e in out_edges(person_id)) {
    if (e.props.type == "HAS_SKILL") { have.push(e.dst); }
  }
  let missing = [];
  foreach (r in required) { if (!in_array(r, have)) { missing.push(r); } }
  return missing;
}

walker career_path_finder(person_id) {
  # enumerate Role nodes and compute missing skills for each
  let results = [];
  foreach (n in all_nodes()) {
    if (n.props.type == "Role" || n.type == "Role") {
      let rid = n.id;
      let missing = run walker skill_gap_analyzer(person_id, rid);
      results.push({ role: rid, missing: missing });
    }
  }
  return results;
}

walker deterministic_score(person_id, role_id, missing_skills, person_interests) {
  # compute deterministic numeric score 0..1 using fixed weights
  let required = [];
  foreach (e in out_edges(role_id)) { if (e.props.type == "REQUIRES_SKILL") { required.push(e.dst); } }
  let skill_match = 0.0;
  if (len(required) > 0) { skill_match = 1.0 - (len(missing_skills) / len(required)); }
  # interest match: 1.0 if any interest token in role title
  let role_title = get_node_prop(role_id, "title") or "";
  let interest_match = 0.0;
  foreach (it in person_interests) {
    if (str_contains(lower(role_title), lower(it))) { interest_match = 1.0; break; }
  }
  # market demand: simple deterministic fallback 0.5
  let market_demand = 0.5;
  let learning_cost = min(1.0, 0.2 * len(missing_skills));
  let time_to_entry = min(1.0, (3 * len(missing_skills)) / 12.0);

  let score = 0.40 * skill_match + 0.20 * interest_match + 0.20 * market_demand + 0.10 * (1.0 - learning_cost) + 0.10 * (1.0 - time_to_entry);
  return round(score, 4);
}

walker scoring_engine(person_id, person_json) {
  let interest = person_json.interests or [];
  let candidates = run walker career_path_finder(person_id);
  let scored = [];
  foreach (c in candidates) {
    let sc = run walker deterministic_score(person_id, c.role, c.missing, interest);
    scored.push({ role: c.role, score: sc, missing: c.missing });
  }
  # sort descending by score then by role id
  scored = sort_by(scored, (x) => (-x.score, x.role));
  return scored;
}

walker alternative_paths(person_id, top_role_id) {
  let alts = [];
  foreach (e in out_edges(top_role_id)) {
    if (e.props.type == "TRANSITIONS_TO" or e.props.type == "GROWS_INTO") { alts.push({ role: e.dst }); }
  }
  return alts;
}

/*
Notes:
- The above JAC code uses common walker primitives (`node_exists`, `node`, `add_edge`, `out_edges`, `all_nodes`, `get_node_prop`, etc.). Adapt to your JAC runtime's exact API.
- All computations are deterministic and numeric; scoring uses the weights specified in the system prompt.
*/
