import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন (আপনার দেওয়া নতুন লিঙ্ক আপডেট করা হয়েছে) ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx619SCj4M_dMA9o2-kzTd-YLtGq6YfMfw1PE-QISinUsDRYqROEGLtzWoE4l2dV5o/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background: #f1f4f9; }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px; border-radius: 25px; color: white; text-align: center;
        margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .big-button {
        display: block; width: 100%; padding: 18px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 18px; font-weight: bold;
        text-decoration: none; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .call-btn { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%); }
    .fb-btn { background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); }
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
    except: return None, None, None

df_s, df_r, df_a = load_all_data()

def upload_image(image_file):
    try:
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.getvalue()).decode('utf-8')}
        res = requests.post("https://api.imgbb.com/1/upload", payload)
        return res.json()['data']['url'] if res.status_code == 200 else "-"
    except: return "-"

# --- ৪. মেনু নেভিগেশন ---
menu = st.sidebar.radio("🧭 মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- ১. হোম পেজ ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস ড্যাশবোর্ড</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="tel:01954343364" class="big-button call-btn">📱 কল করুন</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- ২. প্রোফাইল সার্চ (হাজিরা সহ) ---
elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 তথ্য ও আজকের হাজিরা")
    pin_check = st.sidebar.text_input("অ্যাডমিন পিন (Full Profile):", type="password", key="sec_p")
    sid = st.text_input("আইডি (ID) দিন:").strip()
    
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"👤 নাম: {s[1]}")
            
            # হাজিরা চেক
            if df_a is not None:
                today_d = datetime.now().strftime('%Y-%m-%d')
                today_alt = datetime.now().strftime('%d/%m/%Y')
                # টাইমস্ট্যাম্প থেকে তারিখ এবং আইডি মিলিয়ে দেখা হচ্ছে
                match = df_a[(df_a.iloc[:, 1].str.strip() == sid) & 
                             (df_a.iloc[:, 0].str.contains(today_d) | df_a.iloc[:, 0].str.contains(today_alt))]
                if not match.empty:
                    st.success(f"📅 আজকের হাজিরা: **{match.iloc[-1, 3]}**")
                else:
                    st.error("📅 আজ এখনো হাজিরা দেওয়া হয়নি।")

            if pin_check == ADMIN_PIN:
                details = {"বিবরণ": ["আইডি", "পিতা", "ঠিকানা", "মোবাইল"], "তথ্য": [s[0], s[2], s[4], s[5]]}
                st.table(pd.DataFrame(details))
                if len(s) > 10 and "http" in str(s[10]): st.image(s[10], width=150)
            else:
                st.info(f"🆔 আইডি: {s[0]} (বিস্তারিত তথ্যের জন্য পিন দিন)")
        else: st.error("আইডি পাওয়া যায়নি।")

# --- ৩. দৈনিক হাজিরা ইনপুট ---
elif menu == "📊 দৈনিক হাজিরা":
    if st.sidebar.text_input("পিন দিন:", type="password", key="att_p") == ADMIN_PIN:
        st.header("📊 প্রতিদিনের হাজিরা ইনপুট")
        if df_s is not None:
            with st.form("att_f"):
                att_list = []
                for _, row in df_s.iterrows():
                    status = st.selectbox(f"{row[1]} ({row[0]})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=row[0])
                    att_list.append({"id": row[0], "name": row[1], "status": status})
                if st.form_submit_button("✅ হাজিরা সেভ করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "data": att_list})
                    st.success("হাজিরা সফলভাবে শিটে সেভ হয়েছে!")
    else: st.warning("অ্যাডমিন পিন দিন।")

# --- ৪. রেজাল্ট শিট ---
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি দিন:")
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty: st.table(res.iloc[0])
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# --- ৫. অ্যাডমিন প্যানেল ---
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.sidebar.text_input("পিন:", type="password", key="adm_p") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন", ["নতুন ভর্তি", "ছাত্র তালিকা", "ডিলিট"])
        if opt == "নতুন ভর্তি":
            with st.form("vorti"):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ID"); v2=c1.text_input("Name"); v3=c1.text_input("Father"); v4=c1.text_input("Mother"); v5=c1.text_input("Address")
                v6=c2.text_input("Mobile"); v7=c2.text_input("Thana"); v8=c2.text_input("Zella"); v9=c2.text_input("DOB"); v10=c2.text_input("Birth Cert"); v11=st.file_uploader("Photo")
                if st.form_submit_button("ভর্তি সম্পন্ন"):
                    img = upload_image(v11) if v11 else "-"
                    payload = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("ভর্তি সফল!")
        elif opt == "ছাত্র তালিকা": st.dataframe(df_s)
        elif opt == "ডিলিট":
            did = st.text_input("ডিলিট করার আইডি:")
            if st.button("ডিলিট করুন"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": did})
                st.success("ডিলিট সম্পন্ন!")
    else: st.error("পিন দিন।")
