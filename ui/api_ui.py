import streamlit as st  # type: ignore
import requests
import json
from config.translations import get_text  # type: ignore
from datetime import datetime


def render_api_ui():
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
    ">🔗</div>
    <div>
        <h1 style="margin:0;font-size:1.85rem;font-weight:900;
            background:linear-gradient(135deg,#7C3AED,#A855F7);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:-0.01em;">
            ERP Integration &amp; API
        </h1>
        <p style="margin:0.25rem 0 0;color:#6b7280;font-size:0.92rem;font-weight:500;">
            Connect extracted receipt data to SAP, Oracle, ERPNext, or any REST endpoint
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── API Status card ───────────────────────────────────────────────────────
    st.markdown("#### 📡 API Server Status")

    col_info, col_status = st.columns([3, 1])
    with col_info:
        st.markdown("""
<div style="
    background:rgba(255, 255, 255, 0.7);
    border:1px solid rgba(124, 58, 237, 0.1);
    border-radius:16px; padding:1.4rem 1.6rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
">
    <div style="display:grid;gap:0.7rem;">
        <div style="display:flex;gap:1rem;align-items:center;">
            <span style="color:#6b7280;font-size:0.75rem;font-weight:700;
                         text-transform:uppercase;letter-spacing:0.08em;width:140px;">Base Endpoint</span>
            <code style="color:#7C3AED;background:rgba(124, 58, 237, 0.08);
                          padding:0.3rem 0.8rem;border-radius:8px;font-size:0.88rem;font-weight:600;">
                http://localhost:8000/api/v1
            </code>
        </div>
        <div style="display:flex;gap:1rem;align-items:center;">
            <span style="color:#6b7280;font-size:0.75rem;font-weight:700;
                         text-transform:uppercase;letter-spacing:0.08em;width:140px;">Swagger UI</span>
            <code style="color:#0284c7;background:rgba(56, 189, 248, 0.08);
                          padding:0.3rem 0.8rem;border-radius:8px;font-size:0.88rem;font-weight:600;">
                http://localhost:8000/docs
            </code>
        </div>
        <div style="display:flex;gap:1rem;align-items:center;">
            <span style="color:#6b7280;font-size:0.75rem;font-weight:700;
                         text-transform:uppercase;letter-spacing:0.08em;width:140px;">Auth</span>
            <span style="color:#1e1b4b;font-size:0.9rem;font-weight:500;">API Key (Bearer token in production)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    with col_status:
        try:
            resp = requests.get("http://localhost:8000/", timeout=1)
            if resp.status_code == 200:
                st.markdown("""
<div style="
    background:rgba(236, 253, 245, 0.8);
    border:1px solid rgba(16, 185, 129, 0.15);
    border-left:5px solid #10b981;
    border-radius:16px; padding:1rem;
    text-align:center; height:100%;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.05);
">
    <div style="font-size:1.8rem;margin-bottom:0.4rem;">🟢</div>
    <div style="color:#059669;font-weight:800;font-size:1rem;letter-spacing:0.05em;">ONLINE</div>
    <div style="color:#6b7280;font-size:0.78rem;margin-top:0.2rem;font-weight:500;">API ready</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
<div style="background:rgba(255, 251, 235, 0.8);border:1px solid rgba(245, 158, 11, 0.15);
            border-left:5px solid #f59e0b; border-radius:16px;padding:1rem;text-align:center;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.05);">
    <div style="font-size:1.8rem;">🟡</div>
    <div style="color:#d97706;font-weight:800;letter-spacing:0.05em;">STARTING</div>
</div>""", unsafe_allow_html=True)
        except Exception:
            st.markdown("""
<div style="background:rgba(254, 242, 242, 0.8);border:1px solid rgba(239, 68, 68, 0.15);
            border-left:5px solid #ef4444; border-radius:16px;padding:1rem;text-align:center;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.05);">
    <div style="font-size:1.8rem;">🔴</div>
    <div style="color:#dc2626;font-weight:800;font-size:1rem;letter-spacing:0.05em;">OFFLINE</div>
    <div style="color:#6b7280;font-size:0.75rem;margin-top:0.2rem;font-weight:500;">
        Run <code style="color:#991b1b;background:rgba(239, 68, 68, 0.05);padding:0.1rem 0.3rem;border-radius:4px;">api/main.py</code>
    </div>
</div>""", unsafe_allow_html=True)

    st.divider()

    # ── ERP Configuration ─────────────────────────────────────────────────────
    st.markdown("#### 🏢 ERP Configuration")

    col_a, col_b = st.columns(2)
    with col_a:
        erp_system = st.selectbox(
            "Target ERP System",
            ["ERPNext", "SAP S/4HANA", "Oracle NetSuite",
             "Microsoft Dynamics 365", "Tally ERP", "Generic REST Webhook"],
            key="erp_system_select"
        )
    with col_b:
        erp_env = st.selectbox("Environment", ["Production", "Staging", "Development"], key="erp_env")

    col_c, col_d = st.columns(2)
    with col_c:
        erp_url = st.text_input(
            "ERP Endpoint URL",
            value="https://erp.enterprise.com/api/ingest",
            key="erp_url"
        )
    with col_d:
        erp_secret = st.text_input(
            "Client ID / API Secret",
            type="password",
            placeholder="sk_live_••••••••••••",
            key="erp_secret"
        )

    st.write("")

    # ── Sync trigger ─────────────────────────────────────────────────────────
    if st.button(f"🚀 Trigger Manual ERP Sync → {erp_system}",
                 type="primary", use_container_width=True):
        with st.spinner(f"Mapping and transmitting data to {erp_system}…"):
            try:
                res = requests.post(
                    "http://localhost:8000/api/v1/erp/sync",
                    params={"system": erp_system},
                    timeout=5
                )
                if res.status_code == 200:
                    result = res.json()
                    st.markdown(f"""
<div style="
    background:rgba(236, 253, 245, 0.8);
    border:1px solid rgba(16, 185, 129, 0.2);
    border-left:5px solid #10b981;
    border-radius:16px;padding:1.4rem 1.6rem;margin:1rem 0;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.05);
