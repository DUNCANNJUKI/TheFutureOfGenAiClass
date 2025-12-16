"""
Runnable JAC walkers for BSCN (B-Smart Career Navigator)

This file is a best-effort runnable translation of the Python walkers and
the `walkers.jac` pseudocode into the repository's JAC dialect. It uses
the canonical node and edge labels defined in `ontology.jac` and mirrors
the deterministic scoring logic used by the Python fallback.

Usage (example):
    jac run walkers_runnable.jac

Adapt as needed for your jac runtime/version. The implementation intentionally
uses only straightforward primitives (node, add_edge, out_edges, all_nodes,
get_node_prop, etc.) so it should be compatible with common jac versions
used elsewhere in this repo.
"""

walker profile_analyzer(person_json) {
    # person_json: map { id: "person:1", name: "Alice", skills: [..], interests: [..], location: "ny" }
    let pid = person_json.id;
    if (!node_exists(pid)) {
        node(pid, "Person", { name: person_json.name });
    } else {
        set_node_prop(pid, { name: person_json.name });
    }

    # attach skills
    if (person_json.skills) {
        foreach (s in person_json.skills) {
            let sid = concat("skill:", s);
            if (!node_exists(sid)) { node(sid, "Skill", { id: s }); }
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
    let required = [];
    foreach (e in out_edges(role_id)) {
        if (has_key(e.props, "type") and e.props.type == "REQUIRES_SKILL") { required = required + [ e.dst ]; }
    }

    let have = [];
    foreach (e in out_edges(person_id)) {
        if (has_key(e.props, "type") and e.props.type == "HAS_SKILL") { have = have + [ e.dst ]; }
    }

    let missing = [];
    foreach (r in required) { if (!in_array(r, have)) { missing = missing + [ r ]; } }
    return missing;
}

walker career_path_finder(person_id) {
    let results = [];
    foreach (n in all_nodes()) {
        # Roles may be nodes with type Role or props.type == 'Role'
        if ((has_key(n, "props") and has_key(n.props, "type") and n.props.type == "Role") or n.type == "Role") {
            let rid = n.id;
            let missing = run walker skill_gap_analyzer(person_id, rid);
            results = results + [ { role: rid, missing: missing } ];
        }
    }
    return results;
}

walker deterministic_score(person_id, role_id, missing_skills, person_interests) {
    let required = [];
    foreach (e in out_edges(role_id)) { if (has_key(e.props, "type") and e.props.type == "REQUIRES_SKILL") { required = required + [ e.dst ]; } }

    let skill_match = 0.0;
    if (len(required) > 0) { skill_match = 1.0 - (len(missing_skills) / len(required)); }

    let role_title = get_node_prop(role_id, "title") or "";
    let interest_match = 0.0;
    if (person_interests) {
        foreach (it in person_interests) {
            if (str_contains(lower(role_title), lower(it))) { interest_match = 1.0; break; }
        }
    }

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
        scored = scored + [ { role: c.role, score: sc, missing: c.missing } ];
    }
    # sort_by helper: assume runtime provides a sort_by; otherwise user may adapt
    try {
        scored = sort_by(scored, (x) => (-x.score, x.role));
    } catch (e) {
        # best-effort: leave unsorted if helper not available
        scored = scored;
    }
    return scored;
}

walker alternative_paths(person_id, top_role_id) {
    let alts = [];
    foreach (e in out_edges(top_role_id)) {
        if (has_key(e.props, "type") and (e.props.type == "TRANSITIONS_TO" or e.props.type == "GROWS_INTO")) { alts = alts + [ { role: e.dst } ]; }
    }
    return alts;
}

/* End of runnable walkers */
