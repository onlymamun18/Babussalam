import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz5TpykMcD6f5ZLIBp26HuxOQ-uGOLdHOL0NJzQLq3ag_MzbtosgkLlXqJ6iK16MuKF/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #006699 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-bottom: 5px solid #f1c40f;
    }
    .big-button {
        display: block; width: 100%; padding: 18px; margin: 10px 0;
        text-align: center; color: white !important; font-size: 18px; font-weight: bold;
        text-decoration: none; border-radius: 15px;
    }
    .call-btn { background: #27ae60; }
    .fb-btn { background: #2980b9; }
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
    except:
        return None, None, None

df_s, df_r, df_a = load_all_data()

def upload_image(file):
    try:
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.getvalue()).decode('utf-8')}
        return requests.post("https://api.imgbb.com/1/upload", payload).json()['data']['url']
    except:
        return "-"

# --- ৪. মেনু নেভিগেশন ---
menu = st.sidebar.radio("🧭 প্রধান মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- হোম পেজ ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>ডিজিটাল ক্যাম্পাস ড্যাশবোর্ড</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 কল করুন</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- প্রোফাইল সার্চ ---
elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 প্রোফাইল ও হাজিরা")
    sid = st.text_input("শিক্ষার্থীর আইডি দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"👤 নাম: {s[1]}")
            
            # হাজিরা স্ট্যাটাস চেক
            if df_a is not None:
                t1, t2 = datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%d/%m/%Y')
                match = df_a[(df_a.iloc[:, 1].str.strip() == sid) & (df_a.iloc[:, 0].str.contains(t1) | df_a.iloc[:, 0].str.contains(t2))]
                if not match.empty: st.success(f"✅ আজকের হাজিরা: **{match.iloc[-1, 3]}**")
                else: st.warning("📅 আজ এখনো হাজিরা দেওয়া হয়নি।")
            
            # বিস্তারিত তথ্য (পিন দিয়ে)
            if st.sidebar.text_input("অ্যাডমিন পিন:", type="password") == ADMIN_PIN:
                st.table(pd.DataFrame({
                    "বিবরণ": ["আইডি", "পিতা", "মাতা", "ঠিকানা", "মোবাইল", "থানা", "জেলা", "জন্ম তারিখ", "জন্ম নিবন্ধন"],
                    "তথ্য": [s[0], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9]]
                }))
                if len(s) > 10 and "http" in s[10]: st.image(s[10], width=150, caption="ছাত্রের ছবি")
        else: st.error("দুঃখিত, আইডি পাওয়া যায়নি।")

# --- দৈনিক হাজিরা ---
elif menu == "📊 দৈনিক হাজিরা":
    if st.sidebar.text_input("পিন দিন:", type="password", key="att_p") == ADMIN_PIN:
        st.header("📊 প্রতিদিনের হাজিরা ইনপুট")
        if df_s is not None:
            with st.form("att_f"):
                att_data = []
                for _, row in df_s.iterrows():
                    status = st.selectbox(f"{row[1]} ({row[0]})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=row[0])
                    att_data.append({"id": row[0], "name": row[1], "status": status})
                if st.form_submit_button("✅ হাজিরা সেভ করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "data": att_data})
                    st.success("হাজিরা সফলভাবে শিটে সেভ হয়েছে!")
    else: st.info("অ্যাডমিন পিন দিন।")

# --- রেজাল্ট ---
elif menu == "📝 রেজাল্ট শিট":
    rid = st.text_input("রেজাল্ট দেখতে আইডি:")
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty: st.table(res.iloc[0])
        else: st.error("রেজাল্ট পাওয়া যায়নি।")

# --- অ্যাডমিন প্যানেল ---
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.sidebar.text_input("পিন:", type="password", key="adm_p") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন", ["নতুন ভর্তি (১১টি তথ্য)", "ছাত্র তালিকা", "ডাটা ডিলিট"])
        
        if opt == "নতুন ভর্তি (১১টি তথ্য)":
            with st.form("admission"):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ID*"); v2=c1.text_input("Student Name*"); v3=c1.text_input("Father's Name"); v4=c1.text_input("Mother's Name"); v5=c1.text_area("Full Address")
                v6=c2.text_input("Mobile No*"); v7=c2.text_input("Thana"); v8=c2.text_input("District"); v9=c2.text_input("Date of Birth"); v10=c2.text_input("Birth Cert No")
                v11=st.file_uploader("Student Photo")
                
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    photo = upload_image(v11) if v11 else "-"
                    payload = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": photo}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("ভর্তি সফলভাবে সম্পন্ন হয়েছে!")

        elif opt == "ছাত্র তালিকা": st.dataframe(df_s)
        elif opt == "ডাটা ডিলিট":
            did = st.text_input("ডিলিট আইডি:")
            if st.button("স্থায়ীভাবে ডিলিট"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": did})
                st.warning("ডাটা ডিলিট হয়েছে।")
    else: st.error("সঠিক পিন দিন।")
