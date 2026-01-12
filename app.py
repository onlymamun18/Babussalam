import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import base64

# --- কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbziNe1yiHbRtNZYuDbdY3ZGfbEw1UaigJrWCPexdc1JzKHVDPALHWlgSy4B1Gyd_l7d/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ডিজাইন (সেই আগের প্রিয় লুক) ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f6; }
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
    .notice-box {
        background: #FF512F; color: white; padding: 20px; border-radius: 15px;
        text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 25px;
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

def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট প্রোফাইল", "📊 হাজিরা রিপোর্ট", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম সেকশন (বড় বাটনসহ)
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>যেকোনো প্রয়োজনে আমাদের সাথে যোগাযোগ করুন</h3>", unsafe_allow_html=True)
    st.markdown('<a href="tel:01954343364" class="big-button call-btn">📞 সরাসরি কল করুন (01954343364)</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.facebook.com/share/18Y28D9gKj/" target="_blank" class="big-button fb-btn">🔵 ফেসবুক পেজে যুক্ত হোন</a>', unsafe_allow_html=True)
    
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# ২. স্টুডেন্ট প্রোফাইল (সব তথ্য দেখার জন্য)
elif menu == "🔍 স্টুডেন্ট প্রোফাইল":
    st.header("🔍 শিক্ষার্থীর পূর্ণাঙ্গ তথ্য")
    sid = st.text_input("আইডি (ID) নম্বর দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"নাম: {s['Name']}")
            st.table(pd.DataFrame(s.items(), columns=["বিষয়", "তথ্য"]))
            
            # মোট উপস্থিতি গণনা
            if df_a is not None:
                count = sum(1 for _, row in df_a.iterrows() if str(s['Name']).lower() in str(row.iloc[1]).lower())
                st.info(f"📊 এই পর্যন্ত মোট উপস্থিতি: {count} দিন")
        else: st.error("এই আইডির কোনো শিক্ষার্থী পাওয়া যায়নি।")

# ৩. হাজিরা রিপোর্ট (সবার লিস্ট)
elif menu == "📊 হাজিরা রিপোর্ট":
    st.header("📊 শিক্ষার্থীদের মোট উপস্থিতি তালিকা")
    if df_s is not None and df_a is not None:
        rep_list = []
        for _, row in df_s.iterrows():
            name = row['Name']
            count = sum(1 for _, r in df_a.iterrows() if str(name).lower() in str(r.iloc[1]).lower())
            rep_list.append({"আইডি": row.iloc[0], "নাম": name, "মোট উপস্থিতি": f"{count} দিন"})
        st.dataframe(pd.DataFrame(rep_list), use_container_width=True)

# ৪. রেজাল্ট শিট
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("ফলাফল দেখতে আইডি (ID) নম্বর দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].astype(str) == rid]
        if not res.empty: st.table(res.T)
        else: st.warning("ফলাফল পাওয়া যায়নি।")

# ৫. অ্যাডমিন অ্যাক্সেস (সবকিছু এখান থেকে কন্ট্রোল হবে)
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("অ্যাডমিন পিন দিন:", type="password") == "MdmamuN18":
        opt = st.selectbox("কাজ নির্বাচন করুন", ["মাদরাসার ছাত্র তালিকা", "নতুন ভর্তি (১১টি তথ্য)", "হাজিরা নিন", "ছাত্র ডিলিট", "নোটিশ আপডেট"])
        
        if opt == "মাদরাসার ছাত্র তালিকা":
            st.subheader("📋 সকল শিক্ষার্থীর লিস্ট")
            st.dataframe(df_s, use_container_width=True)

        elif opt == "নতুন ভর্তি (১১টি তথ্য)":
            st.subheader("📝 নতুন শিক্ষার্থীর ভর্তির ফরম")
            with st.form("adm_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                v1=c1.text_input("আইডি*"); v2=c1.text_input("নাম*")
                v3=c1.text_input("পিতার নাম"); v4=c1.text_input("মাতার নাম")
                v5=c1.text_input("জন্ম তারিখ (DD/MM/YYYY)")
                v6=c2.text_input("মোবাইল নম্বর"); v7=c2.text_input("ঠিকানা")
                v8=c2.text_input("থানা"); v9=c2.text_input("জেলা")
                v10=c2.text_input("জন্ম সনদ নং"); v11=st.file_uploader("ছাত্রের ছবি")
                
                if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                    img = upload_image(v11) if v11 else "-"
                    p = {"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "mobile": v6, "address": v7, "thana": v8, "zella": v9, "dob": v5, "birth_cert": v10, "photo": img}
                    requests.post(SCRIPT_URL, json=p)
                    st.success("ভর্তি সম্পন্ন হয়েছে!")

        elif opt == "হাজিরা নিন":
            st.subheader("📝 আজকের হাজিরা জমা দিন")
            sel = st.multiselect("উপস্থিত ছাত্র সিলেক্ট করুন:", df_s['Name'].tolist())
            if st.button("হাজিরা সেভ করুন"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                st.success("হাজিরা সফলভাবে জমা হয়েছে!")

        elif opt == "ছাত্র ডিলিট":
            del_id = st.text_input("যে আইডিটি বাদ দিতে চান:")
            if st.button("ডিলিট করুন"):
                requests.post(SCRIPT_URL, json={"action": "delete", "id": del_id})
                st.warning(f"আইডি {del_id} মুছে ফেলা হয়েছে।")

        elif opt == "নোটিশ আপডেট":
            txt = st.text_area("নতুন নোটিশ লিখুন:")
            if st.button("পাবলিশ করুন"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": txt})
                st.success("নোটিশ আপডেট হয়েছে!")
