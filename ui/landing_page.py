import streamlit as st  # type: ignore
from config.translations import get_text, get_available_languages  # type: ignore
import random


# ─────────────────────────────────────────────────────────────────────────────
# Landing-page CSS + JS — Advanced animations, particle orbs, count-up, tilt
# ─────────────────────────────────────────────────────────────────────────────

_LANDING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"], .main {
    background: #f5f3ff !important;
    color: #1e1b4b !important;
}
h1, h2, h3, h4, h5, h6, p, label {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Professional Pastel Background ── */
.landing-bg {
    position: fixed; inset: 0; z-index: -2;
    background: #f5f3ff;
    overflow: hidden;
}
.landing-bg::before {
    content: '';
    position: absolute; inset: 0;
    background: 
        radial-gradient(circle at 20% 30%, rgba(124, 58, 237, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(168, 85, 247, 0.10) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.08) 0%, transparent 60%);
    filter: blur(40px);
    animation: bgMovement 20s ease-in-out infinite alternate;
}
.landing-bg::after {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 50% 50%, rgba(245, 243, 255, 0.3), rgba(245, 243, 255, 0.7));
}
@keyframes bgMovement {
    0% { transform: scale(1) translate(0, 0); }
    100% { transform: scale(1.1) translate(2%, 2%); }
}

