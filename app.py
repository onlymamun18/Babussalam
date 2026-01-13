import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxbixVRGl2lMJnz8GHt-ZKkn_3riRU0ihcNgv65Fs8ZuWuyI0AkCs8797wK-L26k0hM/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম UI ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background: #f1f4f9; }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px; border-radius: 25px; color: white; text-align: center;
        margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border-bottom: 6px solid #f1c40f;
    }
    .big-button {
        display: block; width: 100%; padding: 18px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 20px; font-weight: bold;
        text-decoration: none; border-radius: 15px; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .call-btn { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%); }
    .fb-btn { background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); }
    div[data-baseweb="input"] { border: 2px solid #1e3c72 !important; border-radius: 10px !important; }
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

# --- ৪. নেভিগেশন মেনু (সবগুলো মেনু ফেরত আনা হয়েছে) ---
menu = st.sidebar.radio("🧭 মেনু নেভিগেশন", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- হোম পেজ ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="tel:01954343364" class="big-button call-btn">📱 সরাসরি কল করুন</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- প্রোফাইল সার্চ (হাজিরা স্ট্যাটাস সহ) ---
elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 শিক্ষার্থীর তথ্য ও আজকের হাজিরা")
    check_pin = st.sidebar.text_input("অ্যাডমিন পিন (ব্যক্তিগত তথ্যের জন্য):", type="password")
    is_admin = (check_pin == ADMIN_PIN)
    
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"👤 নাম: {s[1]}")
            
            # আজকের হাজিরা চেক
            today_str = datetime.now().strftime('%Y-%m-%d')
            if df_a is not None:
                today_att = df_a[(df_a.iloc[:, 1].str.strip() == sid) & (df_a.iloc[:, 0].str.contains(today_str))]
                if not today_att.empty:
                    status = today_att.iloc[-1, 3]
                    st.info(f"📅 আজকের হাজিরার অবস্থা: **{status}**")
                else:
                    st.warning("📅 আজ এখনো হাজিরা দেওয়া হয়নি।")

            if is_admin:
                details = {"বিবরণ": ["আইডি", "পিতা", "মাতা", "ঠিকানা", "মোবাইল", "থানা", "জেলা", "জন্ম তারিখ"],
                           "তথ্য": [s[0], s[2], s[3], s[4], s[5], s[6], s[7], s[8]]}
                st.table(pd.DataFrame(details))
                if len(s) > 10 and str(s[10]).startswith("http"): st.image(s[10], width=150)
            else:
                st.write(f"🆔 আইডি নম্বর: {s[0]}")
                st.info("ℹ️ পূর্ণাঙ্গ প্রোফাইল দেখতে অ্যাডমিন পিন দিন।")
        else: st.error("আইডি পাওয়া যায়নি।")

# --- দৈনিক হাজিরা ---
elif menu == "📊 দৈনিক হাজিরা":
    st.header("📊 প্রতিদিনের হাজিরা ইনপুট")
    if st.sidebar.text_input("পিন দিন:", type="password", key="att_p") == ADMIN_PIN:
        if df_s is not None:
            with st.form("att_f"):
                h_date = st.date_input("তারিখ", datetime.now())
                att_list = []
                for _, row in df_s.iterrows():
                    status = st.selectbox(f"{row[1]} ({row[0]})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=row[0])
                    att_list.append({"date": str(h_date), "id": row[0], "name": row[1], "status": status})
                if st.form_submit_button("✅ সেভ করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "data": att_list})
                    st.success("হাজিরা সেভ হয়েছে!")
    else: st.warning("অ্যাডমিন পিন প্রয়োজন।")

# --- রেজাল্ট শিট ---
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty:
            st.success(f"ফলাফল পাওয়া গেছে: {res.iloc[0, 1]}")
            st.table(res.iloc[0])
        else: st.warning("রেজাল্ট এখনো আপলোড হয়নি।")

# --- অ্যাডমিন প্যানেল ---
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.sidebar.text_input("পিন:", type="password", key="adm_p") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন", ["নতুন ভর্তি", "ছাত্র তালিকা", "ডিলিট"])
        if opt == "নতুন ভর্তি":
            with st.form("adm"):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ID*"); v2=c1.text_input("Name*"); v3=c1.text_input("Father"); v4=c1.text_input("Mother"); v5=c1.text_input("Address")
                v6=c2.text_input("Mobile"); v7=c2.text_input("Thana"); v8=c2.text_input("Zella"); v9=c2.text_input("DOB"); v10=c2.text_input("Birth Cert"); v11=st.file_uploader("Photo")
                if st.form_submit_button("ভর্তি সম্পন্ন"):
                    img = upload_image(v11) if v11 else "-"
                    payload = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("ভর্তি সফল!")
        elif opt == "ছাত্র তালিকা": st.dataframe(df_s)
        elif opt == "ডিলিট":
            did = st.text_input("ডিলিট আইডি:")
            if st.button("ডিলিট"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": did})
                st.success("ডিলিট সম্পন্ন!")
    else: st.warning("পিন দিয়ে লগইন করুন।")
