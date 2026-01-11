import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার লেটেস্ট অ্যাপস স্ক্রিপ্ট ইউআরএল
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxhhWwTsT-V6iKjzHkJ59wgb0FVzORwsHViGGzLG5z7uUiTraV9lRlxIFKvmUXvit51/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- কালারফুল ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f2f1 0%, #f1f8e9 50%, #fff3e0 100%); }
    .main-header { background: linear-gradient(135deg, #004d4d, #008080); padding: 35px; border-radius: 20px; color: white; text-align: center; margin-bottom: 20px; }
    .notice-box { background: linear-gradient(90deg, #FF512F, #DD2476); color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 25px; border: 4px solid #fff; box-shadow: 0 8px 15px rgba(0,0,0,0.2); }
    .stTextInput input { border: 3px solid #008080 !important; border-radius: 12px !important; font-weight: bold !important; }
    .contact-hero { background: linear-gradient(135deg, #ff4b4b, #800000); padding: 25px; border-radius: 20px; color: white; text-align: center; border: 2px solid #fff; }
    .fb-box { background: #ffffff; color: #1877F2 !important; padding: 10px 25px; border-radius: 50px; text-decoration: none; display: inline-block; font-weight: bold; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড ফাংশন
@st.cache_data(ttl=5) # ৫ সেকেন্ড পর পর ফ্রেশ ডাটা আনবে
def load_all_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).applymap(lambda x: str(x).strip() if pd.notnull(x) else x)
        a_df = pd.read_csv(get_url("Form_Responses_1"))
        try:
            n_df = pd.read_csv(get_url("Notice"), header=None) # নোটিশ শিট থেকে ডাটা
            notice = n_df.iloc[0,0] if not n_df.empty else "কোনো নোটিশ নেই"
        except: notice = "কোনো নোটিশ নেই"
        return s_df, a_df, notice
    except: return None, None, "ডাটা লোড হচ্ছে..."

df_s, df_a, latest_notice = load_all_data()
today = datetime.now().strftime("%-m/%-d/%Y")
today_alt = datetime.now().strftime("%d/%m/%Y")

# ইমেজ আপলোড ফাংশন
def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস পোর্টাল</p></div>", unsafe_allow_html=True)
    
    # নোটিশ বোর্ড
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)

    present_names = []
    if df_a is not None and not df_a.empty:
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today) | df_a.iloc[:, 0].astype(str).str.contains(today_alt)]
        if not today_rows.empty:
            for row in today_rows.iloc[:, 1]:
                present_names.extend([n.strip() for n in str(row).split(',')])
    present_names = sorted(list(set(present_names)))

    c1, c2 = st.columns([2, 1])
    with c1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        st.markdown(f"""
            <div class='contact-hero'>
                <h1 style='font-size: 50px; margin:0;'>📞 01954343364</h1>
                <a href='https://web.facebook.com/BabussalamIslamiAcademi' target='_blank' class='fb-box'>🌐 ফেসবুক পেজে চোখ রাখুন</a>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"### ✅ উপস্থিতির তালিকা ({len(present_names)})")
        if present_names:
            for name in present_names:
                st.markdown(f"<div style='color:#004d4d; font-size:18px; padding:5px; border-bottom:1px solid #ddd;'>🟢 {name}</div>", unsafe_allow_html=True)
        else: st.info("আজকে এখনও কেউ হাজিরা দেয়নি।")

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("## 🔍 শিক্ষার্থীর প্রোফাইল ও হাজিরা")
    sid = st.text_input("ছাত্রের আইডি (ID) দিন এবং এন্টার চাপুন:", placeholder="যেমন: 101")
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0] == str(sid)]
        if not student.empty:
            s = student.iloc[0]
            name = str(s['Name']).strip()
            c1, c2 = st.columns([1, 2])
            with c1: st.image(s.get('Photo_URL') if pd.notnull(s.get('Photo_URL')) and s.get('Photo_URL') != "-" else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
            with c2: st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border-left:10px solid #008080;'><h2>{name}</h2><p>পিতা: {s.get('Father_Name')}<br>মোবাইল: {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
            
            is_present = False
            if df_a is not None:
                today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today) | df_a.iloc[:, 0].astype(str).str.contains(today_alt)]
                all_names_today = ",".join(today_data.iloc[:, 1].astype(str)).lower()
                if name.lower() in [n.strip().lower() for n in all_names_today.split(',')]: is_present = True
            
            if is_present: st.success(f"🌟 আলহামদুলিল্লাহ, **{name}** আজকে উপস্থিত আছে।")
            else: st.error(f"⚠️ দুঃখিত, **{name}** আজকে এখনও অনুপস্থিত।")
        else: st.error("এই আইডি দিয়ে কাউকে পাওয়া যায়নি!")

# ৩. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন কোড দিন:", type="password") == "MdmamuN18":
        t1, t2, t3 = st.tabs(["✅ হাজিরা নিন", "➕ নতুন ছাত্র ভর্তি", "📢 নোটিশ আপডেট"])
        
        with t1:
            if df_s is not None:
                selected = st.multiselect("ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা নিশ্চিত করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected)})
                    st.success("হাজিরা সফলভাবে নেওয়া হয়েছে!")
                    st.balloons()
        
        with t2:
            st.markdown("### 📝 নতুন ছাত্র ভর্তি ফরম")
            with st.form("admission", clear_on_submit=True):
                colA, colB = st.columns(2)
                with colA:
                    id_n, name_n = st.text_input("আইডি:"), st.text_input("নাম:")
                    f_name, m_name = st.text_input("পিতা:"), st.text_input("মাতা:")
                with colB:
                    mob_n, add_n = st.text_input("মোবাইল:"), st.text_input("ঠিকানা:")
                    tha_n, zel_n = st.text_input("থানা:"), st.text_input("জেলা:")
                img_file = st.file_uploader("ফোন বা পিসি থেকে ছাত্রের ছবি সিলেক্ট করুন", type=['jpg', 'png', 'jpeg'])
                if st.form_submit_button("ভর্তি সম্পন্ন করুন"):
                    img_url = upload_image(img_file) if img_file else "-"
                    payload = {"action":"admission","id":id_n,"name":name_n,"father":f_name,"mother":m_name,"mobile":mob_n,"address":add_n,"thana":tha_n,"zella":zel_n,"dob":"-","birth_cert":"-","photo":img_url}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success(f"{name_n} এর ভর্তি এবং ছবি সেভ সফল হয়েছে!")

        with t3:
            st.markdown("### 📢 নতুন নোটিশ আপডেট করুন")
            notice_txt = st.text_area("নোটিশটি এখানে লিখুন:")
            if st.button("পাবলিশ করুন"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": notice_txt})
                st.success("নোটিশটি সফলভাবে আপডেট হয়েছে!")
