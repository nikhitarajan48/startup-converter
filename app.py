import streamlit as st
from groq import Groq

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Problem → Startup Converter",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Groq API Key ───────────────────────────────────────────────────────
GROQ_API_KEY = "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"  # ← Paste your gsk_... key here

# ── Custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #f0f0f8;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111118 !important;
    border-right: 1px solid #2a2a38;
}
[data-testid="stSidebar"] * { color: #f0f0f8 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
}

/* Text areas and inputs */
textarea, input[type="text"] {
    background-color: #18181f !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 10px !important;
    color: #f0f0f8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Select boxes */
[data-testid="stSelectbox"] > div > div {
    background-color: #18181f !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 10px !important;
    color: #f0f0f8 !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #7c3aed, #06b6d4) !important;
    border-radius: 4px !important;
}

/* Output box */
.output-box {
    background: #13131e;
    border: 1px solid #2a2a38;
    border-radius: 14px;
    padding: 24px 28px;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    line-height: 1.8;
    color: #d0d0e8;
    margin: 12px 0;
}
.output-box h3 {
    color: #06b6d4;
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    margin: 18px 0 8px 0;
    border-bottom: 1px solid #2a2a38;
    padding-bottom: 6px;
}
.output-box ul { padding-left: 20px; }
.output-box li { margin-bottom: 6px; color: #c0c0d8; }
.output-box p { margin-bottom: 10px; }

/* Step card */
.step-card {
    background: #111118;
    border: 1px solid #2a2a38;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
}

/* Step header */
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #06b6d4;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #f0f0f8;
    margin-bottom: 6px;
}
.step-desc {
    color: #6b6b90;
    font-size: 13px;
    margin-bottom: 20px;
}

/* Chip row */
.chip-selected {
    background: #7c3aed !important;
    color: white !important;
    border: 1px solid #7c3aed !important;
}

/* Info box */
.info-box {
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    color: #a78bfa;
    margin: 10px 0;
}

/* Success box */
.success-box {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    color: #34d399;
    margin: 10px 0;
}

/* Lean rule box */
.lean-box {
    background: rgba(6,182,212,0.08);
    border-left: 3px solid #06b6d4;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    font-size: 12px;
    color: #67e8f9;
    margin: 8px 0 16px 0;
    font-family: 'DM Mono', monospace;
}

/* Section label */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #6b6b90;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* Divider */
hr { border-color: #2a2a38 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────
def init_state():
    defaults = {
        "step": 1,
        "problem": "", "target_users": "", "industry": "",
        "frequency": "", "severity": "",
        "step2": "", "step3": "", "step4": "", "step5": "", "step6": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Groq API call ──────────────────────────────────────────────────────
def call_groq(prompt, system):
    client = Groq(api_key=GROQ_API_KEY)
    msg = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1500,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return msg.choices[0].message.content

# ── Markdown to HTML renderer ──────────────────────────────────────────
def render_output(text):
    lines = text.split("\n")
    html = '<div class="output-box">'
    in_ul = False
    for line in lines:
        s = line.strip()
        if not s:
            if in_ul:
                html += "</ul>"
                in_ul = False
            html += "<br>"
            continue
        if s.startswith("###") or (s.startswith("**") and s.endswith("**")):
            if in_ul: html += "</ul>"; in_ul = False
            clean = s.lstrip("#").strip().strip("*").strip()
            html += f"<h3>{clean}</h3>"
        elif s[0].isdigit() and len(s) > 2 and s[1] in ".)":
            if in_ul: html += "</ul>"; in_ul = False
            clean = s[2:].strip().replace("**", "")
            html += f"<h3>{s[0]}. {clean}</h3>"
        elif s.startswith("- ") or s.startswith("• "):
            if not in_ul:
                html += "<ul>"; in_ul = True
            clean = s.lstrip("-•").strip().replace("**", "")
            html += f"<li>{clean}</li>"
        else:
            if in_ul: html += "</ul>"; in_ul = False
            clean = s.replace("**", "")
            html += f"<p>{clean}</p>"
    if in_ul:
        html += "</ul>"
    html += "</div>"
    return html

# ── Lean rules per step ────────────────────────────────────────────────
LEAN_RULES = {
    1: "📌 Lean Rule: Start with the problem, not the solution. Validate pain before building anything.",
    2: "📌 Lean Rule: Identify your riskiest assumptions early. Focus on what could kill the idea.",
    3: "📌 Lean Rule: Build a solution only after confirming problem-solution fit with real users.",
    4: "📌 Lean Rule: MVP = minimum to learn, not minimum to launch. Remove every non-essential feature.",
    5: "📌 Lean Rule: Build → Measure → Learn. Run the cheapest experiment that tests your assumption.",
    6: "📌 Lean Rule: Don't optimize revenue before validating. Charge early to test real willingness to pay.",
}

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Problem → Startup")
    st.markdown("<small style='color:#6b6b90'>Lean Startup Converter</small>", unsafe_allow_html=True)
    st.markdown("---")

    steps = [
        ("🔍", "Problem Input"),
        ("🧠", "Problem Analysis"),
        ("💡", "Startup Idea"),
        ("🛠️", "MVP Planning"),
        ("🧪", "Validation"),
        ("💰", "Revenue Model"),
    ]

    for i, (icon, label) in enumerate(steps):
        step_num = i + 1
        current = st.session_state.step
        if step_num < current:
            st.markdown(f"<div style='padding:8px 12px;color:#10b981;font-size:13px'>✅ {icon} {label}</div>", unsafe_allow_html=True)
        elif step_num == current:
            st.markdown(f"<div style='padding:8px 12px;background:#1a1a28;border-radius:8px;color:#f0f0f8;font-size:13px;border-left:3px solid #7c3aed'><b>{icon} {label}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='padding:8px 12px;color:#6b6b90;font-size:13px'>{icon} {label}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Export button in sidebar
    if st.session_state.step > 2 and any(st.session_state.get(f"step{i}") for i in range(2, 7)):
        from datetime import datetime
        report = f"""PROBLEM → STARTUP CONVERTER — LEAN STARTUP BRIEF
Generated: {datetime.now().strftime('%B %d, %Y')}

━━━━ PROBLEM INPUT ━━━━━━━━━━━━━━━━━━━━━━━━━━
Problem:      {st.session_state.problem}
Target Users: {st.session_state.target_users}
Industry:     {st.session_state.industry}
Frequency:    {st.session_state.frequency}
Severity:     {st.session_state.severity}

━━━━ PROBLEM ANALYSIS ━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.step2}

━━━━ STARTUP IDEA ━━━━━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.step3}

━━━━ MVP PLAN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.step4}

━━━━ VALIDATION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.step5}

━━━━ REVENUE MODEL ━━━━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.step6}
""".strip()
        st.download_button("📄 Export Report", data=report,
                           file_name="startup-plan.txt", mime="text/plain",
                           use_container_width=True)

    if st.button("↺ Start Over", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown("<br><small style='color:#6b6b90'>v1.0 · Groq + Llama 3.3</small>", unsafe_allow_html=True)

# ── Progress bar ───────────────────────────────────────────────────────
st.progress(st.session_state.step / 6)

# ══════════════════════════════════════════════════════════════════════
# STEP 1 — Problem Input
# ══════════════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<div class="step-num">STEP 01 / 06</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">🔍 Describe Your Problem</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-desc">Enter the real-world problem you\'ve observed. Be specific and concrete.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lean-box">{LEAN_RULES[1]}</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-label">Problem Description</div>', unsafe_allow_html=True)
        problem = st.text_area("", value=st.session_state.problem,
                               placeholder="e.g. Small restaurant owners spend 3-4 hours weekly updating menus across Zomato, Swiggy, and their website manually...",
                               height=130, label_visibility="collapsed", key="prob_input")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-label">Target Users</div>', unsafe_allow_html=True)
            target_users = st.text_input("", value=st.session_state.target_users,
                                         placeholder="e.g. Small restaurant owners in India",
                                         label_visibility="collapsed", key="users_input")
        with col2:
            st.markdown('<div class="section-label">Industry</div>', unsafe_allow_html=True)
            industries = ["Select...", "Food & Restaurant", "Education & EdTech", "Healthcare",
                         "Retail & E-commerce", "Finance & Fintech", "Logistics",
                         "Real Estate", "Agriculture", "Travel & Tourism",
                         "HR & Recruitment", "Marketing", "Legal", "Other"]
            idx = industries.index(st.session_state.industry) if st.session_state.industry in industries else 0
            industry = st.selectbox("", industries, index=idx,
                                    label_visibility="collapsed", key="ind_input")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="section-label">How Often Does This Occur?</div>', unsafe_allow_html=True)
            frequency = st.radio("", ["Daily", "Weekly", "Monthly", "Occasionally", "Constantly"],
                                 index=["Daily","Weekly","Monthly","Occasionally","Constantly"].index(st.session_state.frequency)
                                 if st.session_state.frequency else 0,
                                 horizontal=True, label_visibility="collapsed", key="freq_input")
        with col4:
            st.markdown('<div class="section-label">Problem Severity</div>', unsafe_allow_html=True)
            severity = st.radio("", ["😤 Minor", "😠 Significant", "🔥 Critical", "💸 Costly"],
                                index=["😤 Minor","😠 Significant","🔥 Critical","💸 Costly"].index(st.session_state.severity)
                                if st.session_state.severity else 0,
                                horizontal=True, label_visibility="collapsed", key="sev_input")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Analyze Problem →", key="step1_next"):
            if len(problem.strip()) < 20:
                st.error("⚠️ Please describe the problem in more detail (at least 20 characters).")
            elif not target_users.strip():
                st.error("⚠️ Please enter your target users.")
            else:
                st.session_state.problem = problem
                st.session_state.target_users = target_users
                st.session_state.industry = industry
                st.session_state.frequency = frequency
                st.session_state.severity = severity
                st.session_state.step2 = ""  # reset if re-doing
                st.session_state.step = 2
                st.rerun()

# ══════════════════════════════════════════════════════════════════════
# STEP 2 — Problem Analysis
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="step-num">STEP 02 / 06</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">🧠 Problem Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-desc">AI-powered pain point analysis using Lean Startup methodology.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lean-box">{LEAN_RULES[2]}</div>', unsafe_allow_html=True)

    if not st.session_state.step2:
        with st.spinner("🤖 Analyzing pain points with AI..."):
            try:
                prompt = f"""Analyze this startup problem using Lean Startup principles:
Problem: {st.session_state.problem}
Target Users: {st.session_state.target_users}
Industry: {st.session_state.industry}
Frequency: {st.session_state.frequency}
Severity: {st.session_state.severity}

Provide:
1. **Core Pain Points** (3-4 specific pain points)
2. **Who is Most Affected** (primary customer persona)
3. **Current Alternatives & Why They Fail** (2-3 gaps)
4. **Problem-Market Fit Signal** (evidence this is worth solving)
5. **Key Assumptions to Test** (3 riskiest assumptions)"""
                result = call_groq(prompt, "You are a seasoned Lean Startup coach. Give structured, specific insights.")
                st.session_state.step2 = result
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    st.markdown(render_output(st.session_state.step2), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", key="s2_back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Generate Startup Idea →", key="s2_next"):
            st.session_state.step = 3
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# STEP 3 — Startup Idea
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.markdown('<div class="step-num">STEP 03 / 06</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">💡 Startup Idea & Value Proposition</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-desc">Solution concept and unique value proposition for your startup.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lean-box">{LEAN_RULES[3]}</div>', unsafe_allow_html=True)

    if not st.session_state.step3:
        with st.spinner("🤖 Generating startup idea..."):
            try:
                prompt = f"""Based on this problem, generate a compelling startup idea:
Problem: {st.session_state.problem}
Target Users: {st.session_state.target_users}
Industry: {st.session_state.industry}
Analysis: {st.session_state.step2}

Generate:
1. **Startup Name** (2-3 catchy names with rationale)
2. **One-Line Pitch** (under 20 words)
3. **Core Solution Statement** (2-3 sentences)
4. **Unique Value Proposition** (what makes this 10x better?)
5. **Customer Segment** (detailed early adopter profile)
6. **Key Differentiators** (3-4 things that set this apart)
7. **Unfair Advantage** (what can't others easily copy?)"""
                result = call_groq(prompt, "You are a startup idea specialist trained in Lean Startup and value proposition design.")
                st.session_state.step3 = result
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    st.markdown(render_output(st.session_state.step3), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", key="s3_back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Define MVP →", key="s3_next"):
            st.session_state.step = 4
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# STEP 4 — MVP Planning
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.markdown('<div class="step-num">STEP 04 / 06</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">🛠️ MVP Planning</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-desc">Minimum Viable Product features prioritized by impact vs effort.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lean-box">{LEAN_RULES[4]}</div>', unsafe_allow_html=True)

    if not st.session_state.step4:
        with st.spinner("🤖 Planning MVP features..."):
            try:
                prompt = f"""Create an MVP plan:
Problem: {st.session_state.problem}
Startup Idea: {st.session_state.step3}

1. **MVP Goal** (single sentence hypothesis)
2. **Must-Have Features** (3-5 absolute minimum features)
3. **Nice-to-Have Features** (3-4 for version 2)
4. **Explicitly Excluded** (2-3 things NOT to build)
5. **MVP Build Approach** (tech stack or no-code tools)
6. **Time to MVP** (estimate with rationale)
7. **Success Criteria** (3 measurable metrics)"""
                result = call_groq(prompt, "You are an expert in Lean MVP design. Prioritize speed and learning.")
                st.session_state.step4 = result
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    st.markdown(render_output(st.session_state.step4), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", key="s4_back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Plan Validation →", key="s4_next"):
            st.session_state.step = 5
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# STEP 5 — Validation
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    st.markdown('<div class="step-num">STEP 05 / 06</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">🧪 Validation Experiments</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-desc">Lean experiments to test your assumptions before building.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lean-box">{LEAN_RULES[5]}</div>', unsafe_allow_html=True)

    if not st.session_state.step5:
        with st.spinner("🤖 Designing validation experiments..."):
            try:
                prompt = f"""Design Lean Startup validation experiments:
Problem: {st.session_state.problem}
Target Users: {st.session_state.target_users}
Startup Idea: {st.session_state.step3}
MVP: {st.session_state.step4}

1. **Riskiest Assumption** (#1 thing that if wrong kills this)
2. **Customer Discovery Experiment** (talk to 10-20 customers)
3. **Problem Validation Test** (smoke test or concierge)
4. **Solution Validation Test** (test before building)
5. **Key Metrics** (OMTM + 2 supporting metrics)
6. **Go / No-Go Criteria** (specific thresholds)
7. **4-Week Sprint Plan** (week-by-week schedule)"""
                result = call_groq(prompt, "You are a Lean Startup validation expert. Focus on fast, cheap, specific experiments.")
                st.session_state.step5 = result
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    st.markdown(render_output(st.session_state.step5), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", key="s5_back"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Build Revenue Model →", key="s5_next"):
            st.session_state.step = 6
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# STEP 6 — Revenue Model
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    st.markdown('<div class="step-num">STEP 06 / 06</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">💰 Business Model & Revenue</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-desc">Revenue streams and basic business model canvas.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lean-box">{LEAN_RULES[6]}</div>', unsafe_allow_html=True)

    if not st.session_state.step6:
        with st.spinner("🤖 Building revenue model..."):
            try:
                prompt = f"""Suggest a business model and revenue strategy:
Industry: {st.session_state.industry}
Startup Idea: {st.session_state.step3}
Target Users: {st.session_state.target_users}
MVP: {st.session_state.step4}

1. **Recommended Revenue Model** (primary monetization)
2. **Alternative Revenue Streams** (2-3 secondary options)
3. **Pricing Strategy** (specific price points with rationale)
4. **Customer Acquisition** (top 3 channels for first 100 customers)
5. **Unit Economics** (rough CAC, LTV, payback period)
6. **Key Partners** (2-3 strategic partners)
7. **Lean Canvas Summary** (9-block canvas in bullet form)"""
                result = call_groq(prompt, "You are a startup business model expert. Give practical advice for early-stage startups.")
                st.session_state.step6 = result
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

    st.markdown(render_output(st.session_state.step6), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;padding:30px'>
        <div style='font-size:48px'>🎉</div>
        <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#f0f0f8;margin:12px 0 6px'>
            Your Startup Plan is Complete!
        </div>
        <div style='color:#6b6b90;font-size:13px'>
            Download your full report from the sidebar →
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", key="s6_back"):
            st.session_state.step = 5
            st.rerun()
