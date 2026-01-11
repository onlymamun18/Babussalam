import streamlit as st
import pandas as pd

# --- গুগল শিট কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# অ্যাপ সেটিংস
st.set_page_config(page_title="বাবুস সালাম ডিজিটাল ক্যাম্পাস", page_icon="🕌", layout="wide")

# ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .madrasa-name { text-align: center; color: #008080; font-size: 38px; font-weight: bold; margin-bottom: 5px; }
    .madrasa-address { text-align: center; color: #444; font-size: 16px; margin-bottom: 20px; }
    .notice-card { background: #fff8e1; padding: 15px; border-radius: 10px; border-left: 8px solid #ffa000; margin-bottom: 20px; color: #5f4b00; }
    .profile-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-top: 5px solid #008080; }
    .stButton>button { background-color: #008080 !important; color: white !important; font-weight: bold; border-radius: 10px; width: 100%; height: 45px; }
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

# মেনুবার
menu = st.sidebar.radio("মেনু নির্বাচন করুন:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল ও রিপোর্ট", "➕ নতুন ছাত্র যোগ করুন", "👨‍🏫 শিক্ষক তালিকা", "🔐 অ্যাডমিন প্যানেল"])

# ১. হোম পেজ
if menu == "🏠 হোম পেজ":
    st.markdown("<div class='madrasa-name'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    st.markdown("<div class='madrasa-address'>পূর্বপাড় দিঘুলী, খামারবাড়ী মোড়, দিগপাইত, জামালপুর</div>", unsafe_allow_html=True)
    
    # ব্যানার ছবি
    banner_url = "https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg"
    try: st.image(banner_url, use_container_width=True)
    except: st.info("বাবুস সালাম ইসলামি একাডেমি ডিজিটাল সিস্টেমে স্বাগতম।")
    
    # সর্বশেষ নোটিশ
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        msg = df_n.iloc[-1].values[0]
        st.markdown(f"<div class='notice-card'>📢 <b>সর্বশেষ নোটিশ:</b> {msg}</div>", unsafe_allow_html=True)

# ২. ছাত্র প্রোফাইল (রেজাল্ট ও হাজিরাসহ)
elif menu == "🔍 ছাত্র প্রোফাইল ও রিপোর্ট":
    sid = st.text_input("ছাত্রের আইডি (ID) লিখুন:")
    if sid:
        df_s = load_data("Student_List")
        if df_s is not None:
            id_col = [c for c in df_s.columns if 'ID' in c.upper() or 'আইডি' in c]
            if id_col:
                student = df_s[df_s[id_col[0]].astype(str) == str(sid)]
                if not student.empty:
                    s = student.iloc[0]
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        photo = s.get('Photo_URL', "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                        st.image(str(photo), width=230)
                    with col2:
                        st.markdown(f"""
                        <div class='profile-card'>
                            <h3>👤 {s.get('Name', 'N/A')}</h3>
                            <p><b>পিতার নাম:</b> {s.get('Father_Name', 'N/A')}<br><b>মোবাইল:</b> {s.get('Mobile', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("---")
                    t1, t2 = st.tabs(["📅 হাজিরার তথ্য", "🎓 পরীক্ষার রেজাল্ট"])
                    with t1:
                        df_a = load_data("Form_Responses_1")
                        if df_a is not None:
                            id_a = [c for c in df_a.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                            if id_a:
                                u_att = df_a[df_a[id_a[0]].astype(str) == str(sid)]
                                st.dataframe(u_att, use_container_width=True)
                    with t2:
                        df_r = load_data("Result_Sheet")
                        if df_r is not None:
                            id_r = [c for c in df_r.columns if 'ID' in c.upper() or 'আইডি' in c]
                            if id_r:
                                u_res = df_r[df_r[id_r[0]].astype(str) == str(sid)]
                                st.table(u_res.drop(columns=[id_r[0]]))
                else: st.error("এই আইডি-র কোনো ছাত্র পাওয়া যায়নি।")

# ৩. নতুন ছাত্র যোগ করুন (গুগল ফর্মের মাধ্যমে)
elif menu == "➕ নতুন ছাত্র যোগ করুন":
    st.header("➕ নতুন ছাত্রের তথ্য জমা দিন")
    # এখানে আপনার ছাত্র ভর্তি ফর্মের লিঙ্কটি দিন
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform"
    st.markdown(f'<iframe src="{form_link}" width="100%" height="800" frameborder="0">লোড হচ্ছে...</iframe>', unsafe_allow_html=True)

# ৪. শিক্ষক তালিকা
elif menu == "👨‍🏫 শিক্ষক তালিকা":
    st.header("👨‍🏫 আমাদের শিক্ষকবৃন্দ")
    df_t = load_data("Teacher_List")
    if df_t is not None: st.dataframe(df_t, use_container_width=True)

# ৫. অ্যাডমিন প্যানেল (হাজিরা নেওয়ার জন্য)
elif menu == "🔐 অ্যাডমিন প্যানেল":
    if st.text_input("অ্যাডমিন পাসওয়ার্ড দিন:", type="password") == "admin123":
        st.success("লগইন সফল!")
        hajira_url = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform"
        st.markdown(f'<a href="{hajira_url}" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
        
