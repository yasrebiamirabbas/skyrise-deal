import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import os

# ۱. تنظیمات صفحه (فقط یک‌بار و در شروع کد)
st.set_page_config(
    page_title="Dr.Amir | Investment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ۲. تزریق CSS برای موبایل و شخصی‌سازی (White Labeling)
# تنظیم کردیم که در موبایل فونت‌ها کمی کوچک‌تر شوند تا باکس‌ها به‌هم نریزند
st.markdown("""
    <style>
    /* مخفی کردن منوهای استریم‌لیت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarCollapseButton"] {display: none;} /* قفل کردن سایدبار */

    /* استایل باکس‌های متریک */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.5rem, 5vw, 2rem) !important; 
        color: #FFFFFF !important; 
        font-weight: bold !important; 
    }
    [data-testid="stMetricLabel"] { 
        font-size: 0.9rem !important; 
        color: #D4AF37 !important; 
    }
    .stMetric { 
        background-color: #11141d; 
        border: 2px solid #D4AF37; 
        padding: 15px; 
        border-radius: 12px; 
    }

    /* بهینه‌سازی برای نمایش موبایل */
    @media (max-width: 640px) {
        [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
        .stMetric { padding: 10px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- بدنه اصلی برنامه ---
st.title("🏆 Dr.Amir | Strategic Acquisition")
st.subheader("Binghatti Skyrise Tower C - Deal Architect")

# --- پارامترهای ثابت مالی ---
installment_dates = [
    date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), 
    date(2026, 8, 5), date(2026, 9, 5)
]
BASE_OVERDUE = 216000 
FEES = 28760          
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

# --- سایدبار کنترلی (🕹️ بخش ورودی‌ها) ---
st.sidebar.header("🕹️ Transaction Settings")

closing_date = st.sidebar.date_input("Contract Signature Date", date.today())

# منطق محاسباتی اقساط
overdue_installments = [d for d in installment_dates if closing_date >= d]
future_installments = [d for d in installment_dates if closing_date < d]

min_upfront = BASE_OVERDUE + FEES + (len(overdue_installments) * 64800)
# فرمول محاسبه سقف نقدینگی بر اساس منطق سربه سر
max_upfront = BREAK_EVEN_PRICE - (len(future_installments) * 32400) - 324000

upfront_cash = st.sidebar.slider(
    "Initial Cash Commitment (AED)", 
    float(min_upfront), 
    float(max(max_upfront, min_upfront + 10000)), 
    float(min_upfront), 
    5000.0
)

# --- منطق محاسبات خطی ---
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0

current_total_price = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly_inst = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- نمایش خروجی‌ها (Responsive Columns) ---
st.divider()
k1, k2, k3, k4 = st.columns([1, 1, 1, 1])
with k1:
    st.metric("UPFRONT CASH", f"{upfront_cash:,.0f} AED")
with k2:
    st.metric("MONTHLY INST.", f"{current_monthly_inst:,.0f} AED")
with k3:
    st.metric("FINAL HANDOVER", f"{current_handover:,.0f} AED")
with k4:
    st.metric("TOTAL VALUE", f"{current_total_price:,.0f} AED")

# --- نمودار زمانی داینامیک ---
st.divider()
st.write("### 📅 Payment Schedule")

labels = ["Signature"] + [d.strftime("%b %y") for d in future_installments] + ["Handover"]
values = [upfront_cash] + [current_monthly_inst] * len(future_installments) + [current_handover]

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto',
           marker_color=['#D4AF37'] + ['#1f77b4'] * len(future_installments) + ['#E74C3C'])
])

fig.update_layout(
    template="plotly_dark", 
    height=400, 
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis_tickangle=-45 # کج کردن متن‌ها برای موبایل
)
st.plotly_chart(fig, use_container_width=True)

# --- تحلیل و تصاویر ---
st.divider()
col_a, col_b = st.columns([1, 1])
with col_a:
    st.info(f"""- Liquidity Entry: Only {(upfront_cash/current_total_price)*100:.1f}% of total value.
    - Discount Level: {progress*100:.1f}% towards Break-Even.
    - Future Debt: { (current_monthly_inst * len(future_installments)) + current_handover :,.0f} AED.
    """)
with col_b:
    try:
        st.image("plan_2506.png.jpg", caption="Layout C2506", use_container_width=True)
    except:
        st.caption("Plan image loading...")

st.warning("⚠️ Legal Notice: Performance-based contract. Default leads to forfeiture as per MOU.")
