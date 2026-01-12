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
        font-size: 22px; font-weight: bold; margin-bottom: 25px;
        border: 4px solid #fff; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
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

# --- লজিক ফাংশনস ---
def get_present_list():
    if df_a is None or df_a.empty: return []
    now = datetime.now()
    t_str = f"{now.month}/{now.day}/{now.year}"
    present_names = []
    for _, row in df_a.iterrows():
        if t_str in str(row.iloc[0]):
            names = str(row.iloc[1]).split(',')
            present_names.extend([n.strip().lower() for n in names])
    return list(set(present_names))

def upload_image(image_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(image_file.read()).decode('utf-8')}
        res = requests.post(url, payload)
        return res.json()['data']['url']
    except: return "-"

# --- মেনু ---
menu = st.sidebar.radio("মেইন মেনু", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট প্রোফাইল", "📊 হাজিরা রিপোর্ট", "📝 রেজাল্ট শিট", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<div class='main-header'><h1>🕌 বাবুস সালাম একাডেমি</h1><p>স্মার্ট ডিজিটাল ক্যাম্পাস</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='notice-box'>📢 নোটিশ: {latest_notice}</div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)

# ২. স্টুডেন্ট প্রোফাইল
elif menu == "🔍 স্টুডেন্ট প্রোফাইল":
    st.header("🔍 শিক্ষার্থীর তথ্য অনুসন্ধান")
    is_admin = st.sidebar.text_input("অ্যাডমিন পিন (বিস্তারিত তথ্য দেখতে):", type="password", key="p_pin") == "MdmamuN18"
    sid = st.text_input("আইডি (ID) দিন:").strip()
    if sid and df_s is not None:
        student = df_s[df_s.iloc[:, 0].astype(str) == sid]
        if not student.empty:
            s = student.iloc[0]
            st.subheader(f"নাম: {s['Name']}")
            present_today = get_present_list()
            if s['Name'].lower() in present_today: st.success("✅ আজকে উপস্থিত")
            else: st.error("❌ আজকে অনুপস্থিত")
            
            if is_admin: st.table(pd.DataFrame(s.items(), columns=["বিষয়", "তথ্য"]))
            else: st.info("বিস্তারিত তথ্য দেখতে অ্যাডমিন পিন দিয়ে সাইডবার থেকে লগইন করুন।")
        else: st.error("আইডি পাওয়া যায়নি।")

# ৩. হাজিরা রিপোর্ট
elif menu == "📊 হাজিরা রিপোর্ট":
    st.header("📊 উপস্থিতি সারাংশ")
    if df_s is not None and df_a is not None:
        rep = []
        for _, row in df_s.iterrows():
            count = sum(1 for _, r in df_a.iterrows() if str(row['Name']).lower() in str(r.iloc[1]).lower())
            rep.append({"আইডি": row.iloc[0], "নাম": row['Name'], "মোট উপস্থিতি": f"{count} দিন"})
        st.dataframe(pd.DataFrame(rep), use_container_width=True)

# ৪. রেজাল্ট
elif menu == "📝 রেজাল্ট শিট":
    st.header("📝 পরীক্ষার ফলাফল")
    rid = st.text_input("আইডি দিন:").strip()
    if rid and df_r is not None:
        res = df_r[df_r.iloc[:, 0].astype(str) == rid]
        if not res.empty: st.table(res.T)
        else: st.warning("রেজাল্ট পাওয়া যায়নি।")

# ৫. অ্যাডমিন অ্যাক্সেস
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    if st.text_input("মাস্টার পিন দিন:", type="password", key="adm_master") == "MdmamuN18":
        opt = st.selectbox("কাজ নির্বাচন করুন", ["মাদরাসার ছাত্র তালিকা (All Students)", "হাজিরা নিন", "ছাত্র ব্যবস্থাপনা (ভর্তি/এডিট/ডিলিট)", "নোটিশ আপডেট"])
        
        # --- নতুন: সব ছাত্রের তালিকা দেখার অংশ ---
        if opt == "মাদরাসার ছাত্র তালিকা (All Students)":
            st.subheader("📋 সকল ছাত্রছাত্রীর তালিকা")
            if df_s is not None:
                st.write(f"মোট ছাত্র সংখ্যা: {len(df_s)}")
                st.dataframe(df_s, use_container_width=True)
            else:
                st.error("ছাত্র তালিকা লোড করা সম্ভব হয়নি।")

        # হাজিরা
        elif opt == "হাজিরা নিন":
            st.subheader("📝 হাজিরা ফর্ম")
            p_list = get_present_list()
            rem = [n for n in df_s['Name'].tolist() if n.lower() not in p_list]
            sel = st.multiselect("নাম সিলেক্ট করুন:", rem)
            if st.button("হাজিরা সেভ"):
                requests.post(SCRIPT_URL, json={"action": "attendance", "names": ", ".join(sel)})
                st.success("জমা হয়েছে!")
                st.rerun()

        # ছাত্র ব্যবস্থাপনা
        elif opt == "ছাত্র ব্যবস্থাপনা (ভর্তি/এডিট/ডিলিট)":
            sub_opt = st.radio("কি করতে চান?", ["নতুন ভর্তি (Add)", "তথ্য সংশোধন (Edit)", "ছাত্র বাদ দিন (Delete)"])
            
            if sub_opt == "নতুন ভর্তি (Add)":
                with st.form("add_form"):
                    c1, c2 = st.columns(2)
                    v1=c1.text_input("ID*"); v2=c1.text_input("Name*"); v3=c1.text_input("Father"); v4=c1.text_input("Mother")
                    v6=c2.text_input("Mobile"); v7=c2.text_input("Address"); v11=st.file_uploader("Photo")
                    if st.form_submit_button("ভর্তি নিশ্চিত করুন"):
                        img = upload_image(v11) if v11 else "-"
                        requests.post(SCRIPT_URL, json={"action": "admission", "id": v1, "name": v2, "father": v3, "mother": v4, "mobile": v6, "address": v7, "photo": img})
                        st.success("ভর্তি সফল!")

            elif sub_opt == "তথ্য সংশোধন (Edit)":
                target_id = st.selectbox("সংশোধন করতে আইডি বেছে নিন:", df_s.iloc[:, 0].tolist())
                student_data = df_s[df_s.iloc[:, 0] == target_id].iloc[0]
                with st.form("edit_form"):
                    new_name = st.text_input("নাম", value=student_data['Name'])
                    new_mob = st.text_input("মোবাইল", value=student_data.get('Mobile', ''))
                    if st.form_submit_button("তথ্য আপডেট করুন"):
                        requests.post(SCRIPT_URL, json={"action": "edit", "id": target_id, "name": new_name, "mobile": new_mob})
                        st.success("তথ্য সংশোধিত হয়েছে!")

            elif sub_opt == "ছাত্র বাদ দিন (Delete)":
                del_id = st.selectbox("বাদ দিতে আইডি বেছে নিন:", df_s.iloc[:, 0].tolist())
                if st.button("ছাত্র ডিলিট করুন", type="primary"):
                    requests.post(SCRIPT_URL, json={"action": "delete", "id": del_id})
                    st.warning(f"আইডি {del_id} ডিলিট করা হয়েছে।")
                    st.rerun()

        elif opt == "নোটিশ আপডেট":
            txt = st.text_area("নতুন নোটিশ:")
            if st.button("পাবলিশ"):
                requests.post(SCRIPT_URL, json={"action": "save_notice", "text": txt})
                st.success("নোটিশ আপডেট হয়েছে!")
