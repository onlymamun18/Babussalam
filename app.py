import streamlit as st
import pandas as pd
import requests

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .madrasa-name { text-align: center; color: #008080; font-size: 38px; font-weight: bold; margin-bottom: 5px; }
    .notice-card { background: #fff8e1; padding: 15px; border-radius: 10px; border-left: 8px solid #ffa000; margin-bottom: 20px; }
    .stButton>button { background-color: #008080 !important; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# ছবির এরর হ্যান্ডেল করার ফাংশন
def safe_image(url, width=230):
    default_avatar = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    try:
        if pd.isna(url) or str(url).strip() == "" or not str(url).startswith("http"):
            st.image(default_avatar, width=width)
        else:
            st.image(url, width=width)
    except:
        st.image(default_avatar, width=width)

# --- মেনুবার ---
menu = st.sidebar.radio("মেনু:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল", "➕ নতুন ছাত্র যোগ করুন", "👨‍🏫 শিক্ষক তালিকা", "🔐 অ্যাডমিন"])

# ১. হোম পেজ
if menu == "🏠 হোম পেজ":
    st.markdown("<div class='madrasa-name'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    banner_url = "https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg"
    try: st.image(banner_url, use_container_width=True)
    except: st.info("স্বাগতম!")
    
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        st.markdown(f"<div class='notice-card'>📢 নোটিশ: {df_n.iloc[-1]['Message']}</div>", unsafe_allow_html=True)

# ২. ছাত্র প্রোফাইল
elif menu == "🔍 ছাত্র প্রোফাইল":
    sid = st.text_input("ছাত্রের আইডি লিখুন:")
    if sid:
        df_s = load_data("Student_List")
        df_a = load_data("Form_Responses_1")
        df_r = load_data("Result_Sheet")
        
        if df_s is not None:
            id_col = [c for c in df_s.columns if 'ID' in c.upper() or 'আইডি' in c]
            if id_col:
                student = df_s[df_s[id_col[0]].astype(str) == str(sid)]
                if not student.empty:
                    s = student.iloc[0]
                    col1, col2 = st.columns([1, 2])
                    with col1: safe_image(s.get('Photo_URL'))
                    with col2:
                        st.subheader(f"👤 {s.get('Name', s.get('নাম', 'N/A'))}")
                        st.write(f"পিতার নাম: {s.get('Father_Name', 'N/A')}")
                        st.write(f"মোবাইল: {s.get('Mobile', 'N/A')}")
                    
                    st.write("---")
                    t1, t2 = st.tabs(["📅 হাজিরা", "🎓 রেজাল্ট"])
                    with t1:
                        if df_a is not None:
                            id_a = [c for c in df_a.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                            if id_a:
                                u_att = df_a[df_a[id_a[0]].astype(str) == str(sid)]
                                st.dataframe(u_att, use_container_width=True)
                    with t2:
                        if df_r is not None:
                            id_r = [c for c in df_r.columns if 'ID' in c.upper() or 'আইডি' in c]
                            if id_r:
                                u_res = df_r[df_r[id_r[0]].astype(str) == str(sid)]
                                st.table(u_res.drop(columns=[id_r[0]]))

# ৩. নতুন ছাত্র যোগ করুন (এই ফিচারটি আপনি চাচ্ছিলেন)
elif menu == "➕ নতুন ছাত্র যোগ করুন":
    st.header("➕ নতুন ছাত্রের তথ্য জমা দিন")
    st.info("নিচের তথ্যগুলো পূরণ করে সাবমিট করুন। এটি সরাসরি আপনার ডাটাবেসে জমা হবে।")
    
    # এটি আপনার ছাত্র যোগ করার ফর্ম লিঙ্কের সাথে কানেক্ট করা
    google_form_add_student = "https://docs.google.com/forms/d/e/YOUR_STUDENT_ADD_FORM_ID/viewform" 
    
    st.markdown(f"""
        <iframe src="{google_form_add_student}" width="100%" height="800" frameborder="0" marginheight="0" marginwidth="0">লোড হচ্ছে...</iframe>
    """, unsafe_allow_html=True)

# ৪. শিক্ষক তালিকা
elif menu == "👨‍🏫 শিক্ষক তালিকা":
    df_t = load_data("Teacher_List")
    if df_t is not None: st.dataframe(df_t, use_container_width=True)

# ৫. অ্যাডমিন (হাজিরা ফর্ম)
elif menu == "🔐 অ্যাডমিন":
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button>📝 হাজিরা নিন</button></a>', unsafe_allow_html=True)
        
