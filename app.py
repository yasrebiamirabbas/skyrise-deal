import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ALMOHALENIN | Strategic Proposal", layout="wide")

# 2. Advanced Styling (Gold & Dark Executive Theme)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 1.5rem;}
    .stMetric { 
        background-color: #11141d; 
        border: 1px solid #D4AF37; 
        padding: 20px; 
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1);
    }
    div[data-testid="stMetricValue"] { font-size: 2rem !important; color: #D4AF37 !important; }
    .guide-box {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #D4AF37;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header & Introduction
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>STRATEGIC PORTFOLIO ACQUISITION</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffffff;'>Binghatti Skyrise Tower C | Units C2505 & C2506</h3>", unsafe_allow_html=True)

# 4. Interactive User Guide
with st.container():
    st.markdown("""
    <div class='guide-box'>
        <h4 style='color: #D4AF37; margin-top:0;'>💡 How to evaluate this opportunity:</h4>
        <ol style='color: #e0e0e0;'>
            <li><b>Select Signature Date:</b> See how closing before <b>May 5th</b> drastically reduces your entry liquidity.</li>
            <li><b>Adjust Cash Commitment:</b> Increase your upfront payment to lower the total asset price towards the <b>Break-Even point</b>.</li>
            <li><b>Analyze Timeline:</b> View your 0% interest private payment plan until December 2026.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# 5. Inputs (Top Row)
col_in1, col_in2 = st.columns([1, 2])
with col_in1:
    closing_date = st.date_input("📅 Contract Signature Date", date.today())
with col_in2:
    # Calculation Logic
    installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
    overdue_count = len([d for d in installment_dates if closing_date >= d])
    future_dates = [d for d in installment_dates if closing_date < d]
    
    min_upfront = 216000 + 28760 + (overdue_count * 64800)
    max_upfront = 1156500 - (len(future_dates) * 32400) - 324000
    
    upfront_cash = st.slider("💰 Upfront Cash Commitment (AED)", 
                             float(min_upfront), float(max(max_upfront, min_upfront + 10000)), 
                             float(min_upfront), 5000.0)

# 6. Linear Math & Results
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0
current_total = 1216760 - (progress * (1216760 - 1156500))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# 7. Key Metrics Row
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("ENTRY CASH", f"{upfront_cash:,.0f} AED")
m2.metric("MONTHLY PAYMENT", f"{current_monthly:,.0f} AED")
m3.metric("FINAL HANDOVER", f"{current_handover:,.0f} AED")
m4.metric("TOTAL ASSET PRICE", f"{current_total:,.0f} AED")

# 8. Comparison Section (Visual Hook)
st.divider()
st.write("### ⚖️ Why This Deal vs. Standard Resale")
comp1, comp2 = st.columns(2)
with comp1:
    st.markdown(f"""
    Standard Secondary Market Purchase:
    - Cash Required: ~670,000 AED
    - Entry Barrier: <span style='color:red;'>High Liquidity Needed</span>
    - Financing: Often Bank Required
    """, unsafe_allow_html=True)
with comp2:
    st.markdown(f"""
    ALMOHALENIN Asset Assumption:
    - Cash Required: {upfront_cash:,.0f} AED
    - Entry Barrier: <span style='color:#D4AF37;'>Low (Liability Assumption)</span>
    - Financing: 0% Interest Private Plan
    """, unsafe_allow_html=True)

# 9. Chart
st.divider()
labels = ["Initial Entry"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]
fig = go.Figure(data=[go.Bar(x=labels, y=values, text=[f"{v:,.0f}" for v in values], textposition='auto', marker_color='#D4AF37')])
fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig, use_container_width=True)

# 10. Forfeiture Clause & Footer
st.divider()
st.error("⚠️ Performance-Based MOU: Failure to settle installments results in immediate forfeiture of all paid capital. Transaction will be voided.")
st.markdown("<p style='text-align: center; opacity: 0.5;'>OFFICIAL PROPOSAL | DR. AMIR YASREBI | ALMOHALENIN CEO OFFICE</p>", unsafe_allow_html=True)
