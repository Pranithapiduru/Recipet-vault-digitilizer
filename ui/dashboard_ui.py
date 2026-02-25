# Receipt Vault Analyzer — Premium Dashboard UI
import streamlit as st       # type: ignore
import pandas as pd          # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import io
from datetime import datetime

from database.queries import fetch_all_receipts, search_receipts, delete_receipt  # type: ignore
from ai.insights import generate_ai_insights  # type: ignore
from config.config import CURRENCY_SYMBOL  # type: ignore
from config.translations import get_text    # type: ignore

try:
    from reportlab.lib.pagesizes import A4              # type: ignore
    from reportlab.lib import colors                    # type: ignore
    from reportlab.lib.units import inch                # type: ignore
    from reportlab.platypus import (SimpleDocTemplate,  # type: ignore
        Table, TableStyle, Paragraph, Spacer)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # type: ignore
    from reportlab.lib.enums import TA_CENTER           # type: ignore
    _PDF_OK = True
except ImportError:
    _PDF_OK = False


# ─── Plotly light theme ───────────────────────────────────────────────────────
_PLOT_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#4b5563"),
    colorway=["#7C3AED","#A855F7","#BAE6FD","#C4B5FD","#DDD6FE","#8B5CF6","#6EE7B7"],
    xaxis=dict(gridcolor="rgba(124, 58, 237, 0.05)", linecolor="rgba(124, 58, 237, 0.08)"),
    yaxis=dict(gridcolor="rgba(124, 58, 237, 0.05)", linecolor="rgba(124, 58, 237, 0.08)"),
    legend=dict(bgcolor="rgba(255,255,255,0.4)", bordercolor="rgba(124, 58, 237, 0.1)"),
    margin=dict(l=20, r=20, t=40, b=20),
)


def _apply_plot_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(**_PLOT_TEMPLATE)
    return fig


# ─── PDF report ───────────────────────────────────────────────────────────────
def generate_pdf_report(df: pd.DataFrame, lang: str = "en"):
    buffer = io.BytesIO()
    if not _PDF_OK:
        buffer.write(b"PDF generation requires reportlab. Please install it.")
        buffer.seek(0)
        return buffer

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                             rightMargin=30, leftMargin=30,
                             topMargin=30, bottomMargin=18)
    elements = []
    styles   = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'T', parent=styles['Heading1'], fontSize=22,
        textColor=colors.HexColor('#6C63FF'),
        spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(get_text(lang, "app_name") + " — Expense Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y %H:%M')}",
                               ParagraphStyle('D', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)))
    elements.append(Spacer(1, 20))

    total_spend = df['amount'].sum()
    total_tax   = df['tax'].sum()
    avg_txn     = df['amount'].mean() if not df.empty else 0.0

    summary_data = [
        ['Metric', 'Value'],
        [get_text(lang, 'total_spending'), f'₹{total_spend:,.2f}'],
        [get_text(lang, 'total_tax_paid'), f'₹{total_tax:,.2f}'],
        [get_text(lang, 'receipts_scanned'), str(len(df))],
        [get_text(lang, 'avg_transaction'), f'₹{avg_txn:,.2f}'],
    ]
    t = Table(summary_data, colWidths=[3*inch, 3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), colors.HexColor('#6C63FF')),
        ('TEXTCOLOR',  (0,0),(-1,0), colors.white),
        ('ALIGN',      (0,0),(-1,-1), 'CENTER'),
        ('FONTNAME',   (0,0),(-1,0),  'Helvetica-Bold'),
        ('GRID',       (0,0),(-1,-1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1),(-1,-1), [colors.white, colors.HexColor('#f8f7ff')]),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 30))

    if not df.empty:
        rows = [[get_text(lang,'date'), get_text(lang,'vendor'), 'Category', 'Amount']]
        for _, row in df.iterrows():
            rows.append([
                row['date'].strftime('%Y-%m-%d') if pd.notna(row['date']) else 'N/A',
                str(row.get('vendor', ''))[:22],
                str(row.get('category', '')),
                f"₹{row['amount']:,.2f}"
            ])
        rt = Table(rows, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
        rt.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,0),  colors.HexColor('#a78bfa')),
            ('TEXTCOLOR',  (0,0),(-1,0),  colors.white),
            ('GRID',       (0,0),(-1,-1), 0.4, colors.lightgrey),
            ('ALIGN',      (0,0),(-1,-1), 'CENTER'),
            ('FONTNAME',   (0,0),(-1,0),  'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0,1),(-1,-1), [colors.white, colors.HexColor('#faf9ff')]),
        ]))
        elements.append(rt)

    doc.build(elements)
    buffer.seek(0)
    return buffer


