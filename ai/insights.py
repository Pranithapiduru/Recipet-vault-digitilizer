from ai.gemini_client import GeminiClient
import streamlit as st
from config.translations import get_text

def generate_ai_insights(df, lang="en") -> str:
    """
    Generate natural language spending insights using Gemini.
    """
    api_key = st.session_state.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ **Gemini API Key not found.** Please add it in the sidebar."

    try:
        client = GeminiClient(api_key)
        
        if df.empty:
            return get_text(lang, "no_data_analysis")

        total_spend = df["amount"].sum()
        transaction_count = len(df)
        
        top_vendor = df.groupby("vendor")["amount"].sum().idxmax() if not df.empty else "N/A"
        top_category = df.groupby("category")["amount"].sum().idxmax() if "category" in df.columns else "N/A"
        
        # Get last 5 transactions for context
        recent_tx = df.sort_values("date", ascending=False).head(5)[["date", "vendor", "amount", "category"]].to_string(index=False)
        
        lang_names = {
            "en": "English", "hi": "Hindi", "ta": "Tamil",
            "te": "Telugu", "bn": "Bengali", "mr": "Marathi"
        }
        target_lang = lang_names.get(lang, "English")

        summary_str = f"""
        Analyze this spending dataset and provide insights IN {target_lang.upper()}:
        
        Dataset Summary:
        - Total Spending: {total_spend:.2f}
        - Total Transactions: {transaction_count}
        - Top Vendor: {top_vendor}
        - Top Category: {top_category}
        - Date Range: {df["date"].min()} to {df["date"].max()}
        
        Recent Transactions:
        {recent_tx}
        
        Please provide 3-4 actionable insights or observations based on this data. Format the output with bullet points.
        """

        return client.generate_insights(summary_str)

    except RuntimeError as e:
        # RuntimeError carries our friendly formatted message from GeminiClient
        return str(e)
    except Exception as e:
        return f"❌ **Unexpected error:** {str(e)}"
