import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
# আপনার দেওয়া সঠিক স্ক্রিপ্ট ইউআরএল
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ডিজাইন (সার্চ বক্স এবং বাটন সুন্দর করা) ---
st.markdown("""
    <style>
    .stApp { background: #f4f7f6; }
    .main-header {
        background: linear-gradient(135deg, #004d4d 0%, #008080 100%);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    .big-button {
        display: block; width: 100%; padding: 20px; margin: 10px 0px;
        text-align: center; color: white !important; font-size: 22px; font-weight: bold;
        text-decoration: none; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .fb-btn { background: linear-gradient(90deg, #1877F2 0%, #0056b3 100%); }
    .call-btn { background: linear-gradient(90deg, #28a745 0%, #1e7e34 100%); }
    
    /* সার্চ বক্স সুন্দর করার জন্য */
    div[data-baseweb="input"] {
        border: 2px solid #008080 !important;
        border-radius: 12px !important;
    }
    .stTextInput label { font-size: 18px !important; color: #004d4d !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ডাটা লোড ---
@st.cache_data(ttl=0)
def load_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        s_df.iloc[:, 0] = s_df.iloc[:, 0].str.strip() # আইডি ক্লিন করা
        
        a_df = pd.read_csv(get_url("Form_Responses_1")).astype(str)
        
        try:
            n_df = pd.read_csv(get_url("Notice"))
            notice = n_df.columns[0] if not n_df.empty else "কোনো নোটিশ নেই"
        except: notice = "কোনো নোটিশ নেই"
        
        try: 
            r_df = pd.read_csv(get_url("Result")).astype(str)
            r_df.iloc[:, 0] = r_df.iloc[:, 0].str.strip()
        except: r_df = None
            
        return s_df, a_df, notice, r_df
    except: return None, None, "লোডিং...", None

df_s, df_a, latest_notice, df_r = load_data()

# ইমেজ আপলোড ফাংশন
def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট প্রোফাইল", "📊 হাজিরা রিপোর্ট", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম সেকশন
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background: #FF512F; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px;'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #004d4d;'>যেকোনো প্রয়োজনে আমাদের সাথে যোগাযোগ করুন</h3>", unsafe_allow_html=True)
    st.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 সরাসরি কল করুন (01954343364)</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 আমাদের ফেসবুক পেজ (ক্লিক করুন)</a>', unsafe_allow_html=True)
    
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# ২. প্রোফাইল (আইডি দিয়ে সার্চ)
elif menu == "🔍 স্টুডেন্ট প্রোফাইল":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    sid = st.text_input("সঠিক আইডি (ID) নম্বরটি লিখুন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0] == sid]
        if not student.empty:
            s = student.iloc[0]
            st.success(f"ছাত্রের নাম: {s['Name']}")
            st.markdown("### 📋 শিক্ষার্থীর সব তথ্য:")
            st.table(pd.DataFrame(s.items(), columns=["বিষয়", "তথ্য"]))
        else:
            st.error("দুঃখিত! এই আইডি দিয়ে কোনো ছাত্র খুঁজে পাওয়া যায়নি।")

# ৩. হাজিরা রিপোর্ট
elif menu == "📊 হাজিরা রিপোর্ট":
    st.header("📊 শিক্ষার্থীদের উপস্থিতি রিপোর্ট")
    if df_s is not None and df_a is not None:
        rep = []
        for _, row in df_s.iterrows():
            name = row['Name']
            count = sum(1 for _, r in df_a.iterrows() if str(name).lower() in str(r.iloc[1]).lower())
            rep.append({"আইডি": row.iloc[0], "নাম": name, "মোট উপস্থিতি": f"{count} দিন"})
        st.dataframe(pd.DataFrame(rep), use_container_width=True)

# ৪. রেজাল্ট
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("রেজাল্ট দেখতে আইডি (ID) দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0] == rid]
        if not res.empty:
            st.table(res.T)
        else: st.warning("ফলাফল পাওয়া যায়নি।")

# ৫. অ্যাডমিন অ্যাক্সেস (ডিলিট এবং ১১ তথ্যসহ ভর্তি)
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন দিন:", type="password") == "MdmamuN18":
        opt = st.selectbox("কি করতে চান সিলেক্ট করুন:", ["ছাত্র তালিকা", "নতুন ভর্তি (১১টি তথ্য)", "হাজিরা নিন", "ছাত্র ডিলিট করুন ❌", "নোটিশ আপডেট"])
        
        if opt == "ছাত্র তালিকা":
            st.subheader("📋 সকল ছাত্রছাত্রীর লিস্ট")
            st.dataframe(df_s, use_container_width=True)

        elif opt == "নতুন ভর্তি (১১টি তথ্য)":
            st.subheader("📝 নতুন শিক্ষার্থীর ভর্তির ফরম")
            with st.form("adm_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1=c1.text_input("ছাত্রের আইডি*"); v2=c1.text_input("ছাত্রের নাম*")
                v3=c1.text_input("পিতার নাম"); v4=c1.text_input("মাতার নাম")
                v5=c1.text_input("জন্ম তারিখ"); v6=c2.text_input("মোবাইল নম্বর")
                v7=c2.text_input("ঠিকানা"); v8=c2.text_input("থানা")
                v9=c2.text_input("জেলা"); v10=c2.text_input("জন্ম সনদ নং")
                v11=st.file_uploader("ছাত্রের ছবি")
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    img = upload_image(v11) if v11 else "-"
                    payload = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "mobile": v6, "address": v7, "thana": v8, "zella": v9, "dob": v5, "birth_cert": v10, "photo": img}
                    requests.post(SCRIPT_URL, json=payload)
                    st.success("ভর্তি সফল হয়েছে!")

        elif opt == "ছাত্র ডিলিট করুন ❌":
            st.subheader("🗑️ ছাত্র বাদ দিন")
            del_id = st.text_input("যে আইডিটি ডিলিট করতে চান সেটি লিখুন:").strip()
            if st.button("ডিলিট নিশ্চিত করুন", type="primary"):
                if del_id:
                    res = requests.post(SCRIPT_URL, json={"action": "delete", "id": del_id})
                    st.warning(f"আইডি {del_id} মুছে ফেলা হয়েছে। একবার রিফ্রেশ দিন।")
                else:
                    st.error("দয়া করে একটি আইডি নম্বর লিখুন।")

        elif opt == "হাজিরা নিন":
            st.subheader("📝 আজকের হাজিরা")
            sel = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
            if st.button("হাজিরা সেভ"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                st.success("হাজিরা জমা হয়েছে!")
