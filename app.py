import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# অ্যাপের কনফিগারেশন
st.set_page_config(page_title="বাবুস সালাম ডিজিটাল একাডেমি", page_icon="🕌", layout="wide")

# কাস্টম ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .notice-card { background: #fff3cd; padding: 20px; border-radius: 12px; border-left: 8px solid #ffc107; color: #856404; font-size: 18px; font-weight: bold; margin-bottom: 25px; }
    .profile-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-top: 6px solid #008080; }
    .info-box { background: #f8fafc; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #008080; }
    .stButton>button { background: #008080 !important; color: white !important; font-weight: bold; border-radius: 10px; height: 45px; width: 100%; }
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

# --- মেনুবার ---
menu = st.sidebar.radio("মেনু নির্বাচন করুন:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল ও রিপোর্ট", "👨‍🏫 শিক্ষক তালিকা", "🔐 অ্যাডমিন"])

# ১. হোম পেজ (ব্যানারসহ)
if menu == "🏠 হোম পেজ":
    # ব্যানার লোড করার শক্তিশালী পদ্ধতি
    banner_url = "https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg"
    try:
        st.image(banner_url, use_container_width=True)
    except:
        st.warning("ব্যানার লোড করা যাচ্ছে না, তবে অ্যাপ চলবে।")
    
    st.markdown("<h2 style='text-align: center; color: #008080;'>🕌 ডিজিটাল ম্যানেজমেন্ট সিস্টেমে স্বাগতম</h2>", unsafe_allow_html=True)
    
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        msg = df_n.iloc[-1]['Message']
        st.markdown(f"<div class='notice-card'>📢 নোটিশ: {msg}</div>", unsafe_allow_html=True)

# ২. ছাত্র প্রোফাইল (ছবির এরর ফিক্স করা হয়েছে)
elif menu == "🔍 ছাত্র প্রোফাইল ও রিপোর্ট":
    st.header("🔍 স্টুডেন্ট রিপোর্ট কার্ড")
    sid = st.text_input("ছাত্রের আইডি (ID) লিখুন:", placeholder="যেমন: 10001")
    
    if sid:
        df_s = load_data("Student_List")
        df_a = load_data("Form_Responses_1")
        df_r = load_data("Result_Sheet")
        
        if df_s is not None:
            sid_col = [c for c in df_s.columns if 'ID' in c.upper() or 'আইডি' in c]
            if sid_col:
                student = df_s[df_s[sid_col[0]].astype(str) == str(sid)]
                
                if not student.empty:
                    s = student.iloc[0]
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # ছবির এরর হ্যান্ডেলিং - এটিই আপনার এরর সমাধান করবে
                        photo_url = s.get('Photo_URL')
                        default_avatar = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        
                        try:
                            # যদি ফটো ইউআরএল খালি থাকে বা নাল হয়
                            if pd.isna(photo_url) or str(photo_url).strip() == "" or "http" not in str(photo_url):
                                st.image(default_avatar, width=230, caption="ছবি পাওয়া যায়নি")
                            else:
                                st.image(str(photo_url), width=230, caption=f"ID: {sid}")
                        except:
                            st.image(default_avatar, width=230, caption="ভুল লিঙ্ক")
                    
                    with col2:
                        st.markdown(f"""
                        <div class='profile-card'>
                            <h2 style='color:#008080;'>👤 {s.get('Name', s.get('নাম', 'N/A'))}</h2>
                            <div class='info-box'><b>👨‍💼 পিতার নাম:</b> {s.get('Father_Name', 'N/A')}</div>
                            <div class='info-box'><b>📞 মোবাইল:</b> {s.get('Mobile', 'N/A')}</div>
                            <div class='info-box'><b>📍 ঠিকানা:</b> {s.get('Address', 'N/A')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # হাজিরা ও রেজাল্ট সেকশন
                    st.write("---")
                    tab1, tab2 = st.tabs(["📅 হাজিরার রিপোর্ট", "🎓 রেজাল্ট"])
                    
                    with tab1:
                        if df_a is not None:
                            id_col_a = [c for c in df_a.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                            status_col = [c for c in df_a.columns if 'অবস্থা' in c or 'Status' in c]
                            if id_col_a and status_col:
                                user_att = df_a[df_a[id_col_a[0]].astype(str) == str(sid)]
                                if not user_att.empty:
                                    st.dataframe(user_att[['Timestamp', status_col[0]]], use_container_width=True)
                    
                    with tab2:
                        if df_r is not None:
                            id_col_r = [c for c in df_r.columns if 'ID' in c.upper() or 'আইডি' in c]
                            if id_col_r:
                                user_res = df_r[df_r[id_col_r[0]].astype(str) == str(sid)]
                                if not user_res.empty:
                                    st.table(user_res.drop(columns=[id_col_r[0]]))
                else: st.error("দুঃখিত, এই আইডি-র কোনো ছাত্র পাওয়া যায়নি।")

# ৩. শিক্ষক তালিকা ও ৪. অ্যাডমিন (আগের মতোই থাকবে)
elif menu == "👨‍🏫 শিক্ষক তালিকা":
    st.header("👨‍🏫 আমাদের শিক্ষকবৃন্দ")
    df_t = load_data("Teacher_List")
    if df_t is not None: st.dataframe(df_t, use_container_width=True)

elif menu == "🔐 অ্যাডমিন":
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        st.success("লগইন সফল")
        st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
