/*
Ontology for B-Smart Career Navigator (JAC)

Node Types:
	Person, Skill, Role, Industry, Course, Certification, Company, SalaryBand, Location

Edge Types (labels used on edges):
	HAS_SKILL, REQUIRES_SKILL, LEADS_TO, TRANSITIONS_TO,
	LEARNS_FROM, AVAILABLE_IN, RECOMMENDS, GROWS_INTO, LOCATED_IN

This file provides helper macros/walkers to create nodes and edges in a consistent way
so the walkers can rely on these canonical labels.
*/

walker create_node (nid, ntype, props = {}) {
	# create or update a node with id `nid` and type `ntype`
	if (!node_exists(nid)) {
		node(nid, ntype, props);
	} else {
		# update props if needed
		set_node_prop(nid, props);
	}
}

walker connect (src, dst, etype, props = {}) {
	# add directed edge with label `etype`
	add_edge(src, dst, { "type": etype, "props": props });
}

/*
Note: The actual JAC runtime provides primitives such as `node()`, `edge()`,
`walker`, and graph traversal. The helpers above are intentionally small and
are expected to be adapted to your JAC version. They document the canonical
node and edge labels used by B-Smart.
*/
