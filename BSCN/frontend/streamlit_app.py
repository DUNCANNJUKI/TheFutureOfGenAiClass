import streamlit as st
import requests
import json
from datetime import datetime
import io

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    _HAS_REPORTLAB = True
except Exception:
    _HAS_REPORTLAB = False

API_BASE = st.secrets.get("api_base", "http://127.0.0.1:8002")

st.set_page_config(page_title="B-Smart Career Navigator", layout="wide")

# -- Styling
st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg,#0f1724 0%,#0b2a3a 50%,#2b6f93 100%);} 
    .title {color:#ffffff; font-weight:800; font-size:28px}
    .card {background: rgba(255,255,255,0.96); padding:18px; border-radius:10px; box-shadow: 0 6px 24px rgba(11,38,59,0.12)}
    .muted {color:#243843}
    .accent {color:#ffb366; font-weight:700}
    .small {font-size:13px; color:#243843}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# <span class='title'>B‑Smart Career Navigator</span>", unsafe_allow_html=True)
# Hero / tech background (subtle SVG pattern)
try:
    with open("frontend/assets/tech_bg.svg", "r", encoding="utf-8") as _f:
        svg = _f.read()
except Exception:
    svg = ""

st.markdown(
    f"<div style='padding:12px; border-radius:10px; margin-bottom:12px; background:linear-gradient(90deg, rgba(11,79,108,0.04), rgba(255,127,80,0.02));'>"
    f"<div style=\"display:flex;align-items:center;gap:16px;\">"
    f"<div style=\"width:72px;height:72px;border-radius:12px;background:linear-gradient(135deg,#0b4f6c,#ff7f50);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;\">B</div>"
    f"<div><div style=\"font-size:20px;font-weight:700;color:#0b4f6c\">B‑Smart Career Navigator</div>"
    f"<div style=\"color:#5b6b72\">Upload your CV (.pdf/.docx) or paste text — automatic extraction available.</div></div>"
    f"<div style=\"flex:1;text-align:right;opacity:0.9\">{svg}</div>"
    f"</div></div>",
    unsafe_allow_html=True,
)

left, right = st.columns([2, 3])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    # If a file is uploaded, parse it first and set as initial value for the text area
    uploaded = st.file_uploader("Upload a resume (.pdf or .docx)", type=["pdf", "docx"], key="file_upload")
    parsed_text = ""
    if uploaded is not None:
        fname = uploaded.name.lower()
        try:
            if fname.endswith('.docx'):
                from docx import Document
                doc = Document(uploaded)
                parsed_text = "\n".join([p.text for p in doc.paragraphs if p.text])
            elif fname.endswith('.pdf'):
                from PyPDF2 import PdfReader
                reader = PdfReader(uploaded)
                pages = []
                for p in reader.pages:
                    txt = p.extract_text() or ""
                    pages.append(txt)
                parsed_text = "\n".join(pages)
            else:
                parsed_text = uploaded.getvalue().decode('utf-8', errors='ignore')
            st.success(f"Loaded {uploaded.name} ({len(parsed_text.split())} words)")
        except Exception as e:
            parsed_text = ""
            st.error(f"Failed to extract text from uploaded file: {e}")
        # persist parsed text so it's available across reruns
        st.session_state['parsed_text'] = parsed_text

    # Create the text area with the parsed text as the initial value (avoid mutating session_state after widget creation)
    raw = st.text_area("Paste resume or free text", value=parsed_text or "", height=220, key="raw_input")
    auto_extract = st.checkbox("Auto-extract on upload/paste", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-extract: only call the backend when the text changes (debounce)
    if 'last_extracted_text' not in st.session_state:
        st.session_state['last_extracted_text'] = ''

    if auto_extract:
        # Use the returned widget value `raw` for reliable change detection
        current_text = (raw or "").strip()
        if current_text and current_text != st.session_state['last_extracted_text']:
            try:
                resp = requests.post(f"{API_BASE}/extract", json={"raw_text": current_text}, timeout=15)
                if resp.status_code == 200:
                    st.session_state['extracted'] = resp.json()
                    st.session_state['last_extracted_text'] = current_text
                    st.success("Extraction complete — results ready")
                else:
                    st.error(f"Extraction failed: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Extraction error: {e}")

    st.markdown("---")
    if st.button("Run Recommendation"):
        # Prefer latest extracted JSON, but if missing, attempt extraction on-the-fly
        ex = st.session_state.get("extracted")
        if not ex or not isinstance(ex, dict) or not ex.get('skills'):
            # attempt to extract from current `raw` text area value
            # prefer the raw text area; if empty but a file was uploaded, use parsed_text
            current_text = (raw or "").strip()
            if not current_text:
                current_text = (st.session_state.get('parsed_text') or "").strip()
            if not current_text:
                st.error("No extracted JSON available. Provide text or upload a resume first.")
            else:
                try:
                    resp = requests.post(f"{API_BASE}/extract", json={"raw_text": current_text}, timeout=20)
                    if resp.status_code != 200:
                        st.error(f"Extraction failed: {resp.status_code} {resp.text}")
                        ex = None
                    else:
                        ex = resp.json()
                        st.session_state['extracted'] = ex
                        st.success("Extraction complete — running recommendation")
                except Exception as e:
                    st.error(f"Extraction error: {e}")
        # If we have an extracted JSON, call recommend
        if ex:
            try:
                r = requests.post(f"{API_BASE}/recommend", json=ex, timeout=25)
                if r.status_code != 200:
                    st.error(f"Recommendation failed: {r.status_code} {r.text}")
                else:
                    st.session_state["recommendation"] = r.json()
                    st.success("Recommendation complete — view results on the right")
            except Exception as e:
                st.error(f"Recommendation error: {e}")

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Extracted Profile")
    st.write("**Name:**", st.session_state.get('extracted', {}).get('name', '—'))
    st.write("**Location:**", st.session_state.get('extracted', {}).get('location', '—'))
    st.write("**Skills:**", ', '.join(st.session_state.get('extracted', {}).get('skills', [])) or '—')
    st.write("**Interests:**", ', '.join(st.session_state.get('extracted', {}).get('interests', [])) or '—')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Recommendation")
    rec = st.session_state.get("recommendation")
    if rec:
        st.metric("Role", rec.get('recommended_role','—'), delta=f"Confidence: {rec.get('confidence_score',0):.2f}")
        st.markdown("**Why:**")
        for w in rec.get('why_this_role', []):
            st.write("- ", w)
        st.markdown("**Missing skills:**")
        st.write(', '.join(rec.get('missing_skills', [])) or 'None')
        st.markdown("**Learning plan:**")
        for c in rec.get('learning_plan', []):
            st.write(f"- {c.get('title')} ({c.get('course_id')}) — teaches: {c.get('teaches')}")
        st.markdown("**Alternatives:**")
        st.write(', '.join([a.get('role') for a in rec.get('alternative_paths', [])]) or 'None')
    else:
        st.info("No recommendation yet — upload a CV or paste text and click 'Run Recommendation'")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer with dynamic year and copyright
year = datetime.utcnow().year
st.markdown("<div style='margin-top:16px; text-align:center; color:#5b6b72'>"+
            f"© {year} B‑Smart Career Navigator. Developed by Duncan Njuki, GenAI student OUK."+
            "</div>", unsafe_allow_html=True)

st.markdown("\n\n")


def _generate_pdf_bytes(recommendation: dict, profile: dict) -> bytes:
    if not _HAS_REPORTLAB:
        raise RuntimeError("reportlab is not installed; please install frontend/requirements.txt")
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Header: logo area + system name
    logo_path = "frontend/assets/logo.png"
    y = height - 72
    try:
        img = ImageReader(logo_path)
        c.drawImage(img, 40, y - 48, width=80, height=48, mask='auto')
    except Exception:
        # draw simple box with system initial
        c.setFillColorRGB(0.05, 0.16, 0.25)
        c.rect(40, y - 48, 80, 48, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(58, y - 24, "B")

    c.setFillColorRGB(0.03, 0.15, 0.25)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(140, y - 18, "B‑Smart Career Navigator")

    # Profile section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y - 80, "Profile")
    c.setFont("Helvetica", 11)
    px = 40
    py = y - 100
    c.drawString(px, py, f"Name: {profile.get('name','—')}")
    c.drawString(px + 300, py, f"Location: {profile.get('location','—')}")
    py -= 18
    c.drawString(px, py, "Skills: ")
    skills = ', '.join(profile.get('skills', [])) or '—'
    c.drawString(px + 50, py, skills)
    py -= 18
    c.drawString(px, py, "Interests: ")
    c.drawString(px + 65, py, ', '.join(profile.get('interests', [])) or '—')

    # Recommendation section
    py -= 36
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, py, "Recommendation")
    py -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, py, f"Role: {recommendation.get('recommended_role','—')}")
    c.setFont("Helvetica", 11)
    c.drawString(320, py, f"Confidence: {recommendation.get('confidence_score',0):.2f}")
    py -= 18
    c.drawString(40, py, "Why this role:")
    py -= 14
    for line in recommendation.get('why_this_role', []):
        c.drawString(56, py, f"- {line}")
        py -= 14
        if py < 120:
            c.showPage()
            py = height - 80

    py -= 6
    c.drawString(40, py, "Missing skills:")
    c.drawString(140, py, ', '.join(recommendation.get('missing_skills', [])) or 'None')
    py -= 18
    c.drawString(40, py, "Learning plan:")
    py -= 14
    for item in recommendation.get('learning_plan', []):
        c.drawString(56, py, f"- {item.get('title')} ({item.get('course_id')}) — teaches: {item.get('teaches')}")
        py -= 14
        if py < 120:
            c.showPage()
            py = height - 80

    # Footer
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(40, 40, f"© {datetime.utcnow().year} B‑Smart Career Navigator. Developed by Duncan Njuki")
    c.drawRightString(width - 40, 40, "Generated by BSCN")

    c.save()
    buf.seek(0)
    return buf.read()


if st.button("Download Recommendation PDF"):
    rec = st.session_state.get("recommendation")
    prof = st.session_state.get("extracted", {})
    if not rec:
        st.error("No recommendation available to export. Run Recommendation first.")
    else:
        try:
            pdf_bytes = _generate_pdf_bytes(rec, prof)
            st.download_button("Download PDF", data=pdf_bytes, file_name="BSCN_recommendation.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")
