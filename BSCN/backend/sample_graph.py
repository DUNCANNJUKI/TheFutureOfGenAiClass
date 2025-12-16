"""
Sample deterministic graph dataset to use in demos and tests.
Includes Nodes: Skills, Roles, Courses, Location, SalaryBand
Edges: REQUIRES_SKILL, LEARNS_FROM, LEADS_TO, TRANSITIONS_TO, AVAILABLE_IN
"""
from .graph import Graph

def build_sample_graph() -> Graph:
    g = Graph()
    # Skills
    skills = ["python", "sql", "data-viz", "etl", "statistics", "linux", "cloud"]
    for s in skills:
        g.add_node(f"skill:{s}", "Skill", {"name": s})
    # Roles
    roles = {
        "role:data_analyst": {"title": "Data Analyst"},
        "role:data_engineer": {"title": "Data Engineer"},
        "role:software_engineer": {"title": "Software Engineer"}
    }
    for nid, props in roles.items():
        g.add_node(nid, "Role", props)
    # Role requirements
    g.add_edge("role:data_analyst", "skill:sql", "REQUIRES_SKILL")
    g.add_edge("role:data_analyst", "skill:data-viz", "REQUIRES_SKILL")
    g.add_edge("role:data_analyst", "skill:statistics", "REQUIRES_SKILL")

    g.add_edge("role:data_engineer", "skill:python", "REQUIRES_SKILL")
    g.add_edge("role:data_engineer", "skill:etl", "REQUIRES_SKILL")
    g.add_edge("role:data_engineer", "skill:sql", "REQUIRES_SKILL")
    g.add_edge("role:data_engineer", "skill:cloud", "REQUIRES_SKILL")

    g.add_edge("role:software_engineer", "skill:python", "REQUIRES_SKILL")
    g.add_edge("role:software_engineer", "skill:linux", "REQUIRES_SKILL")

    # Transitions & Leads
    g.add_edge("role:data_analyst", "role:data_engineer", "TRANSITIONS_TO")
    g.add_edge("role:software_engineer", "role:data_engineer", "TRANSITIONS_TO")
    g.add_edge("role:data_engineer", "role:software_engineer", "TRANSITIONS_TO")

    # Courses
    courses = {"course:intro_sql": "Intro to SQL", "course:etl": "ETL Fundamentals", "course:data-viz": "Data Visualization"}
    for nid, title in courses.items():
        g.add_node(nid, "Course", {"title": title})
    g.add_edge("course:intro_sql", "skill:sql", "LEARNS_FROM")
    g.add_edge("course:etl", "skill:etl", "LEARNS_FROM")
    g.add_edge("course:data-viz", "skill:data-viz", "LEARNS_FROM")

    # Locations & availability
    g.add_node("location:ny", "Location", {"city":"New York", "country":"USA"})
    g.add_edge("role:data_analyst", "location:ny", "AVAILABLE_IN")
    g.add_edge("role:data_engineer", "location:ny", "AVAILABLE_IN")
    g.add_edge("role:software_engineer", "location:ny", "AVAILABLE_IN")

    # Salary bands
    g.add_node("salary:mid", "SalaryBand", {"min":40000, "max":90000})
    g.add_edge("role:data_analyst", "salary:mid", "RECOMMENDS")

    return g
