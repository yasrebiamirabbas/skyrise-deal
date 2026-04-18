import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import os

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="ALMOHALENIN | Strategic Proposal", layout="wide")

# 2. Complete White-Labeling & Mobile Readability CSS
st.markdown("""
    <style>
    /* 100% White-Labeling: Hide all Streamlit UI elements */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QS1 {display: none;}
    
    /* Box Readability: High Contrast White on Dark for Values */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.6rem, 5vw, 2.8rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.9);
    }
    /* Gold Labels for distinction */
    [data-testid="stMetricLabel"] { 
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important; 
        color: #D4AF37 !important; 
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Metric Box Container */
    .stMetric { 
        background-color: #11141d; 
        border: 2px solid #D4AF37; 
        padding: 25px 10px !important; 
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Logic Box for mobile */
    .logic-box {
        background-color: #1a1e27;
        padding: 20px;
        border-left: 5px solid #D4AF37;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* Adjust padding for mobile screens */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom:0; font-weight:800;'>ASSET ACQUISITION STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem;'>Binghatti Skyrise Tower C | Developed for High-Yield Investors</p>", unsafe_allow_html=True)

# --- Investment Logic Section ---
with st.container():
    st.markdown("""
    <div class='logic-box'>
        <h3 style='color: #D4AF37; margin-top:0;'>The Strategy: "Liability Assumption"</h3>
        <p style='color: #e0e0e0; font-size: 1.1rem;'>
        This model allows an investor to secure full ownership by assuming the remaining liabilities of the units. 
        Instead of paying full equity upfront, you enter with <b>minimal liquidity</b> while benefiting from a 
        <b>0% interest-free private installment plan</b> until December 2026.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Dynamic Inputs (Top Row) ---
st.write("### 🕹️ Adjust Your Entry Parameters")
input_col1, input_col2 = st.columns([1, 2])

# FIXED CALCULATION LOGIC
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
BASE_OVERDUE = 216000
FEES = 28760
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

with input_col1:
    closing_date = st.date_input("📅 Target Signature Date", date.today())
    is_after_may = closing_date >= date(2026, 5, 5)
    scenario_label = "Scenario B (Post-May 5th)" if is_after_may else "Scenario A (Pre-May 5th Advantage)"
    st.markdown(f"**Current Path:** <span style='color:#D4AF37;'>{scenario_label}</span>", unsafe_allow_html=True)

overdue_count = len([d for d in installment_dates if closing_date >= d])
future_dates = [d for d in installment_dates if closing_date < d]

min_upfront = BASE_OVERDUE + FEES + (overdue_count * 64800)
max_upfront = BREAK_EVEN_PRICE - (len(future_dates) * 32400) - 324000

with input_col2:
    upfront_cash = st.slider("💰 Upfront Cash Commitment (AED)", 
                             float(min_upfront), float(max(max_upfront, min_upfront + 10000)), 
                             float(min_upfront), 5000.0)

# INTERPOLATION CALCULATIONS
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0
current_total = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- High Visibility Metric Boxes ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("ENTRY LIQUIDITY", f"{upfront_cash:,.0f} AED")
m2.metric("MONTHLY PAYMENT", f"{current_monthly:,.0f} AED")
m3.metric("FINAL HANDOVER", f"{current_handover:,.0f} AED")
m4.metric("ALL-IN PRICE", f"{current_total:,.0f} AED")

# --- Unified Market Comparison Section ---
st.divider()
st.write("### ⚖️ Market Comparison: Why this deal?")
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class='logic-box' style='border-left: 5px solid #888; background-color: #4A4A4A;'>
        <h4 style='margin-top:0;'>Standard Resale</h4>
        <p>❌ Upfront Cash: <b>~670,000 AED</b></p>
        <p>❌ Full Equity Payment Required</p>
        <p>❌ High Entry Barrier</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='logic-box'>
        <h4 style='margin-top:0;'>ALMOHALENIN Strategy</h4>
        <p>✅ Upfront Cash: <b>{upfront_cash:,.0f} AED</b></p>
        <p>✅ Liability Assumption Model</p>
        <p>✅ 0% Private Installment Plan</p>
    </div>
    """, unsafe_allow_html=True)
# --- Multi-Color Timeline Chart ---
st.divider()
st.write("### 📅 Personalized Payment Timeline")

labels = ["Entry Signature"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

# Color Coding: Gold for Entry, Blue for Monthly, Red for Handover
bar_colors = ['#D4AF37'] + ['#A49B93'] * len(future_dates) + ['#5D4E49']

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto', 
           marker_color=bar_colors,
           textfont=dict(color="white", size=14))
])

fig.update_layout(
    template="plotly_dark", 
    height=450, 
    margin=dict(l=0, r=0, t=30, b=0), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#333")
)
st.plotly_chart(fig, use_container_width=True)

# --- Property Highlights & Image ---
st.divider()
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown(f"""
    <div style='background-color: #11141d; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37;'>
    <h3 style='color: #D4AF37; margin-top:0;'>🏗️ Property Highlights</h3>
    <ul style='color: #e0e0e0; font-size: 1.1rem; padding-left: 20px;'>
        <li><b>Tower C:</b> Prime location, high floor units.</li>
        <li><b>Leverage:</b> Control 1.2M AED asset with only {(upfront_cash/current_total)*100:.1f}% down.</li>
        <li><b>Efficiency:</b> Acquisition at {(1 - current_total/1243000)*100:.1f}% below market avg.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
with col_r:
    try: st.image("plan_2506.png.jpg", caption="Unit Layout Layout", use_container_width=True)
    except: st.caption("Plan image loading from GitHub...")

# --- Footer & Warning ---
st.error("⚠️ PERFORMANCE-BASED MOU: FAILURE TO SETTLE ANY MONTHLY INSTALLMENTS LEADS TO IMMEDIATE FORFEITURE OF ALL PREVIOUSLY PAID FUNDS AS PER THE MOU TERMS.")
st.markdown("<p style='text-align: center; opacity: 0.6; font-weight: 800; color: #FFF;'>DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
