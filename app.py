import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- Configuration ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- 🔥 Ultra Stylish Professional UI (CSS) ---
st.markdown("""
    <style>
    /* Background Animation */
    .stApp {
        background: linear-gradient(-45deg, #f1f4f9, #dff9fb, #eef2f3, #ffffff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Modern Header */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 50px; border-radius: 30px; color: white; text-align: center;
        margin-bottom: 35px; box-shadow: 0 15px 35px rgba(30, 60, 114, 0.3);
        border-bottom: 6px solid #f1c40f;
    }
    
    /* Stylish Buttons */
    .big-button {
        display: block; width: 100%; padding: 20px; margin: 15px 0px;
        text-align: center; color: white !important; font-size: 22px; font-weight: bold;
        text-decoration: none; border-radius: 15px; transition: 0.4s;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 2px solid rgba(255,255,255,0.2);
    }
    .call-btn { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%); }
    .fb-btn { background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); }
    .big-button:hover { transform: scale(1.02); box-shadow: 0 15px 25px rgba(0,0,0,0.2); }

    /* Info Cards */
    .stTable { background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    div[data-baseweb="input"] { border-radius: 12px !important; border: 2px solid #2a5298 !important; }
    
    .section-tag {
        background: #1e3c72; color: white; padding: 5px 15px; 
        border-radius: 20px; font-size: 14px; margin-bottom: 10px; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Fetching ---
@st.cache_data(ttl=1)
def load_all_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        r_df = pd.read_csv(get_url("Result")).astype(str)
        return s_df, r_df
    except: return None, None

df_s, df_r = load_all_data()

def upload_image(image_file):
    try:
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.getvalue()).decode('utf-8')}
        res = requests.post("https://api.imgbb.com/1/upload", payload)
        return res.json()['data']['url'] if res.status_code == 200 else "-"
    except: return "-"

# --- Navigation ---
menu = st.sidebar.radio("🧭 মেনু নেভিগেশন", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- 1. Home Dashboard ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 45px; margin-bottom: 10px;'>🕌 বাবুস সালাম একাডেমি</h1>
            <p style='font-size: 20px; opacity: 0.9;'>স্মার্ট ডিজিটাল ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-tag'>Emergency Contact</div>", unsafe_allow_html=True)
        st.markdown('<a href="tel:01954343364" class="big-button call-btn">📱 কল করুন: ০১৯৫৪-৩৪৩৩৬৪</a>', unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='section-tag'>Social Media</div>", unsafe_allow_html=True)
        st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 অফিশিয়াল ফেসবুক পেজ</a>', unsafe_allow_html=True)
    
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- 2. Profile Search ---
elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    is_admin = st.sidebar.text_input("অ্যাডমিন পিন দিন (সব তথ্যের জন্য):", type="password") == ADMIN_PIN
    sid = st.text_input("আইডি (ID) নম্বর দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            if is_admin:
                st.table(pd.DataFrame(s.items(), columns=["বিবরণ", "তথ্য"]))
                if 'Photo' in s and s['Photo'] != "-": st.image(s['Photo'], width=200)
            else:
                st.info(f"নাম: {s['Name']} | আইডি: {s['ID']}")
        else: st.error("দুঃখিত, আইডিটি খুঁজে পাওয়া যায়নি।")

# --- 3. Attendance ---
elif menu == "📊 দৈনিক হাজিরা":
    st.header("📊 আজকের হাজিরা (Attendance)")
    if df_s is not None:
        with st.form("att_form"):
            date = st.date_input("তারিখ", datetime.now())
            att_list = []
            for _, row in df_s.iterrows():
                status = st.selectbox(f"{row['Name']} ({row['ID']})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=row['ID'])
                att_list.append({"id": row['ID'], "name": row['Name'], "status": status})
            if st.form_submit_button("হাজিরা জমা দিন"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "date": str(date), "data": att_list})
                st.success("হাজিরা সফলভাবে শিটে সেভ হয়েছে।")

# --- 4. Result Sheet ---
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty:
            st.table(res.T)
            st.download_button("📥 ডাউনলোড রেজাল্ট", res.to_csv().encode('utf-8'), f"Result_{rid}.csv")
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# --- 5. Admin Panel ---
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.text_input("অ্যাডমিন সিকিউরিটি পিন:", type="password") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন:", ["নতুন ভর্তি (১১ তথ্য)", "রেজাল্ট এন্ট্রি (১০ বিষয়)"])
        
        if opt == "নতুন ভর্তি (১১ তথ্য)":
            with st.form("adm_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1=c1.text_input("আইডি*"); v2=c1.text_input("নাম*"); v3=c1.text_input("পিতার নাম"); v4=c1.text_input("মাতার নাম"); v5=c1.text_input("ঠিকানা")
                v6=c2.text_input("মোবাইল"); v7=c2.text_input("থানা"); v8=c2.text_input("জেলা"); v9=c2.text_input("জন্ম তারিখ"); v10=c2.text_input("জন্ম সনদ"); v11=st.file_uploader("ছবি")
                if st.form_submit_button("ভর্তি সম্পন্ন করুন"):
                    img = upload_image(v11) if v11 else "-"
                    requests.post(SCRIPT_URL, json={"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img})
                    st.success("ভর্তি সফল!")

        elif opt == "রেজাল্ট এন্ট্রি (১০ বিষয়)":
            with st.form("res_form", clear_on_submit=True):
                c_top1, c_top2, c_top3 = st.columns(3)
                r_id = c_top1.text_input("আইডি*"); r_name = c_top2.text_input("নাম*"); r_exam = c_top3.text_input("পরীক্ষা*")
                c1, c2, c3 = st.columns(3)
                r1=c1.number_input("আরবি", 0, 100); r2=c2.number_input("বাংলা", 0, 100); r3=c3.number_input("ইংরেজি", 0, 100)
                r4=c1.number_input("গণিত", 0, 100); r5=c2.number_input("হাদিস", 0, 100); r6=c3.number_input("কালিমা", 0, 100)
                r7=c1.number_input("কুরআন", 0, 100); r8=c2.number_input("সমাজ", 0, 100); r9=c3.number_input("বিজ্ঞান", 0, 100)
                r10=c1.number_input("সাধারণ জ্ঞান", 0, 100)
                if st.form_submit_button("রেজাল্ট সেভ করুন"):
                    total = r1+r2+r3+r4+r5+r6+r7+r8+r9+r10
                    avg = total / 10
                    grade = "মুমতাজ (A+)" if avg >= 80 else "জায়্যিদ (A)" if avg >= 60 else "মকবুল (C)" if avg >= 33 else "রাসেব (F)"
                    payload = {"action": "add_result", "id": r_id, "name": r_name, "exam": r_exam, "arb": r1, "ban": r2, "eng": r3, "mat": r4, "had": r5, "kal": r6, "qur": r7, "som": r8, "big": r9, "sgen": r10, "total": total, "grade": grade}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success(f"সেভ হয়েছে! মোট: {total}, গ্রেড: {grade}")
