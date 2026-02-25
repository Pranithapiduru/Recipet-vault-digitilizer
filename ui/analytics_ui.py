import streamlit as st          # type: ignore
import pandas as pd             # type: ignore
import plotly.express as px     # type: ignore
import plotly.graph_objects as go  # type: ignore
from datetime import datetime

from database.queries      import (
    fetch_all_receipts,
    get_user_details,
    update_user_budget
)
from config.translations   import get_text, TRANSLATIONS
from config.config         import CURRENCY_SYMBOL  # type: ignore
from ai.insights           import generate_ai_insights  # type: ignore
from analytics.forecasting import (  # type: ignore
    calculate_moving_averages,
    predict_next_month_spending,
    predict_spending_polynomial,
)
from analytics.advanced_analytics import (  # type: ignore
    detect_subscriptions,
    calculate_burn_rate,
)


# ── Light Plotly theme ────────────────────────────────────────────────────────
_PT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#4b5563", size=12),
    colorway=["#7C3AED","#A855F7","#6366f1","#38bdf8",
               "#10b981","#f59e0b","#ef4444","#ec4899"],
    xaxis=dict(gridcolor="rgba(124, 58, 237, 0.05)",
               linecolor="rgba(124, 58, 237, 0.08)", showgrid=True),
    yaxis=dict(gridcolor="rgba(124, 58, 237, 0.05)",
               linecolor="rgba(124, 58, 237, 0.08)", showgrid=True),
    legend=dict(bgcolor="rgba(255,255,255,0.4)",
                bordercolor="rgba(124, 58, 237, 0.1)"),
    margin=dict(l=10, r=10, t=40, b=10),
    hovermode="x unified",
)


def _pt(fig: go.Figure) -> go.Figure:
    fig.update_layout(**_PT)
    return fig


# ── Insight card ─────────────────────────────────────────────────────────────
def _insight_card(body: str, accent: str = "#7C3AED"):
    st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.12);
    border-left:5px solid {accent};
    border-radius:14px; padding:1.4rem 1.8rem;
    margin:0.8rem 0; color:#374151; line-height:1.75;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
">{body}</div>
""", unsafe_allow_html=True)


# ── KPI chip ──────────────────────────────────────────────────────────────────
def _kpi(col, label: str, value: str, icon: str, color: str):
    with col:
        st.markdown(f"""
<div style="
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.1);
    border-top:4px solid {color};
    border-radius:18px; padding:1.4rem;
    backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    transition: transform 0.3s ease;
" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='';">
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.8rem;">
        <span style="font-size:1.4rem;">{icon}</span>
        <span style="color:#6b7280;font-size:0.72rem;font-weight:700;
                     text-transform:uppercase;letter-spacing:0.08em;">{label}</span>
    </div>
    <div style="font-size:1.6rem;font-weight:900;color:{color};">{value}</div>
</div>
""", unsafe_allow_html=True)


# ── Page header ───────────────────────────────────────────────────────────────
def _page_header(lang: str):
    st.markdown(f"""
<div style="
    display:flex;align-items:center;gap:1.4rem;
    background:rgba(255,255,255,0.7);
    border:1px solid rgba(124, 58, 237, 0.1);
    border-radius:20px; padding:1.6rem 2.2rem; margin-bottom:2rem;
    backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
    box-shadow: 0 10px 40px rgba(124, 58, 237, 0.08);
