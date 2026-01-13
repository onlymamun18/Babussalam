import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম ডিজাইন (আপনার দেওয়া ডিজাইন অপরিবর্তিত) ---
st.markdown("""
    <style>
    .stApp { background: #f1f4f9; }
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px; border-radius: 25px; color: white; text-align: center;
        margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border-bottom: 6px solid #f1c40f;
    }
    .big-button {
        display: block; width: 100%; padding: 18px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 20px; font-weight: bold;
        text-decoration: none; border-radius: 15px; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .call-btn { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%); }
    .fb-btn { background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); }
    div[data-baseweb="input"] { border: 2px solid #1e3c72 !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. ডাটা লোড ---
@st.cache_data(ttl=1)
def load_all_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        r_df = pd.read_csv(get_url("Result")).astype(str)
        return s_df, r_df
    except: return None, None

df_s, df_r = load_all_data()

def upload_image(image_file):
    try:
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.getvalue()).decode('utf-8')}
        res = requests.post("https://api.imgbb.com/1/upload", payload)
        return res.json()['data']['url'] if res.status_code == 200 else "-"
    except: return "-"

# --- ৪. নেভিগেশন মেনু ---
menu = st.sidebar.radio("🧭 মেনু নেভিগেশন", ["🏠 হোম ড্যাশবোর্ড", "🔍 প্রোফাইল সার্চ", "📊 দৈনিক হাজিরা", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন প্যানেল"])

# --- হোম ড্যাশবোর্ড ---
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>আপনার সন্তানের উজ্জ্বল ভবিষ্যৎ গড়তে আমরা প্রতিশ্রুতিবদ্ধ</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #11998e; box-shadow: 0 4px 10px rgba(0,0,0,0.05);"><h4 style="color: #1e3c72; margin:0;">ভর্তি বা যেকোনো প্রয়োজনে</h4><a href="tel:01954343364" class="big-button call-btn" style="text-decoration: none;">📱 সরাসরি কল করুন</a></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #0072ff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);"><h4 style="color: #1e3c72; margin:0;">মাদরাসার নিয়মিত আপডেট</h4><a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn" style="text-decoration: none;">🔵 ফেসবুক পেজ ভিজিট করুন</a></div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# --- প্রোফাইল সার্চ (সঠিক সিরিয়াল ফিক্স) ---
elif menu == "🔍 প্রোফাইল সার্চ":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    is_admin = st.sidebar.text_input("অ্যাডমিন পিন:", type="password") == ADMIN_PIN
    sid = st.text_input("আইডি (ID) দিন:").strip()
    
    if sid and df_s is not None:
        # আইডি সার্চ করা হচ্ছে (কলাম ০)
        student = df_s[df_s.iloc[:, 0].str.strip() == sid]
        
        if not student.empty:
            s = student.iloc[0]
            if is_admin:
                st.success("✅ পূর্ণাঙ্গ তথ্য (অ্যাডমিন ভিউ)")
                # আপনার দেওয়া সিরিয়াল অনুযায়ী টেবিল সাজানো
                details = {
                    "বিবরণ": ["আইডি (ID)", "নাম (Name)", "পিতার নাম", "মাতার নাম", "ঠিকানা", "মোবাইল", "থানা", "জেলা", "জন্ম তারিখ", "জন্ম নিবন্ধন", "ছবি"],
                    "তথ্য": [s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10]]
                }
                st.table(pd.DataFrame(details))
                if s[10] != "nan" and s[10] != "-":
                    st.image(s[10], width=150, caption="ছাত্রের ছবি")
            else:
                st.info(f"ছাত্রের নাম: {s[1]} | আইডি: {s[0]}")
        else:
            st.error("দুঃখিত, এই আইডি পাওয়া যায়নি।")
# --- ৫. হাজিরা সেকশন (একদম নির্ভুল ফিক্স) ---
elif menu == "📊 দৈনিক হাজিরা":
    st.header("📊 প্রতিদিনের হাজিরা")
    if df_s is not None:
        with st.form("attendance_form"):
            h_date = st.date_input("তারিখ নির্বাচন করুন", datetime.now())
            st.write("---")
            
            # ডাটা সংগ্রহের লিস্ট
            final_attendance_list = []
            
            for _, row in df_s.iterrows():
                std_id = row.iloc[0]
                std_name = row.iloc[1]
                
                # ড্রপডাউন মেনু প্রতিটি ছাত্রের জন্য
                status = st.selectbox(f"ছাত্র: {std_name} ({std_id})", ["উপস্থিত", "অনুপস্থিত", "ছুটি"], key=f"key_{std_id}")
                
                # গুগল শিটে পাঠানোর জন্য ডাটা ফরম্যাট করা
                final_attendance_list.append({
                    "date": str(h_date),
                    "id": str(std_id),
                    "name": str(std_name),
                    "status": status
                })
            
            submit = st.form_submit_button("✅ হাজিরা সেভ করুন")
            
            if submit:
                with st.spinner('শিটে ডাটা পাঠানো হচ্ছে...'):
                    # গুগল স্ক্রিপ্টে পোস্ট করা
                    response = requests.post(SCRIPT_URL, json={
                        "action": "attendance",
                        "data": final_attendance_list
                    })
                    
                    if response.status_code == 200:
                        st.success(f"আলহামদুলিল্লাহ! {len(final_attendance_list)} জন ছাত্রের হাজিরা সফলভাবে সেভ হয়েছে।")
                    else:
                        st.error("দুঃখিত! গুগল শিটে ডাটা পাঠানো সম্ভব হয়নি। আপনার গুগল স্ক্রিপ্ট চেক করুন।")
    else:
        st.error("ছাত্র তালিকা (Student_List) লোড করা সম্ভব হয়নি। শিট চেক করুন।")

# --- রেজাল্ট ও অ্যাডমিন (অপরিবর্তিত) ---
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].str.strip() == rid]
        if not res.empty: st.table(res.iloc[0])
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.sidebar.text_input("অ্যাডমিন পিন:", type="password") == ADMIN_PIN:
        opt = st.selectbox("কাজ নির্বাচন করুন:", ["নতুন ভর্তি (১১ তথ্য)", "রেজাল্ট এন্ট্রি (১০ বিষয়)", "ছাত্র তালিকা দেখুন", "ডাটা ডিলিট করুন"])
        if opt == "নতুন ভর্তি (১১ তথ্য)":
            with st.form("adm_f"):
                c1, c2 = st.columns(2)
                v1=c1.text_input("আইডি*"); v2=c1.text_input("নাম*"); v3=c1.text_input("পিতা"); v4=c1.text_input("মাতা"); v5=c1.text_input("ঠিকানা")
                v6=c2.text_input("মোবাইল"); v7=c2.text_input("থানা"); v8=c2.text_input("জেলা"); v9=c2.text_input("জন্ম তারিখ"); v10=c2.text_input("জন্ম সনদ"); v11=st.file_uploader("ছবি")
                if st.form_submit_button("ভর্তি সম্পন্ন"):
                    img = upload_image(v11) if v11 else "-"
                    requests.post(SCRIPT_URL, json={"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "address": v5, "mobile": v6, "thana": v7, "zella": v8, "dob": v9, "birth_cert": v10, "photo": img})
                    st.success("ভর্তি সফল!")
        elif opt == "রেজাল্ট এন্ট্রি (১০ বিষয়)":
            with st.form("res_f"):
                rid=st.text_input("ID*"); rname=st.text_input("Name*"); rexam=st.text_input("Exam*")
                r1=st.number_input("আরবি"); r2=st.number_input("বাংলা"); r3=st.number_input("ইংরেজি"); r4=st.number_input("গণিত"); r5=st.number_input("হাদিস")
                r6=st.number_input("কালিমা"); r7=st.number_input("কুরআন"); r8=st.number_input("সমাজ"); r9=st.number_input("বিজ্ঞান"); r10=st.number_input("সাধারণ জ্ঞান")
                if st.form_submit_button("রেজাল্ট সেভ"):
                    total = r1+r2+r3+r4+r5+r6+r7+r8+r9+r10
                    requests.post(SCRIPT_URL, json={"action": "add_result", "id": rid, "name": rname, "exam": rexam, "total": total})
                    st.success("সেভ হয়েছে!")
        elif opt == "ছাত্র তালিকা দেখুন":
            if df_s is not None: st.dataframe(df_s)
        elif opt == "ডাটা ডিলিট করুন":
            did = st.text_input("আইডি:")
            if st.button("ডিলিট"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": did})
                st.success("ডিলিট সম্পন্ন!")
    else: st.warning("পিন দিয়ে প্যানেল আনলক করুন।")
