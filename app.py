import streamlit as st
import pandas as pd
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ডিজিটাল একাডেমি", page_icon="🕌", layout="wide")

# --- UI ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background: #f8f9fa; }
    .main-header {
        background: linear-gradient(135deg, #008080 0%, #004d4d 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15); margin-bottom: 30px;
    }
    .stat-card {
        background: white; padding: 25px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #008080;
    }
    .card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #eef2f3;
    }
    .stButton>button {
        background: #008080 !important; color: white !important;
        border-radius: 12px !important; font-weight: 600 !important;
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

# --- সাইডবার ---
with st.sidebar:
    st.markdown("<h2 style='color:#008080; text-align:center;'>📋 মেনুবার</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম ইসলামি একাডেমি</h1><p>ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    df_s = load_data("Student_List")
    total_students = len(df_s) if df_s is not None else 0
    
    df_a = load_data("Form_Responses_1")
    today_date = datetime.now().strftime("%-m/%-d/%Y")
    today_present = 0
    if df_a is not None and not df_a.empty:
        today_present = len(df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)])

    with c1: st.markdown(f"<div class='stat-card'><h3>👨‍🎓 মোট ছাত্র</h3><h2 style='color:#008080;'>{total_students} জন</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'><h3>✅ আজকে উপস্থিত</h3><h2 style='color:#28a745;'>{today_present} জন</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><h3>📅 আজকের তারিখ</h3><h2 style='color:#008080;'>{datetime.now().strftime('%d %b %Y')}</h2></div>", unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        st.info(f"📢 নোটিশ: {df_n.iloc[-1, 0]}")

# ২. স্টুডেন্ট রিপোর্ট (ফটো এরর ফিক্সড)
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#008080;'>🔍 ছাত্রের প্রোফাইল</h2>", unsafe_allow_html=True)
    sid = st.text_input("আইডি (ID) টাইপ করুন:")
    
    if sid:
        df_s = load_data("Student_List")
        if df_s is not None:
            student = df_s[df_s.iloc[:, 0].astype(str) == str(sid)]
            if not student.empty:
                s = student.iloc[0]
                c1, c2 = st.columns([1, 2])
                with c1:
                    # নিরাপদ ফটো লোডিং
                    default_img = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                    photo_val = s.get('Photo_URL')
                    if pd.isna(photo_val) or str(photo_val).strip() == "" or not str(photo_val).startswith("http"):
                        st.image(default_img, width=200)
                    else:
                        try: st.image(str(photo_val), width=200)
                        except: st.image(default_img, width=200)
                with c2:
                    st.markdown(f"<div class='card'><h2>{s.get('Name')}</h2><p>পিতা: {s.get('Father_Name')}<br>মোবাইল: {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
                
                st.write("---")
                t1, t2 = st.tabs(["📊 হাজিরা", "🏆 রেজাল্ট"])
                with t1:
                    df_all_a = load_data("Form_Responses_1")
                    if df_all_a is not None:
                        st.dataframe(df_all_a[df_all_a.iloc[:, 1].astype(str) == str(sid)], use_container_width=True)
                with t2:
                    df_r = load_data("Result_Sheet")
                    if df_r is not None:
                        st.table(df_r[df_r.iloc[:, 0].astype(str) == str(sid)])
            else: st.error("ছাত্র পাওয়া যায়নি।")

# ৩. অ্যাডমিন
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন কোড দিন:", type="password") == "MdmamuN18":
        opt = st.radio("অ্যাকশন:", ["✅ হাজিরা নিন", "➕ নতুন ভর্তি"])
        if opt == "✅ হাজিরা নিন":
            st.markdown(f'<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform?embedded=true" width="100%" height="800"></iframe>', unsafe_allow_html=True)
        else:
            st.markdown(f'<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform?embedded=true" width="100%" height="900"></iframe>', unsafe_allow_html=True)
