"""
Global Design System — Receipt Vault Analyzer
Professional pastel light theme with soft violet/lavender palette.
Includes CSS animations, JavaScript scroll-reveal, counter animation, and ripple effects.
"""

import streamlit as st  # type: ignore


# ── Design tokens ──────────────────────────────────────────────────────────────
ACCENT       = "#7C3AED"
ACCENT2      = "#A855F7"
GRADIENT     = "linear-gradient(135deg, #7C3AED 0%, #A855F7 100%)"
BG_LIGHT     = "#f5f3ff"
BG_CARD      = "rgba(255,255,255,0.92)"
GLASS_BORDER = "rgba(124,58,237,0.12)"
TEXT_PRIMARY = "#1e1b4b"
TEXT_MUTED   = "#6b7280"


# ── Shared CSS injected once per render ────────────────────────────────────────
_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ═══════════════════════════════════════
   ROOT / RESET
═══════════════════════════════════════ */
:root {
    --accent:      #7C3AED;
    --accent2:     #A855F7;
    --accent3:     #0EA5E9;
    --success:     #059669;
    --warning:     #D97706;
    --danger:      #DC2626;
    --bg:          #f5f3ff;
    --bg-card:     rgba(255,255,255,0.92);
    --border:      rgba(124,58,237,0.12);
    --text:        #1e1b4b;
    --muted:       #6b7280;
    --gradient:    linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    --gradient-3:  linear-gradient(135deg, #7C3AED 0%, #A855F7 50%, #0EA5E9 100%);
    --shadow-lg:   0 25px 50px rgba(124,58,237,0.10);
    --shadow-glow: 0 0 40px rgba(124,58,237,0.18);
    --radius:      16px;
    --radius-sm:   10px;
    --radius-xs:   6px;
}

/* App shell */
html, body, [data-testid="stAppViewContainer"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, [data-testid="stStatusWidget"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

/* Block container */
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1440px !important;
}

/* ═══════════════════════════════════════
   SOFT PASTEL BACKGROUND
═══════════════════════════════════════ */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: -10;
    background:
        radial-gradient(ellipse 70% 50% at 10% 5%,  rgba(124,58,237,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 90% 85%,  rgba(168,85,247,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 55% 40%,  rgba(14,165,233,0.05) 0%, transparent 50%),
        var(--bg);
    animation: bgShift 20s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes bgShift {
    0%   { background-position: 0% 0%; }
    100% { background-position: 100% 100%; }
}

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.96) !important;
    border-right: 1px solid rgba(124,58,237,0.12) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 4px 0 24px rgba(124,58,237,0.06) !important;
}
[data-testid="stSidebar"] > div:first-child { background: transparent !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text) !important;
    background: none !important;
}
[data-testid="stSidebar"] input {
    background: #f8f7ff !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    color: var(--text) !important;
    border-radius: var(--radius-sm) !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #f8f7ff !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 6px !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(124,58,237,0.04) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 1rem !important;
    margin: 0 !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    font-weight: 500 !important;
    position: relative !important;
    overflow: hidden !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--gradient);
    transform: scaleY(0);
    transition: transform 0.25s ease;
    border-radius: 0 2px 2px 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover::before {
    transform: scaleY(1);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(124,58,237,0.08) !important;
    border-color: rgba(124,58,237,0.3) !important;
    transform: translateX(5px) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(168,85,247,0.08)) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.15) !important;
    color: var(--accent) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"]::before {
    transform: scaleY(1);
}
[data-testid="stSidebar"] button {
    background: rgba(124,58,237,0.06) !important;
    border: 1px solid rgba(124,58,237,0.15) !important;
    color: var(--text) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
}
[data-testid="stSidebar"] button:hover {
    background: rgba(124,58,237,0.12) !important;
    border-color: var(--accent) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] [data-testid="stProgress"] > div > div {
    background: rgba(124,58,237,0.12) !important;
    border-radius: 99px !important;
}
[data-testid="stSidebar"] [data-testid="stProgress"] > div > div > div {
    background: var(--gradient) !important;
    border-radius: 99px !important;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(124,58,237,0.12) !important;
    margin: 1rem 0 !important;
}

