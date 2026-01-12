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
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #f8fafc; }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .big-button {
        display: block; width: 100%; padding: 15px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 18px; font-weight: bold;
        text-decoration: none; border-radius: 12px; transition: 0.3s;
    }
    .call-btn { background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%); }
    .fb-btn { background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); }
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

# --- ৪. মেইন মেনু ---
menu = st.sidebar.radio("🧭 মেনু নেভিগেশন", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- হোম ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ম্যানেজমেন্ট সিস্টেম</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 কল করুন</a>', unsafe_allow_html=True)
    c2.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- প্রোফাইল সার্চ ---
elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    is_admin = st.sidebar.text_input("অ্যাডমিন পিন:", type="password") == ADMIN_PIN
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            if is_admin:
                st.table(pd.DataFrame(s.items(), columns=["বিবরণ", "তথ্য"]))
                if len(s) > 10 and s.iloc[10] != "-": st.image(s.iloc[10], width=200)
            else:
                st.info(f"নাম: {s.iloc[1]} | আইডি: {s.iloc[0]}")
        else: st.error("আইডি পাওয়া যায়নি।")

# --- হাজিরা ---
elif menu == "📊 দৈনিক হাজিরা":
    st.header("📊 আজকের হাজিরা")
    if df_s is not None:
        with st.form("att_final"):
            h_date = st.date_input("তারিখ", datetime.now())
            att_data = []
            for _, row in df_s.iterrows():
                sid, sname = row.iloc[0], row.iloc[1]
                status = st.selectbox(f"{sname} ({sid})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=f"f_{sid}")
                att_data.append({"id": sid, "name": sname, "status": status})
            if st.form_submit_button("হাজিরা সেভ করুন"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "date": str(h_date), "data": att_data})
                st.success("হাজিরা সেভ হয়েছে!")

# --- রেজাল্ট শিট ---
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty: st.table(res.iloc[0])
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# --- পূর্ণাঙ্গ অ্যাডমিন প্যানেল (সব পুরনো অপশনসহ) ---
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.sidebar.text_input("অ্যাডমিন পিন:", type="password") == ADMIN_PIN:
        st.success("অ্যাডমিন অ্যাক্সেস গ্রান্টেড")
        opt = st.selectbox("কাজ নির্বাচন করুন:", ["নতুন ভর্তি (১১ তথ্য)", "রেজাল্ট এন্ট্রি (১০ বিষয়)", "ছাত্র তালিকা দেখুন", "ডাটা ডিলিট করুন"])
        
        if opt == "নতুন ভর্তি (১১ তথ্য)":
            with st.form("adm_full"):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ID*"); v2=c1.text_input("Name*"); v3=c1.text_input("পিতার নাম"); v4=c1.text_input("মাতার নাম"); v5=c1.text_input("ঠিকানা")
                v6=c2.text_input("মোবাইল"); v7=c2.text_input("থানা"); v8=c2.text_input("জেলা"); v9=c2.text_input("জন্ম তারিখ"); v10=c2.text_input("জন্ম সনদ"); v11=st.file_uploader("ছবি")
                if st.form_submit_button("ভর্তি করুন"):
                    img = upload_image(v11) if v11 else "-"
                    requests.post(SCRIPT_URL, json={"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img})
                    st.success("ভর্তি সম্পন্ন!")

        elif opt == "রেজাল্ট এন্ট্রি (১০ বিষয়)":
            with st.form("res_full"):
                ct1, ct2, ct3 = st.columns(3)
                rid=ct1.text_input("ID*"); rname=ct2.text_input("Name*"); rexam=ct3.text_input("পরীক্ষা*")
                c1, c2, c3 = st.columns(3)
                r1=c1.number_input("আরবি"); r2=c2.number_input("বাংলা"); r3=c3.number_input("ইংরেজি")
                r4=c1.number_input("গণিত"); r5=c2.number_input("হাদিস"); r6=c3.number_input("কালিমা")
                r7=c1.number_input("কুরআন"); r8=c2.number_input("সমাজ"); r9=c3.number_input("বিজ্ঞান"); r10=c1.number_input("সাধারণ জ্ঞান")
                if st.form_submit_button("রেজাল্ট সেভ"):
                    total = r1+r2+r3+r4+r5+r6+r7+r8+r9+r10
                    requests.post(SCRIPT_URL, json={"action": "add_result", "id": rid, "name": rname, "exam": rexam, "arb": r1, "ban": r2, "eng": r3, "mat": r4, "had": r5, "kal": r6, "qur": r7, "som": r8, "big": r9, "sgen": r10, "total": total, "grade": "Auto"})
                    st.success("সেভ হয়েছে!")

        elif opt == "ছাত্র তালিকা দেখুন":
            st.write("সম্পূর্ণ শিক্ষার্থী তালিকা:")
            if df_s is not None: st.dataframe(df_s)

        elif opt == "ডাটা ডিলিট করুন":
            st.warning("সতর্কতা: ডাটা ডিলিট করলে আর ফিরে পাওয়া যাবে না।")
            did = st.text_input("যে ছাত্রের ডাটা ডিলিট করবেন তার আইডি দিন:")
            if st.button("ডিলিট নিশ্চিত করুন"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": did})
                st.success("ডিলিট রিকোয়েস্ট পাঠানো হয়েছে।")
    else: st.warning("অ্যাডমিন পিন দিন।")
