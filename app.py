import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import base64
import os

# ۱. تنظیمات اولیه
st.set_page_config(page_title="Skyrise Deal | Strategic Proposal", layout="wide")

# تابع تبدیل عکس به Base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# بارگذاری عکس sky.jpg با اورلی روشن
try:
    bin_str = get_base64('sky.png')
    # اورلی سفید نیمه‌شفاف برای روشن کردن فضا
    bg_style = f'''
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(253, 251, 247, 0.7), rgba(253, 251, 247, 0.9)), url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    '''
except:
    bg_style = '<style>.stApp { background-color: #FDFBF7; }</style>'

# ۲. تزریق CSS برای ظاهر روشن و High-Tech
st.markdown(bg_style, unsafe_allow_html=True)
st.markdown("""
    <style>
    /* حذف المان‌های اضافه Streamlit */
    [data-testid="stSidebar"], [data-testid="stHeader"], footer, #MainMenu {display: none;}
    .block-container {padding-top: 2rem;}

    /* استایل باکس‌های متریک (Bright Glassmorphism) */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.6rem, 5vw, 2.8rem) !important; 
        color: #2D2D2D !important; /* متن تیره برای خوانایی در محیط روشن */
        font-weight: 900 !important;
    }
    [data-testid="stMetricLabel"] { 
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important; 
        color: #B8860B !important; /* طلایی تیره‌تر برای کنتراست */
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    .stMetric { 
        background-color: rgba(255, 255, 255, 0.6) !important; /* شیشه روشن */
        border: 1px solid rgba(212, 175, 55, 0.5) !important; 
        padding: 25px 10px !important; 
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    /* استایل باکس‌های منطق و مقایسه */
    .logic-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-left: 5px solid #D4AF37;
        border-radius: 12px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    /* تنظیم رنگ متون اصلی */
    h1, h3, h4, p, label { color: #2D2D2D !important; font-family: 'Inter', sans-serif; }
    
    /* استایل اسلایدر */
    .stSlider [data-baseweb="slider"] { padding-bottom: 2rem; }
    
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #D4AF37 !important; margin-bottom:0; font-weight:800;'>STRATEGIC CAPITAL LEVERAGE MODEL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666 !important; font-size: 1.1rem;'>Binghatti Skyrise Tower C2506 | Strategic High-Tech Dashboard</p>", unsafe_allow_html=True)

# --- Investment Logic Section ---
with st.container():
    st.markdown("""
    <div class='logic-box'>
        <h3 style='color: #D4AF37 !important; margin-top:0;'>The Strategy: "Total Equity & Credit Assumption"</h3>
        <p style='color: #FFFFFF !important; font-size: 1.15rem; line-height: 1.6;'>
        This structure allows you to <b>step into the seller’s pre-funded strategic position</b>. By acquiring the existing equity and assuming the remaining balance, you bypass bank mortgages entirely. 
        <b>You are acquiring a prime asset by leveraging a combination of the developer’s (Binghatti) interest-free capital and the seller’s already-invested funds.</b> 
        Essentially, you own the property using the builder's money while preserving your own liquidity through a 
        <b>0% interest-free private bridge</b> until December 2026.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Dynamic Inputs ---
st.write("### 🕹️ Adjust Your Entry Parameters")
input_col1, input_col2 = st.columns([1, 2])

# FIXED CALCULATION LOGIC
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
BASE_OVERDUE = 216000
FEES = 28760
BREAK_EVEN_PRICE = 1080000
STRATEGIC_PRICE = 1150000

with input_col1:
    closing_date = st.date_input("📅 Target Signature Date", date.today())
    is_after_may = closing_date >= date(2026, 5, 5)
    scenario_label = "Scenario B (Post-May 5th)" if is_after_may else "Scenario A (Pre-May 5th Advantage)"
    st.markdown(f"**Current Path:** <span style='color:#B8860B;'>{scenario_label}</span>", unsafe_allow_html=True)

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

# --- Metrics Row ---
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
    <div class='logic-box' style='background-color: rgba(240, 240, 240, 0.8); border-left-color: #888;'>
    <h4 style='color: #666 !important; margin-top:0;'>Standard Resale</h4>
    <p style='color: #444 !important;'>❌ Upfront Cash: <b>~{max(upfront_cash,670000):,.0f} AED</b></p>
    <p style='color: #444 !important;'>❌ Full Equity Payment Required</p>
    <p style='color: #444 !important;'>❌ High Entry Barrier</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='logic-box'>
    <h4 style='color: #D4AF37 !important; margin-top:0;'>Creative Strategy</h4>
    <p style='color: #2D2D2D !important;'>✅ Upfront Cash: <b>{upfront_cash:,.0f} AED</b></p>
    <p style='color: #2D2D2D !important;'>✅ Liability Assumption Model</p>
    <p style='color: #2D2D2D !important;'>✅ 0% Private Installment Plan</p>
    </div>
    """, unsafe_allow_html=True)

# --- Timeline Chart ---
st.divider()
st.write("### 📅 Personalized Payment Timeline")

labels = ["Entry Signature"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]
# پالت رنگی: طلایی به خاکستری تیره
bar_colors = ['#D4AF37'] + ['#888888'] * len(future_dates) + ['#2D2D2D']

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto', 
           marker_color=bar_colors,
           textfont=dict(color="white", size=14))
])

fig.update_layout(
    height=450, 
    margin=dict(l=0, r=0, t=30, b=0), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, tickfont=dict(color="#2D2D2D")),
    yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", tickfont=dict(color="#2D2D2D"))
)
st.plotly_chart(fig, use_container_width=True)

# --- Highlights & Layout ---
st.divider()
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown(f"""
    <div class='logic-box'>
    <h3 style='color: #D4AF37 !important; margin-top:0;'>🏗️ Property Highlights</h3>
    <ul style='color: #444; font-size: 1.1rem; padding-left: 20px;'>
        <li><b>Tower C:</b> Prime location, high floor units.</li>
        <li><b>Leverage:</b> Control 1.2M AED asset with only {(upfront_cash/current_total)*100:.1f}% down.</li>
        <li><b>Efficiency:</b> Acquisition at {(1 - current_total/1243000)*100:.1f}% below market avg.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
with col_r:
    try: st.image("plan_2506.png.jpg", caption="Unit Layout Plan", use_container_width=True)
    except: st.caption("Plan image loading...")

# --- Footer ---
st.error("⚠️ PERFORMANCE-BASED MOU: FAILURE TO SETTLE ANY MONTHLY INSTALLMENTS LEADS TO IMMEDIATE FORFEITURE OF ALL PREVIOUSLY PAID FUNDS.")
st.markdown("<p style='text-align: center; opacity: 0.8; font-weight: 800; color: #2D2D2D !important;'>DR. AMIR </p>", unsafe_allow_html=True)
