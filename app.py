import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন কনফিগারেশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# অ্যাপ সেটিংস
st.set_page_config(page_title="বাবুস সালাম ডিজিটাল ক্যাম্পাস", page_icon="🕌", layout="wide")

# প্রফেশনাল ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    .main-header { text-align: center; color: #008080; padding: 20px; font-size: 35px; font-weight: bold; }
    .notice-box { background: #fffbeb; padding: 20px; border-radius: 12px; border-left: 10px solid #f59e0b; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 25px; color: #856404; }
    .profile-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-top: 8px solid #008080; }
    .info-badge { background: #f8fafc; padding: 10px 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #e2e8f0; font-size: 16px; color: #1e293b; }
    .stButton>button { background: linear-gradient(90deg, #008080 0%, #006666 100%); color: white; height: 50px; border-radius: 12px; font-size: 18px; font-weight: 600; border: none; }
    .teacher-card { background: white; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip() # কলামের বাড়তি স্পেস মুছে ফেলা
        return df
    except Exception as e:
        return None

# --- নেভিগেশন সাইডবার ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🕌 ড্যাশবোর্ড</h2>", unsafe_allow_html=True)
    menu = st.selectbox("মেনু নির্বাচন করুন:", ["🏠 হোম ও নোটিশ বোর্ড", "🔍 স্টুডেন্ট প্রোফাইল ও রিপোর্ট", "👨‍🏫 শিক্ষক ও স্টাফ গ্যালারি", "🔐 অ্যাডমিন প্যানেল"])
    st.markdown("---")
    st.info("মাদরাসা ম্যানেজমেন্ট সফটওয়্যার v2.5")

# ১. হোম ও নোটিশ বোর্ড
if menu == "🏠 হোম ও নোটিশ বোর্ড":
    st.markdown("<div class='main-header'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    df_notice = load_data("Notice")
    if df_notice is not None and not df_notice.empty:
        latest_msg = df_notice.iloc[-1]['Message']
        st.markdown(f"<div class='notice-box'>🔔 <b>সর্বশেষ নোটিশ:</b><br>{latest_msg}</div>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1592288333291-70083b2744a5?q=80&w=2000", use_container_width=True)

# ২. স্টুডেন্ট প্রোফাইল (KeyError সমাধানসহ)
elif menu == "🔍 স্টুডেন্ট প্রোফাইল ও রিপোর্ট":
    st.markdown("<h2 style='text-align: center; color: #008080;'>🔍 স্টুডেন্ট রিপোর্ট কার্ড</h2>", unsafe_allow_html=True)
    sid = st.text_input("ছাত্রের আইডি (ID) লিখুন:", placeholder="যেমন: 10001")
    
    if sid:
        df_students = load_data("Student_List")
        df_att = load_data("Form_Responses_1")
        df_res = load_data("Result_Sheet")
        
        if df_students is not None:
            # আইডি কলাম চিনে নেওয়া (ID বা আইডি যাই থাকুক)
            id_col_list = [c for c in df_students.columns if 'ID' in c.upper() or 'আইডি' in c]
            if id_col_list:
                student = df_students[df_students[id_col_list[0]].astype(str) == str(sid)]
                
                if not student.empty:
                    s = student.iloc[0]
                    st.balloons()
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        photo_url = s.get('Photo_URL')
                        avatar = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        try:
                            st.image(str(photo_url) if not pd.isna(photo_url) else avatar, use_container_width=True, caption=f"ID: {sid}")
                        except: st.image(avatar, use_container_width=True)
                    
                    with c2:
                        st.markdown(f"""
                        <div class='profile-card'>
                            <h2 style='color: #008080; margin-top:0;'>👤 {s.get('Name', s.get('নাম', 'N/A'))}</h2>
                            <div class='info-badge'><b>👨‍💼 পিতার নাম:</b> {s.get('Father_Name', s.get('পিতার নাম', 'N/A'))}</div>
                            <div class='info-badge'><b>📞 মোবাইল:</b> {s.get('Mobile', s.get('মোবাইল', 'N/A'))}</div>
                            <div class='info-badge'><b>📍 ঠিকানা:</b> {s.get('Address', s.get('ঠিকানা', 'N/A'))}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.write("---")
                    tab_a, tab_r = st.tabs(["📅 বার্ষিক হাজিরা রিপোর্ট", "🎓 পরীক্ষার রেজাল্ট কার্ড"])
                    
                    with tab_a:
                        if df_att is not None:
                            id_col_att = [c for c in df_att.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                            if id_col_att:
                                att_res = df_att[df_att[id_col_att[0]].astype(str) == str(sid)]
                                st.dataframe(att_res, use_container_width=True)
                    
                    with tab_r:
                        if df_res is not None:
                            # রেজাল্ট শিটেও আইডি কলাম চেক করা
                            id_col_res = [c for c in df_res.columns if 'ID' in c.upper() or 'আইডি' in c]
                            if id_col_res:
                                res_match = df_res[df_res[id_col_res[0]].astype(str) == str(sid)]
                                if not res_match.empty:
                                    st.table(res_match.drop(columns=[id_col_res[0]]))
                                else: st.warning("রেজাল্ট পাওয়া যায়নি।")
                            else: st.error("রেজাল্ট শিটে 'ID' কলাম খুঁজে পাওয়া যাচ্ছে না।")
                else: st.error("এই আইডি-র কোনো তথ্য পাওয়া যায়নি।")

# ৩. শিক্ষক গ্যালারি
elif menu == "👨‍🏫 শিক্ষক ও স্টাফ গ্যালারি":
    st.markdown("<h2 style='text-align: center; color: #008080;'>👨‍🏫 শিক্ষকবৃন্দ</h2>", unsafe_allow_html=True)
    df_t = load_data("Teacher_List")
    if df_t is not None:
        grid = st.columns(3)
        for i, row in df_t.iterrows():
            with grid[i % 3]:
                st.markdown(f"<div class='teacher-card'><h3>{row.get('Name', 'নাম নেই')}</h3><p style='color: #008080;'>{row.get('Designation', 'পদবি নেই')}</p><p>📞 {row.get('Mobile', 'মোবাইল নেই')}</p></div>", unsafe_allow_html=True)

# ৪. অ্যাডমিন প্যানেল
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.text_input("পাসওয়ার্ড দিন:", type="password") == "admin123":
        st.success("লগইন সফল!")
        st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
