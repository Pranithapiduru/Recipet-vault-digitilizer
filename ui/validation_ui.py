from typing import Any, Dict
import streamlit as st          # type: ignore
from datetime import datetime
from database.queries import fetch_all_receipts, receipt_exists  # type: ignore
from config.translations import get_text  # type: ignore
import pandas as pd              # type: ignore

EXPECTED_TAX_RATE = 0.08   # 8%
TOLERANCE         = 0.05   # ±5%


# ═════════════════════════════════════════════════════════════════════════════
#  Pure business logic — no UI
# ═════════════════════════════════════════════════════════════════════════════
def validate_receipt(data: dict, skip_duplicate: bool = False) -> dict:
    results: list[dict] = []
    passed  = True

    # ── Required fields ───────────────────────────────────────────────────────
    required = ["bill_id", "vendor", "date", "amount", "tax"]
    missing  = [f for f in required if data.get(f) is None]

    if missing:
        results.append({"status":"error","title":"Required Fields",
                         "message":f"Missing: {', '.join(missing)}"})
        return {"passed": False, "results": results}
    results.append({"status":"success","title":"Required Fields",
                     "message":"All required fields present"})

    # ── Date format ───────────────────────────────────────────────────────────
    date_val = data.get("date")
    try:
        datetime.strptime(str(date_val), "%Y-%m-%d")
        results.append({"status":"success","title":"Date Format",
                         "message":f"Valid date: {date_val}"})
    except Exception:
        results.append({"status":"error","title":"Date Format",
                         "message":f"Invalid date format: {date_val}"})
        passed = False

    # ── Amount ────────────────────────────────────────────────────────────────
    try:
        amount = float(data.get("amount") or 0)
    except (ValueError, TypeError):
        amount = 0.0

    try:
        tax = float(data.get("tax") or 0)
    except (ValueError, TypeError):
        tax = 0.0

    if amount > 0:
        results.append({"status":"success","title":"Total Amount",
                         "message":f"Amount ₹{amount:.2f} is valid"})
    else:
        results.append({"status":"error","title":"Total Amount",
                         "message":"Invalid/zero amount value"})
        passed = False

    # ── Tax rate ──────────────────────────────────────────────────────────────
    if tax == 0.0:
        results.append({"status":"success","title":"Tax Rate","message":"No tax applied"})
    else:
        valid, actual_rate, used_subtotal = False, 0.0, 0.0
        for subtotal in [amount - tax, amount]:
            if subtotal <= 0:
                continue
            try:
                r = tax / subtotal
            except ZeroDivisionError:
                continue
            if abs(r - EXPECTED_TAX_RATE) <= TOLERANCE:
                valid, actual_rate, used_subtotal = True, r, subtotal
                break
        if valid:
            results.append({"status":"success","title":"Tax Rate",
                             "message":f"Tax rate OK ({actual_rate*100:.2f}%, subtotal ₹{used_subtotal:.2f})"})
        else:
            results.append({"status":"error","title":"Tax Rate",
                             "message":f"Tax mismatch — expected ~{EXPECTED_TAX_RATE*100:.1f}%, "
                                       f"got ₹{tax:.2f} on ₹{amount:.2f}"})
            passed = False

    # ── Duplicate ─────────────────────────────────────────────────────────────
    if not skip_duplicate:
        if receipt_exists(data.get("bill_id")):
            results.append({"status":"error","title":"Duplicate Detection",
                             "message":"Duplicate receipt found in database"})
            passed = False
        else:
            results.append({"status":"success","title":"Duplicate Detection",
                             "message":"No duplicate found"})
    else:
        results.append({"status":"success","title":"Duplicate Detection",
                         "message":"Duplicate check skipped"})

    return {"passed": passed, "results": results}


# ═════════════════════════════════════════════════════════════════════════════
#  UI helpers
# ═════════════════════════════════════════════════════════════════════════════
def _result_card(r: dict):
    is_ok   = r["status"] == "success"
    bg      = "rgba(236, 253, 245, 0.7)" if is_ok else "rgba(254, 242, 242, 0.7)"
    border  = "#10b981"               if is_ok else "#ef4444"
    icon    = "✅"                     if is_ok else "❌"
    textColor = "#065f46"             if is_ok else "#991b1b"
    st.markdown(f"""
<div style="
    background:{bg};
    border:1px solid {border}22;
    border-left:5px solid {border};
    border-radius:12px; padding:1.1rem 1.4rem; margin:0.6rem 0;
    display:flex; align-items:flex-start; gap:0.8rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
">
    <span style="font-size:1.2rem;flex-shrink:0;">{icon}</span>
    <div>
        <div style="font-weight:800;color:{textColor};font-size:0.95rem;margin-bottom:0.25rem;">{r['title']}</div>
        <div style="color:#6b7280;font-size:0.9rem;font-weight:500;">{r['message']}</div>
    </div>
</div>
""", unsafe_allow_html=True)


