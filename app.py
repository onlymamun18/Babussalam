import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzDAkDiA3Y6JaOpabswiWqpvoxHEwlJDkIgDyEXlP4yfhhSoB5HH6akOgk2CbXP-VY/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ডিজাইন ---
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
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড
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

# তারিখের ভিন্নতা দূর করার জন্য ফাংশন
def get_today_attendance():
    if df_a is None or df_a.empty:
        return []
    
    # আজকের দিন, মাস, বছর আলাদা করা
    now = datetime.now()
    t_day = str(now.day)
    t_month = str(now.month)
    t_year = str(now.year)
    
    present_names = []
    for _, row in df_a.iterrows():
        date_str = str(row.iloc[0])
        # চেক করা হচ্ছে আজকের তারিখ এই রো-তে আছে কি না (সহজ পদ্ধতিতে)
        if t_day in date_str and t_month in date_str and t_year in date_str:
            names = str(row.iloc[1]).split(',')
            present_names.extend([n.strip().lower() for n in names])
    return present_names

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট প্রোফাইল", "📊 হাজিরা রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

elif menu == "🔍 স্টুডেন্ট প্রোফাইল":
    st.header("🔍 শিক্ষার্থীর প্রোফাইল")
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"নাম: {s.get('Name', 'N/A')}")
            
            # উপস্থিতি চেক
            p_list = get_today_attendance()
            st.markdown("---")
            if str(s.get('Name','')).lower() in p_list:
                st.success("✅ আজকে উপস্থিত আছে।")
            else:
                st.error("❌ আজকে অনুপস্থিত।")
            
            if df_a is not None:
                count = len(df_a[df_a.iloc[:, 1].str.contains(s['Name'], case=False, na=False)])
                st.info(f"📊 মোট উপস্থিতি: {count} দিন")
        else: st.error("আইডি পাওয়া যায়নি")

elif menu == "📊 হাজিরা রিপোর্ট":
    st.header("📊 মোট উপস্থিতি তালিকা")
    if df_s is not None and df_a is not None:
        rep_list = []
        for _, row in df_s.iterrows():
            name = row['Name']
            count = len(df_a[df_a.iloc[:, 1].str.contains(name, case=False, na=False)])
            rep_list.append({"ID": row.iloc[0], "নাম": name, "মোট উপস্থিতি": f"{count} দিন"})
        st.table(pd.DataFrame(rep_list))

elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন কোড:", type="password") == "MdmamuN18":
        opt = st.selectbox("কাজ নির্বাচন করুন", ["হাজিরা নিন", "নতুন ভর্তি", "নোটিশ আপডেট"])
        
        if opt == "হাজিরা নিন":
            st.subheader("📝 হাজিরা ফর্ম")
            p_list = get_today_attendance()
            rem_students = [n for n in df_s['Name'].tolist() if n.lower() not in p_list]
            
            if not rem_students:
                st.success("✅ সবার হাজিরা শেষ!")
            else:
                sel = st.multiselect("নাম সিলেক্ট করুন:", rem_students)
                if st.button("হাজিরা সেভ"):
                    resp = requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                    st.success("সেভ হয়েছে!")
                    st.rerun()

        elif opt == "নতুন ভর্তি":
            with st.form("adm_form"):
                v1 = st.text_input("আইডি*"); v2 = st.text_input("নাম*")
                if st.form_submit_button("ভর্তি করুন"):
                    requests.post(SCRIPT_URL, json={"action": "admission", "id": v1, "name": v2})
                    st.success("সফল!")
