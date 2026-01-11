import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার লেটেস্ট কাজ করা URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwOnFKR6Cn68KUiNqH40NrQtjEE9KzTvA3HLTXlSuupwRdn7DYvEgqOrWzO7TPqlJud/exec"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-header {
        background: linear-gradient(135deg, #004d4d, #008080);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
    }
    .contact-hero {
        background: #ff4b4b; padding: 25px; border-radius: 20px; color: white; text-align: center;
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
today = datetime.now().strftime("%-m/%-d/%Y")

# --- মেনু ---
menu = st.sidebar.radio("মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1></div>", unsafe_allow_html=True)
    
    present_names = []
    if df_a is not None and not df_a.empty:
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today)]
        if not today_rows.empty:
            all_str = today_rows.iloc[:, 1].astype(str).str.cat(sep=',')
            present_names = sorted(list(set([n.strip() for n in all_str.split(',') if n.strip() != ""])))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        st.markdown(f"""
            <div class='contact-hero'>
                <h3>📞 01954343364</h3>
                <a href='https://web.facebook.com/BabussalamIslamiAcademi' target='_blank' style='color:white; font-weight:bold;'>🌐 ফেসবুক পেজ</a>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.subheader(f"✅ আজকের উপস্থিতি ({len(present_names)})")
        for name in present_names: st.write(f"🟢 {name}")

elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.subheader("🔍 ছাত্রের আইডি দিয়ে খুঁজুন")
    sid = st.text_input("আইডি দিন:")
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == str(sid)]
        if not student.empty:
            s = student.iloc[0]
            st.write(f"### নাম: {s['Name']}")
            # উপস্থিতি চেক
            all_p = ",".join(df_a[df_a.iloc[:, 0].astype(str).str.contains(today)].iloc[:, 1].astype(str)).lower()
            if str(s['Name']).lower() in all_p: st.success("উপস্থিত")
            else: st.error("অনুপস্থিত")

elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন:", type="password") == "MdmamuN18":
        sel = st.multiselect("নাম সিলেক্ট করুন:", df_s['Name'].tolist() if df_s is not None else [])
        if st.button("হাজিরা সেভ"):
            requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
            st.success("সেভ হয়েছে")
