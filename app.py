import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# অ্যাপের প্রাথমিক সেটিংস
st.set_page_config(page_title="বাবুস সালাম ডিজিটাল ক্যাম্পাস", page_icon="🕌", layout="wide")

# প্রফেশনাল ড্যাশবোর্ড ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    .main-header { text-align: center; color: #008080; padding: 20px; font-size: 35px; font-weight: bold; }
    .notice-box { background: #fffbeb; padding: 20px; border-radius: 12px; border-left: 10px solid #f59e0b; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 25px; }
    .profile-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-top: 8px solid #008080; }
    .info-badge { background: #f8fafc; padding: 10px 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #e2e8f0; font-size: 16px; color: #1e293b; }
    .stButton>button { background: linear-gradient(90deg, #008080 0%, #006666 100%); color: white; height: 50px; border-radius: 12px; font-size: 18px; font-weight: 600; border: none; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,128,128,0.3); }
    .teacher-card { background: white; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #e2e8f0; transition: 0.3s; }
    .teacher-card:hover { border-color: #008080; }
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

# --- নেভিগেশন সাইডবার ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🕌 ড্যাশবোর্ড</h2>", unsafe_allow_html=True)
    menu = st.selectbox("মেনু নির্বাচন করুন:", ["🏠 হোম ও নোটিশ বোর্ড", "🔍 স্টুডেন্ট প্রোফাইল ও রিপোর্ট", "👨‍🏫 শিক্ষক ও স্টাফ গ্যালারি", "🔐 অ্যাডমিন প্যানেল"])
    st.markdown("---")
    st.info("মাদরাসা ম্যানেজমেন্ট সফটওয়্যার v2.0")

# ১. হোম ও নোটিশ বোর্ড
if menu == "🏠 হোম ও নোটিশ বোর্ড":
    st.markdown("<div class='main-header'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    
    # অ্যাডভান্সড নোটিশ বোর্ড
    df_notice = load_data("Notice")
    if df_notice is not None and not df_notice.empty:
        latest_msg = df_notice.iloc[-1]['Message']
        st.markdown(f"<div class='notice-box'>🔔 <b>সর্বশেষ নোটিশ:</b><br>{latest_msg}</div>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1592288333291-70083b2744a5?q=80&w=2000", use_container_width=True)

# ২. স্টুডেন্ট প্রোফাইল (সব তথ্য এক পাতায়)
elif menu == "🔍 স্টুডেন্ট প্রোফাইল ও রিপোর্ট":
    st.markdown("<h2 style='text-align: center; color: #008080;'>🔍 স্টুডেন্ট রিপোর্ট কার্ড</h2>", unsafe_allow_html=True)
    sid = st.text_input("ছাত্রের আইডি (ID) লিখুন এবং এন্টার চাপুন:", placeholder="যেমন: 10001")
    
    if sid:
        df_students = load_data("Student_List")
        df_att = load_data("Form_Responses_1")
        df_res = load_data("Result_Sheet")
        
        if df_students is not None:
            student = df_students[df_students['ID'].astype(str) == str(sid)]
            
            if not student.empty:
                s = student.iloc[0]
                st.balloons()
                
                # লেআউট: ছবি ও বায়োডাটা
                c1, c2 = st.columns([1, 2])
                with c1:
                    photo_url = s.get('Photo_URL')
                    avatar = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                    try:
                        st.image(str(photo_url) if not pd.isna(photo_url) else avatar, use_container_width=True, caption=f"ID: {sid}")
                    except:
                        st.image(avatar, use_container_width=True)
                
                with c2:
                    st.markdown(f"""
                    <div class='profile-card'>
                        <h2 style='color: #008080; margin-top:0;'>👤 {s.get('Name', 'N/A')}</h2>
                        <div class='info-badge'><b>👨‍💼 পিতার নাম:</b> {s.get('Father_Name', 'N/A')}</div>
                        <div class='info-badge'><b>📞 মোবাইল:</b> {s.get('Mobile', 'N/A')}</div>
                        <div class='info-badge'><b>📍 ঠিকানা:</b> {s.get('Address', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ট্যাব সিস্টেম: হাজিরা ও রেজাল্ট
                st.write("---")
                tab_a, tab_r = st.tabs(["📅 বার্ষিক হাজিরা রিপোর্ট", "🎓 পরীক্ষার রেজাল্ট কার্ড"])
                
                with tab_a:
                    if df_att is not None:
                        # আপনার আইডি কলামের নাম যাই হোক (Untitled বা আইডি) সেটি খুঁজে বের করবে
                        id_col = [c for c in df_att.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                        if id_col:
                            att_res = df_att[df_att[id_col[0]].astype(str) == str(sid)]
                            if not att_res.empty:
                                st.dataframe(att_res, use_container_width=True)
                            else: st.warning("হাজিরার কোনো তথ্য পাওয়া যায়নি।")
                
                with tab_r:
                    if df_res is not None:
                        res_match = df_res[df_res['ID'].astype(str) == str(sid)]
                        if not res_match.empty:
                            st.table(res_match.drop(columns=['ID']))
                        else: st.warning("রেজাল্ট এখনো আপলোড হয়নি।")
            else:
                st.error("দুঃখিত, এই আইডি-র কোনো ছাত্রের প্রোফাইল খুঁজে পাওয়া যায়নি।")

# ৩. শিক্ষক গ্যালারি
elif menu == "👨‍🏫 শিক্ষক ও স্টাফ গ্যালারি":
    st.markdown("<h2 style='text-align: center; color: #008080;'>👨‍🏫 আমাদের শ্রদ্ধাভাজন শিক্ষকবৃন্দ</h2>", unsafe_allow_html=True)
    df_t = load_data("Teacher_List")
    if df_t is not None:
        grid = st.columns(3)
        for i, row in df_t.iterrows():
            with grid[i % 3]:
                st.markdown(f"""
                <div class='teacher-card'>
                    <h3 style='margin-bottom:5px;'>{row.get('Name')}</h3>
                    <p style='color: #008080; font-weight: bold;'>{row.get('Designation')}</p>
                    <p style='color: #64748b;'>📞 {row.get('Mobile')}</p>
                </div>
                """, unsafe_allow_html=True)

# ৪. অ্যাডমিন প্যানেল
elif menu == "🔐 অ্যাডমিন প্যানেল":
    st.markdown("<h2 style='text-align: center;'>🔐 অ্যাডমিন এক্সেস</h2>", unsafe_allow_html=True)
    pw = st.text_input("সিকিউরিটি পাসওয়ার্ড দিন:", type="password")
    if pw == "admin123":
        st.success("লগইন সফল! নিচে থেকে আপনার কার্যক্রম পরিচালনা করুন।")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
        with col_f2:
            st.info("টিপস: রেজাল্ট বা নতুন ছাত্র যোগ করতে সরাসরি গুগল শিট ব্যবহার করুন।")
