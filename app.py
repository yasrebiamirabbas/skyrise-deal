import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd

# تنظیمات صفحه برای وضوح حداکثری
st.set_page_config(page_title="ALMOHALENIN | Investment Portal", layout="wide")

# استایل‌دهی اختصاصی برای خوانایی باکس‌ها (High Contrast)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #FFFFFF !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { font-size: 16px !important; color: #D4AF37 !important; text-transform: uppercase; }
    .stMetric { background-color: #161b22; border: 2px solid #D4AF37; padding: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 ALMOHALENIN | Executive Acquisition Dashboard")
st.subheader("Binghatti Skyrise Tower C - Strategic Resale Logic")

# --- منطق محاسباتی (Linear Logic) ---
st.sidebar.header("🕹️ Investment Slider")
# تاریخ امروز برای چک کردن ۵ می
today = date.today()
pivot_date = date(2026, 5, 5)

# مقادیر ثابت
overdue_base = 216000 
fees = 28760
next_inst_val = 64800

# تعیین حداقل پیش‌پرداخت بر اساس تاریخ
min_entry = overdue_base + fees
if today >= pivot_date:
    min_entry += next_inst_val

# اسلایدر برای میزان پیش‌پرداخت (بین حداقل تا حداکثر برای رسیدن به سر‌به‌سر)
# سقف اسلایدر را حدودی روی 670,000 درهم می‌گذاریم که نقطه سر‌به‌سر کامل است
upfront_cash = st.sidebar.slider("Upfront Cash Commitment (AED)", 
                                 int(min_entry), 700000, int(min_entry), 5000)

# --- فرمول‌نویسی خطی (Linear Interpolation) ---
# نقطه A (حداقل نقدینگی): قیمت 1,216,760 | اقساط 64,800 | تحویل 648,000
# نقطه B (حداکثر نقدینگی): قیمت 1,156,500 | اقساط 32,400 | تحویل 324,000

# محاسبه درصد پیشرفت اسلایدر بین دو نقطه
range_width = 700000 - min_entry
progress = (upfront_cash - min_entry) / range_width if range_width != 0 else 0

# اعمال تغییرات خطی
total_price = 1216760 - (progress * (1216760 - 1156500))
monthly_inst = 64800 - (progress * (64800 - 32400))
handover_pay = 648000 - (progress * (648000 - 324000))

# --- نمایش شاخص‌ها با وضوح بالا ---
st.divider()
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("UPFRONT PAYMENT", f"{upfront_cash:,.0f} AED")
    st.caption("Due at Contract Signature")
with k2:
    st.metric("MONTHLY INSTALLMENT", f"{monthly_inst:,.0f} AED")
    st.caption("5 Months (May-Sept 2026)")
with k3:
    st.metric("FINAL HANDOVER", f"{handover_pay:,.0f} AED")
    st.caption("Due December 2026")
with k4:
    st.metric("TOTAL ASSET PRICE", f"{total_price:,.0f} AED")
    st.caption("All-Inclusive Valuation")

# --- نمودار زمانی (Payment Timeline) ---
st.divider()
st.write("### 📅 Payment Timeline Visualization")

# داده‌های نمودار خطی زمانی
timeline_dates = ['Contract Signature', 'May 2026', 'June 2026', 'July 2026', 'Aug 2026', 'Sept 2026', 'Handover (Dec)']
payments = [upfront_cash, monthly_inst, monthly_inst, monthly_inst, monthly_inst, monthly_inst, handover_pay]

fig = go.Figure()

# اضافه کردن میله‌ها برای هر مرحله
fig.add_trace(go.Bar(
    x=timeline_dates,
    y=payments,
    text=[f"{p:,.0f}" for p in payments],
    textposition='auto',
    marker_color=['#D4AF37', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#E74C3C'],
    name="Payment Amount"
))

fig.update_layout(
    title="Cash Outflow Schedule",
    xaxis_title="Project Milestones",
    yaxis_title="Amount (AED)",
    template="plotly_dark",
    height=500,
    margin=dict(l=20, r=20, t=50, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# --- تحلیل استراتژیک ---
st.divider()
col_text, col_img = st.columns([1, 1])

with col_text:
    st.write("### 💡 Investment Analysis")
    if progress > 0.8:
        st.success(f"**CASH OPTIMIZED:** You are acquiring the unit at the Break-Even price of {total_price:,.0f} AED. Your future liabilities are reduced by 50%.")
    elif progress < 0.2:
        st.info(f"**LIQUIDITY OPTIMIZED:** You are entering the deal with the minimum cash possible (**{upfront_cash:,.0f} AED**), utilizing the seller's credit bridge for the remaining balance.")
    
    st.write(f"""* Leverage Ratio: You control a 1.2M AED asset with only {upfront_cash/total_price*100:.1f}% down payment.
    * Interest Savings: 0% interest on all future installments.
    * Market Comparison: Current Tower C average is 1,243,000 AED.
    """)

with col_img:
    # نمایش عکس‌ها با وضوح بالا
    try:
        st.image("plan_2505.png.jpg", caption="Layout C2505", use_container_width=True)
    except:
        st.write("Floor plan image not found in repository.")

st.warning("⚠️ Forfeiture Clause: This performance-based deal requires strict adherence to the installment dates. Any default renders the MOU void with no refund of previous payments.")
