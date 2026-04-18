import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd

# ۱. تنظیمات صفحه (همیشه اولین خط کد)
st.set_page_config(page_title="ALMOHALENIN | Executive Dashboard", layout="wide")

# ۲. استایل‌دهی پیشرفته برای خوانایی و White-Labeling
st.markdown("""
    <style>
    /* حذف منوها و فوتر برای ظاهر اختصاصی */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* افزایش خوانایی باکس‌های متریک */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.8rem, 5vw, 2.5rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    [data-testid="stMetricLabel"] { 
        font-size: 1.1rem !important; 
        color: #D4AF37 !important; 
        font-weight: bold !important;
        letter-spacing: 1px;
    }
    .stMetric { 
        background-color: #11141d; 
        border: 2px solid #D4AF37; 
        padding: 25px; 
        border-radius: 15px;
        text-align: center;
    }
    
    /* باکس منطق استراتژی */
    .logic-box {
        background-color: #1a1e27;
        padding: 25px;
        border-right: 5px solid #D4AF37;
        border-radius: 10px;
        margin-bottom: 20px;
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- هدر اصلی ---
st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom:0;'>🏆 Dr.Amir | Strategic Acquisition</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem;'>Binghatti Skyrise Tower C - Units C2505 & C2506</p>", unsafe_allow_html=True)

# --- ورودی‌ها در بالای صفحه ---
st.divider()
input_col1, input_col2 = st.columns([1, 2])

# پارامترهای ثابت
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
BASE_OVERDUE = 216000
FEES = 28760
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

with input_col1:
    closing_date = st.date_input("📅 Contract Signature Date", date.today())
    is_after_may = closing_date >= date(2026, 5, 5)

# منطق محاسبات داینامیک
overdue_count = len([d for d in installment_dates if closing_date >= d])
future_dates = [d for d in installment_dates if closing_date < d]

min_upfront = BASE_OVERDUE + FEES + (overdue_count * 64800)
max_upfront = BREAK_EVEN_PRICE - (len(future_dates) * 32400) - 324000

with input_col2:
    upfront_cash = st.slider("💰 Upfront Cash Commitment (AED)", 
                             float(min_upfront), float(max(max_upfront, min_upfront + 10000)), 
                             float(min_upfront), 5000.0)

# --- محاسبات درونیابی قیمت ---
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0
current_total = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- نمایش شاخص‌ها با فونت درشت و خوانا ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("INITIAL ENTRY", f"{upfront_cash:,.0f} AED")
m2.metric("MONTHLY INST.", f"{current_monthly:,.0f} AED")
m3.metric("FINAL HANDOVER", f"{current_handover:,.0f} AED")
m4.metric("TOTAL ALL-IN", f"{current_total:,.0f} AED")

# --- نمودار زمانی سه‌رنگ ---
st.divider()
st.write("### 📊 Interactive Payment Timeline")
labels = ["Initial Entry"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]

# تعریف رنگ‌های متمایز برای هر مرحله
# طلایی برای پیش‌پرداخت، آبی برای اقساط، قرمز برای تحویل
colors = ['#D4AF37'] + ['#2E86C1'] * len(future_dates) + ['#E74C3C']

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto',
           marker_color=colors)
])

fig.update_layout(
    template="plotly_dark", 
    height=450,margin=dict(l=10, r=10, t=30, b=10),
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14)
)
st.plotly_chart(fig, use_container_width=True)

# --- بخش مقایسه و توضیحات استراتژیک ---
st.divider()
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown(f"""
    <div class='logic-box'>
        <h4 style='color: #D4AF37;'>💡 استراتژی واگذاری تعهدات (Liability Assumption)</h4>
        <p>در این مدل، خریدار با <b>کمترین نقدینگی ممکن</b> وارد معامله شده و از یک <b>وام خصوصی بدون بهره</b> تا پایان سال ۲۰۲۶ بهره‌مند می‌شود.</p>
        <p>هرچه مبلغ پیش‌پرداخت را افزایش دهید، قیمت کل به سمت نقطه سر‌به‌سر ({BREAK_EVEN_PRICE:,.0f} درهم) کاهش می‌یابد.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    Key Deal Insights:
    * Market Average: 1,243,000 AED
    * Your Purchase Price: {current_total:,.0f} AED
    * Immediate Saving: {1243000 - current_total:,.0f} AED
    """)

with col_right:
    try:
        st.image("plan_2506.png.jpg", caption="Strategic Layout C2506", use_container_width=True)
    except:
        st.caption("Plan images hosted on GitHub")

st.error("⚠️ MOU Terms: Performance-based contract. Any missed installment leads to immediate forfeiture of all paid capital. No refunds.")
st.markdown("<p style='text-align: center; opacity: 0.5;'>DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
