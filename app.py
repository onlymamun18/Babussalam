import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbytL1A_55j5kYQOrgmktBy5Pmgidmo8lImlCvZjyTpPZG54nxLbTsLczZ0bLpc1huLY/exec"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- সুপার কালারফুল UI (CSS) ---
st.markdown("""
    <style>
    /* পুরো পেজের ব্যাকগ্রাউন্ড কালারফুল গ্রেডিয়েন্ট */
    .stApp {
        background: linear-gradient(135deg, #e0f2f1 0%, #f1f8e9 50%, #fff3e0 100%);
    }
    
    /* সাইডবার কালারফুল করা */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004d4d 0%, #008080 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* মেইন হেডার - চোখ ধাঁধানো ডার্ক গ্রেডিয়েন্ট */
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 50%, #1de9b6 100%);
        padding: 50px;
        border-radius: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,128,128,0.4);
        margin-bottom: 40px;
        border: 3px solid rgba(255,255,255,0.3);
    }
    
    /* কালারফুল স্ট্যাটাস কার্ড */
    .card-students { background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%); border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .card-present { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .card-ratio { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }

    /* ফর্ম এবং কন্টেইনার কালার */
    .stForm, .stTabs {
        background: rgba(255, 255, 255, 0.9);
        padding: 30px;
        border-radius: 25px;
        border: 2px solid #008080;
    }
    
    /* বাটন স্টাইল */
    .stButton>button {
        background: linear-gradient(135deg, #008080 0%, #004d4d 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        height: 50px;
        font-size: 20px !important;
        box-shadow: 0 5px 15px rgba(0,64,64,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=1)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return df
    except: return None

df_s = load_data("Student_List")
df_a = load_data("Form_Responses_1")
today_date = datetime.now().strftime("%-m/%-d/%Y")

# --- সাইডবার ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🏢 অ্যাডমিন মেনু</h1>", unsafe_allow_html=True)
    menu = st.radio("পেজ পরিবর্তন করুন", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])
    st.markdown("<br><br><div style='text-align:center; border-top:1px solid white; padding-top:10px;'>📞 01954343364</div>", unsafe_allow_html=True)

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown(f"""
        <div class='main-header'>
            <h1 style='font-size: 55px; margin:0;'>🕌 বাবুস সালাম একাডেমি</h1>
            <p style='font-size: 22px;'>স্মার্ট ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p>
            <div style='font-size:18px; margin-top:10px;'>📅 {datetime.now().strftime('%A, %d %B %Y')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    total_students = len(df_s) if df_s is not None else 0
    today_present = 0
    if df_a is not None and not df_a.empty:
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)]
        if not today_rows.empty:
            all_names = today_rows.iloc[:, 1].astype(str).str.cat(sep=',')
            today_present = len(set([n.strip() for n in all_names.split(',') if n.strip() != ""]))

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='card-students'><h3>👨‍🎓 মোট শিক্ষার্থী</h3><h1>{total_students}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card-present'><h3>✅ আজকের উপস্থিতি</h3><h1>{today_present}</h1></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card-ratio'><h3>📊 উপস্থিতি হার</h3><h1>{round((today_present/total_students*100),1) if total_students > 0 else 0}%</h1></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#004d4d; background:white; padding:10px; border-radius:10px; text-align:center;'>🔍 শিক্ষার্থীর প্রোফাইল অনুসন্ধান</h2>", unsafe_allow_html=True)
    sid = st.text_input("আইডি (ID) নম্বর দিন:")
    if sid:
        if df_s is not None:
            student = df_s[df_s.iloc[:, 0].astype(str).str.strip() == str(sid).strip()]
            if not student.empty:
                s = student.iloc[0]
                name = s.get('Name')
                col1, col2 = st.columns([1, 2])
                with col1:
                    img_url = s.get('Photo_URL')
                    st.image(img_url if isinstance(img_url, str) and img_url.startswith("http") else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", use_container_width=True)
                with col2:
                    st.markdown(f"<div style='background:white; padding:30px; border-radius:20px; border-left:10px solid #008080;'><h1>{name}</h1><h3>পিতা: {s.get('Father_Name')}</h3><h3>মোবাইল: {s.get('Mobile')}</h3></div>", unsafe_allow_html=True)
                
                if df_a is not None:
                    today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date)]
                    if any(today_data.iloc[:, 1].astype(str).str.contains(str(name))):
                        st.success(f"🌟 {name} আজকে উপস্থিত আছে।")
                    else:
                        st.error(f"⚠️ {name} আজকে অনুপস্থিত।")
            else: st.error("এই আইডি দিয়ে কাউকে পাওয়া যায়নি।")

# ৩. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন দিন:", type="password") == "MdmamuN18":
        tab1, tab2 = st.tabs(["✅ হাজিরা নিন", "➕ নতুন ছাত্র ভর্তি"])
        
        with tab1:
            st.markdown("### 📋 আজকের হাজিরা তালিকা")
            if df_s is not None:
                all_students = df_s['Name'].tolist()
                selected = st.multiselect("উপস্থিত শিক্ষার্থীদের নাম সিলেক্ট করুন:", all_students)
                if st.button("হাজিরা সেভ করুন"):
                    if selected:
                        requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected)})
                        st.success(f"{len(selected)} জনের হাজিরা নেওয়া হয়েছে!")
                        st.balloons()
        
        with tab2:
            st.markdown("### ➕ নতুন ছাত্র ভর্তি ফরম")
            with st.form("admission_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    n_id = st.text_input("আইডি:")
                    n_name = st.text_input("নাম:")
                with c2:
                    n_father = st.text_input("পিতার নাম:")
                    n_mobile = st.text_input("মোবাইল:")
                n_photo = st.text_input("ছবির লিঙ্ক:")
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    if n_id and n_name:
                        requests.post(SCRIPT_URL, json={"action": "admission", "id": n_id, "name": n_name, "father": n_father, "mobile": n_mobile, "photo": n_photo})
                        st.success(f"{n_name} এর ভর্তি সম্পন্ন হয়েছে।")
