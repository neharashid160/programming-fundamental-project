"""
CapGenius - AI-Powered Instagram Caption Generator
Professional Streamlit UI with working Groq API integration.
"""

import streamlit as st
from caption_engine import (
    generate_caption, suggest_hashtags, get_caption_score,
    save_to_history, load_history, clear_history, test_api_key
)

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="CapGenius",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- Google Fonts ---------- */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ---------- Root tokens ---------- */
:root {
    --bg:        #0d0d12;
    --surface:   #16161f;
    --border:    #2a2a3a;
    --accent:    #c084fc;
    --accent2:   #818cf8;
    --gold:      #fbbf24;
    --text:      #e8e6f0;
    --muted:     #6b6880;
    --success:   #34d399;
    --error:     #f87171;
    --radius:    14px;
}

/* ---------- Global reset ---------- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
.stApp { background: var(--bg); }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem; max-width: 1200px; margin: auto; }

/* ---------- Hero header ---------- */
.hero {
    background: linear-gradient(135deg, #1a0a2e 0%, #16161f 60%, #0d1929 100%);
    border-bottom: 1px solid var(--border);
    padding: 3rem 2rem 2.5rem;
    margin: 0 -2rem 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 60% at 50% -10%, rgba(192,132,252,.18) 0%, transparent 70%);
}
.hero-badge {
    display: inline-block;
    background: rgba(192,132,252,.12);
    border: 1px solid rgba(192,132,252,.3);
    color: var(--accent);
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    padding: .3rem .9rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 400;
    line-height: 1.1;
    margin: 0 0 .75rem;
    background: linear-gradient(135deg, #e8e6f0 30%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    margin: 0;
    letter-spacing: .01em;
}

/* ---------- Section label ---------- */
.section-label {
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .6rem;
}

/* ---------- Cards ---------- */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color .2s;
}
.card:hover { border-color: rgba(192,132,252,.35); }

/* ---------- Caption cards ---------- */
.caption-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
}
.caption-num {
    font-size: .65rem;
    font-weight: 700;
    letter-spacing: .16em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: .5rem;
}
.caption-text {
    font-size: 1rem;
    line-height: 1.65;
    color: var(--text);
    margin-bottom: .8rem;
}
.score-pill {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    background: rgba(251,191,36,.08);
    border: 1px solid rgba(251,191,36,.25);
    color: var(--gold);
    font-size: .75rem;
    font-weight: 600;
    padding: .25rem .7rem;
    border-radius: 999px;
}

/* ---------- Hashtag chips ---------- */
.hashtag-wrap { display: flex; flex-wrap: wrap; gap: .4rem; }
.hashtag-chip {
    background: rgba(129,140,248,.1);
    border: 1px solid rgba(129,140,248,.25);
    color: var(--accent2);
    font-size: .78rem;
    font-weight: 500;
    padding: .25rem .6rem;
    border-radius: 999px;
}

/* ---------- Tips ---------- */
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: .6rem;
    padding: .55rem 0;
    border-bottom: 1px solid rgba(255,255,255,.04);
    font-size: .9rem;
    color: #b8b4cc;
}
.tip-item:last-child { border-bottom: none; }
.tip-dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    margin-top: .45rem;
    flex-shrink: 0;
}

/* ---------- Stat chips ---------- */
.stat-row { display: flex; gap: .8rem; margin-bottom: 1.5rem; }
.stat-chip {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .7rem 1rem;
    text-align: center;
}
.stat-val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: var(--accent);
    line-height: 1;
}
.stat-lbl { font-size: .68rem; color: var(--muted); margin-top: .2rem; letter-spacing: .05em; }