# ─── Dashboard render ─────────────────────────────────────────────────────────
def render_dashboard():
    lang = st.session_state.get("language", "en")

    # Page header — premium animated component
    st.markdown(f"""
<div class="rv-page-header">
    <div class="rv-header-icon">🏠</div>
    <div>
        <h1 class="rv-header-title">{get_text(lang, 'dashboard_header')}</h1>
        <p class="rv-header-sub">Your receipts, your insights — all in one place</p>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Search / Filter ──────────────────────────────────────────────────────
    with st.expander(f"🔍 {get_text(lang, 'filter_receipts_header')}", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            search_vendor = st.text_input(get_text(lang, "vendor_label"), key="d_vendor")
        with c2:
            cats = ["All", "Food", "Travel", "Utility", "Grocery",
                    "Shopping", "Medical", "Entertainment", "Uncategorized"]
            search_cat = st.selectbox(get_text(lang, "category_label"), cats, key="d_cat")
        with c3:
            search_date = st.date_input(get_text(lang, "date"), value=None, key="d_date")

        c4, c5, c6 = st.columns(3)
        with c4:
            min_amt = st.number_input("Min Amount (₹)", min_value=0.0, step=100.0, key="d_min")
        with c5:
            max_amt = st.number_input("Max Amount (₹)", min_value=0.0, step=100.0, key="d_max")
        with c6:
            st.markdown("<div style='margin-top:26px;'></div>", unsafe_allow_html=True)
            apply_f = st.button("🔎 Apply Filters", use_container_width=True, type="primary")

    if apply_f or search_vendor or (search_cat != "All") or search_date or min_amt or max_amt:
        s_date_str = search_date.strftime("%Y-%m-%d") if search_date else None
        receipts = search_receipts(
            vendor=search_vendor,
            category=search_cat if search_cat != "All" else None,
            min_amount=min_amt if min_amt > 0 else None,
            max_amount=max_amt if max_amt > 0 else None,
            start_date=s_date_str
        )
        st.caption(f"Found **{len(receipts)}** matching receipts")
    else:
        receipts = fetch_all_receipts()

    if not receipts:
        st.info(get_text(lang, "no_receipts_found"))
        return

    df = pd.DataFrame(receipts)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date", ascending=False)

    # ── KPI metrics ──────────────────────────────────────────────────────────
    total_spend = df["amount"].sum()
    total_tax   = df["tax"].sum()
    count       = len(df)
    avg         = df["amount"].mean()
    top_cat     = df["category"].value_counts().idxmax() if "category" in df.columns else "—"

    cols = st.columns(5)
    kpis = [
        (get_text(lang, "total_spending"),  f"{CURRENCY_SYMBOL}{total_spend:,.2f}", "💰", "#7C3AED"),
        (get_text(lang, "total_tax_paid"),  f"{CURRENCY_SYMBOL}{total_tax:,.2f}",   "📋", "#A855F7"),
        (get_text(lang, "receipts_scanned"), str(count),                             "🧾", "#6366f1"),
        (get_text(lang, "avg_transaction"), f"{CURRENCY_SYMBOL}{avg:,.2f}",          "📈", "#10b981"),
        (get_text(lang, "top_category"),     top_cat,                                 "🏷️", "#d97706"),
    ]
    for i, (col, (label, val, icon, color)) in enumerate(zip(cols, kpis)):
        with col:
            delay = i * 0.08
            st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.1);
    border-top:3px solid {color};
    border-radius:18px;padding:1.4rem;
    backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
    transition:all 0.35s cubic-bezier(0.4,0,0.2,1);
    box-shadow:0 8px 24px rgba(0,0,0,0.04);
    position:relative; overflow:hidden;
    animation:fadeUp 0.6s cubic-bezier(0.22,1,0.36,1) {delay:.2f}s both;
    cursor:default;
" onmouseover="this.style.transform='translateY(-6px)';this.style.boxShadow='0 18px 48px rgba(124, 58, 237, 0.12)';"
   onmouseout="this.style.transform='';this.style.boxShadow='0 8px 24px rgba(0,0,0,0.04)';"
>
    <div style="position:absolute;top:0;left:0;right:0;height:1px;
                background:linear-gradient(90deg,transparent,{color}44,transparent);opacity:0.6;"></div>
    <div style="display:flex;align-items:center;gap:0.55rem;margin-bottom:0.8rem;">
        <span style="font-size:1.4rem;">{icon}</span>
        <span style="color:#6b7280;font-size:0.72rem;font-weight:700;
                     text-transform:uppercase;letter-spacing:0.08em;">{label}</span>
    </div>
    <div style="font-size:1.6rem;font-weight:900;color:{color};
                letter-spacing:-0.02em;line-height:1.1;">{val}</div>
</div>
""", unsafe_allow_html=True)

    st.write("")

    # Charts removed for a cleaner dashboard (Analytics are available in the dedicated tab)

    st.divider()

    # ── Export ───────────────────────────────────────────────────────────────
    st.markdown(f"#### 📥 {get_text(lang, 'export_reports_header')}")
    e1, e2, e3, e4 = st.columns(4)

    with e1:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ CSV", csv_data,
                           file_name=f"receipts_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv", use_container_width=True)

    with e2:
        excel_buf = io.BytesIO()
        with pd.ExcelWriter(excel_buf, engine="openpyxl") as w:
            df.to_excel(w, index=False, sheet_name="Receipts")
        excel_buf.seek(0)
        st.download_button("⬇️ Excel", excel_buf,
                           file_name=f"receipts_{datetime.now().strftime('%Y%m%d')}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    with e3:
        if _PDF_OK:
            pdf_buf = generate_pdf_report(df, lang)
            st.download_button("⬇️ PDF", pdf_buf,
                               file_name=f"report_{datetime.now().strftime('%Y%m%d')}.pdf",
                               mime="application/pdf", use_container_width=True)
        else:
            st.caption("Install `reportlab` for PDF export")

    with e4:
        json_data = df.to_json(orient="records", date_format="iso", indent=2)
        st.download_button("⬇️ JSON", json_data,
                           file_name=f"receipts_{datetime.now().strftime('%Y%m%d')}.json",
                           mime="application/json", use_container_width=True)

    st.divider()

    # ── Data table ───────────────────────────────────────────────────────────
    st.markdown(f"#### 🗂️ {get_text(lang, 'stored_receipts_header')}")

    df_display = df.copy()
    df_display.insert(0, "Select", False)

    edited_df = st.data_editor(
        df_display,
        column_config={
            "Select":   st.column_config.CheckboxColumn(required=True),
            "date":     st.column_config.DateColumn(get_text(lang, "date"), format="YYYY-MM-DD"),
            "amount":   st.column_config.NumberColumn(format=f"{CURRENCY_SYMBOL}%.2f"),
            "tax":      st.column_config.NumberColumn(format=f"{CURRENCY_SYMBOL}%.2f"),
        },
        disabled=["bill_id","vendor","date","amount","tax","category","subtotal"],
        hide_index=True,
        use_container_width=True,
        key="dash_editor"
    )

    col_del, _ = st.columns([2, 5])
    with col_del:
        if st.button(get_text(lang, "delete_selected_btn"), type="secondary"):
            to_del = edited_df[edited_df["Select"] == True]
            if not to_del.empty:
                for bid in to_del["bill_id"]:
                    delete_receipt(bid)
                st.success(f"Deleted {len(to_del)} receipt(s)")
                st.rerun()
            else:
                st.warning("Select at least one receipt to delete")

    # ── AI Insights ──────────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### 🤖 AI Spending Insights")
    api_key = st.session_state.get("GEMINI_API_KEY")
    if api_key:
        with st.spinner("Generating AI insights…"):
            try:
                insights = generate_ai_insights(df, api_key)
                if insights:
                    st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.15);
    border-radius:18px;padding:1.6rem 2rem;
    color:#374151;line-height:1.8;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.05);
">
{insights}
</div>
""", unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"AI insights unavailable: {e}")
    else:
        st.info("💡 Enter your Gemini API key in the sidebar to unlock AI-powered spending insights.")