">
    <div style="
        width:54px;height:54px;border-radius:14px;
        background:linear-gradient(135deg,#7C3AED,#A855F7);
        display:flex;align-items:center;justify-content:center;
        font-size:1.6rem;box-shadow:0 8px 25px rgba(124, 58, 237, 0.35);flex-shrink:0;
    ">📊</div>
    <div>
        <h1 style="margin:0;font-size:1.85rem;font-weight:900;
            background:linear-gradient(135deg,#7C3AED,#A855F7);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:-0.01em;">
            {get_text(lang,'analytics_header').replace('##', '').strip()}
        </h1>
        <p style="margin:0.25rem 0 0;color:#6b7280;font-size:0.92rem;font-weight:500;">
            {get_text(lang,'analytics_subtitle')}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
def render_analytics():
    lang = st.session_state.get("language", "en")
    _page_header(lang)

    # ── Data ──────────────────────────────────────────────────────────────────
    receipts = fetch_all_receipts()
    if not receipts:
        st.info(get_text(lang, "no_receipts_analytics"))
        return

    df = pd.DataFrame(receipts)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date")

    # ── Sidebar date filter ───────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:#6C63FF;text-transform:uppercase;'
                    'letter-spacing:0.07em;margin:0.8rem 0 0.4rem;">📅 Date Range</div>',
                    unsafe_allow_html=True)
        date_range = st.date_input(
            "Date Range",
            value=(df["date"].min(), df["date"].max()),
            min_value=df["date"].min(),
            max_value=df["date"].max(),
            label_visibility="collapsed"
        )

    if len(date_range) == 2:
        s, e = date_range
        mask = (df["date"].dt.date >= s) & (df["date"].dt.date <= e)
        df_f = df.loc[mask]
    else:
        df_f = df.copy()

    # Budget - PERSISTENT across sessions
    user_email = st.session_state.get("user_email")
    user_data = get_user_details(user_email) if user_email else None
    db_budget = float(user_data.get("budget", 50000.0)) if user_data else 50000.0

    # On login (new session or switch user), sync the widget's own session key
    # with the DB value so it shows correctly. Without this, the widget ignores
    # value= and keeps its own stale key from the previous session.
    if "budget_loaded_for" not in st.session_state or st.session_state.get("budget_loaded_for") != user_email:
        st.session_state["current_budget"] = db_budget
        st.session_state["budget_input_sidebar"] = db_budget  # sync the widget key too!
        st.session_state["budget_loaded_for"] = user_email

    with st.sidebar:
        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:#6C63FF;text-transform:uppercase;'
                    'letter-spacing:0.07em;margin:1.2rem 0 0.4rem;">💰 Budget Strategy</div>',
                    unsafe_allow_html=True)
        new_budget = st.number_input(
            "Monthly Limit (₹)",
            min_value=1.0,
            value=st.session_state["current_budget"],
            step=1000.0,
            key="budget_input_sidebar"
        )
        if st.button("💾 Set Budget", use_container_width=True, key="save_budget_btn"):
            if user_email:
                update_user_budget(user_email, new_budget)
                st.session_state["current_budget"] = new_budget
                st.session_state["budget_input_sidebar"] = new_budget  # keep widget in sync
                st.toast("✅ Budget saved!", icon="💰")
                st.rerun()

    budget_lim = st.session_state.get("current_budget", db_budget)


    # Budget
    current_month = datetime.now().strftime("%Y-%m")
    cm_df   = df[df["date"].dt.strftime("%Y-%m") == current_month]
    cm_total  = cm_df["amount"].sum()
    budget_stats = calculate_burn_rate(cm_total, budget_lim, datetime.now().day)

    # Download in sidebar
    with st.sidebar:
        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
        csv = df_f.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ " + get_text(lang, "download_analytics_btn"),
            csv, "analytics.csv", "text/csv",
            use_container_width=True
        )

    # ── KPI row ───────────────────────────────────────────────────────────────
    total_spend   = df_f["amount"].sum()
    avg_txn       = df_f["amount"].mean() if not df_f.empty else 0.0
    n_txn         = len(df_f)
    top_cat, top_cat_amt = ("—", 0.0)
    if not df_f.empty and "category" in df_f.columns:
        cg = df_f.groupby("category")["amount"].sum().sort_values(ascending=False)
        top_cat, top_cat_amt = cg.index[0], cg.iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    _kpi(k1, get_text(lang, "total_spending"),  f"{CURRENCY_SYMBOL}{total_spend:,.2f}", "💰", "#6C63FF")
    _kpi(k2, get_text(lang, "avg_transaction"), f"{CURRENCY_SYMBOL}{avg_txn:,.2f}",     "📈", "#a78bfa")
    _kpi(k3, get_text(lang, "receipts_scanned"), str(n_txn),                             "🧾", "#38bdf8")
    _kpi(k4, get_text(lang, "top_category"),    top_cat,                                 "🏷️", "#f59e0b")

    st.write("")

    # Budget mini-bar
    if budget_stats:
        pct = budget_stats["percent_used"]
        bar_col = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")
        st.markdown(f"""
<div style="background:rgba(255,255,255,0.7);border:1px solid rgba(124, 58, 237, 0.1);
            border-radius:16px;padding:1.4rem;margin-bottom:1.6rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);">
    <div style="display:flex;justify-content:space-between;margin-bottom:0.7rem;">
        <span style="color:#1e1b4b;font-size:0.85rem;font-weight:700;">💰 Spending Control</span>
        <span style="color:{bar_col};font-size:0.8rem;font-weight:800;">{pct:.1f}% consumed</span>
    </div>
    <div style="background:rgba(124, 58, 237, 0.08);border-radius:99px;height:12px;overflow:hidden;">
        <div style="width:{min(pct,100):.1f}%;background:linear-gradient(90deg, #7C3AED, #A855F7);height:100%;border-radius:99px;
                    transition:width 0.8s cubic-bezier(0.22, 1, 0.36, 1);"></div>
    </div>
    <div style="display:flex;justify-content:space-between;margin-top:0.6rem;">
        <span style="color:#6b7280;font-size:0.78rem;font-weight:600;">₹{cm_total:,.0f} spent</span>
        <span style="color:#6b7280;font-size:0.75rem;font-weight:600;">limit ₹{budget_lim:,.0f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_trends, tab_cats, tab_vendors, tab_adv, tab_ai = st.tabs([
        get_text(lang, "trends_tab"),
        get_text(lang, "categories_tab"),
        get_text(lang, "vendors_tab"),
        get_text(lang, "advanced_tab"),
        get_text(lang, "ai_tab"),
    ])

    # ══════════════ TRENDS ══════════════
    with tab_trends:
        st.markdown("#### 📅 Monthly Spending Trend")

        monthly_df = (
            df_f.set_index("date")
            .resample("M")["amount"].sum()
            .reset_index()
        )
        monthly_df.columns = ["Month", "Amount"]

        fig = px.area(monthly_df, x="Month", y="Amount", markers=True)
        fig.update_traces(
            line=dict(color="#6C63FF", width=3),
            marker=dict(size=9, color="#a78bfa",
                        line=dict(color="#6C63FF", width=2)),
            fillcolor="rgba(108,99,255,0.12)"
        )
        poly = predict_spending_polynomial(df, degree=2)
        if poly is not None:
            fig.add_trace(go.Scatter(
                x=poly["date"], y=poly["predicted_amount"],
                mode="lines",
                name=get_text(lang, "ai_trend_prediction"),
                line=dict(dash="dash", color="#f59e0b", width=2)
            ))
        fig.update_layout(**_PT, title="")
        st.plotly_chart(_pt(fig), use_container_width=True)

        # Summary metrics
        if not monthly_df.empty:
            max_m = monthly_df.loc[monthly_df["Amount"].idxmax()]
            min_m = monthly_df.loc[monthly_df["Amount"].idxmin()]
            avg_m = monthly_df["Amount"].mean()
            var_m = monthly_df["Amount"].std()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(get_text(lang, "highest_spending_month"), max_m["Month"].strftime("%b %Y"))
            m2.metric(get_text(lang, "lowest_spending_month"),  min_m["Month"].strftime("%b %Y"))
            m3.metric(get_text(lang, "avg_monthly_spending"),   f"₹{avg_m:,.0f}")
            m4.metric(get_text(lang, "variance_label"),         f"₹{var_m:,.0f}")

        st.divider()
        st.markdown("#### 📉 Daily Spending + 7-Day Moving Average")

        daily_spend, ma_7 = calculate_moving_averages(df_f, 7)
        fig_ma = go.Figure()
        fig_ma.add_trace(go.Scatter(
            x=daily_spend.index, y=daily_spend,
            name=get_text(lang, "daily_spending"),
            line=dict(color="rgba(108,99,255,0.4)", width=1),
            fill="tozeroy", fillcolor="rgba(108,99,255,0.06)"
        ))
        fig_ma.add_trace(go.Scatter(
            x=ma_7.index, y=ma_7,
            name=get_text(lang, "seven_day_average"),
            line=dict(color="#f59e0b", width=3)
        ))
        st.plotly_chart(_pt(fig_ma), use_container_width=True)

        # Trend Summary Card
        avg_d = daily_spend.mean() if not daily_spend.empty else 0.0
        max_d = daily_spend.max() if not daily_spend.empty else 0.0
        _insight_card(
            f"📉 <strong>Volatility Check:</strong> Your average daily burn is <strong>₹{avg_d:,.2f}</strong>. "
            f"The single highest spending day peaked at <strong>₹{max_d:,.2f}</strong>. "
            f"The 7-day average (gold line) helps smooth out these spikes to show your true spending path.",
            accent="#f59e0b"
        )

        predicted_nm, daily_avg = predict_next_month_spending(df)
        c1, c2 = st.columns(2)
        c1.metric(get_text(lang, "predicted_next_month_label"), f"₹{predicted_nm:,.2f}")
        c2.metric(get_text(lang, "daily_average_label"),        f"₹{daily_avg:,.2f}")

    # ══════════════ CATEGORIES ══════════════
    with tab_cats:
        st.markdown("#### 🏷️ Category Distribution")

        cat_df = df_f.groupby("category")["amount"].sum().reset_index()
        cat_df = cat_df.sort_values("amount", ascending=False)

        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(cat_df, values="amount", names="category", hole=0.52)
            fig_pie.update_traces(textposition="outside", textfont_size=11,
                                   marker=dict(line=dict(color="rgba(0,0,0,0)")))
            fig_pie.update_layout(**_PT)
            fig_pie.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            fig_tree = px.treemap(
                df_f, path=[px.Constant("All Spending"), "category", "vendor"],
                values="amount", color="amount",
                color_continuous_scale=["#1a1a2e", "#6C63FF", "#a78bfa"]
            )
            fig_tree.update_layout(**_PT)
            st.plotly_chart(fig_tree, use_container_width=True)

        if not cat_df.empty:
            top_c   = cat_df.iloc[0]
            low_c   = cat_df.iloc[-1]
            top3    = cat_df.head(3)
            top3_pct = (top3["amount"].sum() / total_spend * 100) if total_spend else 0
            _insight_card(
                f"🏆 <strong>Top category:</strong> {top_c['category']} — "
                f"₹{top_c['amount']:,.0f} ({top_c['amount']/total_spend*100:.1f}% of total)<br>"
                f"✅ <strong>Lowest:</strong> {low_c['category']} — ₹{low_c['amount']:,.0f}<br>"
                f"📊 <strong>Top 3</strong> ({', '.join(top3['category'].tolist())}) account for "
                f"₹{top3['amount'].sum():,.0f} ({top3_pct:.1f}% of total)",
                accent="#f59e0b"
            )

    # ══════════════ VENDORS ══════════════
    with tab_vendors:
        st.markdown("#### 🏪 Vendor Analysis")

        vdf = (
            df_f.groupby("vendor")["amount"]
            .agg(["sum", "count"])
            .reset_index()
            .sort_values("sum", ascending=False)
        )
        vdf.columns = ["vendor", "total", "count"]
        top10 = vdf.head(10)

        fig_v = px.bar(
            top10.sort_values("total"),
            x="total", y="vendor", orientation="h",
            color="total",
            color_continuous_scale=["#1a1a2e", "#6C63FF", "#a78bfa"],
            text="total"
        )
        fig_v.update_traces(
            texttemplate=f"{CURRENCY_SYMBOL}%{{x:,.0f}}",
            textposition="outside", marker_cornerradius=5
        )
        fig_v.update_layout(**_PT, showlegend=False,
                             coloraxis_showscale=False,
                             xaxis_title="Total ₹", yaxis_title="")
        st.plotly_chart(fig_v, use_container_width=True)

        if not vdf.empty:
            tv = vdf.iloc[0]
            lv = vdf.iloc[-1]
            mf = vdf.loc[vdf["count"].idxmax()]
            _insight_card(
                f"💎 <strong>Highest paid:</strong> {tv['vendor']} — "
                f"₹{tv['total']:,.0f} ({tv['count']} transactions)<br>"
                f"🔄 <strong>Most frequent:</strong> {mf['vendor']} — "
                f"{mf['count']} transactions<br>"
                f"📊 <strong>Unique vendors:</strong> {len(vdf)} | "
                f"Avg per vendor: ₹{vdf['total'].mean():,.0f}",
                accent="#38bdf8"
            )

    # ══════════════ ADVANCED ══════════════
    with tab_adv:
        st.markdown("#### 🔬 Spend Scatter — Time vs Amount")

        fig_sc = px.scatter(
            df_f, x="date", y="amount",
            color="category", size="amount",
            size_max=30, opacity=0.8
        )
        fig_sc.update_layout(**_PT)
        st.plotly_chart(fig_sc, use_container_width=True)

        # Scatter Summary
        if not df_f.empty:
            highest_txn = df_f.loc[df_f["amount"].idxmax()]
            _insight_card(
                f"🔬 <strong>Outlier Identification:</strong> Each bubble represents a receipt. "
                f"The largest bubble is your <strong>₹{highest_txn['amount']:,.2f}</strong> transaction at "
                f"<strong>{highest_txn['vendor']}</strong>. Spikes further up indicate expensive, isolated purchases.",
                accent="#38bdf8"
            )

        st.markdown("#### 📦 Transaction Distribution")
        fig_box = px.box(df_f, y="amount", points="all",
                         color_discrete_sequence=["#6C63FF"])
        fig_box.update_layout(**_PT,
                               title=get_text(lang, "transaction_distribution_title"))
        st.plotly_chart(fig_box, use_container_width=True)

        if not df_f.empty:
            q1  = df_f["amount"].quantile(0.25)
            q3  = df_f["amount"].quantile(0.75)
            med = df_f["amount"].median()
            iqr = q3 - q1
            thresh   = q3 + 1.5 * iqr
            outliers = df_f[df_f["amount"] > thresh]
            _insight_card(
                f"📊 <strong>Statistical Spread:</strong> 50% of your transactions fall between <strong>₹{q1:,.2f}</strong> and <strong>₹{q3:,.2f}</strong>. "
                f"Any points above the whiskers are statistically unusual (outliers), totaling <strong>{len(outliers)}</strong> high-value receipts.",
                accent="#6C63FF"
            )

        st.divider()
        st.markdown("#### 🔁 Recurring / Subscription Detection")
        subs = detect_subscriptions(df)
        if not subs.empty:
            st.dataframe(subs, use_container_width=True, hide_index=True)
            total_rec  = subs["avg_amount"].sum() if "avg_amount" in subs.columns else 0
            _insight_card(
                f"📊 <strong>Recurring payments detected:</strong> {len(subs)}<br>"
                f"💰 <strong>Estimated monthly cost:</strong> ₹{total_rec:,.2f}<br>"
                f"💡 <strong>Tip:</strong> Review and cancel any unused subscriptions.",
                accent="#10b981"
            )
        else:
            st.success("✅ No obvious recurring payments detected.")

    # ══════════════ AI INSIGHTS ══════════════
    with tab_ai:
        st.markdown("#### 🤖 AI-Powered Spending Analysis")

        api_key = st.session_state.get("GEMINI_API_KEY")
        if not api_key:
            st.markdown("""
<div style="
    background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.25);
    border-radius:14px;padding:2rem;text-align:center;