/* ---------- Streamlit widget overrides ---------- */
.stTextArea textarea {
    background: #1c1c28 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(192,132,252,.12) !important;
}
.stTextInput input {
    background: #1c1c28 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: .9rem !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(192,132,252,.12) !important;
}
.stSelectbox > div > div {
    background: #1c1c28 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSlider .stSlider { color: var(--accent) !important; }

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #9333ea, #7c3aed) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 600 !important;
    letter-spacing: .02em !important;
    padding: .7rem 1.5rem !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-size: .82rem !important;
    font-weight: 500 !important;
    transition: border-color .2s, color .2s !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* Alerts */
.stAlert {
    border-radius: 10px !important;
    font-size: .88rem !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-size: .88rem !important;
    color: var(--text) !important;
}

/* Divider */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────────────────────────
def init_state():
    defaults = dict(
        captions=[], hashtags=[], scores=[],
        total_generated=0, session_count=0,
        api_key="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", api_verified=False,
        active_tab="generate",
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ AI Caption Generator</div>
  <h1>CapGenius</h1>
  <p>Craft engaging Instagram captions in seconds.
</div>
""", unsafe_allow_html=True)

# ── Tab navigation ───────────────────────────────────────────────────────────
tab_gen, tab_hist = st.tabs(["✨  Generate", "📋  History"])

# ════════════════════════════════════════════════════════
# TAB 1 — GENERATE
# ════════════════════════════════════════════════════════
with tab_gen:

    # ── Stats row ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-chip">
        <div class="stat-val">{st.session_state.total_generated}</div>
        <div class="stat-lbl">Captions Generated</div>
      </div>
      <div class="stat-chip">
        <div class="stat-val">{st.session_state.session_count}</div>
        <div class="stat-lbl">Batches This Session</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two-column layout ───────────────────────────────────────────────────
    left, right = st.columns([5, 4], gap="large")

    with left:
        # API Key
        st.markdown('<div class="section-label">Groq API Key</div>', unsafe_allow_html=True)
        api_input = st.text_input(
            "api_key_field",
            value=st.session_state.api_key,
            type="password",
            placeholder="gsk_...",
            label_visibility="collapsed",
        )
        if api_input != st.session_state.api_key:
            st.session_state.api_key = api_input
            st.session_state.api_verified = False

        vcol1, vcol2 = st.columns([1, 3])
        with vcol1:
            if st.button("Verify Key", type="secondary", use_container_width=True):
                if not st.session_state.api_key.strip():
                    st.error("Enter an API key first.")
                else:
                    with st.spinner("Checking…"):
                        ok, msg = test_api_key(st.session_state.api_key)
                    if ok:
                        st.session_state.api_verified = True
                        st.success("✅ " + msg)
                    else:
                        st.session_state.api_verified = False
                        st.error("❌ " + msg)
        with vcol2:
            if st.session_state.api_verified:
                st.success("Key verified ✓")
            else:
                st.caption("Get a free key at [console.groq.com](https://console.groq.com)")

        st.markdown("<br>", unsafe_allow_html=True)

        # Description
        st.markdown('<div class="section-label">Post Description</div>', unsafe_allow_html=True)
        keywords = st.text_area(
            "desc",
            placeholder="e.g., Golden hour beach shots with friends, summer vibes, sunset silhouettes…",
            height=140,
            label_visibility="collapsed",
        )

        # Controls row
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown('<div class="section-label">Tone</div>', unsafe_allow_html=True)
            tone_opt = st.selectbox(
                "tone",
                ["😄 Casual", "💼 Professional", "😂 Humorous", "🌟 Inspirational", "🔥 Bold"],
                label_visibility="collapsed",
            )
        with cc2:
            st.markdown('<div class="section-label">Variations</div>', unsafe_allow_html=True)
            num_variations = st.slider("vars", 1, 5, 3, label_visibility="collapsed")

        tone_map = {
            "😄 Casual": "Casual", "💼 Professional": "Professional",
            "😂 Humorous": "Humorous", "🌟 Inspirational": "Inspirational", "🔥 Bold": "Bold"
        }
        api_tone = tone_map.get(tone_opt, "Casual")

        st.markdown("<br>", unsafe_allow_html=True)

        # Generate button
        gen_clicked = st.button("✨  Generate Captions", type="primary", use_container_width=True)

        if gen_clicked:
            if not st.session_state.api_key.strip():
                st.error("⚠️ Enter and verify your Groq API key above.")
            elif not keywords.strip():
                st.error("⚠️ Please describe your post first.")
            else:
                try:
                    with st.spinner("Crafting your captions…"):
                        captions = generate_caption(keywords, api_tone, num_variations, st.session_state.api_key)
                        hashtags = suggest_hashtags(keywords, api_tone, st.session_state.api_key)
                        scores = []
                        for cap in captions:
                            try:
                                s, r = get_caption_score(cap, st.session_state.api_key)
                                scores.append((s, r))
                            except Exception:
                                scores.append((7, "Score unavailable"))

                    st.session_state.captions = captions
                    st.session_state.hashtags = hashtags
                    st.session_state.scores = scores
                    st.session_state.total_generated += len(captions)
                    st.session_state.session_count += 1
                    st.success(f"✅ Generated {len(captions)} caption{'s' if len(captions) > 1 else ''}!")
                    st.rerun()

                except ValueError as ve:
                    st.error(f"❌ {ve}")
                except Exception as e:
                    err = str(e).lower()
                    if "401" in err or "auth" in err or "invalid" in err or "unauthorized" in err:
                        st.error("❌ Invalid API key — please check and re-verify.")
                    elif "quota" in err or "rate" in err:
                        st.error("⏱️ Rate limit hit — wait a moment and try again.")
                    else:
                        st.error(f"❌ {e}")

        # ── Results ─────────────────────────────────────────────────────────
        if st.session_state.captions:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Generated Captions</div>', unsafe_allow_html=True)

            for i, cap in enumerate(st.session_state.captions):
                score, reason = (st.session_state.scores[i]
                                 if i < len(st.session_state.scores)
                                 else (7, "Score unavailable"))

                stars = "★" * score + "☆" * (10 - score)
                st.markdown(f"""
                <div class="caption-card">
                  <div class="caption-num">Caption {i+1}</div>
                  <div class="caption-text">{cap}</div>
                  <span class="score-pill">⭐ {score}/10 &nbsp; {reason}</span>
                </div>
                """, unsafe_allow_html=True)

                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    st.code(cap, language=None)
                with btn_c2:
                    if st.button(f"💾 Save #{i+1}", key=f"save_{i}", type="secondary", use_container_width=True):
                        try:
                            save_to_history(cap, st.session_state.hashtags, api_tone)
                            st.success("Saved ✓")
                        except Exception as e:
                            st.error(f"Save failed: {e}")

    with right:
        # ── Tips ────────────────────────────────────────────────────────────
        with st.expander("💡 Tips for Better Captions"):
            tips = [
                ("Be specific", "Describe mood, location, and vibe — not just what's in the photo."),
                ("Pair with emojis", "Emojis break up text and boost scroll-stopping power."),
                ("Add a CTA", "End with a question or action: 'Drop your city below 👇'"),
                ("Stay authentic", "Audiences detect forced copy instantly — write how you talk."),
                ("Use micro hashtags", "Mix 1M+ and niche tags to maximise discoverability."),
            ]
            tip_html = '<div style="padding-top: 0.2rem;">'
            for title, body in tips:
                tip_html += f'<div class="tip-item"><div class="tip-dot"></div><div><strong>{title}</strong> — {body}</div></div>'
            tip_html += "</div>"
            st.markdown(tip_html, unsafe_allow_html=True)

        # ── Hashtags ─────────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Suggested Hashtags</div>', unsafe_allow_html=True)
        if st.session_state.hashtags:
            chips = "".join(f'<span class="hashtag-chip">#{t}</span>'
                            for t in st.session_state.hashtags)
            st.markdown(f'<div class="card"><div class="hashtag-wrap">{chips}</div></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div class="card" style="color:var(--muted);font-size:.88rem">Generate captions to see hashtag suggestions.</div>',
                        unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 2 — HISTORY
# ════════════════════════════════════════════════════════
with tab_hist:
    try:
        history = load_history()
    except Exception:
        history = []

    hcol1, hcol2 = st.columns([5, 2])
    with hcol1:
        st.markdown(f'<div class="section-label">{len(history)} saved caption{"s" if len(history) != 1 else ""}</div>',
                    unsafe_allow_html=True)
    with hcol2:
        if history and st.button("🗑️  Clear All", type="secondary", use_container_width=True):
            try:
                clear_history()
                st.success("History cleared.")
                st.rerun()
            except Exception as e:
                st.error(str(e))

    if not history:
        st.info("No saved captions yet — generate some and hit 💾 Save!")
    else:
        for entry in reversed(history):
            with st.expander(f"🕐 {entry.get('timestamp','—')}  ·  {entry.get('tone','—')}"):
                st.write(entry.get("caption", ""))
                if entry.get("hashtags"):
                    chips = "".join(f'<span class="hashtag-chip">#{t}</span>'
                                    for t in entry["hashtags"])
                    st.markdown(f'<div class="hashtag-wrap" style="margin-top:.5rem">{chips}</div>',
                                unsafe_allow_html=True)