import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
import base64
import os

# ۱. تنظیمات اولیه
st.set_page_config(page_title="Skyrise Deal | Strategic Proposal", layout="wide")

# تابع تبدیل عکس به فرمت قابل نمایش در CSS
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# تلاش برای بارگذاری عکس پس‌زمینه
try:
    bin_str = get_base64('sky.jpg')
    # پس‌زمینه مدرن: عکس ثابت + لایه گرادینت که به Warm White ختم می‌شود
    bg_style = f'''
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(253, 251, 247, 0.95)), url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    '''
except:
    # اگر عکس نبود، همان Warm White ساده
    bg_style = '<style>.stApp { background-color: #FDFBF7; }</style>'

# ۲. تزریق CSS (بدون تغییر در منطق شما، فقط بهبود ظاهر)
st.markdown(bg_style, unsafe_allow_html=True)
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stHeader"], footer, #MainMenu {display: none;}
    
    /* باکس‌های متریک: تیره با متن سفید درخشان */
    [data-testid="stMetricValue"] { 
        font-size: clamp(1.6rem, 5vw, 2.8rem) !important; 
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    [data-testid="stMetricLabel"] { 
        color: #D4AF37 !important; 
        font-weight: 700 !important;
        text-transform: uppercase;
    }
    .stMetric { 
        background-color: rgba(26, 30, 39, 0.9) !important; /* حالت شیشه‌ای تیره */
        border: 1px solid #D4AF37 !important; 
        border-radius: 15px;
        backdrop-filter: blur(10px); /* افکت مدرن بلور */
    }
    
    /* باکس‌های منطق معامله */
    .logic-box {
        background-color: rgba(26, 30, 39, 0.9);
        color: #FFFFFF !important;
        padding: 20px;
        border-left: 5px solid #D4AF37;
        border-radius: 10px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .logic-box h3, .logic-box p, .logic-box b { color: #FFFFFF !important; }

    /* متون روی صفحه اصلی (تیره برای تضاد با Warm White) */
    h1, h3, h4, p, label { color: #1a1e27 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- هدر ---
st.markdown("<h1 style='text-align: center; color: #D4AF37 !important; font-weight:800;'>ASSET ACQUISITION STRATEGY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555 !important;'>Binghatti Skyrise Tower C | Strategic Portfolio</p>", unsafe_allow_html=True)

# --- بخش منطق معامله ---
with st.container():
    st.markdown("""
    <div class='logic-box'>
        <h3 style='color: #D4AF37 !important; margin-top:0;'>The Strategy: "Liability Assumption"</h3>
        <p>This model allows an investor to secure full ownership by assuming the remaining liabilities. 
        Benefit from a <b>0% interest-free private installment plan</b> until December 2026.</p>
    </div>
    """, unsafe_allow_html=True)

# --- ورودی‌ها ---
st.write("### 🕹️ Adjust Parameters")
col_in1, col_in2 = st.columns([1, 2])

# منطق محاسبات (بدون تغییر)
installment_dates = [date(2026, 5, 5), date(2026, 6, 5), date(2026, 7, 5), date(2026, 8, 5), date(2026, 9, 5)]
with col_in1:
    closing_date = st.date_input("Contract Date", date.today())
    overdue_count = len([d for d in installment_dates if closing_date >= d])
    future_dates = [d for d in installment_dates if closing_date < d]
    min_upfront = 216000 + 28760 + (overdue_count * 64800)
    max_upfront = 1156500 - (len(future_dates) * 32400) - 324000

with col_in2:
    upfront_cash = st.slider("Initial Cash (AED)", float(min_upfront), float(max(max_upfront, min_upfront + 10000)), float(min_upfront), 5000.0)

# محاسبات درونیابی
range_val = max_upfront - min_upfront
progress = (upfront_cash - min_upfront) / range_val if range_val > 0 else 0
current_total = 1216760 - (progress * (1216760 - 1156500))
current_monthly = 64800 - (progress * (64800 - 32400))
current_handover = 648000 - (progress * (648000 - 324000))

# --- نمایش شاخص‌ها ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("ENTRY CASH", f"{upfront_cash:,.0f}")
m2.metric("MONTHLY", f"{current_monthly:,.0f}")
m3.metric("HANDOVER", f"{current_handover:,.0f}")
m4.metric("TOTAL PRICE", f"{current_total:,.0f}")

# --- مقایسه بازار ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<div class='logic-box' style='background-color:#4A4A4A; border-left-color:#888;'><h4>Standard Resale</h4><p>❌ Upfront: ~670k AED</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='logic-box'><h4>Creative Strategy</h4><p>✅ Upfront: {upfront_cash:,.0f} AED</p></div>", unsafe_allow_html=True)

# --- نمودار زمانی ---
st.divider()
labels = ["Entry"] + [d.strftime("%b %y") for d in future_dates] + ["Handover"]
values = [upfront_cash] + [current_monthly] * len(future_dates) + [current_handover]
# پالت رنگی: طلایی به خاکستری تیره (Spectrum)
colors = ['#D4AF37', '#A49B93', '#8C7C5A', '#665F50', '#403D39', '#2D2D2D']
final_colors = [colors[0]] + [colors[2]] * len(future_dates) + [colors[5]]

fig = go.Figure(data=[go.Bar(x=labels, y=values, text=[f"{v:,.0f}" for v in values], textposition='auto', marker_color=final_colors)])
fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(tickfont=dict(color="#1a1e27")))
st.plotly_chart(fig, use_container_width=True)

st.error("⚠️ PERFORMANCE-BASED MOU: DEFAULT LEADS TO FORFEITURE.")
st.markdown("<p style='text-align: center; opacity: 0.8; color: #1a1e27 !important;'>DR. AMIR YASREBI | CEO ALMOHALENIN</p>", unsafe_allow_html=True)
