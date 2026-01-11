import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার নতুন ইউআরএল আপডেট করা হলো
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxWcYkDBW8T3mUF3WqZj7Me_l7dTd1xQA95B9QP-gUc9yUaPYWVODyiTaEU_s4Aixzs/exec"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- সুপার কালারফুল CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f2f1 0%, #f1f8e9 50%, #fff3e0 100%); }
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 50%, #1de9b6 100%);
        padding: 40px; border-radius: 25px; color: white; text-align: center;
        box-shadow: 0 10px 25px rgba(0,128,128,0.3); margin-bottom: 20px;
    }
    .contact-hero {
        background: linear-gradient(135deg, #ff4b4b 0%, #800000 100%);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(255,75,75,0.3); margin-top: 30px;
        border: 2px solid #ffffff;
    }
    .present-list {
        background: white; padding: 20px; border-radius: 20px;
        border-left: 10px solid #28a745; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        max-height: 400px; overflow-y: auto;
    }
    .fb-box {
        background: #1877F2; color: white; padding: 10px; 
        border-radius: 10px; text-decoration: none; display: inline-block;
        font-weight: bold; margin-top: 10px;
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
today_1 = datetime.now().strftime("%-m/%-d/%Y")
today_2 = datetime.now().strftime("%d/%m/%Y")

# --- সাইডবার ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color:white;'>🕌 মেনু</h1>", unsafe_allow_html=True)
    menu = st.radio("পেজ পরিবর্তন করুন", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown(f"<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p></div>", unsafe_allow_html=True)
    
    present_names = []
    if df_a is not None and not df_a.empty:
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_1) | df_a.iloc[:, 0].astype(str).str.contains(today_2)]
        if not today_rows.empty:
            all_str = today_rows.iloc[:, 1].astype(str).str.cat(sep=',')
            present_names = sorted(list(set([n.strip() for n in all_str.split(',') if n.strip() != ""])))

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        # উজ্জ্বল কন্টাক্ট সেকশন
        st.markdown(f"""
            <div class='contact-hero'>
                <p style='font-size: 20px; margin:0;'>ভর্তি বা যেকোনো তথ্যের জন্য সরাসরি যোগাযোগ করুন</p>
                <h1 style='font-size: 50px; margin:10px 0;'>📞 01954343364</h1>
                <p style='font-size: 18px;'>আমাদের কার্যক্রম সম্পর্কে জানতে ফেসবুক পেজে চোখ রাখুন</p>
                <a href='https://www.facebook.com/yourpage' class='fb-box'>Facebook Page</a>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"### ✅ আজকের উপস্থিতি ({len(present_names)})")
        if present_names:
            html_list = "".join([f"<li style='font-size:18px; color:#004d4d; border-bottom:1px solid #eee; padding:5px 0;'>🟢 {name}</li>" for name in present_names])
            st.markdown(f"<div class='present-list'><ul style='list-style:none; padding:0;'>{html_list}</ul></div>", unsafe_allow_html=True)
        else:
            st.info("আজকে এখনও কেউ হাজিরা দেয়নি।")

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#004d4d; background:white; padding:10px; border-radius:10px; text-align:center;'>🔍 শিক্ষার্থীর প্রোফাইল অনুসন্ধান</h2>", unsafe_allow_html=True)
    sid = st.text_input("আইডি (ID) নম্বর দিন:")
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str).str.strip() == str(sid).strip()]
        if not student.empty:
            s = student.iloc[0]
            name = s.get('Name')
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(s.get('Photo_URL') if pd.notnull(s.get('Photo_URL')) else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
            with c2:
                st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border-left:8px solid #008080;'><h2>{name}</h2><p>পিতা: {s.get('Father_Name')}<br>মোবাইল: {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
            
            # উপস্থিতি চেক
            if df_a is not None:
                today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_1) | df_a.iloc[:, 0].astype(str).str.contains(today_2)]
                if not today_data.empty and any(today_data.iloc[:, 1].astype(str).str.contains(str(name))):
                    st.success(f"🌟 {name} আজকে উপস্থিত আছে।")
                else:
                    st.error(f"⚠️ {name} আজকে অনুপস্থিত।")

# ৩. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন দিন:", type="password") == "MdmamuN18":
        tab1, tab2 = st.tabs(["✅ হাজিরা নিন", "➕ নতুন ছাত্র ভর্তি"])
        with tab1:
            if df_s is not None:
                selected = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা সেভ করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected)})
                    st.success("হাজিরা নেওয়া হয়েছে!")
                    st.balloons()
        with tab2:
            st.markdown("### 📝 বিস্তারিত ভর্তি ফরম")
            with st.form("admission_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    n_id, n_name = st.text_input("আইডি:"), st.text_input("নাম:")
                    n_father, n_mother = st.text_input("পিতা:"), st.text_input("মাতা:")
                    n_dob = st.date_input("জন্ম তারিখ:")
                with c2:
                    n_mob, n_addr = st.text_input("মোবাইল:"), st.text_input("ঠিকানা:")
                    n_thana, n_zella = st.text_input("থানা:"), st.text_input("জেলা:")
                    n_cert = st.text_input("জন্ম সনদ নং:")
                n_photo = st.text_input("ছবির URL:")
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    payload = {"action":"admission","id":n_id,"name":n_name,"father":n_father,"mother":n_mother,"mobile":n_mob,"address":n_addr,"thana":n_thana,"zella":n_zella,"dob":str(
