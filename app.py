import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
# کد برای مخفی کردن منوی استریم‌لیت و فوتر
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

import os

# ۱. تنظیمات صفحه: سایدبار را در حالت باز (expanded) قفل می‌کنیم
st.set_page_config(
    page_title="ALMOHALENIN | Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# ۲. تزریق CSS برای مخفی کردن دکمه‌های باز و بسته کردن و منوهای اضافه
hide_style = """
    <style>
    /* مخفی کردن دکمه بستن سایدبار */
    [data-testid="stSidebarCollapseButton"] {
        display: none;
    }
    /* مخفی کردن دکمه باز کردن سایدبار (اگر بسته بود) */
    button[kind="header"] {
        display: none;
    }
    /* مخفی کردن منوی اصلی و فوتر استریم‌لیت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* فیکس کردن سایدبار برای عدم حرکت */
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
    }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)


# تنظیمات لوکس برای CEO
st.set_page_config(page_title="Dr.Amir  | Advanced Deal Architect", layout="wide")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 30px !important; color: #FFFFFF !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { font-size: 16px !important; color: #D4AF37 !important; }
    .stMetric { background-color: #11141d; border: 2px solid #D4AF37; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 Dr.Amir | Strategic Acquisition Logic")
st.subheader("Dynamic Calculator: Binghatti Skyrise Tower C")

# --- ۱. تعریف ساختار زمانی اقساط ---
installment_dates = [
    date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), 
    date(2026, 8, 5), date(2026, 9, 5)
]

# پارامترهای ثابت
BASE_OVERDUE = 216000 # مجموع بدهی تا قبل از می
FEES = 28760          # NOC + 2% Commission
BREAK_EVEN_PRICE = 1156500
STRATEGIC_PRICE = 1216760

# --- ۲. سایدبار و کنترل‌های داینامیک ---
st.sidebar.header("🕹️ Transaction Variables")
closing_date = st.sidebar.date_input("Contract Signature Date", date.today())

# تشخیص اقساط معوقه بر اساس تاریخ انتخابی
overdue_installments = [d for d in installment_dates if closing_date >= d]
future_installments = [d for d in installment_dates if closing_date < d]

# محاسبه کف نقدینگی (بدهی فعلی + جریمه‌ها + اقساطی که تاریخشان گذشته)
min_upfront = BASE_OVERDUE + FEES + (len(overdue_installments) * 64800)

# محاسبه سقف نقدینگی برای رسیدن به نقطه سربه سر (Max Upfront)
# فرمول: قیمت سر‌به‌سر منهای (نیمی از اقساط باقی‌مانده + نیمی از مبلغ تحویل)
max_upfront = BREAK_EVEN_PRICE - (len(future_installments) * 32400) - 324000

# اسلایدر داینامیک (کف و سقف بر اساس تاریخ تغییر می‌کنند)
upfront_cash = st.sidebar.slider("Initial Cash Commitment (AED)", 
                                 float(min_entry := min_upfront), 
                                 float(max_entry := max(max_upfront, min_upfront + 10000)), 
                                 float(min_entry), 5000.0)

# --- ۳. منطق درونیابی خطی (Linear Scaling) ---
# محاسبه نسبت نقدینگی پرداختی بین کف و سقف
range_val = max_entry - min_entry
progress = (upfront_cash - min_entry) / range_val if range_val > 0 else 0

# محاسبه مقادیر خروجی بر اساس پیشرفت اسلایدر
current_total_price = STRATEGIC_PRICE - (progress * (STRATEGIC_PRICE - BREAK_EVEN_PRICE))
current_monthly_inst = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- ۴. نمایش خروجی‌ها ---
st.divider()
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("UPFRONT CASH", f"{upfront_cash:,.0f} AED")
    st.caption("Due at Signature")
with k2:
    st.metric("MONTHLY INST.", f"{current_monthly_inst:,.0f} AED")
    st.caption(f"{len(future_installments)} Months Remaining")
with k3:
    st.metric("FINAL HANDOVER", f"{current_handover:,.0f} AED")
    st.caption("December 2026")
with k4:
    st.metric("TOTAL ASSET VALUE", f"{current_total_price:,.0f} AED")
    st.caption(f"{(1 - current_total_price/1243000)*100:.1f}% Below Market")

# --- ۵. نمودار زمانی داینامیک ---
st.divider()
st.write("### 📅 Payment Timeline Visualization")

# ایجاد لیست برای نمودار
labels = ["Signature"] + [d.strftime("%b %y") for d in future_installments] + ["Handover (Dec)"]
values = [upfront_cash] + [current_monthly_inst] * len(future_installments) + [current_handover]

fig = go.Figure(data=[
    go.Bar(x=labels, y=values, 
           text=[f"{v:,.0f}" for v in values], 
           textposition='auto',
           marker_color=['#D4AF37'] + ['#1f77b4'] * len(future_installments) + ['#E74C3C'])
])

fig.update_layout(template="plotly_dark", height=500, xaxis_title="Timeline Stages", yaxis_title="Amount (AED)")
st.plotly_chart(fig, use_container_width=True)

# --- ۶. تحلیل و تصاویر ---
col_a, col_b = st.columns(2)
with col_a:
    st.write("### 💡 Financial Analysis")
    st.info(f"""
    - Liquidity Entry: You are entering this asset with only {(upfront_cash/current_total_price)*100:.1f}% of the total value.
    - Price Strategy: { "Minimum Entry mode selected." if progress < 0.1 else "Cash-Optimization (Discount) mode active." }
    - Monthly Obligation: {current_monthly_inst:,.0f} AED combined for both units.
    """)
with col_b:
    try:
        st.image("plan_2506.png.jpg", caption="Studio Layout C2506", use_container_width=True)
    except:
        st.info("Layout images will appear here once uploaded to GitHub.")

st.warning("⚠️ Legal Notice: This is a performance-based contract. Default on any installment leads to immediate forfeiture of the total paid amount as per the MOU terms.")
