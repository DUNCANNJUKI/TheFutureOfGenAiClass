# Ontology definitions (JAC pseudo-syntax)

# Node types
new_node_type(Person)
new_node_type(Skill)
new_node_type(Role)
new_node_type(Industry)
new_node_type(Course)
new_node_type(Certification)
new_node_type(Company)
new_node_type(SalaryBand)
new_node_type(Location)

# Edge types
new_edge_type(HAS_SKILL)
new_edge_type(REQUIRES_SKILL)
new_edge_type(LEADS_TO)
new_edge_type(TRANSITIONS_TO)
new_edge_type(LEARNS_FROM)
new_edge_type(AVAILABLE_IN)
new_edge_type(RECOMMENDS)
new_edge_type(GROWS_INTO)

# Example helper: create role with required skills (walker-friendly)
# walker code will rely on these node/edge names exactly as above
