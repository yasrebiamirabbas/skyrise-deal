import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="ALMOHALENIN | Strategic Proposal", layout="wide")

# 2. Refined Dark Gray & Gold Theme CSS
st.markdown("""
    <style>
    /* 100% White-Labeling */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QS1 {display: none;}
    
    /* Global Background */
    .stApp {
        background-color: #121212;
    }

    /* Unified Dark Gray Boxes for Metrics */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.6rem, 5vw, 2.5rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] { 
        font-size: 0.9rem !important; 
        color: #FFFFFF !important; 
        font-weight: 400 !important;
        opacity: 0.8;
        letter-spacing: 1px;
    }
    .stMetric { 
        background-color: #2d2d2d !important; 
        border: 1px solid #444444 !important; 
        padding: 20px !important; 
        border-radius: 10px !important;
        text-align: center;
    }
    
    /* Strategy & Highlight Boxes */
    .dark-gray-box {
        background-color: #2d2d2d;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #444444;
        margin-bottom: 20px;
        color: #FFFFFF;
    }

    /* Slider styling to match Gold Theme */
    .stSlider [data-baseweb="slider"] {
        margin-bottom: 25px;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom:0; font-weight:800; letter-spacing: 2px;'>ASSET ACQUISITION STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #bbbbbb; font-size: 1rem; text-transform: uppercase;'>Binghatti Skyrise Tower C | Executive Portfolio</p>", unsafe_allow_html=True)

# --- Investment Logic Section ---
st.markdown(f"""
    <div class='dark-gray-box' style='border-left: 5px solid #D4AF37;'>
        <h3 style='color: #D4AF37; margin-top:0;'>The Strategy: "Liability Assumption"</h3>
        <p style='font-size: 1.1rem; line-height: 1.6;'>
        This model allows an investor to secure full ownership by assuming the remaining liabilities of the units. 
        Instead of paying full equity upfront, you enter with <b>minimal liquidity</b> while benefiting from a 
        <b>0% interest-free private installment plan</b> until December 2026.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Dynamic Inputs ---
st.write("### 🕹️ Adjust Parameters")
input_col1, input_col2 = st.columns([1, 2])

# FIXED CALCULATION LOGIC (Untouched)
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
BASE_OVERDUE = 216000
FEES = 28760
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

with input_col1:
    closing_date = st.date_input("Target Signature Date", date.today())
    is_after_may = closing_date >= date(2026, 5, 5)
    scenario = "Scenario B (Post-May 5th)" if is_after_may else "Scenario A (Pre-May 5th)"
    st.markdown(f"**Path:** <span style='color:#D4AF37;'>{scenario}</span>", unsafe_allow_html=True)

overdue_count = len([d for d in installment_dates if closing_date >= d])
future_dates = [d for d in installment_dates if closing_date < d]

min_upfront = BASE_OVERDUE + FEES + (overdue_count * 64800)
max_upfront = BREAK_EVEN_PRICE - (len(future_dates) * 32400) - 324000

with input_col2:
    upfront_cash = st.slider("Initial Cash Commitment (AED)", 
                             float(min_upfront), float(max(max_upfront, min_upfront + 10000)), 
                             float(min_upfront), 5000.0)

# INTERPOLATION CALCULATIONS
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0
current_total = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- High Visibility Dark Gray Metric Boxes ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("ENTRY LIQUIDITY", f"{upfront_cash:,.0f} AED")
m2.metric("MONTHLY PAYMENT", f"{current_monthly:,.0f} AED")
m3.metric("FINAL HANDOVER", f"{current_handover:,.0f} AED")
m4.metric("ALL-IN PRICE", f"{current_total:,.0f} AED")

# --- Direct Market Comparison ---
st.divider()
st.write("### ⚖️ Market Comparison")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class='dark-gray-box' style='border-color: #444;'>
    <h4 style='color: #888; margin-top:0;'>Standard Resale</h4>
    <p>❌ Upfront Cash: <b>~670,000 AED</b></p>
    <p>❌ Full Equity Payment Required</p>
    <p>❌ High Entry Barrier</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='dark-gray-box' style='border-color: #D4AF37;'>
    <h4 style='color: #D4AF37; margin-top:0;'>ALMOHALENIN Strategy</h4>
    <p>✅ Upfront Cash: <b>{upfront_cash:,.0f} AED</b></p>
    <p>✅ Liability Assumption Model</p>
    <p>✅ 0% Private Installment Plan</p>
    </div>
    """, unsafe_allow_html=True)

# --- Modern Gold-Gray Spectrum Chart ---
st.divider()
st.write("### 📅 Payment Timeline")

labels = ["Entry"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

# Spectrum: Gold -> Muted Gold/Gray -> Dark Charcoal-Gold
# Using a modern metallic spectrum
spectrum_colors = ['#D4AF37'] + ['#8C7C5A'] * (len(future_dates)) + ['#3D392E']

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto', 
           marker=dict(
               color=spectrum_colors,
               line=dict(color='#444', width=1)
           ),
           textfont=dict(color="white", size=14))
])

fig.update_layout(
    template="plotly_dark", 
    height=450, 
    margin=dict(l=0, r=0, t=30, b=0), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#333", zeroline=False)
)
st.plotly_chart(fig, use_container_width=True)

# --- Property Highlights & Layout ---
st.divider()
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown(f"""
    <div class='dark-gray-box' style='border-top: 3px solid #D4AF37;'>
    <h3 style='color: #D4AF37; margin-top:0;'>🏗️ Property Highlights</h3>
    <ul style='color: #FFFFFF; font-size: 1.1rem; padding-left: 20px;'>
        <li><b>Tower C:</b> Prime location, high floor units.</li>
        <li><b>Leverage:</b> Control asset with {(upfront_cash/current_total)*100:.1f}% entry.</li>
        <li><b>Efficiency:</b> Value is {(1 - current_total/1243000)*100:.1f}% vs Market.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
with col_r:
    try: st.image("plan_2506.png.jpg", caption="Studio Layout Tower C", use_container_width=True)
    except: st.caption("Plan image loading...")

# --- Footer & Disclaimer ---
st.error("⚠️ PERFORMANCE-BASED MOU: FAILURE TO SETTLE ANY MONTHLY INSTALLMENTS LEADS TO IMMEDIATE FORFEITURE OF ALL PREVIOUSLY PAID FUNDS AS PER THE MOU TERMS.")
st.markdown("<p style='text-align: center; opacity: 0.8; font-weight: 700; color: #FFFFFF; letter-spacing: 1px;'>DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
