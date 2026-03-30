import streamlit as st
import pandas as pd
import re
import time
import io
import base64
from pathlib import Path
from openai import OpenAI

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="QA Evaluation — Superbank",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO_B64 = "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"

# -----------------------------------------------
# DESIGN SYSTEM  --  Superbank brand
# -----------------------------------------------
PRIMARY    = "#AADC00"
TEAL_DARK  = "#083830"
TEAL_MID   = "#0C4A40"
TEAL_CARD  = "#0F5548"
TEAL_EDGE  = "#1A7060"
WHITE      = "#FFFFFF"
WHITE_MUTE = "#B8D4CC"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif !important;
    background-color: {TEAL_DARK} !important;
    color: {WHITE} !important;
}}

.stApp, .main {{
    background-color: {TEAL_DARK} !important;
}}

/* ── Loading animation panel ── */
.loading-panel {{
    background: {TEAL_CARD};
    border: 1px solid {TEAL_EDGE};
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 0.6rem 0 1rem;
    position: relative;
    overflow: hidden;
}}

/* Scan-line sweep */
.loading-panel::after {{
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(170,220,0,0.07), transparent);
    animation: scanline 2s linear infinite;
}}
@keyframes scanline {{
    0%   {{ left: -60%; }}
    100% {{ left: 140%; }}
}}

/* Spinning ring */
.spinner-ring {{
    display: inline-block;
    width: 18px;
    height: 18px;
    border: 2.5px solid {TEAL_EDGE};
    border-top-color: {PRIMARY};
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
    vertical-align: middle;
    margin-right: 0.5rem;
}}
@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

/* Shimmer progress bar */
.shimmer-bar-wrap {{
    background: {TEAL_EDGE};
    border-radius: 99px;
    height: 6px;
    margin-top: 0.9rem;
    overflow: hidden;
}}
.shimmer-bar {{
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, {PRIMARY}88, {PRIMARY}, {PRIMARY}88);
    background-size: 200% 100%;
    animation: shimmer 1.4s ease-in-out infinite;
}}
@keyframes shimmer {{
    0%   {{ background-position: 200% center; }}
    100% {{ background-position: -200% center; }}
}}

/* Pulse dots */
.pulse-dots span {{
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {PRIMARY};
    margin: 0 2px;
    animation: pulse-dot 1.2s ease-in-out infinite;
}}
.pulse-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
.pulse-dots span:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes pulse-dot {{
    0%, 80%, 100% {{ transform: scale(0.6); opacity: 0.4; }}
    40%           {{ transform: scale(1);   opacity: 1; }}
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {TEAL_MID} !important;
    border-right: 2px solid {TEAL_EDGE} !important;
}}
[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}
[data-testid="stSidebar"] .sidebar-logo {{
    padding: 1.4rem 1.2rem 1rem;
    border-bottom: 1px solid {TEAL_EDGE};
    margin-bottom: 1rem;
}}
[data-testid="stSidebar"] h3 {{
    color: {PRIMARY} !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 1.2rem !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: {TEAL_EDGE} !important;
    opacity: 0.6;
}}
[data-testid="stSidebar"] label {{
    color: {WHITE_MUTE} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}}

/* Main area */
.main .block-container {{
    padding: 0 2rem 3rem !important;
    max-width: 1200px;
    background-color: {TEAL_DARK} !important;
}}

/* Top header bar */
.sb-topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: {TEAL_MID};
    padding: 0.9rem 2rem;
    margin: -1rem -2rem 2rem;
    border-bottom: 3px solid {PRIMARY};
}}
.sb-topbar-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {WHITE};
    letter-spacing: 0.02em;
}}
.sb-topbar-badge {{
    background: {PRIMARY};
    color: {TEAL_DARK};
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}

/* Section headers */
.section-header {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin: 2rem 0 0.5rem;
}}
.section-num {{
    background: {PRIMARY};
    color: {TEAL_DARK};
    font-size: 0.72rem;
    font-weight: 800;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}
.section-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {WHITE};
    letter-spacing: -0.01em;
}}
.section-desc {{
    font-size: 0.84rem;
    color: {WHITE_MUTE};
    margin: 0 0 1rem 2.2rem;
    line-height: 1.55;
}}

