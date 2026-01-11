import streamlit as st
import pandas as pd
from datetime import datetime

# --- ডাটাবেস কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={name}'

# পেজ কনফিগারেশন
st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- প্রিমিয়াম কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    /* পুরো অ্যাপের ব্যাকগ্রাউন্ড */
    .stApp { background-color: #f0f4f7; }
    
    /* সাইডবার ডিজাইন */
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 2px solid #008080; }
    
    /* মেইন হেডার */
    .header-container {
        background: linear-gradient(135deg, #008080 0%, #005a5a 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    /* ড্যাশবোর্ড কার্ড */
    .stat-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-bottom: 5px solid #008080;
        transition: 0.3s;
    }
    .stat-card:hover { transform: translateY(-5px); }
    
    /* নোটিশ বোর্ড ডিজাইন */
    .notice-card {
        background: #fff8e1;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #ffa000;
        color: #5f4b00;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* বাটন ডিজাইন */
    .stButton>button {
        background: linear-gradient(135deg, #008080, #006666) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,128,128,0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return df
    except: return None

# --- নেভিগেশন ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color:#008080;'>🏫 কন্ট্রোল সেন্টার</h1>", unsafe_allow_html=True)
    menu = st.radio("", ["📊 ড্যাশবোর্ড", "🔍 রিপোর্ট কার্ড (Guardian)", "🔐 অ্যাডমিন মাস্টার"])

# ১. ড্যাশবোর্ড (প্রিমিয়াম লুক)
if menu == "📊 ড্যাশবোর্ড":
    st.markdown("""
        <div class='header-container'>
            <h1 style='margin:0;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>
            <p style='opacity:0.9; font-size:18px;'>ডিজিটাল ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p>
        </div>
    """, unsafe_allow_html=True)
    
    # স্ট্যাটাস কার্ডস
    c1, c2, c3 = st.columns(3)
    df_s = load_data("Student_List")
    total_students = len(df_s) if df_s is not None else 0
    
    c1.markdown(f"<div class='stat-card'><h3>👨‍🎓 মোট ছাত্র</h3><h2 style='color:#008080;'>{total_students} জন</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-card'><h3>📅 আজকের তারিখ</h3><h2 style='color:#008080;'>{datetime.now().strftime('%d %b %Y')}</h2></div>", unsafe_allow_html=True)
    
    df_n = load_data("Notice")
    notice_msg = df_n.iloc[-1, 0] if df_n is not None and not df_n.empty else "কোনো নতুন নোটিশ নেই"
    c3.markdown(f"<div class='stat-card'><h3>📢 অ্যাক্টিভ নোটিশ</h3><p style='color:#008080; font-weight:bold;'>{notice_msg}</p></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.image("
