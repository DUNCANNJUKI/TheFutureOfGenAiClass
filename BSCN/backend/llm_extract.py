from typing import Dict, Any, Optional, List
import os
import re
import difflib

try:
    import spacy
    from spacy.matcher import PhraseMatcher
    _HAS_SPACY = True
except Exception:
    _HAS_SPACY = False

# LLM extraction bridge. This module will attempt to call a configured LLM
# provider to extract structured JSON from free text. If no provider is
# configured it falls back to a deterministic heuristic extractor that
# extracts name, skills, interests and location from the input string.


def _normalize_list(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for it in items:
        v = it.strip()
        if not v:
            continue
        v = v.lower()
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def heuristic_extract(text: str, known_skills: Optional[list] = None) -> Dict[str, Any]:
    known_skills = known_skills or [
        "python", "sql", "data-viz", "etl", "statistics", "linux", "cloud", "aws", "gcp", "azure"
    ]
    out = {"id": "person:extracted", "name": "", "skills": [], "interests": [], "location": "", "email": "", "phone": ""}

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Email and phone
    m = re.search(r"([\w\.-]+@[\w\.-]+)", text)
    if m:
        out["email"] = m.group(1)
    m = re.search(r"(\+?\d[\d\-\s]{6,}\d)", text)
    if m:
        out["phone"] = re.sub(r"\s+", "", m.group(1))

    # Name detection: prefer a leading 'Name:' or the first line if it looks like a name
    for l in lines[:5]:
        m = re.match(r"(?i)^(?:name|full name)[:\s]+(.+)$", l)
        if m:
            out["name"] = m.group(1).strip()
            break
    if not out["name"] and lines:
        # Heuristic: first line with 2 words and capitalized
        first = lines[0]
        if len(first.split()) <= 4 and re.search(r"[A-Z]", first):
            out["name"] = first

    # Skills: fuzzy token match
    skills_found = set()
    tokens = re.split(r"[\,;\n\|\/]", text)
    for chunk in tokens:
        for s in known_skills:
            if re.search(rf"\b{re.escape(s)}\b", chunk, flags=re.I):
                skills_found.add(s)
        # fuzzy matching for near-misses
        for word in re.findall(r"\w[\w\-+.#]*", chunk):
            match = difflib.get_close_matches(word.lower(), known_skills, n=1, cutoff=0.85)
            if match:
                skills_found.add(match[0])
    out["skills"] = _normalize_list(list(skills_found))

    # Interests: capture lines starting with 'interests' or 'interested in'
    interests = []
    for l in lines:
        m = re.match(r"(?i)^interests?[:\s]+(.+)$", l)
        if m:
            interests.extend([t.strip() for t in re.split(r"[,;]", m.group(1)) if t.strip()])
        m = re.search(r"interested in[:\s]?(.+)$", l, flags=re.I)
        if m:
            interests.extend([t.strip() for t in re.split(r"[,;]", m.group(1)) if t.strip()])
    out["interests"] = _normalize_list(interests)

    # Location: explicit 'Location:' or common tokens
    for l in lines[:8]:
        m = re.match(r"(?i)^location[:\s]+(.+)$", l)
        if m:
            out["location"] = m.group(1).strip()
            break
    if not out["location"]:
        m = re.search(r"\b(New York|NY|San Francisco|London|Berlin|Nairobi|Remote)\b", text, flags=re.I)
        if m:
            out["location"] = m.group(1)

    return out


def spacy_extract(text: str, known_skills: Optional[list] = None) -> Dict[str, Any]:
    """Use spaCy NER and PhraseMatcher to extract stronger structured fields.
    Falls back to `heuristic_extract` if spaCy or model is missing.
    """
    if not _HAS_SPACY:
        return heuristic_extract(text, known_skills=known_skills)

    try:
        # Try to load a common small English model, fall back to blank pipeline
        try:
            nlp = spacy.load("en_core_web_sm")
        except Exception:
            nlp = spacy.blank("en")

        doc = nlp(text)
        out = {"id": "person:extracted", "name": "", "skills": [], "interests": [], "location": "", "email": "", "phone": ""}

        # PERSON entity for name
        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if persons:
            out["name"] = persons[0]

        # GPE/LOC for location
        locs = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
        if locs:
            out["location"] = locs[0]

        # Email / phone
        m = re.search(r"([\w\.-]+@[\w\.-]+)", text)
        if m:
            out["email"] = m.group(1)
        m = re.search(r"(\+?\d[\d\-\s]{6,}\d)", text)
        if m:
            out["phone"] = re.sub(r"\s+", "", m.group(1))

        # Skills: use PhraseMatcher for known skills list where possible
        known = known_skills or ["python", "sql", "data-viz", "etl", "statistics", "linux", "cloud", "aws", "gcp", "azure"]
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(s) for s in known]
        matcher.add("SKILLS", patterns)
        matches = matcher(doc)
        skills = set()
        for _, start, end in matches:
            span = doc[start:end].text
            skills.add(span.lower())

        # also fallback token matching
        for token in doc:
            for s in known:
                if token.text.lower() == s.lower():
                    skills.add(s.lower())

        out["skills"] = _normalize_list(list(skills))

        # Interests: noun-chunk heuristic
        interests = set()
        for chunk in doc.noun_chunks:
            txt = chunk.text.strip()
            if any(k in txt.lower() for k in ["data", "engineering", "analysis", "ml", "ai", "cloud", "devops"]):
                interests.add(txt)
        out["interests"] = _normalize_list(list(interests))

        return out
    except Exception:
        return heuristic_extract(text, known_skills=known_skills)


def extract_json_from_text(text: str) -> Dict[str, Any]:
    # If an LLM provider is configured, delegate to it. Supported providers
    # can be added here. For now we look for env var `LLM_PROVIDER`.
    provider = os.environ.get("LLM_PROVIDER", "").lower()
    api_key = os.environ.get("LLM_API_KEY")

    if provider in ("openai", "gpt", "claude") and api_key:
        # Try to call the provider (best-effort adapter). We avoid bundling
        # any specific SDK hard dependency here; the runtime may provide one.
        try:
            if provider == "openai":
                import openai
                openai.api_key = api_key
                prompt = (
                    "Extract JSON with fields id,name,skills,interests,location from the following text. "
                    "Return only valid JSON." + "\n\nText:\n" + text
                )
                resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=500)
                content = resp.choices[0].message.content
                import json
                return json.loads(content)
            # Add other provider adapters as needed (claude, anthropic, etc.)
        except Exception:
            # fall back to heuristic
            pass

    # Prefer spaCy extraction when available for more precise fields
    if _HAS_SPACY:
        return spacy_extract(text)

    return heuristic_extract(text)
