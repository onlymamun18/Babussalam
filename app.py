import streamlit as st
import pandas as pd
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={name}'

st.set_page_config(page_title="Babussalam Digital Campus", page_icon="🕌", layout="wide")

# ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .header-box { background: linear-gradient(135deg, #008080, #005a5a); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px; }
    .notice-card { background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 10px solid #ffc107; font-size: 18px; color: #856404; font-weight: bold; }
    .stButton>button { background-color: #008080 !important; color: white !important; font-weight: bold; border-radius: 10px; height: 50px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# মেনুবার
menu = st.sidebar.radio("মেনু নির্বাচন করুন:", ["🏠 হোম পেজ", "🔍 ছাত্র রিপোর্ট (গার্ডিয়ান)", "🔐 অ্যাডমিন কন্ট্রোল"])

# ১. হোম পেজ (নোটিশ বোর্ড)
if menu == "🏠 হোম পেজ":
    st.markdown("<div class='header-box'><h1>🕌 বাবুস সালাম ইসলামি একাডেমি</h1><p>ডিজিটাল ম্যানেজমেন্ট সিস্টেম</p></div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    
    st.markdown("### 📢 জরুরি নোটিশ")
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        st.markdown(f"<div class='notice-card'>{df_n.iloc[-1, 0]}</div>", unsafe_allow_html=True)
    else:
        st.info("বর্তমানে কোনো নোটিশ নেই।")

# ২. ছাত্র রিপোর্ট (গার্ডিয়ান সেকশন)
elif menu == "🔍 ছাত্র রিপোর্ট (গার্ডিয়ান)":
    st.markdown("<h2 style='color:#008080;'>🔍 ছাত্রের প্রতিদিনের রিপোর্ট</h2>", unsafe_allow_html=True)
    sid = st.text_input("ছাত্রের আইডি (ID) দিন:")
    
    if sid:
        # হাজিরা চেক
        df_a = load_data("Form_Responses_1")
        # রেজাল্ট চেক
        df_r = load_data("Result_Sheet")
        
        t1, t2 = st.tabs(["📅 হাজিরা রিপোর্ট", "🏆 পরীক্ষার রেজাল্ট"])
        
        with t1:
            if df_a is not None:
                # আজকের তারিখের হাজিরা আছে কি না দেখা
                u_att = df_a[df_a.iloc[:, 1].astype(str) == str(sid)]
                if not u_att.empty:
                    st.success(f"আইডি {sid} এর হাজিরার তথ্য পাওয়া গেছে।")
                    st.dataframe(u_att, use_container_width=True)
                else:
                    st.warning("আজকের কোনো হাজিরা রেকর্ড পাওয়া যায়নি।")
        
        with t2:
            if df_r is not None:
                u_res = df_r[df_r.iloc[:, 0].astype(str) == str(sid)]
                st.table(u_res)

# ৩. অ্যাডমিন কন্ট্রোল (হাজিরা ও ছাত্র যোগ)
elif menu == "🔐 অ্যাডমিন কন্ট্রোল":
    st.markdown("<h2 style='color:#008080;'>🔐 অ্যাডমিন লগইন</h2>", unsafe_allow_html=True)
    pin = st.text_input("আপনার গোপন পিন (PIN) দিন:", type="password")
    
    if pin == "MdmamuN18":
        st.success("স্বাগতম অ্যাডমিন!")
        
        task = st.selectbox("কি করতে চান?", ["✅ হাজিরা নিন (টিক চিহ্ন)", "➕ নতুন ছাত্র ভর্তি", "📝 নোটিশ আপডেট করুন"])
        
        if task == "✅ হাজিরা নিন (টিক চিহ্ন)":
            st.info("নিচের লিঙ্কে ক্লিক করে চেকবলিস্ট থেকে আজকের হাজিরা সম্পন্ন করুন।")
            # আপনার গুগল ফর্মের হাজিরা লিঙ্ক যেখানে ছাত্রের নামের লিস্ট আছে
            hajira_form = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform"
            st.markdown(f'<a href="{hajira_form}" target="_blank"><button>📝 হাজিরা ফর্ম ওপেন করুন</button></a>', unsafe_allow_html=True)
            
        elif task == "➕ নতুন ছাত্র ভর্তি":
            vorti_form = "https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform"
            st.markdown(f'<iframe src="{vorti_form}" width="100%" height="800"></iframe>', unsafe_allow_html=True)
            
        elif task == "📝 নোটিশ আপডেট করুন":
            st.warning("নোটিশ পরিবর্তন করতে সরাসরি আপনার গুগল শিটের 'Notice' ট্যাবে গিয়ে প্রথম লাইনে নতুন নোটিশটি লিখুন।")
            
    elif pin != "":
        st.error("ভুল পিন! সঠিক পিন দিয়ে চেষ্টা করুন।")
