import streamlit as st
import pandas as pd
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- অস্থির UI ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f6; }
    /* মেইন হেডার */
    .main-header {
        background: linear-gradient(135deg, #008080 0%, #004d4d 100%);
        padding: 45px; border-radius: 25px; color: white; text-align: center;
        box-shadow: 0 15px 30px rgba(0,128,128,0.2); margin-bottom: 35px;
        border-bottom: 8px solid #00b3b3;
    }
    /* স্ট্যাটাস কার্ড */
    .stat-card {
        background: white; padding: 25px; border-radius: 18px;
        text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        border-top: 5px solid #008080; transition: 0.3s;
    }
    .stat-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.1); }
    
    /* কন্টাক্ট বক্স - অস্থির লুক */
    .contact-box {
        background: #ffffff;
        padding: 15px; border-radius: 12px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-top: 20px; text-align: center;
    }
    .contact-link {
        color: #ff4b4b !important; font-weight: bold; text-decoration: none; font-size: 18px;
    }
    
    /* সাইডবার কন্টাক্ট */
    .sidebar-contact {
        background: #e6f2f2; padding: 15px; border-radius: 10px;
        border: 1px dashed #008080; text-align: center; margin-top: 50px;
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
    st.markdown("<h1 style='color:#008080; text-align:center;'>🏫 বাবুস সালাম</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("মেনু নির্বাচন করুন", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])
    
    # সাইডবারে অস্থির কন্টাক্ট সেকশন
    st.markdown(f"""
        <div class='sidebar-contact'>
            <p style='margin:0; font-size:12px; color:#666;'>যেকোনো প্রয়োজনে</p>
            <p style='margin:0; font-weight:bold; color:#008080;'>📞 01954343364</p>
        </div>
    """, unsafe_allow_html=True)

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("""
        <div class='main-header'>
            <h1 style='margin:0; font-size:40px;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>
            <p style='font-size: 20px; opacity: 0.9;'>ডিজিটাল ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    df_s = load_data("Student_List")
    total_students = len(df_s) if df_s is not None else 0
    
    df_a = load_data("Form_Responses_1")
    today_date = datetime.now().strftime("%-m/%-d/%Y")
    today_present = 0
    if df_a is not None and not df_a.empty:
        today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)]
        if not today_data.empty:
            names_string = today_data.iloc[:, 1].astype(str).str.cat(sep=',')
            today_present = len([n for n in names_string.split(',') if n.strip() != ""])

    with c1: st.markdown(f"<div class='stat-card'><h3>👨‍🎓 মোট ছাত্র</h3><h2 style='color:#008080;'>{total_students} জন</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'><h3>✅ আজকে উপস্থিত</h3><h2 style='color:#28a745;'>{today_present} জন</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><h3>📅 তারিখ</h3><h2 style='color:#008080;'>{datetime.now().strftime('%d %b %Y')}</h2></div>", unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    
    # ড্যাশবোর্ডে কন্টাক্ট বক্স
    st.markdown(f"""
        <div class='contact-box'>
            <span style='color:#555;'>মাদরাসা সংক্রান্ত যেকোনো তথ্যের জন্য যোগাযোগ করুন: </span>
            <a href='tel:01954343364' class='contact-link'>📞 01954343364</a>
        </div>
    """, unsafe_allow_html=True)

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#008080;'>🔍 ছাত্রের প্রোফাইল চেক</h2>", unsafe_allow_html=True)
    sid = st.text_input("ছাত্রের আইডি (ID) দিন:")
    if sid:
        df_s = load_data("Student_List")
        if df_s is not None:
            student = df_s[df_s.iloc[:, 0].astype(str) == str(sid)]
            if not student.empty:
                s = student.iloc[0]
                name = s.get('Name')
                col1, col2 = st.columns([1, 2])
                with col1:
                    img_url = str(s.get('Photo_URL', 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'))
                    st.image(img_url, width=200)
                with col2:
                    st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border-left:5px solid #008080;'><h2>{name}</h2><p>পিতা: {s.get('Father_Name')}<br>মোবাইল: {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
                
                st.write("---")
                # উপস্থিতির স্ট্যাটাস চেক
                if df_a is not None and not df_a.empty:
                    today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)]
                    if any(today_data.iloc[:, 1].astype(str).str.contains(str(name))):
                        st.success(f"✅ {name} আজকে উপস্থিত আছে।")
                    else:
                        st.error(f"❌ {name} আজকে অনুপস্থিত।")
            else: st.error("এই আইডি-র কোনো ছাত্র পাওয়া যায়নি।")

# ৩. অ্যাডমিন
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন দিন:", type="password") == "MdmamuN18":
        opt = st.radio("কি করতে চান?", ["✅ হাজিরা নিন", "➕ নতুন ছাত্র ভর্তি"])
        if opt == "✅ হাজিরা নিন":
            st.markdown(f'<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform?embedded=true" width="100%" height="800"></iframe>', unsafe_allow_html=True)
        else:
            st.markdown(f'<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform?embedded=true" width="100%" height="900"></iframe>', unsafe_allow_html=True)
