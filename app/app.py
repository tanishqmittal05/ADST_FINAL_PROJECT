import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Instagram Reach Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Global Dark Theme Design System (CSS)
# Inspired by Linear, Vercel Analytics, and Stripe Dashboard
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Background and Layout */
    .stApp {
        background-color: #0B1020;
        color: #F3F4F6;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }

    /* Clean subtle scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0B1020;
    }
    ::-webkit-scrollbar-thumb {
        background: #1F293D;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3B82F6;
    }

    /* Top Navigation / Header */
    .dashboard-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.85) 0%, rgba(15, 23, 42, 0.6) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 1.1rem;
    }
    .header-logo {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        background: linear-gradient(135deg, #3B82F6 0%, #22D3EE 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.35);
    }
    .header-title-box h1 {
        margin: 0;
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        background: linear-gradient(180deg, #FFFFFF 0%, #E2E8F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-title-box p {
        margin: 0.2rem 0 0 0;
        font-size: 0.86rem;
        color: #94A3B8;
        font-weight: 400;
    }
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.25);
        font-size: 0.78rem;
        font-weight: 600;
        color: #4ADE80;
    }
    .badge-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #22C55E;
        box-shadow: 0 0 8px #22C55E;
    }

    /* Section Headers */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin-top: 1.8rem;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 1.25rem;
        font-weight: 400;
    }

    /* Metric Cards */
    .kpi-card {
        background: linear-gradient(145deg, #111827 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1.35rem 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .kpi-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    .kpi-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .kpi-icon-box {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(59, 130, 246, 0.12);
        color: #3B82F6;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin-bottom: 0.45rem;
        font-feature-settings: "tnum" 1;
    }
    .kpi-subtext {
        font-size: 0.78rem;
        color: #64748B;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .kpi-tag-positive {
        color: #22C55E;
        background: rgba(34, 197, 94, 0.12);
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.72rem;
    }

    /* Chart Container Card */
    .card-wrapper {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.25rem;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-desc {
        font-size: 0.8rem;
        color: #64748B;
        margin-bottom: 1rem;
    }

    /* Streamlit Form & Controls Polish */
    div[data-testid="stForm"] {
        background: #111827;
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 1.75rem 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    
    div[data-testid="stForm"] hr {
        border-color: rgba(255, 255, 255, 0.08);
    }

    label[data-testid="stWidgetLabel"] p {
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        letter-spacing: -0.01em;
    }

    /* Input Fields */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div {
        background-color: #0F172A !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: #3B82F6 !important;
    }

    /* Primary Predict Button */
    button[kind="primaryFormSubmit"], 
    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Prediction Result Showcase Cards */
    .rec-hero-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
        height: 100%;
    }
    .rec-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        background: rgba(34, 211, 238, 0.15);
        border: 1px solid rgba(34, 211, 238, 0.3);
        color: #22D3EE;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
    }
    .rec-highlight-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #22D3EE;
        margin: 0.2rem 0;
        letter-spacing: -0.02em;
    }
    .rec-reach-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4ADE80;
        margin: 0.3rem 0 0.8rem 0;
    }
    .rec-desc {
        font-size: 0.84rem;
        color: #94A3B8;
        line-height: 1.5;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 0.8rem;
        margin-top: 0.8rem;
    }

    /* Insights Banner */
    .insight-pill-group {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
    }
    .insight-pill {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.75rem 1.1rem;
        flex: 1;
        min-width: 250px;
    }
    .insight-pill-label {
        font-size: 0.74rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .insight-pill-value {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F1F5F9;
        margin-top: 0.2rem;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 9px !important;
        padding: 0.5rem 1.2rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background-color: rgba(56, 189, 248, 0.1) !important;
        border-color: #38BDF8 !important;
        transform: translateY(-1px);
    }

    /* Streamlit Alert / Notification Overrides */
    div[data-testid="stAlert"] {
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background-color: #111827;
    }

    /* Dataframe container padding */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Matplotlib & Seaborn Dark Theme Harmonization
# ---------------------------------------------------------
BG_COLOR = "#111827"
PANEL_COLOR = "#0F172A"
TEXT_COLOR = "#E2E8F0"
MUTED_TEXT = "#94A3B8"
GRID_COLOR = "#1E293B"

plt.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': PANEL_COLOR,
    'axes.edgecolor': GRID_COLOR,
    'axes.labelcolor': MUTED_TEXT,
    'xtick.color': MUTED_TEXT,
    'ytick.color': MUTED_TEXT,
    'grid.color': GRID_COLOR,
    'grid.alpha': 0.6,
    'grid.linestyle': '--',
    'text.color': TEXT_COLOR,
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10
})

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# Data & Model Loader
# ---------------------------------------------------------
@st.cache_data
def load_data():
    data_path = BASE_DIR / "data" / "processed" / "processed_data.csv"
    if data_path.exists():
        return pd.read_csv(data_path)
    return None

