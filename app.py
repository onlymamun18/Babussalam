import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন (আপনার দেওয়া নতুন লিঙ্ক এখানে বসানো হয়েছে) ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxbixVRGl2lMJnz8GHt-ZKkn_3riRU0ihcNgv65Fs8ZuWuyI0AkCs8797wK-L26k0hM/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম রঙিন UI ---
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
        return s_df
    except: return None

df_s = load_all_data()

def upload_image(image_file):
    try:
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.getvalue()).decode('utf-8')}
        res = requests.post("https://api.imgbb.com/1/upload", payload)
        return res.json()['data']['url'] if res.status_code == 200 else "-"
    except: return "-"

# --- ৪. নেভিগেশন মেনু ---
menu = st.sidebar.radio("🧭 মেনু নেভিগেশন", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "🔐 অ্যাডমিন প্যানেল"])

# --- হোম পেজ ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>আপনার সন্তানের উজ্জ্বল ভবিষ্যৎ গড়তে আমরা প্রতিশ্রুতিবদ্ধ</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown('<a href="tel:01954343364" class="big-button call-btn">📱 সরাসরি কল করুন</a>', unsafe_allow_html=True)
    with c2: st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজ</a>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- প্রোফাইল সার্চ ---
elif menu == "🔍 প্রোফাইল সার্চ":
    sid = st.text_input("শিক্ষার্থীর আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        if not student.empty:
            s = student.iloc[0]
            st.success(f"ছাত্রের নাম: {s[1]}")
            # আপনার গুগল স্ক্রিপ্টের কলাম সিরিয়াল অনুযায়ী ডাটা ম্যাপিং
            details = {
                "বিবরণ": ["আইডি", "নাম", "পিতার নাম", "মাতার নাম", "ঠিকানা", "মোবাইল নম্বর", "থানা", "জেলা", "জন্ম তারিখ", "জন্ম নিবন্ধন"],
                "তথ্য": [s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9]]
            }
           # ছবির এরর হ্যান্ডলিং (ফিক্সড কোড)
            if len(s) > 10:
                img_path = str(s[10]).strip()
                if img_path.startswith("http"):
                    try:
                        st.image(img_path, width=150, caption="ছাত্রের ছবি")
                    except:
                        st.warning("⚠️ ছবি লোড করা যাচ্ছে না (Invalid Link)")
                else:
                    st.info("📷 এই ছাত্রের কোনো ছবি আপলোড করা নেই।")
        else: st.error("দুঃখিত, এই আইডি পাওয়া যায়নি।")

# --- হাজিরা সেকশন (আপনার স্ক্রিপ্টের সাথে কানেক্টেড) ---
elif menu == "📊 দৈনিক হাজিরা":
    st.header("📊 প্রতিদিনের হাজিরা")
    if df_s is not None:
        with st.form("att_form"):
            h_date = st.date_input("তারিখ নির্বাচন করুন", datetime.now())
            attendance_list = []
            for _, row in df_s.iterrows():
                # প্রতিটি ছাত্রের জন্য ড্রপডাউন
                status = st.selectbox(f"{row[1]} ({row[0]})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=row[0])
                attendance_list.append({
                    "date": str(h_date),
                    "id": row[0],
                    "name": row[1],
                    "status": status
                })
            
            if st.form_submit_button("✅ হাজিরা সেভ করুন"):
                # গুগল স্ক্রিপ্টে 'data' কী এর আন্ডারে পুরো লিস্টটি পাঠানো হচ্ছে
                requests.post(SCRIPT_URL, json={"action": "attendance", "data": attendance_list})
                st.success(f"আলহামদুলিল্লাহ! {len(attendance_list)} জন ছাত্রের হাজিরা সেভ হয়েছে।")

# --- অ্যাডমিন প্যানেল ---
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.sidebar.text_input("অ্যাডমিন পিন দিন:", type="password") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন:", ["নতুন ভর্তি", "ছাত্র তালিকা দেখুন", "ডাটা ডিলিট করুন"])
        
        if opt == "নতুন ভর্তি":
            with st.form("adm_form"):
                c1, c2 = st.columns(2)
                v1=c1.text_input("আইডি (ID)*"); v2=c1.text_input("নাম (Name)*"); v3=c1.text_input("পিতার নাম"); v4=c1.text_input("মাতার নাম"); v5=c1.text_input("ঠিকানা")
                v6=c2.text_input("মোবাইল"); v7=c2.text_input("থানা"); v8=c2.text_input("জেলা"); v9=c2.text_input("জন্ম তারিখ"); v10=c2.text_input("জন্ম সনদ"); v11=st.file_uploader("ছবি দিন")
                
                if st.form_submit_button("ভর্তি সম্পন্ন করুন"):
                    img_url = upload_image(v11) if v11 else "-"
                    # আপনার স্ক্রিপ্টের doPost ফাংশনের ভেরিয়েবলের সাথে মিলিয়ে পাঠানো হচ্ছে
                    payload = {
                        "action": "admission",
                        "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5,
                        "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img_url
                    }
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("সফলভাবে ভর্তি সম্পন্ন হয়েছে!")
        
        elif opt == "ছাত্র তালিকা দেখুন":
            st.dataframe(df_s)
            
        elif opt == "ডাটা ডিলিট করুন":
            did = st.text_input("ডিলিট করতে আইডি দিন:")
            if st.button("ডিলিট নিশ্চিত করুন"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": did})
                st.success("আইডি ডিলিট সম্পন্ন!")
    else: st.warning("সঠিক পিন দিয়ে প্যানেল আনলক করুন।")
