import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import base64
import os

# ۱. تنظیمات اولیه
st.set_page_config(page_title="Skyrise Deal | Strategic Proposal", layout="wide")

# تابع تبدیل عکس به Base64 برای استفاده در پس‌زمینه
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# بارگذاری عکس sky.jpg
try:
    bin_str = get_base64('sky.png')
    # استایل پس‌زمینه ثابت با اورلی گرادینت مدرن
    bg_style = f'''
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(10, 10, 15, 0.85), rgba(10, 10, 15, 0.95)), url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    '''
except:
    bg_style = '<style>.stApp { background-color: #0a0a0f; }</style>'

# ۲. تزریق CSS پیشرفته (High-Tech Design)
st.markdown(bg_style, unsafe_allow_html=True)
st.markdown("""
    <style>
    /* حذف المان‌های اضافه Streamlit */
    [data-testid="stSidebar"], [data-testid="stHeader"], footer, #MainMenu {display: none;}
    .block-container {padding-top: 2rem;}

    /* استایل باکس‌های متریک (Glassmorphism) */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.6rem, 5vw, 2.8rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.4);
    }
    [data-testid="stMetricLabel"] { 
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important; 
        color: #D4AF37 !important; 
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .stMetric { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        border: 1px solid rgba(212, 175, 55, 0.3) !important; 
        padding: 25px 10px !important; 
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(15px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    
    /* استایل باکس‌های منطق و مقایسه (Tech Box) */
    .logic-box {
        background-color: rgba(26, 30, 39, 0.7);
        padding: 20px;
        border-left: 5px solid #D4AF37;
        border-radius: 12px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-top: 1px solid rgba(255,255,255,0.05);
    }

    /* بهینه‌سازی متون */
    h1, h3, h4, p { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    
    /* استایل اسلایدر و اینپوت‌ها */
    .stSlider [data-baseweb="slider"] { padding-bottom: 2rem; }
    
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom:0; font-weight:800; letter-spacing: -1px;'>ASSET ACQUISITION STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa !important; font-size: 1.1rem;'>Binghatti Skyrise Tower C | Strategic High-Tech Dashboard</p>", unsafe_allow_html=True)

# --- Investment Logic Section ---
with st.container():
    st.markdown("""
    <div class='logic-box'>
        <h3 style='color: #D4AF37; margin-top:0;'>The Strategy: "Liability Assumption"</h3>
        <p style='color: #ccc !important; font-size: 1.1rem;'>
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

# --- Direct Market Comparison ---
st.divider()
st.write("### ⚖️ Market Comparison: Why this deal?")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class='logic-box' style='background-color: rgba(20, 20, 25, 0.8); border-left-color: #444;'>
    <h4 style='color: #888; margin-top:0;'>Standard Resale</h4>
    <p style='color: #FFFFFF;'>❌ Upfront Cash: <b>~670,000 AED</b></p>
    <p style='color: #FFFFFF;'>❌ Full Equity Payment Required</p>
    <p style='color: #FFFFFF;'>❌ High Entry Barrier</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='logic-box'>
    <h4 style='color: #D4AF37; margin-top:0;'>Creative Strategy</h4>
    <p style='color: #FFFFFF;'>✅ Upfront Cash: <b>{upfront_cash:,.0f} AED</b></p>
    <p style='color: #FFFFFF;'>✅ Liability Assumption Model</p>
    <p style='color: #FFFFFF;'>✅ 0% Private Installment Plan</p>
    </div>
    """, unsafe_allow_html=True)

# --- Multi-Color Timeline Chart ---
st.divider()
st.write("### 📅 Personalized Payment Timeline")

labels = ["Entry Signature"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

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
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
)
st.plotly_chart(fig, use_container_width=True)

# --- Property Highlights & Image ---
st.divider()
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown(f"""
    <div class='logic-box'>
    <h3 style='color: #D4AF37; margin-top:0;'>🏗️ Property Highlights</h3>
    <ul style='color: #ccc; font-size: 1.1rem; padding-left: 20px;'>
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
st.markdown("<p style='text-align: center; opacity: 0.6; font-weight: 800; color: #FFF !important;'>DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
