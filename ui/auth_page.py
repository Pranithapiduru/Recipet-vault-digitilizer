import streamlit as st  # type: ignore
from config.translations import get_text, get_available_languages  # type: ignore
import hashlib
import json
import os


# ─────────────────────────────────────────────────────────────────────────────
# Auth CSS — dark glassmorphism card centered on an animated background
# ─────────────────────────────────────────────────────────────────────────────
_AUTH_CSS = """
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
    padding: 2rem 1rem 4rem !important;
    max-width: 100% !important;
}

/* ── Professional Pastel Background ── */
.auth-bg {
    position: fixed; inset: 0; z-index: -2;
    background: #f5f3ff;
    overflow: hidden;
}
.auth-bg::before {
    content: '';
    position: absolute; inset: 0;
    background: 
        radial-gradient(circle at 10% 20%, rgba(124, 58, 237, 0.10) 0%, transparent 50%),
        radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 40% 60%, rgba(14, 165, 233, 0.06) 0%, transparent 60%);
    filter: blur(50px);
    animation: authBgMotion 25s ease-in-out infinite alternate;
}
.auth-bg::after {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 50% 50%, rgba(245, 243, 255, 0.4), rgba(245, 243, 255, 0.85));
}
@keyframes authBgMotion {
    0% { transform: scale(1) translate(0, 0); }
    100% { transform: scale(1.05) translate(1%, 1%); }
}

/* ── Floating particles (Pastel) ── */
.auth-particles { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; }
.auth-particle {
    position: absolute; border-radius: 50%;
    background: radial-gradient(circle, rgba(124, 58, 237, 0.4), rgba(168, 85, 247, 0.2));
    animation: particleFloat var(--pd, 12s) ease-in-out infinite var(--delay, 0s);
    opacity: 0;
}
@keyframes particleFloat {
    0%   { opacity: 0;    transform: translateY(100vh) scale(0.5); }
    10%  { opacity: 0.4; }
    90%  { opacity: 0.3; }
    100% { opacity: 0;    transform: translateY(-20px) scale(1); }
}

/* ── Auth card with shimmer sweep border ── */
.auth-card {
    max-width: 460px; margin: 0 auto;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 24px; padding: 3rem 2.8rem;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(124, 58, 237, 0.15);
    box-shadow: 0 40px 100px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.5);
    animation: cardIn 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    position: relative; overflow: hidden;
}
@keyframes cardIn {
    from { opacity: 0; transform: translateY(30px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* Shimmer sweep across card top */
.auth-card::before {
    content: '';
    position: absolute; top: 0; left: -100%; right: auto;
    width: 60%; height: 3px;
    background: linear-gradient(90deg, transparent, #7C3AED, #A855F7, transparent);
    animation: shimmerSweep 3.5s ease-in-out infinite;
    border-radius: 99px;
}
@keyframes shimmerSweep {
    0%   { left: -60%; }
    100% { left: 160%; }
}

/* Gradient glow at bottom of card */
.auth-card::after {
    content: '';
    position: absolute; bottom: 0; left: 25%; right: 25%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.3), rgba(168, 85, 247, 0.3), transparent);
}

.auth-logo {
    display: flex; align-items: center; justify-content: center;
    gap: 0.8rem; margin-bottom: 0.5rem;
}
.auth-logo-icon {
    width: 52px; height: 52px; border-radius: 15px;
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.3);
    animation: iconFloat 4s ease-in-out infinite;
}
@keyframes iconFloat {
    0%,100% { transform: translateY(0px); box-shadow: 0 6px 20px rgba(124, 58, 237, 0.3); }
    50%      { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(124, 58, 237, 0.4); }
}
.auth-app-name { font-size: 1.4rem; font-weight: 800; color: #1e1b4b; }
.auth-subtitle {
    text-align: center; color: #6b7280; font-size: 0.95rem;
    margin-bottom: 2rem; font-weight: 400;
}
.auth-divider {
    display: flex; align-items: center; gap: 1rem;
    margin: 1.5rem 0; color: #9ca3af; font-size: 0.85rem;
}
.auth-divider::before, .auth-divider::after {
    content: ''; flex: 1;
    border-top: 1px solid rgba(124, 58, 237, 0.1);
}
.auth-footer {
    text-align: center; margin-top: 1.2rem;
    color: #6b7280; font-size: 0.88rem;
}
.auth-link { color: #7C3AED; font-weight: 600; cursor: pointer; text-decoration: none; }
.auth-link:hover { text-decoration: underline; }

/* Password strength meter */
.pw-strength-wrap { margin-top: 0.75rem; }
.pw-strength-bar {
    height: 5px; border-radius: 99px;
    background: rgba(0, 0, 0, 0.05);
    overflow: hidden; margin-bottom: 0.4rem;
}
.pw-strength-fill {
    height: 100%; border-radius: 99px;
    transition: width 0.4s ease, background 0.4s ease;
}
.pw-strength-label { font-size: 0.78rem; font-weight: 600; letter-spacing: 0.02em; }

/* Streamlit widget overrides inside auth card */
.stTextInput label, .stSelectbox label {
    color: #4b5563 !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.05em !important;
}
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1.5px solid rgba(124, 58, 237, 0.15) !important;
    border-radius: 12px !important; color: #1e1b4b !important;
    font-size: 0.95rem !important; padding: 0.75rem 1rem !important;
    transition: all 0.25s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
    background: #fff !important;
}
.stTextInput > div > div > input::placeholder { color: #9ca3af !important; }

.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #A855F7) !important;
    border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 1rem !important; padding: 0.75rem !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3) !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    width: 100% !important; position: relative !important; overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 35px rgba(124, 58, 237, 0.4) !important;
    filter: brightness(1.05) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.5) !important;
    border: 1px solid rgba(124, 58, 237, 0.2) !important;
    color: #1e1b4b !important; box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(124, 58, 237, 0.08) !important;
    border-color: #7C3AED !important;
}
[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1.5px solid rgba(124, 58, 237, 0.15) !important;
    border-radius: 12px !important; color: #1e1b4b !important;
}
</style>

<!-- Animated background container -->
<div class="auth-bg"></div>
<div class="auth-particles" id="auth-particles"></div>

<script>
(function() {
    function spawnParticles() {
        const container = document.getElementById('auth-particles');
        if (!container || container.dataset.done) return;
        container.dataset.done = '1';
        for (let i = 0; i < 20; i++) {
            const p = document.createElement('div');
            p.className = 'auth-particle';
            const size = 4 + Math.random() * 8;
            const delay = Math.random() * 15;
            const dur   = 12 + Math.random() * 15;
            p.style.cssText = `width:${size}px; height:${size}px; left:${Math.random()*100}%; --pd:${dur}s; --delay:-${delay}s; animation-delay:-${delay}s;`;
            container.appendChild(p);
        }
    }

    function initPwStrength() {
        const inputs = document.querySelectorAll('input[type="password"]');
        inputs.forEach(inp => {
            if (inp.dataset.pwStrength) return;
            inp.dataset.pwStrength = '1';
            let wrap = inp.closest('[data-testid="stTextInput"]');
            if (!wrap) return;

            const meter = document.createElement('div');
            meter.className = 'pw-strength-wrap';
            meter.innerHTML = '<div class="pw-strength-bar"><div class="pw-strength-fill" style="width:0%"></div></div>' +
                              '<div class="pw-strength-label" style="color:#9ca3af;">Enter a password</div>';
            wrap.appendChild(meter);

            inp.addEventListener('input', function() {
                const v = inp.value;
                const fill  = meter.querySelector('.pw-strength-fill');
                const label = meter.querySelector('.pw-strength-label');
                let score = 0;
                if (v.length >= 8)  score++;
                if (v.length >= 12) score++;
                if (/[A-Z]/.test(v)) score++;
                if (/[0-9]/.test(v)) score++;
                if (/[^A-Za-z0-9]/.test(v)) score++;

                const levels = [
                    { t: 0,  w: '0%',   c: '#9ca3af', l: 'Enter a password' },
                    { t: 1,  w: '20%',  c: '#ef4444', l: '🔴 Very Weak' },
                    { t: 2,  w: '40%',  c: '#f59e0b', l: '🟡 Weak' },
                    { t: 3,  w: '60%',  c: '#fbbf24', l: '🟡 Fair' },
                    { t: 4,  w: '80%',  c: '#A855F7', l: '🟣 Strong' },
                    { t: 5,  w: '100%', c: '#10b981', l: '🟢 Excellent' },
                ];
                const level = levels[v.length === 0 ? 0 : Math.min(score, 5)];
                fill.style.width  = level.w;
                fill.style.background = level.c;
                label.style.color = level.c;
                label.textContent = level.l;
            });
        });
    }

    const obs = new MutationObserver(() => {
        spawnParticles();
        initPwStrength();
    });
    obs.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => { spawnParticles(); initPwStrength(); }, 600);
})();
</script>
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    users_file = "data/users.json"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}


def save_user(email: str, password: str, name: str = "", phone: str = ""):
    users_file = "data/users.json"
    os.makedirs("data", exist_ok=True)
    users = load_users()
    users[email] = {
        "password": hash_password(password),
        "name": name,
        "phone": phone,
        "auth_method": "email"
    }
    with open(users_file, "w") as f:
        json.dump(users, f, indent=2)


def verify_user(email: str, password: str) -> bool:
    users = load_users()
    if email in users:
        return users[email]["password"] == hash_password(password)
    return False


# ─── Login Page ───────────────────────────────────────────────────────────────
def render_login_page():
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)
    lang = st.session_state.get("language", "en")

    # Back button + Language in a row
    col_back, col_gap, col_lang = st.columns([1, 3, 1])
    with col_back:
        if st.button("← Home", key="login_back"):
            st.session_state["page"] = "landing"
            st.rerun()
    with col_lang:
        available_langs = get_available_languages()
        selected_lang = st.selectbox(
            "🌐",
            options=list(available_langs.keys()),
            format_func=lambda x: available_langs[x],
            index=list(available_langs.keys()).index(lang),
            key="lang_login",
            label_visibility="collapsed"
        )
        if selected_lang != lang:
            st.session_state["language"] = selected_lang
            st.rerun()

    # Card
    _, col_card, _ = st.columns([1, 2, 1])
    with col_card:
        st.markdown(f"""
