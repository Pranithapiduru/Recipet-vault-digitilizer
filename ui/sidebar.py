import streamlit as st  # type: ignore
from database.queries import clear_all_receipts, fetch_all_receipts  # type: ignore
from config.translations import get_text, get_available_languages  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore


# Nav items: (translation key, emoji icon)
_NAV_ITEMS = [
    ("upload_receipt",   "📤"),
    ("dashboard",        "🏠"),
    ("analytics",        "📊"),
    ("validation",       "✅"),
    ("chat",             "💬"),
    ("erp_integration",  "🔗"),
]


def render_sidebar() -> str:
    lang = st.session_state.get("language", "en")

    with st.sidebar:
        # ── Global Styles ───────────────────────────────────────────────
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {
                    background-color: #f8fafc;
                    border-right: 1px solid #e2e8f0;
                }
                .sidebar-section-label {
                    font-size: 0.75rem;
                    font-weight: 600;
                    color: #64748b;
                    letter-spacing: 0.05em;
                    margin: 1.5rem 0 0.5rem 0.5rem;
                    text-transform: uppercase;
                }
                .nav-item-active {
                    background: #eff6ff;
                    border-left: 4px solid #3b82f6;
                    color: #1e40af;
                }
            </style>
        """, unsafe_allow_html=True)

        # ── Logo / branding ───────────────────────────────────────────────
        st.markdown("""
            <div style="padding: 1rem 0.5rem 2rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="
                        width: 40px; height: 40px; border-radius: 12px;
                        background: linear-gradient(135deg, #3b82f6, #2563eb);
                        display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
                        color: white; font-size: 1.25rem;
                    ">🧾</div>
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 700; color: #0f172a; line-height: 1;">ReceiptVault</div>
                        <div style="font-size: 0.7rem; font-weight: 500; color: #64748b; margin-top: 2px;">Smart Analytics</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────
        st.markdown('<div class="sidebar-section-label">Main Menu</div>', unsafe_allow_html=True)
        nav_options = [f"{icon}  {get_text(lang, key)}" for key, icon in _NAV_ITEMS]
        
        # We use a radio with label hidden for a cleaner look
        page_label = st.radio(
            "Navigation",
            nav_options,
            index=0,
            label_visibility="collapsed",
            key="sidebar_nav"
        )
        selected_text = page_label.split("  ", 1)[-1].strip()

        st.markdown('<div style="margin: 1.5rem 0.5rem; border-top: 1px solid #e2e8f0;"></div>', unsafe_allow_html=True)

        # ── Monthly Budget tracker ─────────────────────────────────────────
        st.markdown('<div class="sidebar-section-label">Spending Goal</div>', unsafe_allow_html=True)

        receipts = fetch_all_receipts()
        current_month = datetime.now().strftime("%Y-%m")
        if receipts:
            df = pd.DataFrame(receipts)
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            current_spend = df[df["date"].dt.strftime("%Y-%m") == current_month]["amount"].sum()
        else:
            current_spend = 0.0

        budget_limit = st.session_state.get("monthly_budget", 50000.0)
        
        pct = min((current_spend / budget_limit * 100) if budget_limit > 0 else 0, 100)
        bar_color = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")

        st.markdown(f"""
            <div style="padding: 0.5rem; background: white; border-radius: 12px; border: 1px solid #e2e8f0; margin: 0 0.5rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.8rem; font-weight: 600; color: #1e293b;">₹{current_spend:,.0f}</span>
                    <span style="font-size: 0.75rem; color: #64748b;">Goal: ₹{budget_limit:,.0f}</span>
                </div>
                <div style="background: #f1f5f9; border-radius: 6px; height: 6px; overflow: hidden;">
                    <div style="width: {pct}%; background: {bar_color}; height: 100%; transition: width 0.5s easy-in-out;"></div>
                </div>
                <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.5rem; font-weight: 500;">
                    {pct:.1f}% used this month
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ── Footer info ───────────────────────────────────────────────────
        st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin: 2rem 0.5rem 1rem; border-top: 1px solid #e2e8f0;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 0.65rem; padding: 1rem 0;">v2.2 · Standard Layout</div>', unsafe_allow_html=True)

    return selected_text
