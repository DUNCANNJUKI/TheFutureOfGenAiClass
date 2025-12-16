"""
CLI demo to run the JAC fallback runner
"""
from jac.run_jac_fallback import run_recommendation
import json

if __name__ == '__main__':
    person = {"id":"person:demo","name":"Demo","skills":["python","sql"],"interests":["data"],"location":"ny"}
    out = run_recommendation(person)
    print(json.dumps(out, indent=2))