<div class="auth-card">
    <div class="auth-logo">
        <div class="auth-logo-icon">🧾</div>
        <div class="auth-app-name">{get_text(lang, 'app_name')}</div>
    </div>
    <div class="auth-subtitle">Welcome back — sign in to continue</div>
</div>
""", unsafe_allow_html=True)

        # Google placeholder
        if st.button("  🔐  Continue with Google  ", key="google_login", use_container_width=True, type="secondary"):
            st.info("🔐 Google OAuth requires additional setup. Use email/password below.")

        st.markdown('<div class="auth-divider"><span>or</span></div>', unsafe_allow_html=True)

        email = st.text_input(
            get_text(lang, "email"),
            placeholder="your.email@example.com",
            key="login_email"
        )
        password = st.text_input(
            get_text(lang, "password"),
            type="password",
            placeholder="••••••••",
            key="login_password"
        )

        st.write("")
        if st.button(f"  {get_text(lang, 'login')}  →", key="login_submit", use_container_width=True):
            if email and password:
                if verify_user(email, password):
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["page"] = "app"
                    st.success(f"✅ {get_text(lang, 'welcome')}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
            else:
                st.warning("⚠️ Please fill in all fields")

        st.markdown(f"""
<div class="auth-footer">
    {get_text(lang, 'no_account')} &nbsp;