/* ═══════════════════════════════════════
   TYPOGRAPHY
═══════════════════════════════════════ */
h1, h2, h3, h4, h5, h6, p, label, li, .stText {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMarkdownContainer"] h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    border-bottom: none !important;
    padding-bottom: 0 !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stMarkdownContainer"] h2 {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    background: none !important;
    -webkit-text-fill-color: var(--text) !important;
    margin-top: 1.2rem !important;
}
[data-testid="stMarkdownContainer"] h3 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    background: none !important;
    -webkit-text-fill-color: var(--muted) !important;
    margin-top: 0.8rem !important;
}
[data-testid="stMarkdownContainer"] h4 {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    margin-top: 0.6rem !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: var(--text) !important;
}

/* ═══════════════════════════════════════
   METRICS — Premium pastel cards
═══════════════════════════════════════ */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: var(--radius) !important;
    padding: 1.4rem 1.6rem !important;
    backdrop-filter: blur(16px) !important;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08) !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--gradient-3);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}
div[data-testid="metric-container"]::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at top left, rgba(124,58,237,0.05), transparent 70%);
    opacity: 0;
    transition: opacity 0.35s ease;
    pointer-events: none;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-6px) scale(1.01) !important;
    border-color: rgba(124,58,237,0.3) !important;
    box-shadow: 0 20px 50px rgba(124,58,237,0.14), 0 0 0 1px rgba(124,58,237,0.15) !important;
}
div[data-testid="metric-container"]:hover::before { transform: scaleX(1); }
div[data-testid="metric-container"]:hover::after { opacity: 1; }
[data-testid="stMetricValue"] {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    background: var(--gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    -webkit-text-fill-color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
[data-testid="stMetricDelta"] { font-weight: 600 !important; }

/* ═══════════════════════════════════════
   BUTTONS — Ripple Effect
═══════════════════════════════════════ */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    background: rgba(255,255,255,0.85) !important;
    color: var(--text) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0; left: 0;
    pointer-events: none;
    background-image: radial-gradient(circle, rgba(124,58,237,0.2) 10%, transparent 10.01%);
    background-repeat: no-repeat;
    background-position: 50%;
    transform: scale(10, 10);
    opacity: 0;
    transition: transform 0.5s, opacity 0.6s;
}
.stButton > button:active::after {
    transform: scale(0, 0);
    opacity: 0.35;
    transition: 0s;
}
.stButton > button[kind="primary"] {
    background: var(--gradient) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(124,58,237,0.45) !important;
    filter: brightness(1.06) !important;
}
.stButton > button:hover {
    background: rgba(124,58,237,0.08) !important;
    border-color: rgba(124,58,237,0.4) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(124,58,237,0.1) !important;
    color: var(--accent) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #34d399) !important;
    border: none !important;
    color: white !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(5,150,105,0.3) !important;
    transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(5,150,105,0.45) !important;
    filter: brightness(1.05) !important;
}

/* ═══════════════════════════════════════
   INPUTS
═══════════════════════════════════════ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background: rgba(255,255,255,0.95) !important;
    border: 1.5px solid rgba(124,58,237,0.18) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15), 0 4px 16px rgba(124,58,237,0.08) !important;
    background: #ffffff !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stRadio label {
    color: var(--text) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.95) !important;
    border: 1.5px solid rgba(124,58,237,0.18) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    transition: border-color 0.25s ease !important;
}
[data-baseweb="select"] > div:hover { border-color: var(--accent) !important; }
[data-baseweb="option"] { background: #ffffff !important; color: var(--text) !important; }
[data-baseweb="option"]:hover { background: rgba(124,58,237,0.08) !important; }

/* ═══════════════════════════════════════
   FILE UPLOADER
═══════════════════════════════════════ */
@keyframes uploaderPulse {
    0%, 100% {
        border-color: rgba(124,58,237,0.3);
        box-shadow: 0 0 0 0 rgba(124,58,237,0);
    }
    50% {
        border-color: rgba(124,58,237,0.55);
        box-shadow: 0 0 20px rgba(124,58,237,0.12);
    }
}
[data-testid="stFileUploader"] {
    background: rgba(124,58,237,0.03) !important;
    border: 2px dashed rgba(124,58,237,0.32) !important;
    border-radius: var(--radius) !important;
    padding: 1.8rem !important;
    transition: all 0.35s ease !important;
    animation: uploaderPulse 3s ease-in-out infinite !important;
}
[data-testid="stFileUploader"]:hover {
    background: rgba(124,58,237,0.06) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,0.08), 0 12px 40px rgba(124,58,237,0.12) !important;
    animation: none !important;
    transform: scale(1.01) !important;
}
[data-testid="stFileUploader"] * { color: var(--text) !important; }
[data-testid="stFileUploader"] button {
    background: var(--gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1rem !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.3) !important;
    transition: all 0.25s ease !important;
}
[data-testid="stFileUploader"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(124,58,237,0.45) !important;
}

