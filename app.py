import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার দেওয়া লেটেস্ট URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwOnFKR6Cn68KUiNqH40NrQtjEE9KzTvA3HLTXlSuupwRdn7DYvEgqOrWzO7TPqlJud/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- প্রিমিয়াম কালারফুল ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f7; }
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 100%);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    .notice-box {
        background: #ff4b4b; color: white; padding: 18px; border-radius: 12px;
        text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 25px;
        border: 4px solid #fff; box-shadow: 0 5px 15px rgba(255,75,75,0.3);
    }
    .result-card {
        background: white; padding: 25px; border-radius: 15px;
        border-top: 10px solid #008080; box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    }
    /* সার্চ বক্সের উজ্জ্বল বর্ডার */
    .stTextInput>div>div>input {
        border: 3px solid #008080 !important;
        border-radius: 10px !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড ফাংশন (ক্লিন ও নির্ভুল)
def load_sheet_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip() # কলামের নামের বাড়তি স্পেস মুছে ফেলবে
        return df.astype(str) # সব ডাটা স্ট্রিং হিসেবে নিবে যাতে ম্যাচিং সহজ হয়
    except:
        return pd.DataFrame()

df_s = load_sheet_data("Student_List")
df_a = load_sheet_data("Form_Responses_1")
df_n = load_sheet_data("Notice")
df_r = load_sheet_data("Result")

# আজকের তারিখ (গুগল শিটের স্টাইলে)
today_date = datetime.now().strftime("%-m/%-d/%Y") # যেমন: 1/11/2026

# --- সাইডবার মেনু ---
menu = st.sidebar.radio("প্রধান মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 রিপোর্ট ও রেজাল্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    
    # নোটিশ প্রদর্শন (যদি থাকে)
    if not df_n.empty:
        # নোটিশ ট্যাবের প্রথম রো-এর প্রথম কলামটি দেখাবে
        msg = df_n.columns[0] if len(df_n.columns) > 0 else "কোনো নোটিশ নেই"
        st.markdown(f"<div class='notice-box'>📢 নোটিশ: {msg}</div>", unsafe_allow_html=True)

    # উপস্থিতি হিসাব
    present_today = []
    if not df_a.empty:
        # তারিখের কলামে আজকের তারিখ আছে এমন রোগুলো ফিল্টার
        today_rows = df_a[df_a.iloc[:, 0].str.contains(today_date, na=False)]
        for entries in today_rows.iloc[:, 1]:
            present_today.extend([n.strip() for n in str(entries).split(',') if n.strip()])
    
    present_today = sorted(list(set(present_today)))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        st.info("যোগাযোগ: 01954343364 | [ফেসবুক পেজ](https://web.facebook.com/BabussalamIslamiAcademi)")
    with col2:
        st.markdown(f"### ✅ আজকের উপস্থিতি ({len(present_today)})")
        if present_today:
            for p in present_today:
                st.markdown(f"<div style='color:#004d4d; font-size:18px; padding:5px; border-bottom:1px solid #eee;'>🟢 {p}</div>", unsafe_allow_html=True)
        else:
            st.warning("এখনও কেউ হাজিরা দেয়নি।")

# ২. রিপোর্ট ও রেজাল্ট
elif menu == "🔍 রিপোর্ট ও রেজাল্ট":
    st.markdown("<h2 style='color:#004d4d; text-align:center;'>🔍 ছাত্রের তথ্য ও ফলাফল</h2>", unsafe_allow_html=True)
    search_id = st.text_input("এখানে ছাত্রের আইডি (ID) লিখুন:").strip()
    
    if search_id:
        # স্টুডেন্ট লিস্ট থেকে আইডি খুঁজে বের করা
        student = df_s[df_s.iloc[:, 0] == search_id]
        if not student.empty:
            s_data = student.iloc[0]
            st.markdown(f"<div class='result-card'><h3>নাম: {s_data['Name']}</h3><p>পিতা: {s_data.get('Father_Name', '-')}</p></div>", unsafe_allow_html=True)
            
            # রেজাল্ট প্রদর্শন (ডাইনামিক - শিটে যা আছে সব দেখাবে)
            st.markdown("---")
            st.subheader("📊 পরীক্ষার রেজাল্ট")
            if not df_r.empty:
                # রেজাল্ট শিটের ১ম কলামের সাথে আইডি মিলানো
                res_info = df_r[df_r.iloc[:, 0] == search_id]
                if not res_info.empty:
                    # রেজাল্ট টেবিলটিকে লম্বালম্বিভাবে দেখাবে (Transpose) যাতে সহজে পড়া যায়
                    final_res = res_info.set_index(res_info.columns[0]).T
                    final_res.columns = ["প্রাপ্ত তথ্য/মার্কস"]
                    st.table(final_res)
                else:
                    st.warning("রেজাল্ট শিটে এই আইডির তথ্য পাওয়া যায়নি।")
            
            # উপস্থিতি স্ট্যাটাস চেক
            st.markdown("---")
            all_names = ",".join(df_a[df_a.iloc[:, 0].str.contains(today_date, na=False)].iloc[:, 1]).lower()
            if s_data['Name'].lower() in all_names:
                st.success(f"✅ আলহামদুলিল্লাহ, {s_data['Name']} আজকে উপস্থিত আছে।")
                st.balloons()
            else:
                st.error(f"❌ দুঃখিত, {s_data['Name']} আজকে এখনও অনুপস্থিত।")
        else:
            st.error("দুঃখিত, এই আইডি দিয়ে কোনো ছাত্র পাওয়া যায়নি।")

# ৩. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    pwd = st.text_input("সিক্রেট পিন দিন:", type="password")
    if pwd == "MdmamuN18":
        tab1, tab2, tab3 = st.tabs(["✅ হাজিরা নিন", "➕ নতুন ছাত্র ভর্তি", "📢 নোটিশ আপডেট"])
        
        with tab1:
            if not df_s.empty:
                selected_names = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা সেভ করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected_names)})
                    st.success("হাজিরা সফলভাবে শিটে সেভ হয়েছে!")

        with tab2:
            st.info("ভর্তি ফরমের জন্য আগের সিস্টেম ব্যবহার করুন।")

        with tab3:
            st.markdown("### 📢 নোটিশ বোর্ড আপডেট")
            msg_txt = st.text_area("নতুন নোটিশটি এখানে লিখুন:")
            if st.button("পাবলিশ নোটিশ"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": msg_txt})
                st.success("নোটিশটি সফলভাবে হোমপেজে আপডেট হয়েছে!")
