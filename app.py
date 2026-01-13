import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz5TpykMcD6f5ZLIBp26HuxOQ-uGOLdHOL0NJzQLq3ag_MzbtosgkLlXqJ6iK16MuKF/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #006699 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-bottom: 5px solid #f1c40f;
    }
    .big-button {
        display: block; width: 100%; padding: 18px; margin: 10px 0;
        text-align: center; color: white !important; font-size: 18px; font-weight: bold;
        text-decoration: none; border-radius: 15px;
    }
    .call-btn { background: #27ae60; }
    .fb-btn { background: #2980b9; }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. ডাটা লোড ---
@st.cache_data(ttl=1)
def load_all_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        r_df = pd.read_csv(get_url("Result")).astype(str)
        a_df = pd.read_csv(get_url("Form_Responses_1")).astype(str)
        return s_df, r_df, a_df
    except:
        return None, None, None

df_s, df_r, df_a = load_all_data()

def upload_image(file):
    try:
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.getvalue()).decode('utf-8')}
        return requests.post("https://api.imgbb.com/1/upload", payload).json()['data']['url']
    except:
        return "-"

# --- ৪. মেনু নেভিগেশন ---
menu = st.sidebar.radio("🧭 প্রধান মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- হোম পেজ ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>ডিজিটাল ক্যাম্পাস ড্যাশবোর্ড</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 কল করুন</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_