/* ═══════════════════════════════════════
   DATAFRAME / TABLES
═══════════════════════════════════════ */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.07) !important;
}
[data-testid="stDataFrame"] iframe { border-radius: var(--radius) !important; }

/* ═══════════════════════════════════════
   TABS — Premium pill style
═══════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.85) !important;
    border-radius: var(--radius) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    padding: 0.4rem !important;
    gap: 0.25rem !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 2px 12px rgba(124,58,237,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 0.55rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: var(--muted) !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    background: transparent !important;
    position: relative !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--accent) !important;
    background: rgba(124,58,237,0.07) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--gradient) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.3) !important;
}

/* ═══════════════════════════════════════
   EXPANDER
═══════════════════════════════════════ */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
}
.streamlit-expanderHeader:hover {
    border-color: var(--accent) !important;
    background: rgba(124,58,237,0.05) !important;
    transform: translateX(3px) !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(124,58,237,0.1) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
}

/* ═══════════════════════════════════════
   ALERTS
═══════════════════════════════════════ */
.stAlert { border-radius: var(--radius-sm) !important; font-family: 'Inter', sans-serif !important; }
[data-baseweb="notification"] {
    background: rgba(255,255,255,0.9) !important;
    border-radius: var(--radius-sm) !important;
    border-left-width: 4px !important;
    color: var(--text) !important;
    backdrop-filter: blur(8px) !important;
}
[data-baseweb="notification"][kind="positive"],
[data-baseweb="notification"][kind="success"] {
    border-left-color: #059669 !important;
    background: rgba(5,150,105,0.06) !important;
}
[data-baseweb="notification"][kind="info"] {
    border-left-color: #0EA5E9 !important;
    background: rgba(14,165,233,0.06) !important;
}
[data-baseweb="notification"][kind="warning"] {
    border-left-color: #D97706 !important;
    background: rgba(217,119,6,0.06) !important;
}
[data-baseweb="notification"][kind="negative"],
[data-baseweb="notification"][kind="error"] {
    border-left-color: #DC2626 !important;
    background: rgba(220,38,38,0.06) !important;
}

/* ═══════════════════════════════════════
   DIVIDER
═══════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid rgba(124,58,237,0.12) !important;
    margin: 1.5rem 0 !important;
}

/* ═══════════════════════════════════════
   SPINNER
═══════════════════════════════════════ */
[data-testid="stSpinner"] > div { border-top-color: var(--accent) !important; }

/* ═══════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════ */
[data-testid="stProgress"] > div > div {
    background: rgba(124,58,237,0.10) !important;
    border-radius: 99px !important;
    overflow: hidden !important;
}
[data-testid="stProgress"] > div > div > div {
    background: var(--gradient) !important;
    border-radius: 99px !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stProgress"] > div > div > div::after {
    content: '';
    position: absolute;
    top: 0; left: -100%; bottom: 0;
    width: 60%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: progressShine 2s infinite;
}
@keyframes progressShine {
    to { left: 200%; }
}

/* ═══════════════════════════════════════
   RADIO (main area)
═══════════════════════════════════════ */
[data-testid="stRadio"] > div { gap: 0.5rem !important; }
[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(124,58,237,0.14) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] label:hover {
    border-color: var(--accent) !important;
    background: rgba(124,58,237,0.06) !important;
}
[data-testid="stRadio"] label[data-checked="true"] {
    background: var(--gradient) !important;
    border-color: var(--accent) !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.25) !important;
}

