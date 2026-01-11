import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার লেটেস্ট দেওয়া URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyaOoNMXgz2bbQEDPDiMBpmgOEjFeIJEkuNU_zCdHCuq2GRsG_cp5L-P_wTPufmsvP2/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ডিজাইন (কালারফুল ও সুন্দর) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f2f1 0%, #f1f8e9 50%, #fff3e0 100%); }
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 100%);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    .notice-box {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        font-size: 24px; font-weight: bold; margin-bottom: 25px;
        border: 4px solid #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input { border: 2px solid #008080 !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড
@st.cache_data(ttl=1)
def load_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        a_df = pd.read_csv(get_url("Form_Responses_1")).astype(str)
        try:
            n_df = pd.read_csv(get_url("Notice"))
            notice = n_df.columns[0] if not n_df.empty else "কোনো নোটিশ নেই"
        except: notice = "কোনো নোটিশ নেই"
        try: r_df = pd.read_csv(get_url("Result")).astype(str)
        except: r_df = None
        return s_df, a_df, notice, r_df
    except: return None, None, "লোডিং...", None

df_s, df_a, latest_notice, df_r = load_data()
today = datetime.now().strftime("%-m/%-d/%Y")

# ইমেজ আপলোড
def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "📊 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    
    # উপস্থিতি চেক
    present_list = []
    if df_a is not None and not df_a.empty:
        today_data = df_a[df_a.iloc[:, 0].str.contains(today, na=False)]
        for entries in today_data.iloc[:, 1]:
            present_list.extend([n.strip() for n in str(entries).split(',') if n.strip()])
    present_list = sorted(list(set(present_list)))

    c1, c2 = st.columns([2, 1])
    with c1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    with c2:
        st.subheader(f"✅ আজকের উপস্থিতি ({len(present_list)})")
        for p in present_list: st.write(f"🟢 {p}")

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.header("🔍 স্টুডেন্ট প্রোফাইল")
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0] == sid]
        if not student.empty:
            s = student.iloc[0]
            st.write(f"### নাম: {s['Name']}")
            st.image(s.get('Photo_URL', 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'), width=150)
        else: st.error("পাওয়া যায়নি!")

# ৩. রেজাল্ট শিট
elif menu == "📊 রেজাল্ট শিট":
    st.header("📊 পরীক্ষার ফলাফল")
    rid = st.text_input("আইডি নম্বর দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0] == rid]
        if not res.empty: st.table(res.T)
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# ৪. অ্যাডমিন অ্যাক্সেস (ভর্তি ফরম ফিক্সড)
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন:", type="password") == "MdmamuN18":
        adm_opt = st.selectbox("কাজ বেছে নিন", ["নতুন ভর্তি", "হাজিরা নিন", "নোটিশ"])
        
        if adm_opt == "নতুন ভর্তি":
            with st.form("full_admission", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1 = c1.text_input("আইডি (ID)*"); v2 = c1.text_input("ছাত্রের নাম*")
                v3 = c1.text_input("পিতার নাম"); v4 = c1.text_input("মাতার নাম")
                v5 = c1.text_input("জন্ম তারিখ (DD/MM/YYYY)")
                v6 = c2.text_input("মোবাইল নম্বর"); v7 = c2.text_input("ঠিকানা")
                v8 = c2.text_input("থানা"); v9 = c2.text_input("জেলা")
                v10 = c2.text_input("জন্ম সনদ নম্বর")
                v11 = st.file_uploader("ছবি")
                
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    pic = upload_image(v11) if v11 else "-"
                    # ১১টি কলামের ডাটা অ্যাপস স্ক্রিপ্টে পাঠানো হচ্ছে
                    payload = {
                        "action": "admission", "id": v1, "name": v2, "father": v3,
                        "mother": v4, "mobile": v6, "address": v7, "thana": v8,
                        "zella": v9, "dob": v5, "birth_cert": v10, "photo": pic
                    }
                    r = requests.post(SCRIPT_URL, json=payload)
                    if r.status_code == 200: st.success("সফলভাবে ভর্তি করা হয়েছে!")
                    else: st.error("সার্ভার সমস্যা!")

        elif adm_opt == "হাজিরা নিন":
            if df_s is not None:
                selected = st.multiselect("ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা সেভ"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected)})
                    st.success("হাজিরা নেওয়া হয়েছে!")