/* Metric cards */
.metric-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.2rem;
}}
.metric-card {{
    background: {TEAL_CARD};
    border: 1px solid {TEAL_EDGE};
    border-radius: 10px;
    padding: 1rem 1.3rem;
    position: relative;
    overflow: hidden;
}}
.metric-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: {PRIMARY};
}}
.metric-card .mc-label {{
    font-size: 0.7rem;
    font-weight: 600;
    color: {WHITE_MUTE};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.35rem;
}}
.metric-card .mc-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {WHITE};
    line-height: 1;
}}

/* Alert cards */
.alert {{
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    line-height: 1.55;
    margin: 0.4rem 0 1rem;
    border-left: 4px solid;
    color: {WHITE};
}}
.alert strong {{ font-weight: 700; color: {WHITE}; }}
.alert-info    {{ background: #0D3545; border-color: #5BC4D8; }}
.alert-warning {{ background: #1E3A0E; border-color: {PRIMARY}; }}
.alert-error   {{ background: #3D0F0F; border-color: #FF6B6B; }}
.alert-success {{ background: #0D3320; border-color: {PRIMARY}; }}

/* Expander */
[data-testid="stExpander"] {{
    background: {TEAL_CARD} !important;
    border: 1px solid {TEAL_EDGE} !important;
    border-radius: 10px !important;
    margin-bottom: 0.7rem !important;
}}
[data-testid="stExpander"] * {{
    color: {WHITE} !important;
}}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] details summary {{
    color: {WHITE} !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}}

/* Dataframe */
[data-testid="stDataFrame"] {{
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid {TEAL_EDGE} !important;
}}

/* File uploader */
[data-testid="stFileUploader"] {{
    background: {TEAL_CARD};
    border: 2px dashed {TEAL_EDGE};
    border-radius: 10px;
    padding: 0.5rem;
}}
[data-testid="stFileUploader"] * {{
    color: {WHITE} !important;
}}

/* Progress bar */
.stProgress > div > div > div > div {{
    background: {PRIMARY} !important;
}}
.stProgress > div > div {{
    background: {TEAL_EDGE} !important;
    border-radius: 99px !important;
}}

/* Buttons */
.stButton > button[kind="primary"] {{
    background: {PRIMARY} !important;
    color: {TEAL_DARK} !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.9rem !important;
    transition: opacity 0.15s ease !important;
}}
.stButton > button[kind="primary"]:hover {{
    opacity: 0.85 !important;
}}
.stDownloadButton > button {{
    background: {PRIMARY} !important;
    color: {TEAL_DARK} !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}}

/* Code blocks */
.stCodeBlock, [data-testid="stCode"] {{
    background: #041A16 !important;
    border: 1px solid {TEAL_EDGE} !important;
    border-radius: 6px !important;
}}
code, pre {{
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    color: {PRIMARY} !important;
    background: transparent !important;
}}

hr {{
    border-color: {TEAL_EDGE} !important;
    opacity: 0.5;
}}

p, li, span, label, div {{
    color: {WHITE};
}}
.stMarkdown p, .stMarkdown li {{
    color: {WHITE} !important;
}}
</style>
"""

# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
### ROLE & OBJECTIVE
You are an **Expert Quiz Scoring Evaluator**. Your task is to objectively grade an Agent's response by comparing it against an Authoritative Answer Key and Scoring Guideline.

You must be **meticulous, fair, and consistent**. You do not grade based on grammar or writing style, but solely on the **accuracy of the core solution**.

### INPUT VARIABLES
1. **Question:** {q}
2. **Answer Key (THE TRUTH):** {a}
3. **Scoring Guideline (NUANCE):** {g}
4. **Maximum Score:** {w}
5. **Agent Answer:** {r}

---
### Scoring Rubric & Principles:

1.  Strict Adherence to Answer Key: Your evaluation is confined exclusively to the information within the Answer Key. Do not use any external knowledge or make assumptions about what is implied. If a concept is not in the key, it is not a requirement.
2.  Focus on the Core Concept (The "Inti"): The primary goal is to determine if the agent captured the main solution or the "inti dari penanganan".
    * If the Agent Answer successfully addresses the core concept(s) from the Answer Key, it must receive the maximum score ({w}).
    * Missing minor details, rephrasing the information, or providing a correct but non-detailed summary is acceptable for a full score.
    * If the Agent false classify the answer but the information is correct, it is also acceptable for a full score.
3.  Principle of Generosity: When in doubt, score higher. Do not penalize for differences in phrasing or sentence structure if the agent's meaning aligns with the Answer Key. Avoid being overly strict.
4.  Partial Credit: If the Agent Answer contains some correct information from the Answer Key but misses the core concept or a major required step, assign 6-8 as a score.
5.  Low Credit: If the Agent Answer contains mostly incorrect information from the Answer Key, assign 3-5 as a score.
5.  Score Range: The Score must be a whole number (integer) between 0 and {w}, inclusive.

---

### Evaluation Process:

1.  Analyze: Carefully read the Question, Answer Key, and Agent Answer.
2.  Compare: Compare the key points of the Agent Answer directly against the requirements outlined in the Answer Key.
3.  Score: Based on the Scoring Rubric, assign an integer Score.
4.  Validate: Formulate the Validation text based on the score, following the specific format instructions below.

---

### Required Output Format:

Score: [Assign an integer score from 0 to {w}]
Validation: [Provide your validation text here based on the rules below] in Bahasa Indonesia

* If Score = {w}: The Validation must be exactly "OK".
* If Score < {w}: The Validation must be a brief, constructive explanation of what key information was missing from the Agent Answer when compared to the Answer Key. (e.g., "Kurang informasi mengenai X.", "Langkah penanganan sudah sesuai, namun tidak mengedukasi nasabah tentang Y.")


### 5. FINAL OUTPUT FORMAT (STRICT)
You must output ONLY the following two lines. Do not add markdown, bolding, or headers.

Score: [Integer]
Validation: [Text in Bahasa Indonesia]
"""

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', str(text).lower().strip())

def is_short_answer(text: str) -> bool:
    return len(str(text).strip().split()) <= 2

def extract_pg_option_words(answer_key: str, n_words: int = 5) -> list:
    cleaned = re.sub(r'^[a-zA-Z]\.\s*', '', answer_key.strip())
    return normalize_text(cleaned).split()[:n_words]

def pg_match(answer_key: str, agent_answer: str) -> bool:
    key_norm   = normalize_text(answer_key)
    agent_norm = normalize_text(agent_answer)
    letter_m   = re.match(r'^([a-z])\.', key_norm)
    if letter_m:
        if re.search(rf'\b{letter_m.group(1)}\b', agent_norm):
            return True
    key_words = extract_pg_option_words(answer_key, n_words=5)
    if not key_words:
        return False
    if ' '.join(key_words) in agent_norm:
        return True
    agent_set = set(agent_norm.split())
    return all(w in agent_set for w in key_words)

def detect_cross_agent_copying(responses_df: pd.DataFrame, sot_df: pd.DataFrame) -> list:
    q_cols    = [c for c in responses_df.columns if c.startswith('q')]
    q_types   = {i: str(sot_df.iloc[i].get('Question Type', '')).strip()
                 for i in range(min(len(sot_df), len(q_cols)))}
    non_pg    = [q_cols[i] for i in q_types if q_types[i].upper() != 'PG']
    findings  = []

    for col in non_pg:
        q_idx = int(col.replace('q', '')) - 1
        if q_idx < len(sot_df):
            q_text   = str(sot_df.iloc[q_idx].get('Question', '')).strip()
            q_prev   = q_text[:100] + '...' if len(q_text) > 100 else q_text
            q_type   = str(sot_df.iloc[q_idx].get('Question Type', '')).strip()
        else:
            q_prev, q_type = '', ''

        ans_to_agents: dict = {}
        for _, row in responses_df.iterrows():
            ans = normalize_text(row[col])
            if len(ans.split()) <= 5:
                continue
            ans_to_agents.setdefault(ans, []).append(row.get('email', 'Unknown'))

        for ans, agents in ans_to_agents.items():
            if len(agents) >= 2:
                findings.append({
                    'question_col':     col.upper(),
                    'question_preview': q_prev,
                    'question_type':    q_type,
                    'shared_answer':    ans,
                    'agents':           agents,
                })
    return findings

def evaluate_answer_ai(client: OpenAI, q, a, w, r, g=None) -> str:
    g_text = g.strip() if isinstance(g, str) and g.strip() else "N/A"
    user_prompt = (
        f"Question: {q}\n"
        f"Answer Key: {a}\n"
        f"Scoring Guidelines: {g_text}"
        f"Maximum Score: {w}\n"
        f"Agent Answer: {r}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def parse_ai_response(content: str, max_score: int) -> tuple:
    sm = re.search(r"Score:\s*(\d+)",    content, re.IGNORECASE)
    vm = re.search(r"Validation:\s*(.+)", content, re.IGNORECASE | re.DOTALL)
    if sm and vm:
        try:
            return int(sm.group(1)), vm.group(1).strip()
        except ValueError:
            return 0, "Error parsing integer score."
    return 0, f"PARSING ERROR: {content}"

def run_evaluation(client, sot_df, responses_df, progress_bar, loading_panel_placeholder) -> dict:
    responses_df  = responses_df.fillna("no answer")
    q_cols        = [c for c in responses_df.columns if c.startswith('q')]
    total_steps   = len(q_cols) * len(responses_df)
    step, results = 0, {}

    # Compute how many AI calls there will be (non-PG, non-short-essay questions)
    ai_call_count = 0
    for num in range(len(q_cols)):
        if num >= len(sot_df):
            break
        qtype = str(sot_df.iloc[num].get('Question Type', '')).strip()
        is_pg    = qtype.upper() == 'PG'
        is_essay = 'benar' in qtype.lower() and 'salah' in qtype.lower()
        if not is_pg and not is_essay:
            ai_call_count += len(responses_df)
    ai_calls_done = 0

    for num in range(len(q_cols)):
        col   = q_cols[num]
        if num >= len(sot_df):
            break
        row   = sot_df.iloc[num]
        q     = row.get('Question', '')
        a     = row.get('Answer Key', '')
        w     = row.get('Weightage', 10)
        g     = row.get('Scoring Guidline (For AI)', '')
        qtype = str(row.get('Question Type', '')).strip()

        if pd.isna(q) or str(q).strip() in ('', 'nan'):
            step += len(responses_df)
            progress_bar.progress(min(step / total_steps, 1.0))
            continue

        is_pg    = qtype.upper() == 'PG'
        is_essay = 'benar' in qtype.lower() and 'salah' in qtype.lower()
        scores, validations = [], []

        # ── Update the fancy loading panel ──
        overall_pct = int(100 * step / total_steps) if total_steps else 0
        q_label     = f"Question {num + 1} of {len(q_cols)}"
        type_label  = qtype if qtype else "Unknown"
        method      = "Rule-based (instant)" if (is_pg or is_essay) else f"GPT-4o · {len(responses_df)} agent(s)"
        shimmer_w   = max(4, overall_pct)

        loading_panel_placeholder.markdown(
            f"""
            <div class="loading-panel">
              <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.55rem;">
                <span class="spinner-ring"></span>
                <span style="font-size:0.9rem;font-weight:700;color:{WHITE};">Processing {q_label}</span>
                <span style="margin-left:auto;font-size:0.75rem;color:{WHITE_MUTE};">{overall_pct}% done</span>
              </div>
              <div style="display:flex;gap:2rem;font-size:0.8rem;color:{WHITE_MUTE};margin-bottom:0.2rem;">
                <span>Type&nbsp;<strong style="color:{WHITE};">{type_label}</strong></span>
                <span>Method&nbsp;<strong style="color:{PRIMARY};">{method}</strong></span>
                <span>AI calls&nbsp;<strong style="color:{WHITE};">{ai_calls_done}/{ai_call_count}</strong></span>
              </div>
              <div class="shimmer-bar-wrap">
                <div class="shimmer-bar" style="width:{shimmer_w}%;"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i in range(len(responses_df)):
            r = responses_df[col].iloc[i]
            if is_essay and is_short_answer(str(r)):
                scores.append(0)
                validations.append("Jawaban terlalu singkat (kurang dari 3 kata), tidak dapat dievaluasi.")
            elif is_pg:
                if pg_match(str(a), str(r)):
                    scores.append(int(w)); validations.append("OK")
                else:
                    scores.append(0); validations.append("Jawaban tidak sesuai dengan pilihan yang benar.")
            else:
                for retry in range(3):
                    try:
                        content = evaluate_answer_ai(client, q, a, w, r, g); break
                    except Exception as e:
                        if "429" in str(e) or "rate limit" in str(e).lower():
                            time.sleep(3 + retry)
                        else:
                            raise
                else:
                    content = "Score: 0\nValidation: Rate limit error."
                sv, vv = parse_ai_response(content, int(w))
                scores.append(sv); validations.append(vv)
                ai_calls_done += 1
                time.sleep(3.5)

            step += 1
            progress_bar.progress(min(step / total_steps, 1.0))

        results[num + 1] = pd.DataFrame({
            'timestamp':        responses_df['timestamp'],
            'email':            responses_df['email'],
            col:                responses_df[col],
            f'Score_{col}':     scores,
            f'Validation_{col}': validations,
        })
    return results

def build_excel(results: dict, cross_agent_findings: list) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for q_num, df in results.items():
            df.to_excel(writer, sheet_name=f'Q{q_num}', index=False)

        if results:
            base = None
            for df in results.values():
                if base is None:
                    base = df[['timestamp', 'email']].drop_duplicates('email').copy()
            parts = [base.set_index('email')]
            for q_num, df in results.items():
                sc = [c for c in df.columns if c.startswith('Score_')][0]
                parts.append(df[['email', sc]].rename(columns={sc: f'Q{q_num}_Score'}).set_index('email'))
            summary = pd.concat(parts, axis=1).reset_index()
            sc_cols = [c for c in summary.columns if c.endswith('_Score')]
            summary['Total Score'] = summary[sc_cols].sum(axis=1)
            flagged = {a for f in cross_agent_findings for a in f['agents']}
            summary['Integrity Flag'] = summary['email'].apply(
                lambda e: 'FLAGGED - Potential Copying' if e in flagged else 'OK'
            )
            summary.to_excel(writer, sheet_name='Summary', index=False)

            if cross_agent_findings:
                rows = []
                for f in cross_agent_findings:
                    for agent in f['agents']:
                        rows.append({
                            'Question Column':  f['question_col'],
                            'Question Type':    f['question_type'],
                            'Question Preview': f['question_preview'],
                            'Agent Email':      agent,
                            'Shared Answer':    f['shared_answer'],
                        })
                pd.DataFrame(rows).to_excel(writer, sheet_name='Integrity Report', index=False)
    return output.getvalue()

# ─────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────

def section(num: str, title: str, desc: str = ""):
    st.markdown(
        f'<div class="section-header">'
        f'<div class="section-num">{num}</div>'
        f'<div class="section-title">{title}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if desc:
        st.markdown(f'<p class="section-desc">{desc}</p>', unsafe_allow_html=True)

def alert(kind: str, msg: str):
    st.markdown(f'<div class="alert alert-{kind}">{msg}</div>', unsafe_allow_html=True)

def metrics_row(values: list):
    cols_html = ""
    for label, value in values:
        cols_html += (
            f'<div class="metric-card">'
            f'<div class="mc-label">{label}</div>'
            f'<div class="mc-value">{value}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="metric-row">{cols_html}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    st.markdown(CSS, unsafe_allow_html=True)

    # ── Top bar ──
    st.markdown(
        f'<div class="sb-topbar">'
        f'<img src="data:image/webp;base64,{LOGO_B64}" style="height:28px;">'
        f'<div class="sb-topbar-title">AI Agent for grading quiz</div>'
        f'<div class="sb-topbar-badge">Customer &amp; Experience Team - Trainer</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Sidebar  ──
    with st.sidebar:
        st.markdown(
            f'<div class="sidebar-logo">'
            f'<img src="data:image/webp;base64,{LOGO_B64}" style="height:22px; filter:brightness(0) invert(1);">'
            f'</div>',
            unsafe_allow_html=True,
        )
        
        # ADDED DYNAMIC API KEY INPUT HERE
        st.markdown("### Configuration")
        api_key_input = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        
        if api_key_input:
            st.markdown(
                f'<div class="alert alert-success" style="font-size:0.8rem;margin-top:0;">'
                f'🔑 API key configured</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="alert alert-warning" style="font-size:0.8rem;margin-top:0;">'
                f'⚠️ Please enter your API key</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### File Format")
        st.markdown(
            '<p style="font-size:0.8rem;color:#B8D4CC;line-height:1.6;">'
            'Upload an <code>.xlsx</code> file with two sheets:<br>'
            '<strong style="color:#E5E7EB;">SOT</strong> — Questions, Answer Keys, Weightage, Question Type<br>'
            '<strong style="color:#E5E7EB;">Responses</strong> — timestamp, email, q1, q2, ...'
            '</p>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("### Scoring Rules")
        rules = [
            ("PG", "Matched by option letter or first-5-word comparison (normalized + jumble)"),
            ("Benar-Salah Essay", "Answers of 2 words or fewer receive a score of 0 automatically"),
            ("All other types", "Evaluated by GPT-4o against the Answer Key and Scoring Guidelines"),
            ("Integrity check", "Cross-agent identical answers for the same question are flagged"),
        ]
        for rtype, rdesc in rules:
            st.markdown(
                f'<p style="font-size:0.78rem;color:#B8D4CC;margin:0.4rem 0;line-height:1.5;">'
                f'<span style="color:#AADC00;font-weight:600;">{rtype}</span><br>{rdesc}</p>',
                unsafe_allow_html=True,
            )

    # ── Step 1: Upload ──
    section("1", "Upload Response File",
            "Upload the monthly XLSX file containing the SOT and Responses sheets.")

    uploaded_file = st.file_uploader(
        "Drop your file here or click to browse",
        type=["xlsx"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        alert("info", "No file uploaded yet. Please select the monthly response file to get started.")
        return

    # ── Load data ──
    try:
        sot_df_raw = pd.read_excel(uploaded_file, sheet_name="SOT")
        uploaded_file.seek(0)
        responses_df = pd.read_excel(uploaded_file, sheet_name="Responses")
    except Exception as e:
        alert("error", f'Could not read the file. Ensure it has both "SOT" and "Responses" sheets.<br><code>{e}</code>')
        return

    sot_df = sot_df_raw[
        sot_df_raw['Question'].notna() &
        (sot_df_raw['Question'].astype(str).str.strip() != '') &
        (sot_df_raw['Question'].astype(str).str.lower() != 'nan')
    ].copy().reset_index(drop=True)

    q_cols = [c for c in responses_df.columns if c.startswith('q')]

    # ── Step 2: Review ──
    section("2", "Review Loaded Data")
    metrics_row([
        ("Questions in SOT", len(sot_df)),
        ("Agent Responses",  len(responses_df)),
        ("Response Columns", len(q_cols)),
    ])

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("SOT — Question Overview", expanded=False):
            st.dataframe(
                sot_df[['No', 'Question Type', 'Question', 'Answer Key', 'Weightage']],
                use_container_width=True, height=260,
            )
    with c2:
        with st.expander("Responses — First 5 Rows", expanded=False):
            st.dataframe(responses_df.head(), use_container_width=True, height=260)

    # ── Step 3: Integrity Check ──
    section("3", "Integrity Check",
            "Detects agents who submitted word-for-word identical answers for the same question. "
            "Only non-PG questions are checked. Answers of 5 words or fewer are excluded.")

    cross_agent_findings = detect_cross_agent_copying(responses_df, sot_df)
    flagged_emails = {a for f in cross_agent_findings for a in f['agents']}

    if cross_agent_findings:
        alert("warning",
              f'<strong>{len(cross_agent_findings)} case(s)</strong> of potential cross-agent copying detected '
              f'across <strong>{len(flagged_emails)} agent(s)</strong>. Review the details below.')

        for finding in cross_agent_findings:
            with st.expander(
                f"{finding['question_col']}  —  {len(finding['agents'])} agents with an identical answer",
                expanded=True,
            ):
                left, right = st.columns([1, 2], gap="large")
                with left:
                    st.markdown(
                        f'<p style="font-size:0.8rem;color:#FFFFFF;font-weight:500;margin-bottom:0.2rem;">Question Column</p>'
                        f'<p style="font-weight:700;font-family:\'DM Mono\',monospace;margin-bottom:0.8rem;">{finding["question_col"]}</p>'
                        f'<p style="font-size:0.8rem;color:#FFFFFF;font-weight:500;margin-bottom:0.2rem;">Question Type</p>'
                        f'<p style="font-weight:600;margin-bottom:0.8rem;">{finding["question_type"]}</p>'
                        f'<p style="font-size:0.8rem;color:#FFFFFF;font-weight:500;margin-bottom:0.2rem;">Question Preview</p>'
                        f'<p style="font-size:0.85rem;margin-bottom:0.8rem;">{finding["question_preview"]}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<p style="font-size:0.8rem;color:#FFFFFF;font-weight:500;margin-bottom:0.3rem;">Agents who submitted this exact answer</p>', unsafe_allow_html=True)
                    agent_df = pd.DataFrame({'Agent Email': finding['agents']})
                    agent_df.index = agent_df.index + 1
                    st.dataframe(agent_df, use_container_width=True)
                with right:
                    st.markdown(f'<p style="font-size:0.8rem;color:#FFFFFF;font-weight:500;margin-bottom:0.4rem;">Shared answer — word-for-word identical across all flagged agents</p>', unsafe_allow_html=True)
                    st.code(finding['shared_answer'], language=None)
    else:
        alert("success", "No cross-agent copying detected. Every agent submitted a unique answer for each question.")

    # ── Step 4: Run Evaluation ──
    section("4", "Run Evaluation",
            "Scores all agent responses using the rules above. PG and short-essay questions are scored "
            "instantly. All other question types are sent to GPT-4o.")

    if st.button("Start Evaluation", type="primary", use_container_width=True):
        
        # ADDED SAFEGUARD HERE
        if not api_key_input:
            alert("error", "⚠️ Please enter your OpenAI API key in the sidebar configuration before starting the evaluation.")
            return

        client = OpenAI(api_key=api_key_input)
        st.markdown("---")

        # Native Streamlit progress bar (thin, stays at top)
        progress_bar = st.progress(0.0, text="")

        # Fancy animated loading panel placeholder
        loading_panel_placeholder = st.empty()

        start = time.time()
        try:
            results = run_evaluation(client, sot_df, responses_df, progress_bar, loading_panel_placeholder)
        except Exception as e:
            loading_panel_placeholder.empty()
            alert("error", f'An error occurred during evaluation: <code>{e}</code>')
            return

        elapsed = time.time() - start

        # Replace loading panel with a done message
        loading_panel_placeholder.markdown(
            f"""
            <div class="loading-panel" style="border-color:{PRIMARY};">
              <div style="display:flex;align-items:center;gap:0.6rem;">
                <span style="font-size:1.2rem;">✅</span>
                <span style="font-size:0.95rem;font-weight:700;color:{PRIMARY};">
                  Evaluation complete — {elapsed:.0f}s
                </span>
                <span class="pulse-dots" style="margin-left:auto;">
                  <span></span><span></span><span></span>
                </span>
              </div>
              <div style="font-size:0.8rem;color:{WHITE_MUTE};margin-top:0.4rem;">
                All {len(q_cols)} question(s) processed across {len(responses_df)} agent response(s).
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        progress_bar.progress(1.0, text="")

        # ── Results Summary ──
        section("5", "Results Summary")

        base = responses_df[['email']].drop_duplicates().copy()
        parts = [base.set_index('email')]
        for q_num, df in results.items():
            sc = [c for c in df.columns if c.startswith('Score_')][0]
            parts.append(df[['email', sc]].rename(columns={sc: f'Q{q_num}'}).set_index('email'))
        summary_df = pd.concat(parts, axis=1).reset_index()
        q_sc_cols  = [c for c in summary_df.columns if re.match(r'^Q\d+$', c)]
        summary_df['Total'] = summary_df[q_sc_cols].sum(axis=1)
        summary_df['Integrity'] = summary_df['email'].apply(
            lambda e: 'Flagged' if e in flagged_emails else 'OK'
        )

        metrics_row([
            ("Agents Evaluated",    len(summary_df)),
            ("Avg Total Score",     f"{summary_df['Total'].mean():.1f}"),
            ("Flagged for Copying", len(flagged_emails)),
        ])

        st.dataframe(summary_df, use_container_width=True, height=420)

        # ── Download ──
        section("6", "Download Report")
        excel_bytes = build_excel(results, cross_agent_findings)
        st.download_button(
            label="Download Full Evaluation Report (.xlsx)",
            data=excel_bytes,
            file_name="evaluation_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        alert("success",
              "Report includes one sheet per question (Q1, Q2, ...), a Summary sheet, "
              "and an Integrity Report sheet if any copying was detected.")


if __name__ == "__main__":
    main()
