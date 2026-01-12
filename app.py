import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন (আপনার দেওয়া তথ্য অনুযায়ী) ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyaOoNMXgz2bbQEDPDiMBpmgOEjFeIJEkuNU_zCdHCuq2GRsG_cp5L-P_wTPufmsvP2/exec"
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
    .contact-hero { background: linear-gradient(135deg, #ff4b4b, #800000); padding: 20px; border-radius: 15px; color: white; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড
@st.cache_data(ttl=1)
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
today = datetime.now().strftime("%-m/%-d/%Y")

def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "📊 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড (ক্লিন ডিজাইন)
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    st.markdown(f"<div class='contact-hero'><h3>📞 যোগাযোগ: 01954343364</h3></div>", unsafe_allow_html=True)

# ২. স্টুডেন্ট রিপোর্ট (সিকিউর ভিউ + ব্যক্তিগত হাজিরা)
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    is_admin = False
    with st.sidebar:
        if st.text_input("অ্যাডমিন পিন:", type="password", key="rep_pin") == "MdmamuN18":
            is_admin = True
            st.success("🔓 অ্যাডমিন মোড অ্যাক্টিভ")

    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"নাম: {s.get('Name', 'N/A')}")
            
            if is_admin:
                # অ্যাডমিন হলে সব ১১টি কলামের ডাটা দেখাবে
                st.table(pd.DataFrame(s.items(), columns=["বিষয়", "তথ্য"]))
            else:
                st.warning("🔒 ব্যক্তিগত তথ্য লুকানো আছে। শুধু অ্যাডমিন পিন দিয়ে সব দেখা যাবে।")

            # ব্যক্তিগত হাজিরা চেক
            all_p = ""
            if df_a is not None and not df_a.empty:
                today_rows = df_a[df_a.iloc[:, 0].str.contains(today, na=False)]
                all_p = ",".join(today_rows.iloc[:, 1].astype(str)).lower()
            
            st.markdown("---")
            if str(s.get('Name','')).lower() in all_p:
                st.success(f"✅ **{s['Name']}** আজকে উপস্থিত আছে।")
            else: 
                st.error(f"❌ **{s['Name']}** আজকে এখনও অনুপস্থিত।")
        else: st.error("এই আইডির কোনো ছাত্র পাওয়া যায়নি।")

# ৩. রেজাল্ট শিট (আলাদা সেকশন)
elif menu == "📊 রেজাল্ট শিট":
    st.header("📊 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি (ID) দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].astype(str) == rid]
        if not res.empty: 
            st.table(res.T)
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# ৪. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন কোড:", type="password") == "admin_main") == "MdmamuN18":
        opt = st.selectbox("কাজ নির্বাচন করুন", ["নতুন ভর্তি", "হাজিরা নিন", "নোটিশ আপডেট"])
        
        if opt == "নতুন ভর্তি":
            with st.form("adm_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1 = c1.text_input("আইডি*"); v2 = c1.text_input("নাম*")
                v3 = c1.text_input("পিতার নাম"); v4 = c1.text_input("মাতার নাম")
                v5 = c1.text_input("জন্ম তারিখ (DD/MM/YYYY)")
                v6 = c2.text_input("মোবাইল নম্বর"); v7 = c2.text_input("ঠিকানা")
                v8 = c2.text_input("থানা"); v9 = c2.text_input("জেলা")
                v10 = c2.text_input("জন্ম সনদ নম্বর")
                v11 = st.file_uploader("ছাত্রের ছবি")
                
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    img_url = upload_image(v11) if v11 else "-"
                    payload = {
                        "action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, 
                        "mobile": v6, "address": v7, "thana": v8, "zella": v9, "dob": v5, 
                        "birth_cert": v10, "photo": img_url
                    }
                    requests.post(SCRIPT_URL, json=payload)
                    st.success(f"{v2} এর ভর্তি সম্পন্ন হয়েছে!")

        elif opt == "হাজিরা নিন":
            if df_s is not None:
                sel = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা সেভ"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                    st.success("হাজিরা শিটে জমা হয়েছে!")

        elif opt == "নোটিশ আপডেট":
            n_txt = st.text_area("নতুন নোটিশ:")
            if st.button("পাবলিশ"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": n_txt})
                st.success("নোটিশ আপডেট হয়েছে!")
