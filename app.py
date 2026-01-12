import streamlit as st
import pandas as pd
import requests
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- প্রিমিয়াম UI ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f6; }
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 100%);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .big-button {
        display: block; width: 100%; padding: 20px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 22px; font-weight: bold;
        text-decoration: none; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .fb-btn { background: linear-gradient(90deg, #1877F2 0%, #0056b3 100%); }
    .call-btn { background: linear-gradient(90deg, #28a745 0%, #1e7e34 100%); }
    div[data-baseweb="input"] { border: 2px solid #008080 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ডাটা লোড ---
@st.cache_data(ttl=0)
def load_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        s_df.iloc[:, 0] = s_df.iloc[:, 0].str.strip()
        try:
            r_df = pd.read_csv(get_url("Result")).astype(str)
            r_df.iloc[:, 0] = r_df.iloc[:, 0].str.strip()
        except: r_df = None
        return s_df, r_df
    except: return None, None

df_s, df_r = load_data()

# --- ফটো আপলোড ফাংশন ---
def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.getvalue()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url'] if res.status_code == 200 else "-"
    except: return "-"

# --- মেইন মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 সরাসরি কল করুন (01954343364)</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 আমাদের ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    is_admin = st.sidebar.text_input("অ্যাডমিন পিন দিন:", type="password") == ADMIN_PIN
    sid = st.text_input("আইডি (ID) নম্বর দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0] == sid]
        if not student.empty:
            s = student.iloc[0]
            if is_admin:
                st.success(f"অ্যাডমিন ভিউ: {s['Name']}")
                st.table(pd.DataFrame(s.items(), columns=["বিষয়", "তথ্য"]))
                if s.get('Photo') and s['Photo'] != "-": st.image(s['Photo'], width=200)
            else:
                st.info("গার্ডিয়ান ভিউ")
                st.subheader(f"নাম: {s['Name']}")
                st.write(f"আইডি: {s['ID']}")
        else: st.error("দুঃখিত, এই আইডি পাওয়া যায়নি।")

elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0] == rid]
        if not res.empty:
            st.table(res.T)
        else: st.warning("ফলাফল পাওয়া যায়নি।")

elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন:", type="password") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন:", ["নতুন ভর্তি (১১ তথ্য)", "রেজাল্ট এন্ট্রি (সব বিষয়)", "ছাত্র তালিকা", "ডিলিট"])
        
        if opt == "নতুন ভর্তি (১১ তথ্য)":
            with st.form("adm_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ID*"); v2=c1.text_input("Name*"); v3=c1.text_input("Father"); v4=c1.text_input("Mother"); v5=c1.text_input("Address")
                v6=c2.text_input("Mobile"); v7=c2.text_input("Thana"); v8=c2.text_input("Zella"); v9=c2.text_input("DOB"); v10=c2.text_input("Birth Cert")
                v11=st.file_uploader("ছবি আপলোড")
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    img_url = upload_image(v11) if v11 else "-"
                    # আপনার দেওয়া সিরিয়াল অনুযায়ী: ID, Name, Father, Mother, Address, Mobile, Thana, Zella, DOB, Birth Cert, Photo
                    payload = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img_url}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("সফলভাবে ভর্তি করা হয়েছে!")

        elif opt == "রেজাল্ট এন্ট্রি (সব বিষয়)":
            with st.form("res_form", clear_on_submit=True):
                r_id = st.text_input("ID*")
                c1, c2 = st.columns(2)
                r_arb = c1.text_input("আরবি"); r_qur = c2.text_input("কুরআন")
                r_ban = c1.text_input("বাংলা"); r_mat = c2.text_input("গণিত")
                r_eng = c1.text_input("ইংরেজি"); r_tot = c2.text_input("মোট গ্রেড")
                if st.form_submit_button("রেজাল্ট সেভ করুন"):
                    requests.post(SCRIPT_URL, json={"action": "add_result", "id": r_id, "arb": r_arb, "qur": r_qur, "ban": r_ban, "mat": r_mat, "eng": r_eng, "total": r_tot})
                    st.success("রেজাল্ট সেভ হয়েছে!")
