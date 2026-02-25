import streamlit as st  # type: ignore
from config.translations import get_text, get_available_languages  # type: ignore
from database.queries import clear_all_receipts  # type: ignore


def render_header():
    """Render a premium top-bar with a floating user menu in the top-right."""
    user_email = st.session_state.get("user_email", "User")
    lang = st.session_state.get("language", "en")
    budget_limit = st.session_state.get("monthly_budget", 50000.0)

    # ── Header CSS ────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Styling for the user menu popover */
    [data-testid="stVerticalBlock"] > div:nth-child(1) [data-testid="stPopover"] {
        position: fixed;
        top: 3.8rem;
        right: 1.5rem;
        z-index: 1000;
        width: auto !important;
    }
    [data-testid="stVerticalBlock"] > div:nth-child(1) [data-testid="stPopover"] > button {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.4rem 0.9rem !important;
        color: #1e1b4b !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.08) !important;
        transition: all 0.2s ease !important;
        width: auto !important;
    }
    [data-testid="stVerticalBlock"] > div:nth-child(1) [data-testid="stPopover"] > button:hover {
        background: #fff !important;
        border-color: #7C3AED !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.12) !important;
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

    # Using an empty container to hold the fixed-position popover
    _, user_col = st.columns([8, 2])
    
    with user_col:
        # The button label is now more compact
        display_name = user_email.split('@')[0]
        if len(display_name) > 12:
            display_name = display_name[:10] + ".."
        
        with st.popover(f"📧 {display_name}", use_container_width=False):
            st.markdown(f"### ⚙️ {get_text(lang, 'settings')}")
            st.markdown(f"**Logged in as:** `{user_email}`")
            
            st.divider()

            # 🌐 Language Selector
            available_langs = get_available_languages()
            lang_options = list(available_langs.keys())
            current_lang_idx = lang_options.index(lang) if lang in lang_options else 0
            
            new_lang = st.selectbox(
                get_text(lang, "available_languages"),
                options=lang_options,
                format_func=lambda x: available_langs[x],
                index=current_lang_idx,
                key="hdr_lang_select"
            )
            if new_lang != lang:
                st.session_state["language"] = new_lang
                st.rerun()

            # 🔑 API Key Input
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                value=st.session_state.get("GEMINI_API_KEY", ""),
                placeholder="Paste key here...",
                key="hdr_api_key"
            )
            if api_key != st.session_state.get("GEMINI_API_KEY", ""):
                st.session_state["GEMINI_API_KEY"] = api_key
            
            # 💰 Budget adjustment
            new_budget = st.number_input(
                "Monthly Goal (₹)",
                min_value=0.0,
                value=budget_limit,
                step=1000.0,
                key="hdr_budget_input"
            )
            if new_budget != budget_limit:
                st.session_state["monthly_budget"] = new_budget
                st.rerun()

            st.divider()
            
            # 🗑 Clear Data
            if st.button("🗑 " + get_text(lang, "clear_data") if "clear_data" in get_text(lang, "dashboard") else "🗑 Clear All Data", 
                         use_container_width=True, type="secondary", key="hdr_clear_data"):
                if st.session_state.get("confirm_delete_hdr", False):
                    clear_all_receipts()
                    st.toast("Data cleared!", icon="🗑")
                    st.session_state["confirm_delete_hdr"] = False
                    st.rerun()
                else:
                    st.session_state["confirm_delete_hdr"] = True
                    st.warning("Click again to confirm")

            # 🚪 Logout
            if st.button("🚪 " + get_text(lang, "logout"), use_container_width=True, type="primary", key="hdr_logout"):
                st.session_state["authenticated"] = False
                st.session_state["user_email"] = None
                st.session_state["page"] = "landing"
                st.rerun()

    return st.session_state.get("current_nav_page", "dashboard")
