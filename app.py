import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import os

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="ALMOHALENIN | Strategic Proposal", layout="wide")

# 2. Styling: Warm White Background, Dark Gray Boxes, White Text, 100% White-Labeled
st.markdown("""
    <style>
    /* 100% White-Labeling */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QS1 {display: none;}
    
    /* Total Background: Warm White */
    .stApp {
        background-color: #FDFBF7;
    }

    /* Metric Boxes & Logic Boxes: Dark Gray with White Text */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.6rem, 5vw, 2.5rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
    }
    [data-testid="stMetricLabel"] { 
        font-size: clamp(0.9rem, 2vw, 1rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 600 !important;
        opacity: 0.9;
        text-transform: uppercase;
    }
    .stMetric { 
        background-color: #2D2D2D !important; 
        border: 1px solid #1A1A1A !important; 
        padding: 25px 10px !important; 
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Logic Box: Dark Gray with White Text */
    .logic-box {
        background-color: #2D2D2D;
        color: #FFFFFF;
        padding: 20px;
        border-left: 5px solid #D4AF37;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Mobile Adjustments */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    }
    
    /* Ensuring text outside boxes is dark for Warm White background */
    h1, h3, h4, p, span, label {
        color: #2D2D2D !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #D4AF37 !important; margin-bottom:0; font-weight:800;'>ASSET ACQUISITION STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555 !important; font-size: 1.1rem;'>Binghatti Skyrise Tower C | Developed for High-Yield Investors</p>", unsafe_allow_html=True)

# --- Investment Logic Section ---
with st.container():
    st.markdown("""
    <div class='logic-box'>
        <h3 style='color: #D4AF37 !important; margin-top:0;'>The Strategy: "Liability Assumption"</h3>
        <p style='color: #FFFFFF !important; font-size: 1.1rem;'>
        This model allows an investor to secure full ownership by assuming the remaining liabilities of the units. 
        Instead of paying full equity upfront, you enter with <b>minimal liquidity</b> while benefiting from a 
        <b>0% interest-free private installment plan</b> until December 2026.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Dynamic Inputs (Top Row) ---
st.markdown("<h3 style='color: #2D2D2D !important;'>🕹️ Adjust Your Entry Parameters</h3>", unsafe_allow_html=True)
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

# --- Direct Market Comparison ---
st.divider()
st.markdown("<h3 style='color: #2D2D2D !important;'>⚖️ Market Comparison: Why this deal?</h3>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class='logic-box' style='background-color: #4A4A4A; border-left: 5px solid #888;'>
    <h4 style='color: #CCC !important; margin-top:0;'>Standard Resale</h4>
    <p style='color: #FFF !important;'>❌ Upfront Cash: <b>~670,000 AED</b></p>
    <p style='color: #FFF !important;'>❌ Full Equity Payment Required</p>
    <p style='color: #FFF !important;'>❌ High Entry Barrier</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='logic-box'>
    <h4 style='color: #D4AF37 !important; margin-top:0;'>ALMOHALENIN Strategy</h4>
    <p style='color: #FFF !important;'>✅ Upfront Cash: <b>{upfront_cash:,.0f} AED</b></p>
    <p style='color: #FFF !important;'>✅ Liability Assumption Model</p>
    <p style='color: #FFF !important;'>✅ 0% Private Installment Plan</p>
    </div>
    """, unsafe_allow_html=True)

# --- Multi-Color Spectrum Timeline Chart ---
st.divider()
st.markdown("<h3 style='color: #2D2D2D !important;'>📅 Personalized Payment Timeline</h3>", unsafe_allow_html=True)

labels = ["Entry Signature"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

# Gold to Dark Gray Gold spectrum mixture
# Gold -> Muted Gold -> Bronze Gray -> Dark Gray
bar_colors = ['#D4AF37', '#B3995D', '#8C7C5A', '#665F50', '#403D39', '#2D2D2D']
# Adjust color list length to match bar count
final_colors = [bar_colors[0]] + [bar_colors[2]] * len(future_dates) + [bar_colors[5]]

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto', 
           marker_color=final_colors,
           textfont=dict(color="white", size=14))
])

fig.update_layout(
    height=450, 
    margin=dict(l=0, r=0, t=30, b=0), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, tickfont=dict(color="#2D2D2D")),
    yaxis=dict(showgrid=True, gridcolor="#DDD", tickfont=dict(color="#2D2D2D"))
)
st.plotly_chart(fig, use_container_width=True)

# --- Property Highlights & Image ---
st.divider()
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown(f"""
    <div class='logic-box'>
    <h3 style='color: #D4AF37 !important; margin-top:0;'>🏗️ Property Highlights</h3>
    <ul style='color: #FFFFFF !important; font-size: 1.1rem; padding-left: 20px;'>
        <li><b>Tower C:</b> Prime location, high floor units.</li>
        <li><b>Leverage:</b> Control 1.2M AED asset with only {(upfront_cash/current_total)*100:.1f}% down.</li>
        <li><b>Efficiency:</b> Acquisition at {(1 - current_total/1243000)*100:.1f}% below market avg.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
with col_r:
    try: st.image("plan_2506.png.jpg", caption="Unit Layout", use_container_width=True)
    except: st.caption("Plan image loading from GitHub...")

# --- Footer & Warning ---
st.error("⚠️ PERFORMANCE-BASED MOU: FAILURE TO SETTLE ANY MONTHLY INSTALLMENTS LEADS TO IMMEDIATE FORFEITURE OF ALL PREVIOUSLY PAID FUNDS AS PER THE MOU TERMS.")
st.markdown("<p style='text-align: center; opacity: 0.9; font-weight: 800; color: #2D2D2D !important;'>DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
