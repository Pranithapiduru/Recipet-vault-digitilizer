# Receipt Vault — Chat with Your Data
import streamlit as st   # type: ignore
import pandas as pd      # type: ignore
from database.queries import fetch_all_receipts  # type: ignore


def render_chat():
    lang = st.session_state.get("language", "en")

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
<div style="
    display:flex;align-items:center;gap:1.4rem;
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.12);
    border-radius:20px; padding:1.6rem 2.2rem; margin-bottom:2rem;
    backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
    box-shadow: 0 10px 40px rgba(124, 58, 237, 0.08);
">
    <div style="
        width:54px;height:54px;border-radius:14px;
        background:linear-gradient(135deg,#7C3AED,#A855F7);
        display:flex;align-items:center;justify-content:center;
        font-size:1.6rem;box-shadow:0 8px 25px rgba(124, 58, 237, 0.35);flex-shrink:0;
    ">💬</div>
    <div>
        <h1 style="margin:0;font-size:1.85rem;font-weight:900;
            background:linear-gradient(135deg,#7C3AED,#A855F7);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:-0.01em;">
            Chat with your Receipts
        </h1>
        <p style="margin:0.25rem 0 0;color:#6b7280;font-size:0.92rem;font-weight:500;">
            Ask natural-language questions about your spending, vendors, or trends
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Data check ────────────────────────────────────────────────────────────
    receipts = fetch_all_receipts()
    if not receipts:
        st.markdown("""
<div style="
    background:rgba(255,255,255,0.7);
    border:2px dashed rgba(124, 58, 237, 0.2);
    border-radius:24px; padding:3.5rem 2rem; text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.02);
">
    <div style="font-size:3rem;margin-bottom:1rem;">📂</div>
    <div style="color:#1e1b4b;font-weight:800;font-size:1.2rem;margin-bottom:0.5rem;">No data yet</div>
    <div style="color:#6b7280;font-size:0.95rem;font-weight:500;">
        Upload receipts first to start chatting with your data.
    </div>
</div>
""", unsafe_allow_html=True)
        return

    df = pd.DataFrame(receipts)

    # ── API key guard ─────────────────────────────────────────────────────────
    api_key = st.session_state.get("GEMINI_API_KEY")
    if not api_key:
        st.markdown("""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.15);
    border-radius:20px; padding:2.5rem; text-align:center; margin-bottom:2rem;
    box-shadow:0 10px 40px rgba(124, 58, 237, 0.05);
">
    <div style="font-size:3.5rem;margin-bottom:1rem;">🔑</div>
    <div style="color:#1e1b4b;font-size:1.2rem;font-weight:800;margin-bottom:0.6rem;">
        Gemini API Key Required
    </div>
    <div style="color:#6b7280;font-size:0.95rem;font-weight:500;line-height:1.6;">
        Enter your Google Gemini API key in the sidebar to enable AI chat.<br>
        Your key is used only for querying your own data.
    </div>
</div>
""", unsafe_allow_html=True)
        return

    # ── Quick-prompt suggestions ──────────────────────────────────────────────
    suggestions = [
        "What's my biggest spending category?",
        "How much did I spend last month?",
        "Who is my most visited vendor?",
        "Show me anomalies in my spending.",
    ]

    st.markdown('<div style="margin:1rem 0 0.8rem;color:#7C3AED;font-size:0.75rem;font-weight:800;'
                'text-transform:uppercase;letter-spacing:0.1em;">💡 Suggested questions</div>',
                unsafe_allow_html=True)

    sug_cols = st.columns(len(suggestions))
    for col, sugg in zip(sug_cols, suggestions):
        with col:
            if st.button(sugg, key=f"sugg_{sugg[:20]}", use_container_width=True):
                st.session_state.setdefault("messages", [])
                st.session_state["messages"].append({"role": "user", "content": sugg})
                st.session_state["_pending_prompt"] = sugg

    st.write("")

    # ── Chat history ──────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Clear button
    col_clear, _ = st.columns([1, 5])
    with col_clear:
        if st.button("🗑 Clear chat", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("_pending_prompt", None)
            st.rerun()

    # Render existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Process pending prompt from suggestion buttons ────────────────────────
    pending = st.session_state.pop("_pending_prompt", None)
    if pending:
        _send_to_ai(pending, df, api_key)

    # ── Chat input ────────────────────────────────────────────────────────────
    if prompt := st.chat_input("E.g. 'How much did I spend at Amazon last month?'"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        _send_to_ai(prompt, df, api_key)


def _send_to_ai(prompt: str, df: "pd.DataFrame", api_key: str):
    from ai.gemini_client import GeminiClient  # type: ignore
    with st.chat_message("assistant"):
        with st.spinner("Analysing your data…"):
            try:
                client  = GeminiClient(api_key)
                summary = df.to_string(index=False)
                resp    = client.chat_with_data(prompt, summary)
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
            except Exception as e:
                error_msg = f"❌ Chat failed: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})