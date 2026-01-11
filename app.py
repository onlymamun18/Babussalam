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
    .stApp { background-color: #f0f4f7; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 2px solid #008080; }
    .header-container {
        background: linear-gradient(135deg, #008080 0%, #005a5a 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-bottom: 30px;
    }
    .stat-card {
        background: white; padding: 25px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 5px solid #008080;
        transition: 0.3s;
    }
    .stat-card:hover { transform: translateY(-5px); }
    .notice-card {
        background: #fff8e1; padding: 20px; border-radius: 15px; border-left: 10px solid #ffa000;
        color: #5f4b00; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background: linear-gradient(135deg, #008080, #006666) !important;
        color: white !important; border-radius: 10px !important; padding: 15px !important;
        font-weight: bold !important; border: none !important;
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
    menu = st.sidebar.radio("", ["📊 ড্যাশবোর্ড", "🔍 রিপোর্ট কার্ড (Guardian)", "🔐 অ্যাডমিন মাস্টার"])

# ১. ড্যাশবোর্ড
if menu == "📊 ড্যাশবোর্ড":
    st.markdown("""
        <div class='header-container'>
            <h1 style='margin:0;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>
            <p style='opacity:0.9; font-size:18px;'>ডিজিটাল ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    df_s = load_data("Student_List")
    total_students = len(df_s) if df_s is not None else 0
    
    c1.markdown(f"<div class='stat-card'><h3>👨‍🎓 মোট ছাত্র</h3><h2 style='color:#008080;'>{total_students} জন</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-card'><h3>📅 আজকের তারিখ</h3><h2 style='color:#008080;'>{datetime.now().strftime('%d %b %Y')}</h2></div>", unsafe_allow_html=True)
    
    df_n = load_data("Notice")
    notice_msg = df_n.iloc[-1, 0] if df_n is not None and not df_n.empty else "কোনো নতুন নোটিশ নেই"
    c3.markdown(f"<div class='stat-card'><h3>📢 অ্যাক্টিভ নোটিশ</h3><p style='color:#008080; font-weight:bold;'>{notice_msg}</p></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# ২. গার্ডিয়ান সেকশন
elif menu == "🔍 রিপোর্ট কার্ড (Guardian)":
    st.markdown("<h2 style='color:#008080;'>🔍 ছাত্রের রিপোর্ট অনুসন্ধান</h2>", unsafe_allow_html=True)
    sid = st.text_input("ছাত্রের আইডি (ID) লিখুন:", placeholder="আইডি টাইপ করে এন্টার দিন")
    
    if sid:
        df_s = load_data("Student_List")
        if df_s is not None:
            student = df_s[df_s.iloc[:, 0].astype(str) == str(sid)]
            if not student.empty:
                s = student.iloc[0]
                col1, col2 = st.columns([1, 2])
                with col1:
                    img_url = str(s.get('Photo_URL', 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'))
                    st.image(img_url, width=220)
                with col2:
                    st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.05); border-left:5px solid #008080;'><h2>{s.get('Name')}</h2><p><b>পিতার নাম:</b> {s.get('Father_Name')}<br><b>মোবাইল:</b> {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
                
                st.write("---")
                t1, t2 = st.tabs(["📅 প্রতিদিনের হাজিরা", "🏆 পরীক্ষার রেজাল্ট"])
                with t1:
                    df_a = load_data("Form_Responses_1")
                    if df_a is not None:
                        st.dataframe(df_a[df_a.iloc[:, 1].astype(str) == str(sid)], use_container_width=True)
                with t2:
                    df_r = load_data("Result_Sheet")
                    if df_r is not None:
                        st.table(df_r[df_r.iloc[:, 0].astype(str) == str(sid)])
            else: st.error("দুঃখিত, এই আইডি দিয়ে কোনো ছাত্র খুঁজে পাওয়া যায়নি।")

# ৩. অ্যাডমিন কন্ট্রোল
elif menu == "🔐 অ্যাডমিন মাস্টার":
    st.markdown("<h2 style='color:#008080;'>🔐 অ্যাডমিন সিকিউরড জোন</h2>", unsafe_allow_html=True)
    pin = st.text_input("অ্যাডমিন পিন (PIN) দিন:", type="password")
    
    if pin == "MdmamuN18":
        st.success("লগইন সফল!")
        task = st.radio("অ্যাকশন নির্বাচন করুন:", ["✅ ডিজিটাল হাজিরা নিন", "➕ নতুন ছাত্র ভর্তি করুন", "📢 নোটিশ বোর্ড এডিট"])
        
        if task == "✅ ডিজিটাল হাজিরা নিন":
            st.markdown("<div class='notice-card'>নিচে হাজিরা দিন এবং সাবমিট বাটনে ক্লিক করুন।</div>", unsafe_allow_html=True)
            hajira_form = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform?embedded=true"
            st.markdown(f'<iframe src="{hajira_form}" width="100%" height="800" frameborder="0"></iframe>', unsafe_allow_html=True)

        elif task == "➕ নতুন ছাত্র ভর্তি করুন":
            vorti_form = "https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform?embedded=true"
            st.markdown(f'<iframe src="{vorti_form}" width="100%" height="1000" frameborder="0"></iframe>', unsafe_allow_html=True)
            
        elif task == "📢 নোটিশ বোর্ড এডিট":
            st.warning("নোটিশ পরিবর্তন করতে সরাসরি গুগল শিটের 'Notice' ট্যাবে গিয়ে প্রথম কলামে লিখুন।")
            
    elif pin != "":
        st.error("ভুল পিন! সঠিক পিন ছাড়া কন্ট্রোল সম্ভব নয়।")
