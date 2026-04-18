import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd

# تنظیمات تم حرفه‌ای
st.set_page_config(page_title="ALMOHALENIN | Executive Dashboard", layout="wide")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #FFFFFF !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { font-size: 16px !important; color: #D4AF37 !important; }
    .stMetric { background-color: #161b22; border: 2px solid #D4AF37; padding: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 ALMOHALENIN | Strategic Acquisition Portal")
st.subheader("Binghatti Skyrise - Tower C | Dynamic Investment Logic")

# --- پارامترهای ثابت ---
PIVOT_DATE = date(2026, 5, 5)
BASE_OVERDUE = 216000 
FEES = 28760
MAY_INSTALLMENT = 64800
MAX_UPFRONT_TARGET = 700000 # نقطه‌ای که به سر‌به‌سر کامل می‌رسیم

# --- سایدبار کنترلی ---
st.sidebar.header("🕹️ Deal Configuration")

# 1. انتخاب تاریخ (تاثیرگذار بر کف نقدینگی)
closing_date = st.sidebar.date_input("Target Closing Date", date.today())
is_after_may = closing_date >= PIVOT_DATE

# محاسبه حداقل نقدینگی لازم در تاریخ انتخابی
current_min_entry = BASE_OVERDUE + FEES + (MAY_INSTALLMENT if is_after_may else 0)

# 2. اسلایدر نقدینگی (شروع از کفِ محاسبه شده در مرحله قبل)
upfront_cash = st.sidebar.slider("Upfront Cash Commitment (AED)", 
                                 int(current_min_entry), 800000, int(current_min_entry), 5000)

# --- منطق محاسباتی خطی ---
# محاسبه درصد پیشرفت بر اساس نقدینگی مازاد
extra_cash = upfront_cash - current_min_entry
# سقف نقدینگی فرضی برای محاسبه نرخ تخفیف
max_range = 800000 - current_min_entry
progress = extra_cash / max_range if max_range > 0 else 0

# تعدیل قیمت کل (بین 1,216,760 تا 1,156,500)
total_price = 1216760 - (progress * (1216760 - 1156500))

# تعدیل اقساط ماهانه (بین 64,800 تا 32,400)
monthly_inst = 64800 - (progress * (64800 - 32400))

# تعدیل مبلغ تحویل (بین 648,000 تا 324,000)
handover_pay = 648000 - (progress * (648000 - 324000))

# --- نمایش نتایج ---
st.divider()
if is_after_may:
    st.warning(f"⚠️ Date Impact: Closing after May 5th. The May installment ({MAY_INSTALLMENT:,.0f} AED) is now included in the Upfront Cash.")
else:
    st.success(f"✅ Early Bird Advantage: Closing before May 5th. Lower upfront entry confirmed.")

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("UPFRONT CASH", f"{upfront_cash:,.0f} AED")
with k2:
    st.metric("MONTHLY INST.", f"{monthly_inst:,.0f} AED")
    st.caption(f"{'4' if is_after_may else '5'} Months Remaining")
with k3:
    st.metric("FINAL HANDOVER", f"{handover_pay:,.0f} AED")
with k4:
    st.metric("TOTAL ASSET PRICE", f"{total_price:,.0f} AED")

# --- نمودار زمانی داینامیک ---
st.divider()
st.write("### 📅 Payment Schedule Visualization")

# تنظیم محور زمان بر اساس تاریخ بستن معامله
if is_after_may:
    timeline = ['Closing', 'June 26', 'July 26', 'Aug 26', 'Sept 26', 'Handover']
    amounts = [upfront_cash, monthly_inst, monthly_inst, monthly_inst, monthly_inst, handover_pay]
else:
    timeline = ['Closing', 'May 26', 'June 26', 'July 26', 'Aug 26', 'Sept 26', 'Handover']
    amounts = [upfront_cash, monthly_inst, monthly_inst, monthly_inst, monthly_inst, monthly_inst, handover_pay]

fig = go.Figure(data=[
    go.Bar(x=timeline, y=amounts, 
           text=[f"{a:,.0f}" for a in amounts], 
           textposition='auto',
           marker_color=['#D4AF37'] + ['#1f77b4']*(len(timeline)-2) + ['#E74C3C'])
])

fig.update_layout(template="plotly_dark", height=450, title="Cash Outflow Timeline")
st.plotly_chart(fig, use_container_width=True)

# --- تحلیل نهایی ---
st.divider()
col_a, col_b = st.columns(2)
with col_a:
    st.write("### 📈 Investor ROI Analysis")
    market_val = 1243000
    profit_on_entry = market_val - total_price
    st.write(f"- Immediate Equity Gain: {profit_on_entry:,.0f} AED")
    st.write(f"- Price vs Market: {(total_price/market_val - 1)*100:.1f}%")
    st.write(f"- Interest Saved: 100% (No bank financing required)")

with col_b:
    try:
        st.image("plan_2505.png.jpg", caption="Studio Layout C2505", use_container_width=True)
    except:
        st.info("Upload floor plans to GitHub to see them here.")

st.warning("⚠️ MOU Clause: Strict performance-based contract. Default on installments results in 100% forfeiture of all paid capital.")