/* ═══════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(124,58,237,0.04); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, rgba(124,58,237,0.3), rgba(168,85,247,0.3));
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, rgba(124,58,237,0.6), rgba(168,85,247,0.6));
}

/* ═══════════════════════════════════════
   KEYFRAME ANIMATIONS
═══════════════════════════════════════ */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.94); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 18px rgba(124,58,237,0.10); }
    50%       { box-shadow: 0 0 42px rgba(124,58,237,0.28); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}
@keyframes spin360 {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(124,58,237,0.25); }
    50%       { border-color: rgba(124,58,237,0.6); }
}

/* Page-level entrance animation */
.main > div { animation: fadeUp 0.45s cubic-bezier(0.22,1,0.36,1); }

/* Scroll-reveal utility (applied by JS) */
.rv-hidden {
    opacity: 0;
    transform: translateY(28px);
    transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.22,1,0.36,1);
}
.rv-visible {
    opacity: 1 !important;
    transform: translateY(0) !important;
}

/* Shimmer loading skeleton */
.shimmer {
    background: linear-gradient(90deg,
        rgba(124,58,237,0.04) 25%,
        rgba(124,58,237,0.10) 50%,
        rgba(124,58,237,0.04) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.6s infinite;
    border-radius: 8px;
}

/* ═══════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(124,58,237,0.1) !important;
    border-radius: 14px !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.6rem !important;
    color: var(--text) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(124,58,237,0.22) !important;
    background: rgba(255,255,255,0.95) !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.95) !important;
    border: 1.5px solid rgba(124,58,237,0.25) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

/* ═══════════════════════════════════════
   DATA EDITOR
═══════════════════════════════════════ */
[data-testid="stDataEditor"] {
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.07) !important;
}

/* ═══════════════════════════════════════
   NUMBER INPUT
═══════════════════════════════════════ */
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(124,58,237,0.15) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(124,58,237,0.08) !important;
    border-color: var(--accent) !important;
}

/* ═══════════════════════════════════════
   SLIDER
═══════════════════════════════════════ */
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,0.22) !important;
}

/* ═══════════════════════════════════════
   TOAST
═══════════════════════════════════════ */
[data-testid="stToast"] {
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(124,58,237,0.15) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 20px 50px rgba(124,58,237,0.12) !important;
}

/* ═══════════════════════════════════════
   CHECKBOX
═══════════════════════════════════════ */
[data-baseweb="checkbox"] span {
    background: rgba(255,255,255,0.9) !important;
    border-color: rgba(124,58,237,0.25) !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
}
[data-baseweb="checkbox"] [aria-checked="true"] span {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 10px rgba(124,58,237,0.3) !important;
}

/* ═══════════════════════════════════════
   CAPTION
═══════════════════════════════════════ */
[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
}