">
    <div style="font-size:3rem;margin-bottom:0.8rem;">🔑</div>
    <div style="color:#f1f5f9;font-size:1.05rem;font-weight:600;margin-bottom:0.4rem;">
        Gemini API Key Required
    </div>
    <div style="color:#94a3b8;font-size:0.9rem;">
        Enter your key in the sidebar to unlock AI-generated spending insights.
    </div>
</div>
""", unsafe_allow_html=True)
            return

        if st.button(get_text(lang, "generate_ai_report_btn"),
                     type="primary", use_container_width=True):
            with st.spinner(get_text(lang, "analyzing_ai")):
                try:
                    insight = generate_ai_insights(df_f, lang=lang)
                    st.session_state["ai_insights_cache"] = insight
                except Exception as e:
                    st.session_state["ai_insights_cache"] = f"❌ **Unexpected error:** {e}"

        if "ai_insights_cache" in st.session_state:
            cached = st.session_state["ai_insights_cache"]
            # If it's an error/warning message, use native streamlit component so markdown renders
            if cached.startswith("⚠️") or cached.startswith("⚠"):
                st.warning(cached)
            elif cached.startswith("❌"):
                st.error(cached)
            else:
                st.markdown(f"""
<div style="
    background:rgba(108,99,255,0.07);
    border:1px solid rgba(108,99,255,0.22);
    border-radius:14px;padding:1.8rem 2rem;
    color:#e2e8f0;line-height:1.8;margin-top:1rem;
">{cached}</div>
""", unsafe_allow_html=True)