def _status_banner(passed: bool, context: str = ""):
    if passed:
        st.markdown(f"""
<div style="
    background:rgba(236, 253, 245, 0.8);
    border:1px solid rgba(16, 185, 129, 0.2);
    border-radius:16px; padding:1.2rem 1.6rem; margin:1rem 0;
    display:flex; align-items:center; gap:1rem;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.05);
">
    <span style="font-size:1.8rem;">🎉</span>
    <div>
        <div style="font-weight:800;color:#059669;font-size:1.05rem;">Validation Passed</div>
        <div style="color:#6b7280;font-size:0.88rem;font-weight:500;">{context}</div>
    </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div style="
    background:rgba(254, 242, 242, 0.9);
    border:1px solid rgba(239, 68, 68, 0.2);
    border-radius:16px; padding:1.2rem 1.6rem; margin:1rem 0;
    display:flex; align-items:center; gap:1rem;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.05);
">
    <span style="font-size:1.8rem;">❌</span>
    <div>
        <div style="font-weight:800;color:#dc2626;font-size:1.05rem;">Validation Failed</div>
        <div style="color:#6b7280;font-size:0.88rem;font-weight:500;">{context}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  Main UI
# ═════════════════════════════════════════════════════════════════════════════
def validation_ui():
    lang = st.session_state.get("language", "en")

    # Page header
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
    ">✅</div>
    <div>
        <h1 style="margin:0;font-size:1.85rem;font-weight:900;
            background:linear-gradient(135deg,#7C3AED,#A855F7);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:-0.01em;">
            Receipt Validation
        </h1>
        <p style="margin:0.25rem 0 0;color:#6b7280;font-size:0.92rem;font-weight:500;">
            Verify integrity, tax compliance and duplicate status of any receipt
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Last uploaded receipt ─────────────────────────────────────────────────
    last_data   = st.session_state.get("LAST_EXTRACTED_RECEIPT")
    last_report = st.session_state.get("LAST_VALIDATION_REPORT")

    if last_data and last_report:
        st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.12);
    border-radius:18px; padding:1.4rem 1.8rem; margin-bottom:1.5rem;
    backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    box-shadow: 0 4px 24px rgba(124, 58, 237, 0.08);
">
    <div style="font-weight:700;color:#1e1b4b;font-size:1rem;margin-bottom:0.8rem;">
        🎯 {get_text(lang, 'current_upload_header')}
    </div>
""", unsafe_allow_html=True)
        for r in last_report["results"]:
            _result_card(r)
        vendor  = last_data.get("vendor", "Receipt")
        _status_banner(last_report["passed"], f"Vendor: {vendor}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.4);
    border:1px dashed rgba(124, 58, 237, 0.2);
    border-radius:18px; padding:2rem; text-align:center;
    margin-bottom:1.5rem;
    backdrop-filter:blur(12px);
">
    <div style="font-size:2rem;margin-bottom:0.5rem;">📂</div>
    <div style="color:#6b7280; font-weight:500;">{get_text(lang, 'no_receipt_uploaded')} — upload one on the Upload page first.</div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Stored receipt lookup ─────────────────────────────────────────────────
    st.markdown(f"""
<div style="font-weight:700;color:#1e1b4b;font-size:1.1rem;margin-bottom:0.8rem;">
    🔍 {get_text(lang, 'validate_stored_header')}
</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bill_id = st.text_input("Bill ID", placeholder="e.g. INV-001", key="val_bid")
    with col2:
        vendor  = st.text_input("Vendor",  placeholder="e.g. Amazon",  key="val_vnd")
    with col3:
        amount_inp = st.text_input("Amount", placeholder="e.g. 1500",  key="val_amt")
    with col4:
        tax_inp    = st.text_input("Tax",    placeholder="e.g. 120",    key="val_tax")

    st.write("")
    if st.button("🔎 Run Validation", use_container_width=True, type="primary"):
        receipts = fetch_all_receipts()
        match: dict[str, Any] | None = None

        for rec in receipts:
            r: Dict[str, Any] = rec
            if bill_id   and bill_id   not in str(r.get("bill_id", "")):   continue
            if vendor    and vendor.lower() not in str(r.get("vendor","")).lower(): continue
            if amount_inp:
                try:
                    if float(amount_inp) != float(r.get("amount", -1)):    continue
                except ValueError:
                    pass
            if tax_inp:
                try:
                    if float(tax_inp) != float(r.get("tax", -1)):          continue
                except ValueError:
                    pass
            match = r
            break

        if match is None:
            st.error("❌ No matching stored receipt found")
        else:
            match_typed: Dict[str, Any] = match  # type: ignore
            report = validate_receipt(match_typed, skip_duplicate=True)
            st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.12);
    border-radius:18px; padding:1.4rem 1.8rem; margin-top:1rem;
    backdrop-filter:blur(16px);
    box-shadow: 0 4px 24px rgba(124, 58, 237, 0.08);
">
    <div style="font-weight:700;color:#1e1b4b;margin-bottom:0.8rem;">
        🧪 {get_text(lang, 'validation_for')} <span style="color:#7C3AED;">
        {match_typed.get('bill_id', 'Unknown')}</span>
    </div>
""", unsafe_allow_html=True)
            for r in report["results"]:
                _result_card(r)
            _status_banner(report["passed"],
                           f"Vendor: {match_typed.get('vendor','—')}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ── All stored receipts quick overview ────────────────────────────────────
    st.markdown(f"""
<div style="font-weight:700;color:#1e1b4b;font-size:1.1rem;margin-bottom:0.8rem;">
    {get_text(lang, 'stored_receipts_header')}
</div>
""", unsafe_allow_html=True)
    all_receipts = fetch_all_receipts()
    if all_receipts:
        df = pd.DataFrame(all_receipts)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        st.dataframe(
            df[["bill_id","vendor","date","amount","tax","category"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
                "tax":    st.column_config.NumberColumn("Tax",    format="₹%.2f"),
                "date":   st.column_config.DateColumn("Date",      format="YYYY-MM-DD"),
            }
        )
    else:
        st.info("No stored receipts found.")