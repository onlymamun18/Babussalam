import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
# আপনার দেওয়া সঠিক শিট আইডি এবং স্ক্রিপ্ট ইউআরএল
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyaOoNMXgz2bbQEDPDiMBpmgOEjFeIJEkuNU_zCdHCuq2GRsG_cp5L-P_wTPufmsvP2/exec"
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
        font-size: 24px; font-weight: bold; margin-bottom: 25px;
        border: 4px solid #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input { border: 2px solid #008080 !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড ফাংশন
@st.cache_data(ttl=1)
def load_data():
    try:
        # স্টুডেন্ট লিস্ট এবং অন্যান্য শিট পড়া
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        a_df = pd.read_csv(get_url("Form_Responses_1")).astype(str)
        try:
            n_df = pd.read_csv(get_url("Notice"))
            notice = n_df.columns[0] if not n_df.empty else "কোনো নোটিশ নেই"
        except: notice = "কোনো নোটিশ নেই"
        try:
            r_df = pd.read_csv(get_url("Result")).astype(str)
        except: r_df = None
        return s_df, a_df, notice, r_df
    except: return None, None, "লোডিং...", None

df_s, df_a, latest_notice, df_r = load_data()
today = datetime.now().strftime("%-m/%-d/%Y") # যেমন: 1/11/2026

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
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    
    # উপস্থিতি চেক
    present_list = []
    if df_a is not None and not df_a.empty:
        today_data = df_a[df_a.iloc[:, 0].str.contains(today, na=False)]
        for entries in today_data.iloc[:, 1]:
            present_list.extend([n.strip() for n in str(entries).split(',') if n.strip()])
    present_list = sorted(list(set(present_list)))

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
        st.info("হটলাইন: 01954343364")
    with col_b:
        st.subheader(f"✅ আজকের উপস্থিতি ({len(present_list)})")
        for p in present_list: st.write(f"🟢 {p}")

# ২. স্টুডেন্ট রিপোর্ট (অ্যাডমিন বনাম সাধারণ ইউজার ভিউ)
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='text-align:center; color:#004d4d;'>🔍 শিক্ষার্থীর তথ্য অনুসন্ধান</h2>", unsafe_allow_html=True)
    
    # অ্যাডমিন কিনা যাচাই করার জন্য পিন চেক (আগের পিনটাই ব্যবহার করছি)
    is_admin = False
    with st.sidebar:
        st.markdown("---")
        admin_pin = st.text_input("অ্যাডমিন ভিউ আনলক করুন (পিন দিন):", type="password", key="report_pin")
        if admin_pin == "MdmamuN18":
            is_admin = True
            st.success("অ্যাডমিন মোড চালু")

    sid = st.text_input("আইডি (ID) লিখে এন্টার দিন:").strip()
    
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == sid]
        
        if not student.empty:
            s = student.iloc[0]
            
            # রেজাল্ট চেক (এটি সবাই দেখবে)
            st.markdown(f"### শিক্ষার্থীর নাম: {s.get('Name', 'N/A')}")
            st.write(f"**আইডি নম্বর:** {sid}")

            # যদি অ্যাডমিন হয় তবে সব দেখাবে
            if is_admin:
                st.info("🔓 অ্যাডমিন ভিউ: সকল ব্যক্তিগত তথ্য নিচে দেওয়া হলো")
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    photo_url = s.get('Photo', '-')
                    if photo_url and photo_url != "-" and str(photo_url).startswith("http"):
                        st.image(photo_url, width=180)
                    else:
                        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
                
                with col_info:
                    details = {
                        "পিতার নাম": s.get('Father', '-'),
                        "মাতার নাম": s.get('Mother', '-'),
                        "মোবাইল নম্বর": s.get('Mobile', '-'),
                        "জন্ম তারিখ": s.get('DOB', '-'),
                        "ঠিকানা": s.get('Address', '-'),
                        "থানা": s.get('Thana', '-'),
                        "জেলা": s.get('Zella', '-'),
                        "জন্ম সনদ নং": s.get('Birth_Cert', '-')
                    }
                    st.table(pd.DataFrame(details.items(), columns=["গোপনীয় বিষয়", "তথ্য"]))
            else:
                st.warning("🔒 ব্যক্তিগত তথ্য লুকানো আছে। শুধু অ্যাডমিন পিন দিয়ে সব দেখা যাবে।")

            # রেজাল্ট শিট (এটি সবাই দেখবে)
            st.markdown("---")
            st.subheader("📊 পরীক্ষার ফলাফল")
            if df_r is not None:
                res = df_r[df_r.iloc[:, 0].astype(str) == sid]
                if not res.empty:
                    st.table(res.T)
                else:
                    st.write("রেজাল্ট এখনও আপলোড করা হয়নি।")
            
            # উপস্থিতি (এটি সবাই দেখবে)
            all_present = ",".join(df_a[df_a.iloc[:, 0].astype(str).str.contains(today, na=False)].iloc[:, 1].astype(str)).lower()
            if str(s.get('Name', '')).lower() in all_present:
                st.success("✅ আজকে উপস্থিত আছে।")
            else:
                st.error("❌ আজকে অনুপস্থিত।")
        else:
            st.error("দুঃখিত, এই আইডির কোনো ছাত্র পাওয়া যায়নি!")
