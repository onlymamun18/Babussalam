import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার নতুন দেওয়া স্ক্রিপ্ট লিঙ্ক এখানে বসানো হয়েছে
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- প্রিমিয়াম ডিজাইন ---
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
        font-size: 22px; font-weight: bold; margin-bottom: 25px;
        border: 4px solid #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .contact-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
        border-left: 5px solid #008080; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ডাটা লোড ---
@st.cache_data(ttl=0)
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

# ইমেজ আপলোড
def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট প্রোফাইল", "📊 হাজিরা রিপোর্ট", "📝 রেজাল্ট শিট", "📞 যোগাযোগ ও সোশ্যাল", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# ২. প্রোফাইল
elif menu == "🔍 স্টুডেন্ট প্রোফাইল":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"নাম: {s['Name']}")
            st.table(pd.DataFrame(s.items(), columns=["বিষয়", "তথ্য"]))
        else: st.error("এই আইডির কোনো ছাত্র পাওয়া যায়নি।")

# ৩. হাজিরা রিপোর্ট
elif menu == "📊 হাজিরা রিপোর্ট":
    st.header("📊 মোট উপস্থিতি তালিকা")
    if df_s is not None and df_a is not None:
        rep = []
        for _, row in df_s.iterrows():
            count = sum(1 for _, r in df_a.iterrows() if str(row['Name']).lower() in str(r.iloc[1]).lower())
            rep.append({"আইডি": row.iloc[0], "নাম": row['Name'], "মোট উপস্থিতি": f"{count} দিন"})
        st.dataframe(pd.DataFrame(rep), use_container_width=True)

# ৪. রেজাল্ট
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].astype(str) == rid]
        if not res.empty: st.table(res.T)
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# ৫. যোগাযোগ ও সোশ্যাল (আপনার চাহিদা অনুযায়ী)
elif menu == "📞 যোগাযোগ ও সোশ্যাল":
    st.header("📞 আমাদের সাথে যোগাযোগ")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='contact-card'><h3>📱 মোবাইল</h3><p>01954343364</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='contact-card'><h3>🌐 ফেসবুক পেজ</h3><a href='https://www.facebook.com/share/18Y28D9gKj/' target='_blank'>ফেসবুক পেজে যেতে ক্লিক করুন</a></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='contact-card'><h3>📧 ইমেইল</h3><p>babussalam@gmail.com</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='contact-card'><h3>📍 ঠিকানা</h3><p>ঢাকা, বাংলাদেশ</p></div>", unsafe_allow_html=True)

# ৬. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন:", type="password") == "MdmamuN18":
        opt = st.selectbox("কাজ নির্বাচন করুন", ["মাদরাসার ছাত্র তালিকা", "হাজিরা নিন", "ছাত্র ভর্তি/এডিট/ডিলিট", "নোটিশ আপডেট"])
        
        if opt == "মাদরাসার ছাত্র তালিকা":
            st.subheader("📋 সকল শিক্ষার্থীর লিস্ট")
            st.dataframe(df_s, use_container_width=True)

        elif opt == "হাজিরা নিন":
            st.subheader("📝 আজকের হাজিরা")
            sel = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
            if st.button("হাজিরা সেভ করুন"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                st.success("হাজিরা সফলভাবে জমা হয়েছে!")

        elif opt == "ছাত্র ভর্তি/এডিট/ডিলিট":
            mode = st.radio("অ্যাকশন:", ["নতুন ভর্তি (Add)", "তথ্য সংশোধন (Edit)", "ছাত্র বাদ দিন (Delete)"])
            
            if mode == "নতুন ভর্তি (Add)":
                with st.form("add_student"):
                    v1=st.text_input("ID*"); v2=st.text_input("Name*"); v3=st.text_input("Father"); v4=st.text_input("Mother")
                    v6=st.text_input("Mobile"); v7=st.text_input("Address"); v11=st.file_uploader("Photo")
                    if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                        img = upload_image(v11) if v11 else "-"
                        payload = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "mobile": v6, "address": v7, "photo": img}
                        requests.post(SCRIPT_URL, json=payload)
                        st.success("ছাত্র সফলভাবে ভর্তি করা হয়েছে!")

            elif mode == "Edit (সংশোধন)":
                st.info("সংশোধন করার জন্য সরাসরি গুগল শিট ব্যবহার করা সবচেয়ে নিরাপদ।")

            elif mode == "Delete (বাদ দিন)":
                del_id = st.text_input("যে আইডি বাদ দিতে চান:")
                if st.button("ডিলিট করুন", type="primary"):
                    requests.post(SCRIPT_URL, json={"action": "delete", "id": del_id})
                    st.warning("আইডি মুছে ফেলা হয়েছে।")

        elif opt == "নোটিশ আপডেট":
            txt = st.text_area("নতুন নোটিশ:")
            if st.button("পাবলিশ"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": txt})
                st.success("নোটিশ আপডেট হয়েছে!")
