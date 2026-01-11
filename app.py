import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার লেটেস্ট কাজ করা Apps Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwOnFKR6Cn68KUiNqH40NrQtjEE9KzTvA3HLTXlSuupwRdn7DYvEgqOrWzO7TPqlJud/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- প্রিমিয়াম কালারফুল ডিজাইন ---
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
        font-size: 24px; font-weight: bold; margin-bottom: 25px;
        border: 4px solid #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .contact-hero {
        background: linear-gradient(135deg, #ff4b4b 0%, #800000 100%);
        padding: 25px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(255,75,75,0.3); border: 2px solid #ffffff;
    }
    .fb-box {
        background: #ffffff; color: #1877F2 !important; padding: 10px 25px; 
        border-radius: 50px; text-decoration: none; display: inline-block;
        font-weight: bold; margin-top: 15px; font-size: 18px;
    }
    .stTextInput>div>div>input {
        border: 3px solid #008080 !important; border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড ফাংশন
@st.cache_data(ttl=1)
def load_data():
    try:
        s_df = pd.read_csv(get_url("Student_List"))
        s_df.columns = s_df.columns.str.strip()
        
        a_df = pd.read_csv(get_url("Form_Responses_1"))
        a_df.columns = a_df.columns.str.strip()
        
        try:
            n_df = pd.read_csv(get_url("Notice"))
            notice = n_df.columns[0] if not n_df.empty else "কোনো নোটিশ নেই"
        except: notice = "কোনো নোটিশ নেই"
        
        try: r_df = pd.read_csv(get_url("Result"))
        except: r_df = None
            
        return s_df, a_df, notice, r_df
    except: return None, None, "লোডিং...", None

df_s, df_a, latest_notice, df_r = load_data()
today = datetime.now().strftime("%-m/%-d/%Y")

# ইমেজ আপলোড ফাংশন
def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "📊 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)

    present_names = []
    if df_a is not None and not df_a.empty:
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today, na=False)]
        if not today_rows.empty:
            all_str = today_rows.iloc[:, 1].astype(str).str.cat(sep=',')
            present_names = sorted(list(set([n.strip() for n in all_str.split(',') if n.strip()])))

    c1, c2 = st.columns([2, 1])
    with c1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        st.markdown(f"""<div class='contact-hero'><h2>📞 01954343364</h2><a href='https://web.facebook.com/BabussalamIslamiAcademi' target='_blank' class='fb-box'>🌐 ফেসবুক পেজ</a></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"### ✅ উপস্থিতির তালিকা ({len(present_names)})")
        if present_names:
            for name in present_names: st.write(f"🟢 {name}")
        else: st.info("আজকে কেউ হাজিরা দেয়নি।")

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("## 🔍 শিক্ষার্থীর প্রোফাইল অনুসন্ধান")
    sid = st.text_input("আইডি (ID) দিন:")
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == str(sid)]
        if not student.empty:
            s = student.iloc[0]
            st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border-left:10px solid #008080;'><h2>{s['Name']}</h2><p>পিতা: {s.get('Father_Name', '-')}</p></div>", unsafe_allow_html=True)
            
            all_p = ",".join(df_a[df_a.iloc[:, 0].astype(str).str.contains(today, na=False)].iloc[:, 1].astype(str)).lower()
            if str(s['Name']).lower() in all_p: st.success("✅ আজকে উপস্থিত আছে।")
            else: st.error("❌ আজকে অনুপস্থিত।")
        else: st.error("আইডি পাওয়া যায়নি!")

# ৩. রেজাল্ট শিট
elif menu == "📊 রেজাল্ট শিট":
    st.header("📊 পরীক্ষার ফলাফল")
    rid = st.text_input("আপনার আইডি (ID) দিন:")
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].astype(str) == str(rid)]
        if not res.empty: st.table(res)
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# ৪. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন কোড:", type="password") == "MdmamuN18":
        t1, t2, t3 = st.tabs(["✅ হাজিরা নিন", "➕ নতুন ভর্তি", "📢 নোটিশ আপডেট"])
        with t1:
            if df_s is not None:
                sel = st.multiselect("ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা নিশ্চিত করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                    st.success("হাজিরা সেভ হয়েছে!")
        with t2:
            with st.form("admission", clear_on_submit=True):
                cA, cB = st.columns(2)
                id_v = cA.text_input("আইডি:"); name_v = cA.text_input("নাম:")
                mob_v = cB.text_input("মোবাইল:"); f_v = cB.text_input("পিতা:")
                img_v = st.file_uploader("ছবি আপলোড করুন", type=['jpg','png','jpeg'])
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    photo_link = upload_image(img_v) if img_v else "-"
                    payload = {"action":"admission","id":id_v,"name":name_v,"father":f_v,"mobile":mob_v,"photo":photo_link}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("ভর্তি সফল হয়েছে!")
        with t3:
            nt = st.text_area("নতুন নোটিশ:")
            if st.button("পাবলিশ করুন"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": nt})
                st.success("নোটিশ আপডেট হয়েছে!")
