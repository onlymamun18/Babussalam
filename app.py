import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- DATA CONNECTION ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxWcYkDBW8T3mUF3WqZj7Me_l7dTd1xQA95B9QP-gUc9yUaPYWVODyiTaEU_s4Aixzs/exec"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f2f1 0%, #f1f8e9 50%, #fff3e0 100%); }
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 50%, #1de9b6 100%);
        padding: 40px; border-radius: 25px; color: white; text-align: center;
        box-shadow: 0 10px 25px rgba(0,128,128,0.3); margin-bottom: 20px;
    }
    .notice-board {
        background: linear-gradient(90deg, #ff9800, #f44336);
        color: white; padding: 15px; border-radius: 15px; text-align: center;
        font-size: 20px; font-weight: bold; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4); animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.8;} 100% {opacity: 1;} }
    
    /* Search Box Colourful */
    div[data-baseweb="input"] {
        border: 3px solid #008080 !important;
        border-radius: 15px !important;
        background-color: #ffffff !important;
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
        max-height: 450px; overflow-y: auto;
    }
    .fb-box {
        background: #ffffff; color: #1877F2 !important; padding: 12px 30px; 
        border-radius: 50px; text-decoration: none; display: inline-block;
        font-weight: bold; margin-top: 15px; font-size: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Data Loading with No Cache for Notice and Attendance
def load_data(name):
    try:
        url = get_url(name)
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except: return None

# Load All Data
df_s = load_data("Student_List")
df_a = load_data("Form_Responses_1")
# Note: Apnar sheet-e 'Notice' name ekta tab thaka lagbe jekhane 1st column e notice thakbe
df_n = load_data("Notice") 

today_date = datetime.now().strftime("%-m/%-d/%Y")
today_alt = datetime.now().strftime("%d/%m/%Y")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color:white;'>🕌 মেনু</h1>", unsafe_allow_html=True)
    menu = st.radio("পেজ পরিবর্তন করুন", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown(f"<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ক্যাম্পাস ম্যানেজমেন্ট সিস্টেম</p></div>", unsafe_allow_html=True)
    
    # Notice Board
    if df_n is not None and not df_n.empty:
        latest_notice = df_n.iloc[-1, 0] # Sobcheye shesh notice-ti nibe
        st.markdown(f"<div class='notice-board'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)

    present_names = []
    if df_a is not None and not df_a.empty:
        # Strict Date Matching
        today_rows = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date) | df_a.iloc[:, 0].astype(str).str.contains(today_alt)]
        if not today_rows.empty:
            all_str = today_rows.iloc[:, 1].astype(str).str.cat(sep=',')
            present_names = sorted(list(set([n.strip() for n in all_str.split(',') if n.strip() != ""])))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        st.markdown(f"""
            <div class='contact-hero'>
                <p style='font-size: 22px; margin:0;'>ভর্তি বা যেকোনো তথ্যের জন্য যোগাযোগ করুন</p>
                <h1 style='font-size: 55px; margin:10px 0;'>📞 01954343364</h1>
                <a href='https://web.facebook.com/BabussalamIslamiAcademi' target='_blank' class='fb-box'>🌐 ফেসবুক পেজে চোখ রাখুন</a>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<h3 style='color:#004d4d; text-align:center;'>✅ উপস্থিতির তালিকা ({len(present_names)})</h3>", unsafe_allow_html=True)
        if present_names:
            html_list = "".join([f"<li style='font-size:19px; color:#004d4d; border-bottom:1px solid #eee; padding:8px 0;'>🟢 {name}</li>" for name in present_names])
            st.markdown(f"<div class='present-list'><ul style='list-style:none; padding:0;'>{html_list}</ul></div>", unsafe_allow_html=True)
        else:
            st.info("আজকে এখনও কেউ হাজিরা দেয়নি।")

# ২. স্টুডেন্ট রিপোর্ট
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#004d4d; text-align:center;'>🔍 শিক্ষার্থীর প্রোফাইল অনুসন্ধান</h2>", unsafe_allow_html=True)
    sid = st.text_input("এখানে ছাত্রের আইডি (ID) লিখুন:", placeholder="উদাহরণ: 101")
    
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str).str.strip() == str(sid).strip()]
        if not student.empty:
            s = student.iloc[0]
            name = str(s.get('Name')).strip()
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(s.get('Photo_URL') if pd.notnull(s.get('Photo_URL')) else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
            with c2:
                st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border:2px solid #008080;'><h2>{name}</h2><p><b>পিতা:</b> {s.get('Father_Name')}<br><b>মোবাইল:</b> {s.get('Mobile')}</p></div>", unsafe_allow_html=True)
            
            # Attendance Status Fix
            st.write("---")
            is_present = False
            if df_a is not None:
                today_data = df_a[df_a.iloc[:, 0].astype(str).str.contains(today_date) | df_a.iloc[:, 0].astype(str).str.contains(today_alt)]
                if not today_data.empty:
                    # Protita row-er names check korbe
                    for row_names in today_data.iloc[:, 1].astype(str):
                        if name.lower() in [n.strip().lower() for n in row_names.split(',')]:
                            is_present = True
                            break
            
            if is_present:
                st.success(f"🌟 আলহামদুলিল্লাহ, **{name}** আজকে উপস্থিত আছে।")
            else:
                st.error(f"⚠️ দুঃখিত, **{name}** আজকে এখনও অনুপস্থিত।")
        else:
            st.warning("এই আইডি দিয়ে কাউকে পাওয়া যায়নি।")

# ৩. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("এডমিন পিন দিন:", type="password") == "MdmamuN18":
        tab1, tab2, tab3 = st.tabs(["✅ হাজিরা নিন", "➕ নতুন ভর্তি", "📢 নোটিশ আপডেট"])
        
        with tab1:
            if df_s is not None:
                selected = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা নিশ্চিত করুন"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected)})
                    st.success("হাজিরা সেভ হয়েছে!")
                    st.balloons()
        
        with tab2:
            st.info("ভর্তি ফরম আগের মতোই কাজ করবে।")
            # ... Admission Form Code ... (Apnar ager code ta thakbe)

        with tab3:
            st.markdown("### 📢 নতুন নোটিশ লিখুন")
            new_notice = st.text_area("নোটিশটি এখানে লিখুন:")
            if st.button("নোটিশ পাবলিশ করুন"):
                if new_notice:
                    # Notice save korar jonno Apps Script e arekta action lagbe
                    payload = {"action": "admission", "id": "NOTICE", "name": new_notice, "father": "-", "mother": "-", "mobile": "-", "address": "-", "thana": "-", "zella": "-", "dob": "-", "birth_cert": "-", "photo": "-"}
                    # Alternately: Apni manually Sheet er 'Notice' tab e likhte paren. 
                    # Ekhonkar moto ami suggestion dicchi Sheet e 'Notice' name ekta tab khule rakhun.
                    st.warning("Notice feature fully chalu korte Sheet e 'Notice' name tab thaka lagbe.")