@st.cache_resource
def load_model():
    model_path = BASE_DIR / "models" / "final_model.joblib"
    if model_path.exists():
        return joblib.load(model_path)
    return None

df = load_data()
model = load_model()

# ---------------------------------------------------------
# Dashboard Header
# ---------------------------------------------------------
st.markdown("""
<div class="dashboard-header">
    <div class="header-left">
        <div class="header-logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
        </div>
        <div class="header-title-box">
            <h1>Instagram Reach Intelligence</h1>
            <p>Data-driven audience engagement analytics & optimal posting time engine</p>
        </div>
    </div>
    <div class="header-badge">
        <span class="badge-dot"></span>
        Production Model Active
    </div>
</div>
""", unsafe_allow_html=True)

if df is not None and model is not None:
    # ---------------------------------------------------------
    # 1. KPI Metric Section
    # ---------------------------------------------------------
    total_posts = len(df)
    avg_reach = int(df['Reach'].mean())
    day_reach_means = df.groupby('day_name')['Reach'].mean()
    best_day = day_reach_means.idxmax()
    best_day_val = int(day_reach_means.max())
    delta_vs_avg = int(((best_day_val - avg_reach) / avg_reach) * 100) if avg_reach else 0

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-label">Total Posts Analyzed</span>
                <div class="kpi-icon-box">
                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path d="M4 6h16M4 12h16m-7 6h7"></path>
                    </svg>
                </div>
            </div>
            <div class="kpi-value">{total_posts:,}</div>
            <div class="kpi-subtext">
                <span class="kpi-tag-positive">Verified</span> Full verified historical dataset
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-label">Average Reach</span>
                <div class="kpi-icon-box" style="background: rgba(34, 211, 238, 0.12); color: #22D3EE; border-color: rgba(34, 211, 238, 0.25);">
                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                    </svg>
                </div>
            </div>
            <div class="kpi-value">{avg_reach:,}</div>
            <div class="kpi-subtext">
                <span class="kpi-tag-positive">Mean</span> Unique accounts reached per post
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-label">Best Performing Day</span>
                <div class="kpi-icon-box" style="background: rgba(34, 197, 94, 0.12); color: #22C55E; border-color: rgba(34, 197, 94, 0.25);">
                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                </div>
            </div>
            <div class="kpi-value">{best_day}</div>
            <div class="kpi-subtext">
                <span class="kpi-tag-positive">+{delta_vs_avg}%</span> {best_day_val:,} avg reach vs mean
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. Historical Data Insights
    # ---------------------------------------------------------
    st.markdown("""
    <div class="section-title">
        <svg width="20" height="20" fill="none" stroke="#3B82F6" stroke-width="2" viewBox="0 0 24 24">
            <path d="M18 20V10M12 20V4M6 20v-6"></path>
        </svg>
        Historical Performance Analytics
    </div>
    <div class="section-subtitle">Empirical reach distributions grouped by posting schedule and creative format</div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        st.markdown("""
        <div class="card-title">Average Reach by Day of Week</div>
        <div class="card-desc">Weekly cadence comparison based on historical distribution</div>
        """, unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(6.2, 4.2))
        order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Coordinated SaaS gradient palette: Cyan to Blue
        day_palette = ["#22D3EE", "#38BDF8", "#3B82F6", "#2563EB", "#1D4ED8", "#4ADE80", "#22C55E"]
        
        sns.barplot(
            x="day_name",
            y="Reach",
            data=df,
            order=order,
            ax=ax,
            palette=day_palette,
            ci=None,
            edgecolor=None
        )
        
        ax.set_ylabel("Average Reach", color=MUTED_TEXT, fontsize=10, labelpad=8)
        ax.set_xlabel("", visible=False)
        ax.tick_params(axis='x', rotation=30, labelsize=9.5)
        ax.tick_params(axis='y', labelsize=9.5)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
        ax.grid(axis='y', linestyle='--', alpha=0.35, color=GRID_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(GRID_COLOR)
        ax.spines['bottom'].set_color(GRID_COLOR)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with colB:
        st.markdown("""
        <div class="card-title">Average Reach by Content Format</div>
        <div class="card-desc">Creative format impact across Carousels, Reels, Images, and Stories</div>
        """, unsafe_allow_html=True)
        
        fig2, ax2 = plt.subplots(figsize=(6.2, 4.2))
        
        # Distinct modern palette for content types
        post_palette = ["#3B82F6", "#22D3EE", "#10B981", "#6366F1"]
        
        sns.barplot(
            x="Post Type",
            y="Reach",
            data=df,
            ax=ax2,
            palette=post_palette,
            ci=None,
            edgecolor=None
        )
        
        ax2.set_ylabel("Average Reach", color=MUTED_TEXT, fontsize=10, labelpad=8)
        ax2.set_xlabel("", visible=False)
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=9.5)
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
        ax2.grid(axis='y', linestyle='--', alpha=0.35, color=GRID_COLOR)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color(GRID_COLOR)
        ax2.spines['bottom'].set_color(GRID_COLOR)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)

    # ---------------------------------------------------------
    # 3. Post Predictor & Recommendation Engine
    # ---------------------------------------------------------
    st.markdown("""
    <div class="section-title">
        <svg width="20" height="20" fill="none" stroke="#22D3EE" stroke-width="2" viewBox="0 0 24 24">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
        AI Post Predictor & Day Optimization Engine
    </div>
    <div class="section-subtitle">Simulate content parameters across all 7 days to identify maximum audience engagement</div>
    """, unsafe_allow_html=True)

    with st.form("predictor_form"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            post_type = st.selectbox(
                "Post Type / Format",
                options=df["Post Type"].unique(),
                help="Select the media creative format for the planned post"
            )
            campaign_type = st.selectbox(
                "Campaign Objective",
                options=df["Campaign Type"].unique(),
                help="Select the promotional theme or campaign purpose"
            )
            hashtag_count = st.number_input(
                "Number of Hashtags",
                min_value=0,
                max_value=30,
                value=5,
                step=1,
                help="Number of relevant hashtags attached to the caption"
            )
        with p_col2:
            target_month = st.slider(
                "Target Month of Publication",
                min_value=1,
                max_value=12,
                value=6,
                format="Month %d",
                help="Month index (1 = January, 12 = December)"
            )
            
            # Interactive contextual note inside form
            month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            st.caption(f"📅 Target Publication Month: **{month_names[target_month - 1]}** (Seasonal adjustments will be factored into the model)")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("⚡ Predict Reach & Recommend Day")

    if submit:
        # Evaluate for all 7 days
        days_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        predictions = []
        
        for day_num, day_name in days_map.items():
            weekend_flag = 1 if day_num >= 5 else 0
            features = pd.DataFrame([{
                "day_of_week": day_num,
                "is_weekend": weekend_flag,
                "month": target_month,
                "Post Type": post_type,
                "Campaign Type": campaign_type,
                "hashtag_count": hashtag_count
            }])
            
            pred = model.predict(features)[0]
            predictions.append({"Day": day_name, "Predicted Reach": int(pred)})
            
        results_df = pd.DataFrame(predictions)
        results_df["Rank"] = results_df["Predicted Reach"].rank(method="min", ascending=False).astype(int)
        results_df = results_df.sort_values("Rank").reset_index(drop=True)
        
        best_day_rec = results_df.iloc[0]["Day"]
        best_reach_rec = results_df.iloc[0]["Predicted Reach"]
        baseline_diff = int(best_reach_rec - avg_reach)
        diff_pct = (baseline_diff / avg_reach) * 100 if avg_reach else 0
        diff_sign = "+" if baseline_diff >= 0 else ""

        # --- PREDICTION RESULT & RECOMMENDATION ---
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        r_col1, r_col2 = st.columns([1.1, 1.3])
        with r_col1:
            st.markdown(f"""
            <div class="rec-hero-card">
                <span class="rec-badge">Optimization Verdict</span>
                <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">Optimal Publishing Day</div>
                <div class="rec-highlight-val">{best_day_rec}</div>
                <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.8rem;">Maximum Estimated Reach</div>
                <div class="rec-reach-val">{best_reach_rec:,} accounts</div>
                <div class="rec-desc">
                    <span style="color: {'#22C55E' if baseline_diff >= 0 else '#EF4444'}; font-weight: 600;">
                        {diff_sign}{diff_pct:.1f}% ({diff_sign}{baseline_diff:,} reach)
                    </span> vs historical account average ({avg_reach:,}).<br><br>
                    Based on machine learning predictions with {post_type} format and {campaign_type} campaign in Month {target_month}, 
                    <strong>{best_day_rec}</strong> maximizes expected organic reach.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with r_col2:
            st.markdown("""
            <div class="card-title" style="margin-bottom: 0.75rem;">
                Weekly Schedule Comparison
            </div>
            """, unsafe_allow_html=True)
            
            # Formatted table of alternatives
            display_table = results_df[["Rank", "Day", "Predicted Reach"]].copy()
            st.dataframe(
                display_table.style.format({"Predicted Reach": "{:,}"}).background_gradient(
                    subset=["Predicted Reach"], cmap="Blues"
                ),
                use_container_width=True,
                height=225
            )
            
        # --- TIME COMPARISON LINE CHART ---
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card-title">Predicted Reach Trajectory across Weekdays</div>
        <div class="card-desc">Day-by-day simulated reach curve for this specific configuration</div>
        """, unsafe_allow_html=True)
        
        # Ensure chronological ordering Monday -> Sunday for the line plot
        chronological_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        plot_df = results_df.set_index("Day").reindex(chronological_days).reset_index()

        fig3, ax3 = plt.subplots(figsize=(10.5, 3.4))
        
        # Plot styled line with glowing points
        ax3.plot(
            plot_df["Day"],
            plot_df["Predicted Reach"],
            color="#38BDF8",
            linewidth=2.5,
            marker='o',
            markersize=7,
            markerfacecolor="#22D3EE",
            markeredgecolor="#0B1020",
            markeredgewidth=2
        )
        
        # Highlight best day on chart
        best_row = plot_df[plot_df["Day"] == best_day_rec].iloc[0]
        ax3.scatter([best_row["Day"]], [best_row["Predicted Reach"]], color="#22C55E", s=130, zorder=5, label=f"Recommended ({best_day_rec})")
        
        # Horizontal baseline of average reach
        ax3.axhline(avg_reach, color="#64748B", linestyle=":", alpha=0.65, label=f"Dataset Avg ({avg_reach:,})")

        ax3.set_ylabel("Predicted Reach", color=MUTED_TEXT, fontsize=9.5)
        ax3.tick_params(axis='x', labelsize=9.5)
        ax3.tick_params(axis='y', labelsize=9)
        ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
        ax3.grid(True, linestyle='--', alpha=0.25, color=GRID_COLOR)
        ax3.legend(facecolor=PANEL_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR, fontsize=8.5, loc="lower right")
        
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_color(GRID_COLOR)
        ax3.spines['bottom'].set_color(GRID_COLOR)
        
        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)

    # ---------------------------------------------------------
    # 4. Data Explorer & Key Insights
    # ---------------------------------------------------------
    st.markdown("""
    <div class="section-title">
        <svg width="20" height="20" fill="none" stroke="#A78BFA" stroke-width="2" viewBox="0 0 24 24">
            <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
        </svg>
        Dataset Explorer & Key Insights
    </div>
    <div class="section-subtitle">Inspect processed training records, evaluate correlation factors, and export tabular data</div>
    """, unsafe_allow_html=True)

    best_content_format = df.groupby('Post Type')['Reach'].mean().idxmax()
    best_campaign = df.groupby('Campaign Type')['Reach'].mean().idxmax()

    st.markdown(f"""
    <div class="insight-pill-group">
        <div class="insight-pill">
            <div class="insight-pill-label">Top Content Format</div>
            <div class="insight-pill-value" style="color: #38BDF8;">{best_content_format}</div>
        </div>
        <div class="insight-pill">
            <div class="insight-pill-label">Top Campaign Strategy</div>
            <div class="insight-pill-value" style="color: #A78BFA;">{best_campaign}</div>
        </div>
        <div class="insight-pill">
            <div class="insight-pill-label">Overall Peak Day</div>
            <div class="insight-pill-value" style="color: #4ADE80;">{best_day}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data Table View
    st.dataframe(df.head(100), use_container_width=True, height=330)

    # Download Button with clear styling
    col_dl1, col_dl2 = st.columns([1, 4])
    with col_dl1:
        st.download_button(
            label="⬇ Download Processed CSV",
            data=df.to_csv(index=False),
            file_name='processed_instagram_data.csv',
            mime='text/csv',
            help="Export the clean processed dataset containing all 50,000 records"
        )
else:
    st.error("Data or model not found. Please ensure the machine learning pipeline has been executed.")
