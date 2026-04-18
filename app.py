import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd

# ۱. تنظیمات صفحه (اولین خط کد اجرایی)
st.set_page_config(
    page_title="ALMOHALENIN | Executive Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ۲. تزریق CSS برای حذف نشانه‌ها، خوانایی حداکثری و موبایل
st.markdown("""
    <style>
    /* حذف تمام نشانه‌های استریم‌لیت */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .block-container {padding-top: 1.5rem; padding-bottom: 1rem;}

    /* استایل باکس‌های متریک با خوانایی فوق‌العاده بالا */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.8rem, 5vw, 2.8rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        line-height: 1.2;
    }
    [data-testid="stMetricLabel"] { 
        font-size: 1.1rem !important; 
        color: #D4AF37 !important; 
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stMetric { 
        background-color: #11141d; 
        border: 2px solid #D4AF37; 
        padding: 25px 15px !important; 
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* بهینه‌سازی اختصاصی برای موبایل */
    @media (max-width: 768px) {
        [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- بخش هدر ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom:0; font-weight:800;'>ASSET ACQUISITION STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.2rem;'>Binghatti Skyrise Tower C | Developed for High-Yield Investors</p>", unsafe_allow_html=True)

# --- بخش ورودی‌های داینامیک در بالای صفحه ---
st.divider()
input_col1, input_col2 = st.columns([1, 2])

# پارامترهای ثابت محاسباتی
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
BASE_OVERDUE = 216000
FEES = 28760
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

with input_col1:
    closing_date = st.date_input("📅 Target Signature Date", date.today())

overdue_count = len([d for d in installment_dates if closing_date >= d])
future_dates = [d for d in installment_dates if closing_date < d]

min_upfront = BASE_OVERDUE + FEES + (overdue_count * 64800)
max_upfront = BREAK_EVEN_PRICE - (len(future_dates) * 32400) - 324000

with input_col2:
    upfront_cash = st.slider("💰 Upfront Cash Commitment (AED)", 
                             float(min_upfront), float(max(max_upfront, min_upfront + 10000)), 
                             float(min_upfront), 5000.0)

# --- منطق محاسبات درونیابی ---
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0
current_total = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- نمایش باکس‌های متریک (High Visibility) ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("INITIAL ENTRY", f"{upfront_cash:,.0f}")
m2.metric("MONTHLY INST.", f"{current_monthly:,.0f}")
m3.metric("FINAL HANDOVER", f"{current_handover:,.0f}")
m4.metric("TOTAL ASSET PRICE", f"{current_total:,.0f}")

# --- نمودار زمانی سه‌رنگ (Visual Distinction) ---
st.divider()
st.write("### 📅 Payment Schedule Analysis")

labels = ["Initial Entry"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

# تخصیص رنگ‌ها: طلایی برای ورود، آبی برای اقساط، قرمز برای تحویل
bar_colors = ['#D4AF37'] + ['#2E86C1'] * len(future_dates) + ['#E74C3C']

fig = go.Figure(data=[
    go.Bar(x=labels, y=values,text=[f"{v:,.0f}" for v in values], 
           textposition='auto',
           marker_color=bar_colors,
           textfont=dict(size=14, color='white'))
])

fig.update_layout(
    template="plotly_dark", 
    height=450, 
    margin=dict(l=10, r=10, t=20, b=10),
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial", size=12)
)
st.plotly_chart(fig, use_container_width=True)

# --- تحلیل استراتژیک و تصاویر ---
st.divider()
col_l, col_r = st.columns([1, 1])

with col_l:
    st.markdown(f"""
    <div style='background-color: #1a1e27; padding: 25px; border-left: 5px solid #D4AF37; border-radius: 10px;'>
        <h3 style='color: #D4AF37; margin-top:0;'>Strategic Analysis</h3>
        <ul style='color: #e0e0e0; font-size: 1.1rem;'>
            <li><b>Leverage:</b> Control a 1.2M AED asset with only <b>{(upfront_cash/current_total)*100:.1f}%</b> initial cash.</li>
            <li><b>Efficiency:</b> Acquisition price is currently <b>{(1 - current_total/1243000)*100:.1f}%</b> below market average.</li>
            <li><b>Credit Bridge:</b> 0% interest private plan for <b>{(current_monthly * len(future_dates)) + current_handover :,.0f} AED</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    try: st.image("plan_2506.png.jpg", caption="Studio Layout Tower C", use_container_width=True)
    except: st.caption("Floor plan image loading from repository...")

st.error("⚠️ PERFORMANCE-BASED MOU: FAILURE TO SETTLE ANY MONTHLY INSTALLMENTS LEADS TO IMMEDIATE FORFEITURE OF ALL PREVIOUSLY PAID FUNDS AS PER THE MOU TERMS.")
st.markdown("<p style='text-align: center; opacity: 0.5; font-weight:bold;'>OFFICIAL PROPOSAL | DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
