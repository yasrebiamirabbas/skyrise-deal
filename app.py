import streamlit as st
from datetime import date
import os

# تنظیمات اصلی صفحه
st.set_page_config(page_title="AMIR - Skyrise Deal", layout="wide")

# بخش هدر و برندینگ
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Deal Strategic Investment Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Binghatti Skyrise - Tower C (C2505 & C2506)</h3>", unsafe_allow_html=True)

# نمایش تصاویر پلان‌ها با چک کردن وجود فایل
st.divider()
col_img1, col_img2 = st.columns(2)

# نام فایل‌ها را اینجا چک کنید (باید دقیقاً با فایل‌های گیت‌هاب یکی باشد)
img1_path = "plan_2505.png"
img2_path = "plan_2506.png"

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

# ورودی‌های کاربر در سایدبار
st.sidebar.header("Deal Parameters")
target_date = st.sidebar.date_input("Target Closing Date", date.today())
deal_tier = st.sidebar.radio("Select Strategy Tier", ["Break-Even Exit", "Strategic All-Inclusive"])

# داده‌های استخراج شده از مستندات SOA
[span_0](start_span)[span_1](start_span)overdue_now = 216000 # مجموع بدهی معوقه هر دو واحد[span_0](end_span)[span_1](end_span)
[span_2](start_span)[span_3](start_span)next_installment = 64800 # مجموع اقساط سررسید 5 می[span_2](end_span)[span_3](end_span)
[span_4](start_span)[span_5](start_span)pivot_date = date(2026, 5, 5) # تاریخ کلیدی تغییر نقدینگی[span_4](end_span)[span_5](end_span)
noc_comm_fees = 28760 # هزینه NOC + 2% کمیسیون

# منطق محاسبات زمانی
is_after_may = target_date >= pivot_date
calculated_overdue = overdue_now + (next_installment if is_after_may else 0)

# تعیین قیمت نهایی بر اساس استراتژی منتخب
if deal_tier == "Break-Even Exit":
    total_deal_value = 1156500
else:
    total_deal_value = 1216760

# نمایش نتایج نهایی
st.divider()
st.header(f"📊 Summary of {deal_tier} Offer")

c1, c2, c3 = st.columns(3)
with c1:
    initial_cash = calculated_overdue + noc_comm_fees
    st.metric("Initial Cash Required", f"{initial_cash:,.0f} AED")
    st.caption("Includes: Current Overdue + NOC + Commission")

with c2:
    # [span_6](start_span)[span_7](start_span)مجموع اقساط ماهانه باقی‌مانده[span_6](end_span)[span_7](end_span)
    remaining_monthly = 324000 if not is_after_may else 259200
    st.metric("Future Monthly Payments", f"{remaining_monthly:,.0f} AED")
    st.write("64,800 AED / month (Total for both units)")

with c3:
    st.metric("Final Handover (Dec 1, 2026)", "648,000 AED")
    [span_8](start_span)[span_9](start_span)st.write("30% Final Payment to Developer[span_8](end_span)[span_9](end_span)")

# نمایش قیمت تمام شده خریدار
st.success(f"**Total Acquisition Price for the Buyer: {total_deal_value:,.0f} AED**")

# بند حقوقی تفاهم‌نامه (MOU)
st.warning("⚠️ MOU Term: In case of failure to settle any monthly installments, all previous payments will be forfeited in favor of the seller, and the transaction will be deemed null and void.")
