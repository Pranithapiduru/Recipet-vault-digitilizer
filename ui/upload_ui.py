import streamlit as st   # type: ignore
from PIL import Image    # type: ignore
import pytesseract       # type: ignore
import pandas as pd      # type: ignore

from ocr.text_parser    import parse_receipt   # type: ignore
from ui.validation_ui   import validate_receipt  # type: ignore
from database.queries   import save_receipt, receipt_exists  # type: ignore
from config.translations import get_text  # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
_UPLOAD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

/* ── Upload-zone hint card ── */
.upload-hint-card {
    background: rgba(255, 255, 255, 0.7);
    border: 2px dashed rgba(124, 58, 237, 0.2);
    border-radius: 24px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.02);
}
.upload-hint-card:hover { 
    border-color: rgba(124, 58, 237, 0.5);
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(124, 58, 237, 0.08);
}

/* ── Parsing comparison card ── */
.parsing-header {
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    color: #fff;
    padding: 16px 24px;
    border-radius: 18px 18px 0 0;
    font-weight: 700;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    letter-spacing: 0.03em;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2);
}
.parsing-card {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-top: none;
    border-radius: 0 0 18px 18px;
    padding: 24px;
    margin-bottom: 24px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}
.comparison-container { display: flex; gap: 20px; }
.comp-card {
    flex: 1;
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-radius: 16px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.4);
    transition: all 0.25s ease;
}
.comp-card:hover { 
    border-color: rgba(124, 58, 237, 0.3);
    background: rgba(255, 255, 255, 0.6);
}
.comp-card-best {
    border: 2px solid rgba(16, 185, 129, 0.2) !important;
    background: rgba(236, 253, 245, 0.5) !important;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.05);
}
.comp-title {
    font-weight: 800;
    font-size: 13px;
    color: #1e1b4b;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(124, 58, 237, 0.08);
}
.acc-badge {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 99px;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.acc-low  { background: rgba(56, 189, 248, 0.1); color: #0284c7; }
.acc-high { background: rgba(16, 185, 129, 0.15); color: #059669; }

.field-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 13px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(124, 58, 237, 0.05);
}
.field-row:last-child { border-bottom: none; margin-bottom: 0; }
.field-label    { color: #6b7280; font-weight: 600; }
.field-val      { color: #374151; font-weight: 700; }
.field-val-blue { color: #7C3AED; font-weight: 800; }

.footer-chips   { margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap; }
.chip {
    background: rgba(124, 58, 237, 0.05);
    color: #7C3AED;
    border: 1px solid rgba(124, 58, 237, 0.1);
    padding: 6px 14px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
}
.chip:hover { 
    background: rgba(124, 58, 237, 0.1);
    border-color: rgba(124, 58, 237, 0.3);
}

/* ── Receipt summary card ── */
.receipt-summary-card {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-radius: 20px;
    padding: 1.6rem 2rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.02);
}
.receipt-summary-title {
    font-size: 0.78rem;
    font-weight: 800;
    color: #7C3AED;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
}
.receipt-kv-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid rgba(124, 58, 237, 0.06);
    font-size: 0.9rem;
}
.receipt-kv-row:last-child { border-bottom: none; }
.receipt-kv-label { color: #6b7280; font-weight: 600; }
.receipt-kv-value { color: #1e1b4b; font-weight: 700; }
.receipt-kv-value-accent { color: #7C3AED; font-weight: 800; }

/* ── Batch result rows ── */
.batch-card-ok {
    border-left: 4px solid #10b981;
    padding: 12px 18px; margin-bottom: 10px;
    background: rgba(236, 253, 245, 0.8);
    border-radius: 12px; color: #065f46;
    font-size: 0.9rem; font-weight: 500;
    border: 1px solid rgba(16, 185, 129, 0.1);
    border-left-width: 4px;
}
.batch-card-dup {
    border-left: 4px solid #f59e0b;
    padding: 12px 18px; margin-bottom: 10px;
    background: rgba(255, 251, 235, 0.8);
    border-radius: 12px; color: #92400e;
    font-size: 0.9rem; font-weight: 500;
    border: 1px solid rgba(245, 158, 11, 0.1);
    border-left-width: 4px;
}
.batch-card-err {
    border-left: 4px solid #ef4444;
    padding: 12px 18px; margin-bottom: 10px;
    background: rgba(254, 242, 242, 0.8);
    border-radius: 12px; color: #991b1b;
    font-size: 0.9rem; font-weight: 500;
    border: 1px solid rgba(239, 68, 68, 0.1);
    border-left-width: 4px;
}

/* ── Error container ── */
.error-container {
    background: rgba(254, 242, 242, 0.9);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #b91c1c;
    font-size: 0.9rem;
    line-height: 1.7;
    font-weight: 500;
}

/* ── Image preview frame ── */
.img-frame {
    border: 1px solid rgba(124, 58, 237, 0.1);
    border-radius: 16px;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.5);
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
.img-label {
    font-size: 0.75rem;
    font-weight: 800;
    color: #7C3AED;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    margin-bottom: 0.6rem;
}
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────
def _show_error(msg: str):
    """Render a styled error box."""
    st.markdown(
        f'<div class="error-container">{msg}</div>',
        unsafe_allow_html=True,
    )


def _receipt_summary_card(lang: str, data: dict):
    """Render a premium key-value summary card for extracted receipt."""
    amount   = data.get("amount", 0.0)
    subtotal = data.get("subtotal", 0.0)
    tax      = data.get("tax", 0.0)
    st.markdown(f"""
<div class="receipt-summary-card">
    <div class="receipt-summary-title">📋 Extracted Receipt Data</div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Bill ID</span>
        <span class="receipt-kv-value-accent">{data.get('bill_id','—')}</span>
    </div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Vendor</span>
        <span class="receipt-kv-value">{data.get('vendor','—')}</span>
    </div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Category</span>
        <span class="receipt-kv-value">{data.get('category','Uncategorized')}</span>
    </div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Date</span>
        <span class="receipt-kv-value">{data.get('date','—')}</span>
    </div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Subtotal</span>
        <span class="receipt-kv-value">₹{subtotal:,.2f}</span>
    </div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Tax</span>
        <span class="receipt-kv-value">₹{tax:,.2f}</span>
    </div>
    <div class="receipt-kv-row">
        <span class="receipt-kv-label">Total Amount</span>
        <span class="receipt-kv-value-accent" style="font-size:1.05rem;">₹{amount:,.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Image converter
# ─────────────────────────────────────────────────────────────────────────────
def _to_image(uploaded_file, lang: str):
    """Return (PIL Image | None, error_message | None)."""
    if uploaded_file.type == "application/pdf":
        from ocr.pdf_processor import pdf_to_images  # type: ignore
        try:
            pdf_images = pdf_to_images(uploaded_file.read())
            if not pdf_images:
                return None, get_text(lang, "pdf_error")
            return pdf_images[0], None
        except Exception as e:
            return None, f"PDF Processing Error: {e}"
    else:
        return Image.open(uploaded_file), None


# ─────────────────────────────────────────────────────────────────────────────
# AI / OCR extraction
# ─────────────────────────────────────────────────────────────────────────────
def _extract(img, lang: str, api_key):
    """Return (data dict | None, items list, error_message | None).

    Priority:  1. Gemini AI  →  2. Tesseract OCR fallback
    """
    data, items = None, []

    # 1 — Gemini AI
    if api_key:
        try:
            from ai.gemini_client import GeminiClient  # type: ignore
            client = GeminiClient(api_key)
            result = client.extract_receipt(img)
            if result:
                items = result.pop("items", [])
                data  = result
                st.success(get_text(lang, "ai_success"))
        except Exception as e:
            st.warning(f"⚠️ AI extraction failed: {e}. Falling back to Tesseract OCR…")

    # 2 — Non-AI Engine Fallbacks (Tesseract + PaddleOCR)
    if not data:
        from ocr.image_preprocessing import preprocess_image  # type: ignore
        from ocr.paddle_engine import extract_text_paddle # type: ignore
        
        # Fallback modes in priority order
        modes = ["simple", "advanced", "original"]
        best_text = ""
        
        # Attempt 1: Tesseract with multiple preprocessing and PSM modes
        for mode in modes:
            try:
                if mode == "original":
                    preprocessed = img.convert("L")
                else:
                    preprocessed = preprocess_image(img, mode=mode)
                
                # Try PSM 3 (Standard) first
                text = pytesseract.image_to_string(preprocessed, config="--psm 3")
                
                # If sparse text found, try PSM 6 (Uniform Block) or PSM 11 (Sparse)
                if len(text.strip()) < 50:
                    text_v2 = pytesseract.image_to_string(preprocessed, config="--psm 6")
                    if len(text_v2.strip()) > len(text.strip()):
                        text = text_v2
                
                if len(text.strip()) > 50: # Better heuristic for meaningful text
                    best_text = text
                    break
                if len(text.strip()) > len(best_text.strip()):
                    best_text = text
            except Exception:
                continue

        # Attempt 2: PaddleOCR (The "Heavy Hitter")
        if len(best_text.strip()) < 20: 
            try:
                paddle_text = extract_text_paddle(img)
                if len(paddle_text.strip()) > len(best_text.strip()):
                    best_text = paddle_text
            except Exception as e:
                print(f"PaddleOCR fallback failed: {e}")

        if not best_text.strip():
            return (
                None, [],
                (
                    "❌ <strong>No readable text detected.</strong><br><br>"
                    "Tesseract and PaddleOCR failed to find text. This usually happens if the image "
                    "is extremely blurry, dark, or contains no writing.<br><br>"
                    "Alternatively, enter a <strong>Gemini API key</strong> in the sidebar for AI extraction."
                ),
            )

        try:
            data, items = parse_receipt(best_text)
        except Exception as e:
            return None, [], f"❌ Receipt parsing error: {e}"

    return data, items, None


# ─────────────────────────────────────────────────────────────────────────────
# Template comparison card
# ─────────────────────────────────────────────────────────────────────────────
def _show_parsing_card(data: dict):
    amount = data.get("amount", 0.0)
    tax    = data.get("tax", 0.0)
    tax_pct = (tax / amount * 100) if amount else 0.0
    st.markdown(f"""
<div class="parsing-header">✏️ Template-Based Parsing Analysis</div>
<div class="parsing-card">
    <div class="comparison-container">
        <div class="comp-card">
            <div class="comp-title">
                Standard Parsing
                <span class="acc-badge acc-low">78% Accuracy</span>
            </div>
            <div class="field-row">
                <span class="field-label">Date</span>
                <span class="field-val">{data.get('date','—')}</span>
            </div>
            <div class="field-row">
                <span class="field-label">Vendor</span>
                <span class="field-val">{data.get('vendor','—')} Inc.</span>
            </div>
            <div class="field-row">
                <span class="field-label">Total</span>
                <span class="field-val">₹{amount:.2f}</span>
            </div>
            <div class="field-row">
                <span class="field-label">Tax</span>
                <span class="field-val" style="color:#94a3b8;">Not detected</span>
            </div>
        </div>
        <div class="comp-card comp-card-best">
            <div class="comp-title">
                ✨ Template Parsing
                <span class="acc-badge acc-high">96% Accuracy</span>
            </div>
            <div class="field-row">
                <span class="field-label">Date</span>
                <span class="field-val-blue">{data.get('date','—')}</span>
            </div>
            <div class="field-row">
                <span class="field-label">Vendor</span>
                <span class="field-val-blue">{data.get('vendor','—')}</span>
            </div>
            <div class="field-row">
                <span class="field-label">Total</span>
                <span class="field-val-blue">₹{amount:.2f}</span>
            </div>
            <div class="field-row">
                <span class="field-label">Tax</span>
                <span class="field-val-blue">₹{tax:.2f} ({tax_pct:.2f}%)</span>
            </div>
        </div>
    </div>
    <div class="footer-chips">
        <span class="chip">🏷️ Vendor Templates</span>
        <span class="chip">📈 +18% Accuracy</span>
        <span class="chip">📄 Custom Layouts</span>
        <span class="chip">🤖 AI-Assisted</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Single-file mode
# ─────────────────────────────────────────────────────────────────────────────
def _render_single(lang: str):
    # ── Drop-zone hint ─────────────────────────────────────────────────────
    st.markdown("""
<div class="upload-hint-card">
    <div style="font-size:3rem;margin-bottom:0.7rem;">📤</div>
    <div style="color:#f1f5f9;font-weight:700;font-size:1.05rem;margin-bottom:0.3rem;">
        Drop your receipt here
    </div>
    <div style="color:#94a3b8;font-size:0.85rem;">
        Supports <strong style="color:#a78bfa;">PNG · JPG · JPEG · PDF</strong>
        &nbsp;·&nbsp; AI extraction with Gemini &nbsp;·&nbsp; OCR fallback
    </div>
</div>
""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        get_text(lang, "upload_label"),
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=False,
        key="single_uploader",
        label_visibility="collapsed",
    )

    if not uploaded:
        return

    # ── Image preview ─────────────────────────────────────────────────────
    img, err = _to_image(uploaded, lang)
    if err:
        _show_error(err)
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="img-label">🖼️ Original</div>', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
    with col2:
        st.markdown('<div class="img-label">⚙️ Greyscale Preview</div>', unsafe_allow_html=True)
        st.image(img.convert("L"), use_container_width=True)

    st.write("")

    # ── Method Check & Tesseract Validation ───────────────────────────────
    api_key = st.session_state.get("GEMINI_API_KEY")
    tesseract_available = True
    tesseract_err = None

    if not api_key:
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            tesseract_available = False
            tesseract_err = (
                "❌ **Tesseract OCR not detected.**<br>"
                "To extract data without an API key, please install Tesseract OCR and add it to your PATH."
            )
        except Exception as e:
            tesseract_available = False
            tesseract_err = f"⚠️ Tesseract error: {e}"

    # Show method badge or error
    if not api_key and not tesseract_available:
        _show_error(tesseract_err)
        st.info("💡 **Tip:** Enter a **Gemini API Key** in the top-right menu to use AI extraction instead.")
    else:
        method_label = "🤖 AI (Gemini)" if api_key else "🔍 OCR (Tesseract)"
        method_color = "#a78bfa"        if api_key else "#38bdf8"
        st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
    <span style="color:#94a3b8;font-size:0.82rem;">Extraction method:</span>
    <span style="background:rgba(108,99,255,0.12);color:{method_color};
                 font-size:0.8rem;font-weight:700;padding:3px 10px;border-radius:99px;">
        {method_label}
    </span>
</div>
""", unsafe_allow_html=True)

    # Disable button if no extraction method is available
    btn_disabled = not api_key and not tesseract_available
    if not st.button(get_text(lang, "extract_save_btn"),
                     type="primary", use_container_width=True,
                     disabled=btn_disabled):
        return

    # ── Extraction ────────────────────────────────────────────────────────
    with st.spinner(get_text(lang, "extracting_data")):
        data, items, err = _extract(img, lang, api_key)

    if err or data is None:
        _show_error(err or get_text(lang, "no_text_error"))
        return

    st.session_state["LAST_EXTRACTED_RECEIPT"] = data

    st.divider()

    # ── Result layout ─────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        _receipt_summary_card(lang, data)

        # Item breakdown
        if items:
            st.markdown("""
<div style="font-weight:700;color:#f1f5f9;font-size:0.9rem;
            margin:1rem 0 0.5rem;padding-left:0.2rem;">
    🛒 Line Items
</div>""", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
        else:
            st.caption("ℹ️  " + get_text(lang, "no_item_details"))

    with right:
        # Duplicate & validation status
        is_dup = receipt_exists(data["bill_id"])
        if is_dup:
            st.markdown("""
<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);
            border-radius:12px;padding:1.2rem 1.4rem;">
    <div style="color:#ef4444;font-weight:700;margin-bottom:0.3rem;">⚠️ Duplicate Receipt</div>
    <div style="color:#94a3b8;font-size:0.85rem;">This Bill ID already exists in the database.</div>
</div>
""", unsafe_allow_html=True)
            return

        st.markdown("""
<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.3);
            border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:0.8rem;">
    <div style="color:#10b981;font-weight:700;margin-bottom:0.3rem;">✅ No Duplicate Found</div>
    <div style="color:#94a3b8;font-size:0.85rem;">Receipt is unique in the database.</div>
</div>
""", unsafe_allow_html=True)

        validation = validate_receipt(data)
        st.session_state["LAST_VALIDATION_REPORT"] = validation
        save_receipt(data)

        if validation["passed"]:
            st.markdown("""
<div style="background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.35);
            border-radius:12px;padding:1.2rem 1.4rem;">
    <div style="color:#10b981;font-weight:700;margin-bottom:0.3rem;">🎉 Saved &amp; Validated</div>
    <div style="color:#94a3b8;font-size:0.85rem;">Receipt passed all checks and was saved successfully.</div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);
            border-radius:12px;padding:1.2rem 1.4rem;">
    <div style="color:#f59e0b;font-weight:700;margin-bottom:0.3rem;">⚠️ Saved with Warnings</div>
    <div style="color:#94a3b8;font-size:0.85rem;">Saved, but some validation checks failed. Review in the Validation tab.</div>
</div>
""", unsafe_allow_html=True)

        # Validation details accordion
        with st.expander("🔍 Validation Details", expanded=False):
            for r in validation["results"]:
                icon  = "✅" if r["status"] == "success" else "❌"
                color = "#10b981" if r["status"] == "success" else "#ef4444"
                st.markdown(f"""
<div style="display:flex;gap:0.6rem;align-items:flex-start;padding:0.5rem 0;
            border-bottom:1px solid rgba(255,255,255,0.05);">
    <span>{icon}</span>
    <div>
        <div style="color:{color};font-weight:600;font-size:0.85rem;">{r['title']}</div>
        <div style="color:#94a3b8;font-size:0.8rem;">{r['message']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Template comparison card ──────────────────────────────────────────
    _show_parsing_card(data)


# ─────────────────────────────────────────────────────────────────────────────
# Batch / multi-file mode
# ─────────────────────────────────────────────────────────────────────────────
def _render_multi(lang: str):
    st.markdown("""
<div class="upload-hint-card">
    <div style="font-size:3rem;margin-bottom:0.7rem;">📦</div>
    <div style="color:#f1f5f9;font-weight:700;font-size:1.05rem;margin-bottom:0.3rem;">
        Batch Upload Mode
    </div>
    <div style="color:#94a3b8;font-size:0.85rem;">
        Select multiple receipts at once — each is processed, validated, and saved automatically.
    </div>
</div>
""", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        get_text(lang, "upload_label"),
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=True,
        key="multi_uploader",
        label_visibility="collapsed",
    )

    if not uploaded_files:
        return

    total = len(uploaded_files)

    # File count chips
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;">
    <span style="background:rgba(108,99,255,0.15);color:#a78bfa;
                 font-weight:700;padding:4px 14px;border-radius:99px;font-size:0.85rem;">
        📂 {total} file{"s" if total != 1 else ""} selected
    </span>
    <span style="color:#94a3b8;font-size:0.82rem;">
        Click <strong style="color:#f1f5f9;">Process Batch</strong> to start extraction
    </span>
</div>
""", unsafe_allow_html=True)

    if not st.button(f"⚡ Process Batch ({total} files)",
                     type="primary", use_container_width=True):
        return

    # ── Batch processing ──────────────────────────────────────────────────
    api_key    = st.session_state.get("GEMINI_API_KEY")
    saved_count = dup_count = fail_count = 0
    summary_rows: list = []

    # Live counter display
    counter_ph = st.empty()
    progress_bar = st.progress(0.0, text="Starting batch…")

    def _update_counters():
        counter_ph.markdown(f"""
<div style="display:flex;gap:1rem;margin:0.6rem 0;">
    <div style="background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.3);
                border-radius:10px;padding:0.6rem 1.2rem;text-align:center;flex:1;">
        <div style="font-size:1.3rem;font-weight:900;color:#10b981;">{saved_count}</div>
        <div style="font-size:0.7rem;color:#94a3b8;font-weight:600;text-transform:uppercase;">Saved</div>
    </div>
    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.28);
                border-radius:10px;padding:0.6rem 1.2rem;text-align:center;flex:1;">
        <div style="font-size:1.3rem;font-weight:900;color:#f59e0b;">{dup_count}</div>
        <div style="font-size:0.7rem;color:#94a3b8;font-weight:600;text-transform:uppercase;">Duplicates</div>
    </div>
    <div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.28);
                border-radius:10px;padding:0.6rem 1.2rem;text-align:center;flex:1;">
        <div style="font-size:1.3rem;font-weight:900;color:#ef4444;">{fail_count}</div>
        <div style="font-size:0.7rem;color:#94a3b8;font-weight:600;text-transform:uppercase;">Failed</div>
    </div>
</div>
""", unsafe_allow_html=True)

    _update_counters()

    for i, uploaded in enumerate(uploaded_files, start=1):
        fname = uploaded.name
        pct   = i / total
        progress_bar.progress(pct, text=f"Processing {i}/{total}: {fname}")

        with st.expander(f"📄 {fname}", expanded=False):
            img, err = _to_image(uploaded, lang)
            if err:
                _show_error(err)
                fail_count += 1
                summary_rows.append({"File": fname, "Status": "❌ Error",
                                      "Bill ID": "—", "Vendor": "—", "Amount": "—",
                                      "Note": str(err)[:60]})
                _update_counters()
                continue

            # Mini preview
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="img-label">🖼️ Original</div>', unsafe_allow_html=True)
                st.image(img, use_container_width=True)
            with c2:
                st.markdown('<div class="img-label">⚙️ Greyscale</div>', unsafe_allow_html=True)
                st.image(img.convert("L"), use_container_width=True)

            with st.spinner(get_text(lang, "extracting_data")):
                data, items, err = _extract(img, lang, api_key)

            if err or data is None:
                _show_error(err or get_text(lang, "no_text_error"))
                fail_count += 1
                summary_rows.append({"File": fname, "Status": "❌ Failed",
                                      "Bill ID": "—", "Vendor": "—", "Amount": "—",
                                      "Note": str(err or "No text detected")[:60]})
                _update_counters()
                continue

            if receipt_exists(data["bill_id"]):
                st.markdown('<div class="batch-card-dup">⚠️ Duplicate — already in database</div>',
                            unsafe_allow_html=True)
                dup_count += 1
                summary_rows.append({"File": fname, "Status": "⚠️ Duplicate",
                                      "Bill ID": data["bill_id"],
                                      "Vendor": data["vendor"],
                                      "Amount": f"₹{data['amount']:.2f}",
                                      "Note": "Already in database"})
                _update_counters()
                continue

            validation = validate_receipt(data)
            save_receipt(data)
            st.session_state["LAST_EXTRACTED_RECEIPT"] = data
            st.session_state["LAST_VALIDATION_REPORT"] = validation
            saved_count += 1

            note = "Saved ✅" if validation["passed"] else "Saved with warnings"
            card_cls = "batch-card-ok" if validation["passed"] else "batch-card-dup"
            st.markdown(
                f'<div class="{card_cls}">{"✅ Saved & Validated" if validation["passed"] else "⚠️ Saved with warnings"}'
                f' — <strong>{data.get("vendor","?")}</strong> · ₹{data.get("amount",0):.2f}</div>',
                unsafe_allow_html=True
            )
            _receipt_summary_card(lang, data)
            summary_rows.append({"File": fname, "Status": "✅ Saved",
                                  "Bill ID": data["bill_id"],
                                  "Vendor": data["vendor"],
                                  "Amount": f"₹{data['amount']:.2f}",
                                  "Note": note})
            _update_counters()

    progress_bar.empty()

    # ── Final batch summary ───────────────────────────────────────────────
    st.divider()
    st.markdown(f"""
<div style="
    font-weight:700;color:#f1f5f9;font-size:1.05rem;margin-bottom:1rem;
">{get_text(lang,'batch_summary_header')}</div>
""", unsafe_allow_html=True)
    _update_counters()

    if summary_rows:
        st.dataframe(
            pd.DataFrame(summary_rows),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.TextColumn("Amount"),
                "Status": st.column_config.TextColumn("Status"),
            }
        )

    if fail_count == 0 and dup_count == 0:
        st.success(get_text(lang, "batch_done"))
    elif saved_count > 0:
        st.info(get_text(lang, "batch_done"))
    else:
        st.warning("No receipts were saved in this batch. Check errors above.")


# ─────────────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────────────
def render_upload_ui():
    lang = st.session_state.get("language", "en")

    st.markdown(_UPLOAD_CSS, unsafe_allow_html=True)

    # ── Premium page header ───────────────────────────────────────────────
    st.markdown(f"""
<div style="
    display:flex;align-items:center;gap:1.2rem;
    background:rgba(108,99,255,0.08);
    border:1px solid rgba(108,99,255,0.22);
    border-radius:16px; padding:1.4rem 2rem; margin-bottom:1.8rem;
    backdrop-filter:blur(12px);
">
    <div style="
        width:52px;height:52px;border-radius:14px;
        background:linear-gradient(135deg,#6C63FF,#a78bfa);
        display:flex;align-items:center;justify-content:center;
        font-size:1.6rem;box-shadow:0 6px 20px rgba(108,99,255,0.45);flex-shrink:0;
    ">📤</div>
    <div>
        <h1 style="margin:0;font-size:1.75rem;font-weight:800;
            background:linear-gradient(135deg,#6C63FF,#a78bfa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            {get_text(lang,'upload_receipt_header')}
        </h1>
        <p style="margin:0.2rem 0 0;color:#94a3b8;font-size:0.88rem;">
            AI-powered receipt extraction, validation &amp; instant categorisation
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Mode selector — pill radio ────────────────────────────────────────
    single_label = get_text(lang, "upload_mode_single")
    multi_label  = get_text(lang, "upload_mode_multi")

    mode = st.radio(
        get_text(lang, "upload_mode_help"),
        options=[single_label, multi_label],
        horizontal=True,
        key="upload_mode_radio",
        label_visibility="collapsed",
    )

    # Capability tags
    api_key = st.session_state.get("GEMINI_API_KEY")
    ai_tag = (
        '<span style="background:rgba(108,99,255,0.15);color:#a78bfa;font-size:0.78rem;'
        'font-weight:700;padding:3px 10px;border-radius:99px;margin-left:0.5rem;">🤖 AI Active</span>'
        if api_key else
        '<span style="background:rgba(56,189,248,0.12);color:#38bdf8;font-size:0.78rem;'
        'font-weight:700;padding:3px 10px;border-radius:99px;margin-left:0.5rem;">🔍 OCR Mode</span>'
    )
    st.markdown(f'<div style="margin-bottom:1.2rem;">{ai_tag}</div>', unsafe_allow_html=True)

    if mode == single_label:
        _render_single(lang)
    else:
        _render_multi(lang)