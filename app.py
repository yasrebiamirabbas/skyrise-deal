import streamlit as st
import plotly.graph_objects as go
from datetime import date
import os
# تنظیمات تم لوکس
st.set_page_config(page_title="ALMOHALENIN | Binghatti Executive", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# هدر برندینگ
st.title("🏆 ALMOHALENIN | Creative Exit Strategy")
st.subheader("Binghatti Skyrise Tower C - Investment Portal")

# نمایش تصاویر پلان‌ها با چک کردن وجود فایل
st.divider()
col_img1, col_img2 = st.columns(2)

# نام فایل‌ها را اینجا چک کنید (باید دقیقاً با فایل‌های گیت‌هاب یکی باشد)
img1_path = "plan_2505.png.jpg"
img2_path = "plan_2506.png.jpg"

with col_img1:
    if os.path.exists(img1_path):
        st.image(img1_path, caption="Unit C2505 Floor Plan", use_container_width=True)
    else:
        st.warning(f"Image {img1_path} not found in repository.")

with col_img2:
    if os.path.exists(img2_path):
        st.image(img2_path, caption="Unit C2506 Floor Plan", use_container_width=True)
    else:
        st.warning(f"Image {img2_path} not found in repository.")

# سایدبار کنترل
st.sidebar.header("🕹️ Deal Controller")
target_date = st.sidebar.date_input("Closing Date", date.today())
equity_recovery = st.sidebar.slider("Seller Equity Recovery (Your Profit/Return)", 0, 550000, 0, 5000)

# محاسبات پایه از SOA
overdue_now = 216000 
#[span_1](end_span)[span_2](end_span)
next_inst = 64800
#[span_3](end_span)[span_4](end_span)
pivot_date = date(2026, 5, 5)
#[span_5](end_span)[span_6](end_span)
fees = 28760 
# NOC + 2% Commission
remaining_balance = 972000 # کل مانده اقساط باقی‌مانده بعد از تسویه معوقات

# منطق زمانی
is_after_may = target_date >= pivot_date
initial_overdue = overdue_now + (next_inst if is_after_may else 0)

# مبالغ نهایی
down_payment = initial_overdue + fees + equity_recovery
total_acquisition = 1188000 + fees + equity_recovery
#[span_7](end_span)[span_8](end_span)
market_avg = 1243000 
#[span_9](end_span)

# نمایش شاخص‌های اصلی
st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("INITIAL CASH REQUIRED", f"{down_payment:,.0f} AED", help="Overdue + Fees + Selected Equity")
with c2:
    st.metric("TOTAL ACQUISITION COST", f"{total_acquisition:,.0f} AED")
with c3:
    savings = market_avg - total_acquisition
    st.metric("SAVINGS VS MARKET", f"{savings:,.0f} AED", delta=f"{(savings/market_avg)*100:.1f}%")

# نمودار تحلیل پرداخت‌ها
st.write("### 📊 Payment Structure Breakdown")
fig = go.Figure(data=[
    go.Bar(name='Initial Cash', x=['Investment Structure'], y=[down_payment], marker_color='#d4af37'),
    go.Bar(name='Monthly Installments', x=['Investment Structure'], y=[324000 if not is_after_may else 259200], marker_color='#1e2130'),
    go.Bar(name='Handover (Dec 2026)', x=['Investment Structure'], y=[648000], marker_color='#3e4561')
])
fig.update_layout(barmode='stack', height=400, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# تحلیل استراتژیک
st.divider()
st.write("### 💡 Strategy Analysis")
col1, col2 = st.columns(2)

with col1:
    if equity_recovery == 0:
        st.success("STRICT DISTRESSED: This is a fast-exit scenario with the lowest possible entry barrier for the buyer.")
    elif equity_recovery < 250000:
        st.info("BALANCED GROWTH: A mid-tier offer providing equity return while keeping the price well below market average.")
    else:
        st.warning("PREMIUM STRUCTURE: A high-leverage acquisition for buyers seeking long-term interest-free plans.")

with col2:
    st.write(f"**Investor Memo:** By acquiring this unit for {total_acquisition:,.0f} AED, the buyer secures a prime asset in Business Bay with an interest-free credit bridge until December 2026. This structure provides a 5x leverage compared to standard bank-financed purchases.")

# کپی‌رایت
st.markdown("<p style='text-align: center; opacity: 0.5;'>Managed by ALMOHALENIN | Dr. Amir Yasrebi</p>", unsafe_allow_html=True)
