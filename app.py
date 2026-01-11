import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzufVqWM8fj-sF3cpLsQG-9tBV3E_DxXtNqc7svsHrdFIChBv2fvOpJkPThm-G3Kf73/exec"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- সেই অস্থির UI ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f6; }
    .main-header {
        background: linear-gradient(135deg, #008080 0%, #004d4d 100%);
        padding: 45px; border-radius: 25px; color: white; text-align: center;
        box-shadow: 0 15px 30px rgba(0,128,128,0.2); margin-bottom: 35px;
        border-bottom: 8px solid #00b3b3;
    }
    .stat-card {
        background: white; padding: 25px; border-radius: 18px;
        text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        border-top: 5px solid #008080;
    }
    .contact-box {
        background: #ffffff; padding: 15px; border-radius: 12px;
        border-left: 5px solid #ff4b4b; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-top: 20px; text-align: center;
    }
    .sidebar-contact {
        background: #e6f2f2; padding: 15px; border-radius: 10px;
        border: 1px dashed #008080; text-align: center; margin-top: 50px;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #008080 !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return df
    except: return None

# ডাটা লোড
df_s = load_data("Student_List")
df_a = load_data("Form_Responses_1")
today_date = datetime.now().strftime("%-m/%-d/%Y")

# --- সাইডবার ---
with st.sidebar:
    st.markdown("<h1 style='color:#008080; text-align:center;'>🏫 বাবুস সালাম</h1>", unsafe_allow_html=True)
    menu = st.radio("মেনু নির্বাচন করুন", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])
    st.markdown(f"<div class='sidebar-contact'><p style='margin:0; font-size:12px;'>যেকোনো প্রয়োজনে</p><p style='margin:0; font-weight:bold; color:#008080;'>📞 01954343364</p></div>", unsafe_allow_html=True)

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম ইসলামি একাডেমি</h1><p>ডিজিটাল ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p></div>", unsafe_allow_html=True)
    
    total_students = len(df_s) if df_s is not None else 0
    today_present = 0
    if df_a is not None and not df_a.empty:
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)]
        if not today_rows.empty:
            all_names = today_rows.iloc[:, 1].astype(str).str.cat(sep=',')
            today_present = len(set([n.strip() for n in all_names.split(',') if n.strip() != ""]))

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stat-card'><h3>👨‍🎓 মোট ছাত্র</h3><h2 style='color:#008080;'>{total_students} জন</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'><h3>✅ আজকে উপস্থিত</h3><h2 style='color:#28a745;'>{today_present} জন</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><h3>📅 তারিখ</h3><h2 style='color:#008080;'>{datetime.now().strftime('%d %b %Y')}</h2></div>", unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    st.markdown(f"<div class='contact-box'><span>মাদরাসা তথ্যের জন্য: </span><a href='tel:01954343364' style='color:#ff4b4b; font-weight:bold; text-decoration:none;'>📞 01954343364</a></div>", unsafe_allow_html=True)

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#008080;'>🔍 ছাত্রের প্রোফাইল চেক</h2>", unsafe_allow_html=True)
    sid = st.text_input("ছাত্রের আইডি (ID) দিন:")
    if sid:
        if df_s is not None:
            student = df_s[df_s.iloc[:, 0].astype(str).str.strip() == str(sid).strip()]
            if not student.empty:
                s = student.iloc[0]
                name = s.get('Name')
                col1, col2 = st.columns([1, 2])
                with col1:
                    img_url = s.get('Photo_URL')
                    if isinstance(img_url, str) and img_url.startswith("http"):
                        st.image(img_url, width=200)
                    else:
                        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
                with col2:
                    st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border-left:5px solid #008080;'><h2>{name}</h2><p>পিতা: {s.get('Father_Name')}<br>মোবাইল: {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
                
                st.write("---")
                if df_a is not None:
                    today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)]
                    if any(today_data.iloc[:, 1].astype(str).str.contains(str(name))):
                        st.success(f"✅ {name} আজকে উপস্থিত আছে।")
                    else:
                        st.error(f"❌ {name} আজকে অনুপস্থিত।")
            else: st.error("এই আইডি-র কোনো ছাত্র পাওয়া যায়নি।")

# ৩. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন দিন:", type="password") == "MdmamuN18":
        st.markdown("<h2 style='color:#008080;'>✅ সরাসরি হাজিরা প্যানেল</h2>", unsafe_allow_html=True)
        
        if df_s is not None:
            all_students = df_s['Name'].tolist()
            selected_students = st.multiselect("আজকে যারা এসেছে তাদের নাম সিলেক্ট করুন:", all_students)
            
            if st.button("হাজিরা সেভ করুন"):
                if selected_students:
                    names_to_send = ", ".join(selected_students)
                    try:
                        resp = requests.post(SCRIPT_URL, json={"names": names_to_send})
                        if "Success" in resp.text:
                            st.success(f"সাফল্যের সাথে {len(selected_students)} জনের হাজিরা নেওয়া হয়েছে!")
                            st.balloons()
                        else:
                            st.error("ডাটা পাঠাতে সমস্যা হয়েছে।")
                    except:
                        st.error("সার্ভার কানেকশন এরর!")
                else:
                    st.warning("আগে ছাত্র সিলেক্ট করুন।")