# ৩. রেজাল্ট শিট
elif menu == "📊 রেজাল্ট শিট":
    st.header("📊 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি (ID) দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0] == rid]
        if not res.empty: st.table(res.T)
        else: st.warning("রেজাল্ট খুঁজে পাওয়া যায়নি।")

# ৪. অ্যাডমিন অ্যাক্সেস (সব তথ্যসহ ভর্তি ফরম)
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("পিন কোড:", type="password") == "MdmamuN18":
        adm_opt = st.selectbox("কি করতে চান?", ["নতুন ভর্তি", "হাজিরা নিন", "নোটিশ আপডেট"])
        
        if adm_opt == "নতুন ভর্তি":
            st.markdown("### 📝 বিস্তারিত ভর্তি ফরম")
            with st.form("admission_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                f_id = c1.text_input("আইডি (ID)*"); f_name = c1.text_input("নাম*")
                f_father = c1.text_input("পিতার নাম"); f_mother = c1.text_input("মাতার নাম")
                f_dob = c1.text_input("জন্ম তারিখ (DD/MM/YYYY)")
                f_mob = c2.text_input("মোবাইল নম্বর"); f_addr = c2.text_input("ঠিকানা")
                f_thana = c2.text_input("থানা"); f_zella = c2.text_input("জেলা")
                f_cert = c2.text_input("জন্ম সনদ নম্বর")
                f_img = st.file_uploader("ছাত্রের ছবি সিলেক্ট করুন")
                
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    if f_id and f_name:
                        pic_url = upload_image(f_img) if f_img else "-"
                        # অ্যাপস স্ক্রিপ্টের লজিক অনুযায়ী ডাটা পাঠানো
                        payload = {
                            "action": "admission", "id": f_id, "name": f_name, "father": f_father,
                            "mother": f_mother, "mobile": f_mob, "address": f_addr, 
                            "thana": f_thana, "zella": f_zella, "dob": f_dob, 
                            "birth_cert": f_cert, "photo": pic_url
                        }
                        try:
                            r = requests.post(SCRIPT_URL, json=payload)
                            if r.status_code == 200: st.success(f"{f_name} এর ভর্তি সফল হয়েছে!")
                            else: st.error("সার্ভারে ডাটা পাঠানো যায়নি।")
                        except: st.error("কানেকশন এরর!")
                    else: st.error("আইডি এবং নাম অবশ্যই দিতে হবে।")

        elif adm_opt == "হাজিরা নিন":
            if df_s is not None:
                selected = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
                if st.button("হাজিরা সেভ"):
                    requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(selected)})
                    st.success("হাজিরা নেওয়া হয়েছে!")

        elif adm_opt == "নোটিশ আপডেট":
            txt = st.text_area("নতুন নোটিশ লিখুন:")
            if st.button("পাবলিশ"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": txt})
                st.success("নোটিশ আপডেট হয়েছে!")
