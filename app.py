import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx:out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম রঙিন UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f6; }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 35px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .big-button {
        display: block; width: 100%; padding: 15px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 18px; font-weight: bold;
        text-decoration: none; border-radius: 12px; transition: 0.3s;
    }
    .call-btn { background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%); }
    .fb-btn { background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); }
    .big-button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    div[data-baseweb="input"] { border: 2px solid #1e3c72 !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. ডাটা লোড ---
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

# --- ৪. মেনু নেভিগেশন ---
menu = st.sidebar.radio("🧭 মেনু", ["🏠 হোম", "🔍 প্রোফাইল", "📊 হাজিরা", "📝 রেজাল্ট", "🔐 অ্যাডমিন"])

# --- হোম পেজ ---
if menu == "🏠 হোম":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>একটি আধুনিক ও স্মার্ট মাদরাসা ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 কল করুন</a>', unsafe_allow_html=True)
    c2.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- প্রোফাইল সার্চ (রিসার্চড ডিমান্ড অনুযায়ী) ---
elif menu == "🔍 প্রোফাইল":
    st.header("🔍 শিক্ষার্থীর তথ্য")
    is_admin_p = st.sidebar.text_input("অ্যাডমিন পিন দিন:", type="password") == ADMIN_PIN
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            if is_admin_p:
                st.success("✅ অ্যাডমিন ভিউ (সব তথ্য)")
                st.table(pd.DataFrame(s.items(), columns=["বিবরণ", "তথ্য"]))
                if len(s) > 10 and s.iloc[10] != "-": st.image(s.iloc[10], width=200)
            else:
                st.info("ℹ️ সাধারণ ভিউ")
                st.subheader(f"নাম: {s.iloc[1]}") 
                st.write(f"আইডি: {s.iloc[0]}")
        else: st.error("আইডি পাওয়া যায়নি।")

# --- হাজিরা ---
elif menu == "📊 হাজিরা":
    st.header("📊 দৈনিক হাজিরা")
    if df_s is not None:
        with st.form("att_form"):
            h_date = st.date_input("তারিখ", datetime.now())
            att_data = []
            for i, row in df_s.iterrows():
                sid, sname = row.iloc[0], row.iloc[1]
                status = st.selectbox(f"{sname} ({sid})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=f"a_{sid}")
                att_data.append({"id": sid, "name": sname, "status": status})
            if st.form_submit_button("হাজিরা জমা দিন"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "date": str(h_date), "data": att_data})
                st.success("হাজিরা সেভ হয়েছে!")

# --- রেজাল্ট শিট ---
elif menu == "📝 রেজাল্ট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty: st.table(res.iloc[0])
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# --- অ্যাডমিন প্যানেল (ভর্তি ও রেজাল্ট) ---
elif menu == "🔐 অ্যাডমিন":
    if st.sidebar.text_input("অ্যাডমিন সিকিউরিটি পিন:", type="password") == ADMIN_PIN:
        opt = st.selectbox("কাজ:", ["ভর্তি (১১ তথ্য)", "রেজাল্ট (১০ বিষয়)"])
        if opt == "ভর্তি (১১ তথ্য)":
            with st.form("adm_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ID*"); v2=c1.text_input("Name*"); v3=c1.text_input("Father"); v4=c1.text_input("Mother"); v5=c1.text_input("Address")
                v6=c2.text_input("Mobile"); v7=c2.text_input("Thana"); v8=c2.text_input("District"); v9=c2.text_input("DOB"); v10=c2.text_input("Birth Reg"); v11=st.file_uploader("Photo")
                if st.form_submit_button("ভর্তি সম্পন্ন করুন"):
                    img = upload_image(v11) if v11 else "-"
                    requests.post(SCRIPT_URL, json={"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img})
                    st.success("ভর্তি সফল!")

        elif opt == "রেজাল্ট (১০ বিষয়)":
            with st.form("res_form", clear_on_submit=True):
                c_top1, c_top2, c_top3 = st.columns(3)
                r_id=c_top1.text_input("ID*"); r_name=c_top2.text_input("Name*"); r_exam=c_top3.text_input("Exam*")
                c1, c2, c3 = st.columns(3)
                r1=c1.number_input("আরবি", 0, 100); r2=c2.number_input("বাংলা", 0, 100); r3=c3.number_input("ইংরেজি", 0, 100)
                r4=c1.number_input("গণিত", 0, 100); r5=c2.number_input("হাদিস", 0, 100); r6=c3.number_input("কালিমা", 0, 100)
                r7=c1.number_input("কুরআন", 0, 100); r8=c2.number_input("সমাজ", 0, 100); r9=c3.number_input("বিজ্ঞান", 0, 100)
                r10=c1.number_input("সাধারণ জ্ঞান", 0, 100) # কলামে ঠিক করা হয়েছে
                if st.form_submit_button("সেভ করুন"):
                    total = r1+r2+r3+r4+r5+r6+r7+r8+r9+r10
                    avg = total / 10
                    grade = "A+" if avg >= 80 else "A" if avg >= 60 else "C" if avg >= 33 else "F"
                    payload = {"action": "add_result", "id": r_id, "name": r_name, "exam": r_exam, "arb": r1, "ban": r2, "eng": r3, "mat": r4, "had": r5, "kal": r6, "qur": r7, "som": r8, "big": r9, "sgen": r10, "total": total, "grade": grade}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success(f"সেভ হয়েছে! মোট: {total}")