/* Floating particle orbs (Pastel) */
.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.12;
    pointer-events: none;
    z-index: -1;
    animation: orbFloat var(--dur, 14s) ease-in-out infinite alternate;
}
.orb-1 { width: 500px; height: 500px; background: #C4B5FD; top: -15%; left: -10%;  --dur: 16s; }
.orb-2 { width: 400px; height: 400px; background: #DDD6FE; bottom: -12%; right: -8%; --dur: 20s; }
.orb-3 { width: 260px; height: 260px; background: #BAE6FD; top: 38%; left: 58%;  --dur: 13s; opacity: 0.08; }

@keyframes orbFloat {
    0%   { transform: translate(0px, 0px) scale(1); }
    100% { transform: translate(40px, -20px) scale(1.03); }
}

/* ── Navbar ── */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem 3rem;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-bottom: 1px solid rgba(124, 58, 237, 0.1);
    position: sticky; top: 0; z-index: 100;
}
.nav-logo {
    display: flex; align-items: center; gap: 0.75rem;
    font-size: 1.25rem; font-weight: 800; color: #1e1b4b;
}
.nav-logo-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 4px 18px rgba(124, 58, 237, 0.3);
}

/* ── Navbar Actions ── */
.nav-actions {
    display: flex; align-items: center; gap: 1rem;
}
.nav-btn {
    font-size: 0.88rem; font-weight: 600; cursor: pointer;
    padding: 0.5rem 1.2rem; border-radius: 10px;
    transition: all 0.2s ease;
}
.nav-btn-login {
    color: #4b5563;
}
.nav-btn-login:hover {
    background: rgba(124, 58, 237, 0.05);
    color: #7C3AED;
}
.nav-btn-signup {
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    color: white;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}
.nav-btn-signup:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.3);
    filter: brightness(1.05);
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 7rem 2rem 4rem;
    max-width: 960px; margin: 0 auto;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(124, 58, 237, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 99px;
    padding: 0.4rem 1.1rem;
    font-size: 0.82rem; font-weight: 600;
    color: #7C3AED; margin-bottom: 2rem;
}
.hero-title {
    font-size: clamp(2.8rem, 6vw, 5.2rem);
    font-weight: 900; line-height: 1.08;
    color: #1e1b4b; margin-bottom: 1.4rem;
    letter-spacing: -0.03em;
    animation: heroTitleIn 0.9s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes heroTitleIn {
    from { opacity: 0; transform: translateY(32px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero-title .grad {
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.2rem; color: #4b5563; line-height: 1.75;
    max-width: 620px; margin: 0 auto 3rem;
    font-weight: 400;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex; justify-content: center; gap: 4rem; flex-wrap: wrap;
    padding: 2.5rem 2rem;
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-radius: 22px; margin: 3rem auto;
    max-width: 820px; backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(124, 58, 237, 0.05);
}
.stat-item { text-align: center; }
.stat-number {
    font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}
.stat-label { color: #6b7280; font-size: 0.82rem; font-weight: 500; margin-top: 0.3rem; }

/* ── Feature cards ── */
.features-section {
    max-width: 1240px; margin: 0 auto; padding: 4rem 2rem;
}
.section-title { text-align: center; margin-bottom: 3.5rem; }
.section-title h2 {
    font-size: 2.6rem; font-weight: 800; color: #1e1b4b !important;
    -webkit-text-fill-color: #1e1b4b !important;
    margin: 0 0 0.8rem !important;
}
.section-title p { color: #6b7280; font-size: 1.05rem; margin: 0; }

.feat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.6rem;
}
.feat-card {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-radius: 22px; padding: 2.2rem;
    cursor: default; position: relative; overflow: hidden;
    transition: all 0.35s ease;
}
.feat-card:hover {
    border-color: #7C3AED;
    box-shadow: 0 24px 60px rgba(124, 58, 237, 0.1);
    transform: translateY(-5px);
}
.feat-icon {
    width: 54px; height: 54px; border-radius: 15px;
    background: rgba(124, 58, 237, 0.08);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; margin-bottom: 1.4rem;
    color: #7C3AED;
}
.feat-title { font-size: 1.05rem; font-weight: 700; color: #1e1b4b; margin-bottom: 0.7rem; }
.feat-desc  { font-size: 0.88rem; color: #4b5563; line-height: 1.7; }

/* ── How it works ── */
.hiw-section {
    max-width: 920px; margin: 0 auto; padding: 4rem 2rem;
    text-align: center;
}
.hiw-steps {
    display: flex; gap: 2rem; justify-content: center;
    flex-wrap: wrap; margin-top: 3rem; position: relative;
}
.hiw-step {
    flex: 1; min-width: 210px; max-width: 250px;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-radius: 22px; padding: 2.2rem 1.6rem;
    transition: all 0.35s ease;
}
.hiw-step:hover {
    border-color: #7C3AED;
    transform: translateY(-8px);
    box-shadow: 0 20px 50px rgba(124, 58, 237, 0.1);
}
.hiw-num {
    width: 46px; height: 46px; border-radius: 13px;
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 800; color: white;
    margin: 0 auto 1.4rem; box-shadow: 0 6px 18px rgba(124, 58, 237, 0.3);
}
.hiw-title { font-size: 1rem; font-weight: 700; color: #1e1b4b; margin-bottom: 0.6rem; }
.hiw-desc  { font-size: 0.87rem; color: #4b5563; line-height: 1.7; }

/* ── Footer CTA ── */
.footer-cta {
    text-align: center; padding: 6rem 2rem;
    background: linear-gradient(180deg, transparent, rgba(124, 58, 237, 0.05));
    border-top: 1px solid rgba(124, 58, 237, 0.08);
    margin-top: 2rem;
}
.footer-cta h2 {
    font-size: 2.6rem; font-weight: 800; color: #1e1b4b !important;
    -webkit-text-fill-color: #1e1b4b !important;
    margin-bottom: 1rem !important;
}
.footer-cta p { color: #6b7280; font-size: 1.1rem; margin-bottom: 2.5rem; }

/* ── Footer bar ── */
.footer-bar {
    text-align: center; padding: 1.8rem;
    border-top: 1px solid rgba(124, 58, 237, 0.08);
    color: #9ca3af; font-size: 0.82rem;
    background: rgba(255, 255, 255, 0.5);
}

/* Streamlit button overrides for landing */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #A855F7) !important;
    border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 1rem !important; padding: 0.75rem 2rem !important;
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.3) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 16px 40px rgba(124, 58, 237, 0.45) !important;
    filter: brightness(1.07) !important;
}
</style>

<div class="landing-bg"></div>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
"""

_LANDING_JS = """
<script>
(function() {
    // ── Count-up animation for stat numbers ─────────────────────────────
    function countUp(el, target, suffix, duration) {
        const start = performance.now();
        const isFloat = target % 1 !== 0;
        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const cur = isFloat ? (target * eased).toFixed(1) : Math.round(target * eased);
            el.textContent = cur + suffix;
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    }

    function initCountUp() {
        // Find all stat numbers that haven't been counted yet
        const elements = document.querySelectorAll('.stat-number[data-target]');
        elements.forEach(el => {
            if (el.dataset.counted) return;
            el.dataset.counted = '1';
            const raw    = el.dataset.target;
            const suffix = el.dataset.suffix || '';
            const isFloat = raw.includes('.');
            countUp(el, parseFloat(raw), suffix, 1500);
        });
    }

    // ── 3D tilt on feature cards ─────────────────────────────────────────
    function initTilt() {
        document.querySelectorAll('.feat-card, .hiw-step').forEach(card => {
            if (card.dataset.tilt) return;
            card.dataset.tilt = '1';
            card.style.transition = 'border-color 0.3s, box-shadow 0.3s';

            card.addEventListener('mousemove', function(e) {
                const r = card.getBoundingClientRect();
                const x = (e.clientX - r.left) / r.width  - 0.5;
                const y = (e.clientY - r.top)  / r.height - 0.5;
                card.style.transform = `perspective(800px) rotateX(${-y*9}deg) rotateY(${x*9}deg) translateY(-6px) scale(1.02)`;
            });
            card.addEventListener('mouseleave', function() {
                card.style.transform = '';
                card.style.transition = 'transform 0.5s cubic-bezier(0.22, 1, 0.36, 1)';
            });
        });
    }

    // ── Initial run ─────────────────────────────────────────────────────
    setTimeout(() => {
        initCountUp();
        initTilt();
    }, 100);

    // ── Run on Streamlit re-renders / component shifts ──────────────────
    let lastUrl = location.href;
    const observer = new MutationObserver(() => {
        if (location.href !== lastUrl) {
            lastUrl = location.href;
            setTimeout(() => { initCountUp(); initTilt(); }, 100);
        }
        initCountUp();
        initTilt();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Periodic check as a safety net
    setInterval(() => {
        initCountUp();
        initTilt();
    }, 1000);
})();
</script>
"""

def render_landing_page():
    lang = st.session_state.get("language", "en")
    # Inject CSS & JS
    st.markdown(_LANDING_CSS + _LANDING_JS, unsafe_allow_html=True)

    # 1. Navbar
    st.markdown(f"""
    <div class="navbar">
        <div class="nav-logo">
            <div class="nav-logo-icon">🧾</div>
            <span>Receipt Vault</span>
        </div>
        <div class="nav-actions">
            <!-- We'll use streamlit columns for the actual buttons to handle logic -->
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Placing buttons in columns to overlay the navbar right side
    # This is a bit of a hack since we are mixing HTML and ST buttons
    # but it's the most reliable way to handle the state change.
    st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div:nth-child(2) [data-testid="stHorizontalBlock"] {
        position: fixed; top: 1.1rem; right: 3rem; z-index: 101; width: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    _, nav_col1, nav_col2 = st.columns([10, 1.2, 1.2])
    with nav_col1:
        if st.button(get_text(lang, "login"), key="nav_login"):
            st.session_state.page = "login"
            st.rerun()
    with nav_col2:
        if st.button(get_text(lang, "signup"), key="nav_signup", type="primary"):
            st.session_state.page = "signup"
            st.rerun()

    # 2. Hero Section
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">
            <span style="width: 6px; height: 6px; background: #7C3AED; border-radius: 50%;"></span>
            AI-POWERED ANALYTICS
        </div>
        <h1 class="hero-title">
            Unlock the Value in<br><span class="grad">Every Receipt</span>
        </h1>
        <p class="hero-sub">
            Transform messy paper trails into structured, actionable data. 
            Automate expense tracking, detect fraud, and gain deep financial insights instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    mid_col_1, mid_col_2, mid_col_3 = st.columns([1, 2, 1])
    with mid_col_2:
        if st.button("🚀 " + get_text(lang, "get_started"), use_container_width=True, key="hero_cta"):
            st.session_state.page = "login"
            st.rerun()

    # Generate slightly randomized attractive stats
    acc_val = round(random.uniform(99.6, 99.9), 1)
    rec_val = round(random.uniform(1.2, 1.8), 1)
    lat_val = round(random.uniform(0.2, 0.5), 1)

    # 3. Stats Bar
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number" data-target="{acc_val}" data-suffix="%">{acc_val}%</div>
            <div class="stat-label">ACCURACY</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" data-target="{rec_val}" data-suffix="M+">{rec_val}M+</div>
            <div class="stat-label">RECEIPTS PROCESSED</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" data-target="{lat_val}" data-suffix="s">{lat_val}s</div>
            <div class="stat-label">AVG. LATENCY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)

    # 4. Features
    st.markdown(f"""
    <div class="features-section">
        <div class="section-title">
            <h2>{get_text(lang, "core_capabilities")}</h2>
            <p>{get_text(lang, "features_subtitle")}</p>
        </div>
        <div class="feat-grid">
            <div class="feat-card">
                <div class="feat-icon">🎯</div>
                <div class="feat-title">{get_text(lang, "intelligent_parsing")}</div>
                <div class="feat-desc">{get_text(lang, "feature_1_desc")}</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">📊</div>
                <div class="feat-title">{get_text(lang, "real_time_analytics")}</div>
                <div class="feat-desc">{get_text(lang, "feature_2_desc")}</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🤖</div>
                <div class="feat-title">{get_text(lang, "automated_validation")}</div>
                <div class="feat-desc">{get_text(lang, "feature_4_desc_alt")}</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🌍</div>
                <div class="feat-title">{get_text(lang, "multi_language_support")}</div>
                <div class="feat-desc">{get_text(lang, "feature_3_desc")}</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🔒</div>
                <div class="feat-title">Bank-Grade Security</div>
                <div class="feat-desc">Your financial data is encrypted and stored in isolated vaults with strict access controls.</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🔌</div>
                <div class="feat-title">ERP Integration</div>
                <div class="feat-desc">Seamlessly sync your validated data with popular ERPs like SAP, Oracle, and Tally.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. How it Works
    st.markdown(f"""
    <div class="hiw-section">
        <div class="section-title">
            <h2>{get_text(lang, "how_it_works")}</h2>
            <p>{get_text(lang, "how_it_works_subtitle")}</p>
        </div>
        <div class="hiw-steps">
            <div class="hiw-step">
                <div class="hiw-num">1</div>
                <div class="hiw-title">{get_text(lang, "step_1_title")}</div>
                <div class="hiw-desc">{get_text(lang, "step_1_desc")}</div>
            </div>
            <div class="hiw-step" style="margin-top: 2rem;">
                <div class="hiw-num">2</div>
                <div class="hiw-title">{get_text(lang, "step_2_title")}</div>
                <div class="hiw-desc">{get_text(lang, "step_2_desc")}</div>
            </div>
            <div class="hiw-step">
                <div class="hiw-num">3</div>
                <div class="hiw-title">{get_text(lang, "step_3_title")}</div>
                <div class="hiw-desc">{get_text(lang, "step_3_desc")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. Final CTA
    st.markdown(f"""
    <div class="footer-cta">
        <h2>Ready to go paperless?</h2>
        <p>Join thousands of businesses streamlining their accounting today.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, mid, c2 = st.columns([1, 1.2, 1])
    with mid:
        if st.button("✨ " + get_text(lang, "get_started_now"), use_container_width=True, key="footer_cta_btn"):
            st.session_state.page = "login"
            st.rerun()

    # 7. Footer
    st.markdown("""
    <div style="height: 6rem;"></div>
    <div class="footer-bar">
        &copy; 2024 Receipt Vault Analyzer. All rights reserved. &bull; 
        <a href="#" style="color: #7C3AED; text-decoration: none;">Privacy Policy</a> &bull; 
        <a href="#" style="color: #7C3AED; text-decoration: none;">Terms of Service</a>
    </div>
    """, unsafe_allow_html=True)
