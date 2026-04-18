import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd

# ۱. تنظیمات صفحه (بدون سایدبار)
st.set_page_config(
    page_title="Dr.Amir | Strategic Acquisition",
    layout="wide"
)

# ۲. استایل‌دهی مدرن برای حذف سایدبار و بهبود نمایش موبایل
st.markdown("""
    <style>
    /* حذف کامل فضاهای اضافه و سایدبار */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}

    /* استایل باکس‌های متریک */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.2rem, 4vw, 1.8rem) !important; 
        color: #FFFFFF !important; 
    }
    .stMetric { 
        background-color: #11141d; 
        border: 1px solid #D4AF37; 
        padding: 15px; 
        border-radius: 12px;
        text-align: center;
    }
    
    /* استایل بخش ورودی‌ها (بالای صفحه) */
    .stSelectbox, .stSlider {
        background-color: #1a1e27;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- محتوای اصلی ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🏆 Dr.Amir | Strategic Acquisition</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Binghatti Skyrise Tower C - Units C2505 & C2506</p>", unsafe_allow_html=True)

# --- ۳. بخش ورودی‌ها (به جای سایدبار، در بالای صفحه) ---
st.divider()
input_col1, input_col2 = st.columns([1, 2])

with input_col1:
    closing_date = st.date_input("📅 Contract Signature Date", date.today())

# منطق محاسبات (ثابت‌ها)
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
BASE_OVERDUE = 216000
FEES = 28760
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

# تشخیص اقساط معوقه و آتی
overdue_count = len([d for d in installment_dates if closing_date >= d])
future_dates = [d for d in installment_dates if closing_date < d]

min_upfront = BASE_OVERDUE + FEES + (overdue_count * 64800)
# سقف نقدینگی بر اساس منطق شما برای رسیدن به پایین‌ترین قیمت (سربه سر)
max_upfront = BREAK_EVEN_PRICE - (len(future_dates) * 32400) - 324000

with input_col2:
    upfront_cash = st.slider("💰 Initial Cash Commitment (AED)", 
                             float(min_upfront), float(max(max_upfront, min_upfront + 10000)), 
                             float(min_upfront), 5000.0)

# --- ۴. منطق درونیابی قیمت ---
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0

current_total = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- ۵. نمایش شاخص‌ها (Responsive Metrics) ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("CASH UPFRONT", f"{upfront_cash:,.0f}")
with m2:
    st.metric("MONTHLY INST.", f"{current_monthly:,.0f}")
with m3:
    st.metric("FINAL PAYMENT", f"{current_handover:,.0f}")
with m4:
    st.metric("TOTAL ASSET PRICE", f"{current_total:,.0f}")

# --- ۶. نمودار زمانی (Timeline) ---
st.divider()
labels = ["Initial Signature"] + [d.strftime("%b %y") for d in future_dates] + ["Handover (Dec)"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto',
           marker_color=['#D4AF37'] + ['#1f77b4'] * len(future_dates) + ['#E74C3C'])
])

fig.update_layout(
    template="plotly_dark", 
    height=450, 
    margin=dict(l=10, r=10, t=20, b=10),
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# --- ۷. تحلیل و تصاویر ---
st.divider()
col_left, col_right = st.columns([1, 1])
with col_left:
    st.markdown(f"""
    ### 📈 Strategic Analysis
    * Initial Entry: You control the asset with only {(upfront_cash/current_total)*100:.1f}% of its value.* Price Efficiency: Currently {(1 - current_total/1243000)*100:.1f}% below market average.
    * Liability: Interest-free credit bridge for { (current_monthly * len(future_dates)) + current_handover :,.0f} AED.
    """)
with col_right:
    try:
        st.image("plan_2506.png.jpg", caption="Studio Layout Tower C", use_container_width=True)
    except:
        st.caption("Plan images hosted on GitHub")

st.warning("⚠️ MOU Terms: Default on any installment leads to total forfeiture of previously paid funds.")
