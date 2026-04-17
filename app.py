import streamlit as st
from datetime import date

# تنظیمات صفحه برای نمایش بهتر در موبایل و دسکتاپ
st.set_page_config(page_title="ALMOHALENIN - Binghatti Deal", layout="wide")

# استایل‌دهی ساده برای تیترها
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>ALMOHALENIN Strategic Investment Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Binghatti Skyrise - Tower C (C2505 & C2506)</h3>", unsafe_allow_html=True)

# بخش نمایش فایل‌های تصویری (پلان‌ها)
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.image("plan_2505.png", caption="Unit C2505 Plan", use_column_width=True)
with col2:
    st.image("plan_2506.png", caption="Unit C2506 Plan", use_column_width=True)

# ورودی‌های تعاملی در سایدبار
st.sidebar.header("Deal Customization")
target_date = st.sidebar.date_input("Target Closing Date", date.today())
deal_tier = st.sidebar.radio("Select Strategy", ["Break-Even Exit", "Strategic All-Inclusive"])

# داده‌های استخراج شده از SOA
[span_0](start_span)[span_1](start_span)overdue_now = 216000 # مجموع بدهی معوقه هر دو واحد[span_0](end_span)[span_1](end_span)
[span_2](start_span)[span_3](start_span)next_installment = 64800 # مجموع قسط 5 می برای هر دو واحد[span_2](end_span)[span_3](end_span)
[span_4](start_span)[span_5](start_span)pivot_date = date(2026, 5, 5) # موعد قسط بعدی[span_4](end_span)[span_5](end_span)
noc_comm_fees = 28760 # هزینه NOC و 2% کمیسیون

# منطق محاسباتی زمان
is_after_may = target_date >= pivot_date
calculated_overdue = overdue_now + (next_installment if is_after_may else 0)

# تعیین قیمت نهایی بر اساس استراتژی
if deal_tier == "Break-Even Exit":
    total_deal_value = 1156500
else:
    total_deal_value = 1216760

# نمایش نتایج به صورت بصری
st.divider()
st.header(f"📊 Offer Details: {deal_tier}")

m1, m2, m3 = st.columns(3)
with m1:
    initial_cash = calculated_overdue + noc_comm_fees
    st.metric("Initial Cash Required", f"{initial_cash:,.0f} AED", delta="Includes Overdue & Fees")
    st.caption("Payable immediately to secure the deal.")

with m2:
    # مجموع اقساط باقی‌مانده از کل قیمت منهای بدهی معوقه و قسط نهایی
    future_installments = 324000 if not is_after_may else 259200
    st.metric("Future Monthly Payments", f"{future_installments:,.0f} AED")
    st.write("64,800 AED / Month (Total)")

with m3:
    st.metric("Final Handover (Dec 2026)", "648,000 AED")
    st.write("30% Final Payment for 2 Units")

# پیام نهایی و قیمت کل
st.info(f"The Total Acquisition Price for the buyer is exactly: **{total_deal_value:,.0f} AED**")

# بخش ویدئو (در صورت داشتن فایل، نام آن را جایگزین کنید)
st.divider()
st.subheader("Project Presentation")
# st.video("sky_rise_render.mp4") # اگر فایل ویدئو دارید، این خط را فعال کنید