/* ═══════════════════════════════════════
   PAGE HEADER COMPONENT
═══════════════════════════════════════ */
.rv-page-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.4s ease-out;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08);
}
.rv-page-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--gradient-3);
}
.rv-page-header::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 200px; height: 100%;
    background: radial-gradient(ellipse at right, rgba(124,58,237,0.07), transparent 70%);
    pointer-events: none;
}
.rv-header-icon {
    width: 56px; height: 56px;
    border-radius: 14px;
    background: var(--gradient);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 8px 24px rgba(124,58,237,0.35);
    flex-shrink: 0;
    animation: float 4s ease-in-out infinite;
}
.rv-header-title {
    margin: 0;
    font-size: 1.85rem;
    font-weight: 800;
    background: var(--gradient-3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
.rv-header-sub {
    margin: 0.25rem 0 0;
    color: var(--muted);
    font-size: 0.88rem;
}

/* ═══════════════════════════════════════
   STAT CARD COMPONENT
═══════════════════════════════════════ */
.rv-stat-card {
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(124,58,237,0.12);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    backdrop-filter: blur(12px);
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 24px rgba(124,58,237,0.07);
    position: relative;
    overflow: hidden;
}
.rv-stat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 48px rgba(124,58,237,0.14);
    border-color: rgba(124,58,237,0.28);
}
</style>
"""

_GLOBAL_JS = """
<script>
(function() {
    // ── Scroll-reveal observer ──────────────────────────────────────────
    function initScrollReveal() {
        const targets = document.querySelectorAll(
            '[data-testid="metric-container"], .rv-stat-card, .feat-card, .hiw-step'
        );
        if (!targets.length) return;
        const obs = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('rv-visible');
                    e.target.classList.remove('rv-hidden');
                    obs.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        targets.forEach(t => {
            t.classList.add('rv-hidden');
            obs.observe(t);
        });
    }

    // ── Ripple on all Streamlit buttons ────────────────────────────────
    function initRipple() {
        document.querySelectorAll('.stButton > button').forEach(btn => {
            if (btn.dataset.ripple) return;
            btn.dataset.ripple = '1';
            btn.addEventListener('click', function(e) {
                const r = document.createElement('span');
                const rect = btn.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height) * 2;
                r.style.cssText = [
                    'position:absolute', 'border-radius:50%',
                    'background:rgba(124,58,237,0.22)',
                    `width:${size}px`, `height:${size}px`,
                    `left:${e.clientX - rect.left - size/2}px`,
                    `top:${e.clientY - rect.top - size/2}px`,
                    'transform:scale(0)', 'animation:rippleAnim 0.6s linear',
                    'pointer-events:none'
                ].join(';');
                btn.style.position = 'relative';
                btn.style.overflow = 'hidden';
                btn.appendChild(r);
                setTimeout(() => r.remove(), 650);
            });
        });
    }

    // ── 3D tilt on cards ───────────────────────────────────────────────
    function initTilt() {
        document.querySelectorAll('.feat-card, .hiw-step, [data-testid="metric-container"]').forEach(card => {
            if (card.dataset.tilt) return;
            card.dataset.tilt = '1';
            card.addEventListener('mousemove', function(e) {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width  - 0.5;
                const y = (e.clientY - rect.top)  / rect.height - 0.5;
                card.style.transform = `perspective(900px) rotateX(${-y*7}deg) rotateY(${x*7}deg) translateY(-4px) scale(1.01)`;
            });
            card.addEventListener('mouseleave', function() {
                card.style.transform = '';
                card.style.transition = 'transform 0.4s ease';
            });
        });
    }

    // ── Run on DOM changes (Streamlit re-renders) ───────────────────────
    const observer = new MutationObserver(() => {
        initScrollReveal();
        initRipple();
        initTilt();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Initial run
    setTimeout(() => {
        initScrollReveal();
        initRipple();
        initTilt();
    }, 600);

    // Ripple keyframe injection
    if (!document.getElementById('rv-ripple-style')) {
        const s = document.createElement('style');
        s.id = 'rv-ripple-style';
        s.textContent = '@keyframes rippleAnim { to { transform: scale(1); opacity: 0; } }';
        document.head.appendChild(s);
    }
})();
</script>
"""


def apply_global_styles():
    """Inject the professional pastel light design system and JS enhancements into the page."""
    st.markdown(_GLOBAL_CSS + _GLOBAL_JS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = "📊"):
    """Render a premium animated page header."""
    sub_html = f'<p class="rv-header-sub">{subtitle}</p>' if subtitle else ''
    st.markdown(f"""
<div class="rv-page-header">
    <div class="rv-header-icon">{icon}</div>
    <div>
        <h1 class="rv-header-title">{title}</h1>
        {sub_html}
    </div>
</div>
""", unsafe_allow_html=True)


def stat_card(label: str, value: str, icon: str = "📈", color: str = "#7C3AED", delta: str = ""):
    """Render a custom glassmorphism stat card with hover animation."""
    delta_html = f'<div style="color:#059669;font-size:0.8rem;font-weight:600;margin-top:0.3rem;">{delta}</div>' if delta else ""
    return f"""
<div class="rv-stat-card" style="border-top: 3px solid {color};">
    <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.8rem;">
        <span style="font-size:1.5rem;">{icon}</span>
        <span style="color:#6b7280;font-size:0.73rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;">{label}</span>
    </div>
    <div style="font-size:2rem;font-weight:900;color:{color};letter-spacing:-0.02em;">{value}</div>
    {delta_html}
</div>"""


# apply_page_header kept as alias for backward compatibility
def apply_page_header(title: str, subtitle: str = "", icon: str = "📊"):
    page_header(title, subtitle, icon)