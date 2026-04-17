import streamlit as st
from datetime import date

# تنظیمات صفحه
st.set_page_config(page_title="AMIR - Skyrise Deal", layout="wide")

# برندینگ و تیتر
st.title("🏗️  Strategic Investment Calculator")
st.subheader("Binghatti Skyrise - Units C2505 & C2506")

# بخش نمایش تصاویر (پلان واحدها)
col1, col2 = st.columns(2)
with col1:
    st.image("plan_2505.png", caption="Unit C2505 - Floor Plan") # نام فایل عکس خود را اینجا بگذارید
with col2:
    st.image("plan_2506.png", caption="Unit C2506 - Floor Plan")

# ورودی‌های کاربر
st.sidebar.header("Deal Parameters")
target_date = st.sidebar.date_input("Target Closing Date", date.today())
deal_type = st.sidebar.selectbox("Select Deal Tier", ["Break-Even Exit", "Strategic All-Inclusive"])

# داده‌های ثابت از SOA
[span_0](start_span)[span_1](start_span)overdue_now = 216000 #[span_0](end_span)[span_1](end_span)
[span_2](start_span)[span_3](start_span)next_installment_total = 64800 #[span_2](end_span)[span_3](end_span)
pivot_date = date(2026, 5, 5)

# منطق محاسبه زمان
is_after_may = target_date >= pivot_date
current_overdue = overdue_now + (next_installment_total if is_after_may else 0)

# تعیین قیمت کل بر اساس انتخاب کاربر
total_price = 1156500 if deal_type == "Break-Even Exit" else 1216760
fees = 28760 # NOC + 2% Commission

# خروجی نهایی
st.divider()
st.header(f"💰 Offer Summary: {deal_type}")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Initial Cash Required", f"{current_overdue + fees:,.0f} AED")
    st.caption("Includes Overdue + NOC + Commission")

with c2:
    remaining_installments = 324000 if not is_after_may else 259200
    st.metric("Future Monthly Total", f"{remaining_installments:,.0f} AED")
    st.write("64,800 AED / month")

with c3:
    st.metric("Final Handover (Dec 2026)", "648,000 AED")
    st.write("30% of Total Value")

st.success(f"Total Acquisition Cost: {total_price:,.0f} AED")

# بخش ویدئو
st.divider()
st.subheader("Project Walkthrough")
# st.video("sky_rise_render.mp4") # لینک یا فایل ویدئو را اینجا بگذارید