">
    <div style="color:#059669;font-weight:800;font-size:1.05rem;margin-bottom:0.4rem;">
        ✅ Sync Successful
    </div>
    <div style="color:#6b7280;font-size:0.92rem;font-weight:500;">
        {result.get('exported_records', '?')} records exported to {erp_system}
        at {datetime.now().strftime('%H:%M:%S')}
    </div>
</div>
""", unsafe_allow_html=True)
                    with st.expander("📄 View Transmitted ERP Payload (JSON)"):
                        st.json(result.get("payload_preview", {}))
                else:
                    st.error("⚠️ API returned an error. Is the backend running?")
            except Exception:
                st.markdown("""
<div style="
    background:rgba(254, 242, 242, 0.9);
    border:1px solid rgba(239, 68, 68, 0.2);
    border-left:5px solid #ef4444;
    border-radius:16px; padding:1.4rem 1.6rem; margin:1rem 0;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.05);
">
    <div style="color:#dc2626;font-weight:800;font-size:1.05rem;margin-bottom:0.4rem;">⚠️ Backend Not Available</div>
    <div style="color:#6b7280;font-size:0.92rem;font-weight:500;line-height:1.6;">
        The sync API is offline. Start the backend with:<br>
        <code style="color:#dc2626;background:rgba(239, 68, 68, 0.05);padding:0.2rem 0.5rem;border-radius:6px;font-weight:700;">
        python api/main.py
        </code>
    </div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Endpoint reference table ──────────────────────────────────────────────
    st.markdown("#### 📚 REST API Endpoint Reference")

    endpoints = [
        ("GET",    "/api/v1/receipts",         "List all receipts (supports ?vendor, ?category, ?date filters)"),
        ("GET",    "/api/v1/receipts/{id}",     "Get a single receipt by Bill ID"),
        ("POST",   "/api/v1/receipts",          "Ingest a new parsed receipt payload"),
        ("DELETE", "/api/v1/receipts/{id}",     "Remove a receipt by Bill ID"),
        ("POST",   "/api/v1/erp/sync",          "Trigger a push to the configured ERP endpoint"),
        ("GET",    "/api/v1/analytics/summary", "Aggregate spend summary (totals, categories, top vendors)"),
    ]

    method_colors = {
        "GET":    ("#0284c7", "rgba(56, 189, 248, 0.1)"),
        "POST":   ("#059669", "rgba(16, 185, 129, 0.1)"),
        "DELETE": ("#dc2626", "rgba(239, 68, 68, 0.08)"),
        "PUT":    ("#d97706", "rgba(245, 158, 11, 0.08)"),
    }

    for method, path, desc in endpoints:
        mc, mbg = method_colors.get(method, ("#6b7280", "rgba(0,0,0,0.03)"))
        st.markdown(f"""
<div style="
    display:flex;align-items:center;gap:1.2rem;
    background:rgba(255, 255, 255, 0.6);
    border:1px solid rgba(124, 58, 237, 0.08);
    border-radius:12px;padding:0.8rem 1.4rem;margin-bottom:0.6rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.01);
">
    <span style="
        background:{mbg};color:{mc};
        font-weight:800;font-size:0.72rem;
        padding:0.3rem 0.7rem;border-radius:6px;
        letter-spacing:0.08em;flex-shrink:0;width:64px;text-align:center;
    ">{method}</span>
    <code style="color:#7C3AED;font-size:0.88rem;font-weight:700;flex-shrink:0;min-width:240px;background:rgba(124, 58, 237, 0.04);padding:0.2rem 0.5rem;border-radius:4px;">{path}</code>
    <span style="color:#4b5563;font-size:0.85rem;font-weight:500;">{desc}</span>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Code snippet ─────────────────────────────────────────────────────────
    st.markdown("#### 🖥️ Integration Example")

    tab_curl, tab_py, tab_json = st.tabs(["cURL", "Python", "ERP Field Map"])

    with tab_curl:
        st.code("""# Fetch all receipts (optionally filtered)
curl -X GET "http://localhost:8000/api/v1/receipts?vendor=Amazon" \\
     -H "accept: application/json" \\
     -H "Authorization: Bearer <your_api_key>"

# Trigger ERP sync
curl -X POST "http://localhost:8000/api/v1/erp/sync?system=ERPNext" \\
     -H "accept: application/json" \\
     -H "Authorization: Bearer <your_api_key>""", language="bash")

    with tab_py:
        st.code("""import requests

BASE = "http://localhost:8000/api/v1"
HEADERS = {"Authorization": "Bearer <your_api_key>"}

# List filtered receipts
resp = requests.get(f"{BASE}/receipts", params={"category": "Food"}, headers=HEADERS)
receipts = resp.json()

# Sync to ERPNext
sync = requests.post(f"{BASE}/erp/sync", params={"system": "ERPNext"}, headers=HEADERS)
print(sync.json())""", language="python")

    with tab_json:
        st.markdown("""
<div style="
    background:rgba(255,255,255,0.7); border:1px solid rgba(124, 58, 237, 0.1);
    border-radius:16px; padding:1.8rem 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02);
">
    <div style="color:#1e1b4b;font-size:0.8rem;font-weight:800;
                text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.2rem;">
        Receipt Vault → ERP Field Mapping
    </div>
""", unsafe_allow_html=True)
        mappings = [
            ("bill_id",   "ExternalInvID / JournalEntryRef"),
            ("vendor",    "Supplier / CreditorName"),
            ("date",      "PostingDate / TransactionDate"),
            ("amount",    "GrossAmount / TotalInclTax"),
            ("tax",       "TaxAmount / VATAmount"),
            ("category",  "CostCentre / ExpenseType"),
            ("subtotal",  "NetAmount / BaseAmount"),
        ]
        for src, target in mappings:
            st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            padding:0.75rem 0;border-bottom:1px solid rgba(124, 58, 237, 0.06);">
    <code style="color:#7C3AED;font-size:0.88rem;font-weight:700;background:rgba(124, 58, 237, 0.04);padding:0.2rem 0.5rem;border-radius:4px;">{src}</code>
    <span style="color:#6b7280;font-size:0.8rem;font-weight:800;">⟶</span>
    <code style="color:#0284c7;font-size:0.88rem;font-weight:700;background:rgba(56, 189, 248, 0.04);padding:0.2rem 0.5rem;border-radius:4px;">{target}</code>
</div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