</div>
""", unsafe_allow_html=True)
        if st.button(f"Create account →", key="go_signup", use_container_width=True, type="secondary"):
            st.session_state["page"] = "signup"
            st.rerun()


# ─── Signup Page ──────────────────────────────────────────────────────────────
def render_signup_page():
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)
    lang = st.session_state.get("language", "en")

    col_back, col_gap, col_lang = st.columns([1, 3, 1])
    with col_back:
        if st.button("← Home", key="signup_back"):
            st.session_state["page"] = "landing"
            st.rerun()
    with col_lang:
        available_langs = get_available_languages()
        selected_lang = st.selectbox(
            "🌐",
            options=list(available_langs.keys()),
            format_func=lambda x: available_langs[x],
            index=list(available_langs.keys()).index(lang),
            key="lang_signup",
            label_visibility="collapsed"
        )
        if selected_lang != lang:
            st.session_state["language"] = selected_lang
            st.rerun()

    _, col_card, _ = st.columns([1, 2, 1])
    with col_card:
        st.markdown(f"""
<div class="auth-card">
    <div class="auth-logo">
        <div class="auth-logo-icon">🧾</div>
        <div class="auth-app-name">{get_text(lang, 'app_name')}</div>
    </div>
    <div class="auth-subtitle">Create your free account — takes 30 seconds</div>
</div>
""", unsafe_allow_html=True)

        if st.button("  🔐  Sign up with Google  ", key="google_signup", use_container_width=True, type="secondary"):
            st.info("🔐 Google OAuth requires additional setup. Use email/password below.")

        st.markdown('<div class="auth-divider"><span>or</span></div>', unsafe_allow_html=True)

        name = st.text_input("Full Name", placeholder="Jane Doe", key="signup_name")
        email = st.text_input(get_text(lang, "email"), placeholder="your.email@example.com", key="signup_email")
        phone = st.text_input(get_text(lang, "phone_number"), placeholder="+91 98765 43210", key="signup_phone")
        password = st.text_input(get_text(lang, "password"), type="password", placeholder="Min. 6 characters", key="signup_password")
        confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")

        st.write("")
        if st.button(f"  {get_text(lang, 'signup')}  →", key="signup_submit", use_container_width=True):
            if name and email and phone and password and confirm:
                if password != confirm:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    users = load_users()
                    if email in users:
                        st.error("❌ Email already registered")
                    else:
                        save_user(email, password, name, phone)
                        st.success("✅ Account created! Redirecting to login…")
                        st.session_state["page"] = "login"
                        st.rerun()
            else:
                st.warning("⚠️ Please fill in all fields")

        st.markdown(f'<div class="auth-footer">{get_text(lang, "have_account")} &nbsp;</div>', unsafe_allow_html=True)
        if st.button("Sign in instead →", key="go_login", use_container_width=True, type="secondary"):
            st.session_state["page"] = "login"
            st.rerun()