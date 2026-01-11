import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# CSS ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .madrasa-name { text-align: center; color: #008080; font-size: 40px; font-weight: bold; margin-top: 10px; }
    .madrasa-address { text-align: center; color: #444; font-size: 18px; margin-bottom: 25px; }
    .notice-card { background: #fff8e1; padding: 20px; border-radius: 12px; border-left: 8px solid #ffa000; margin-bottom: 25px; color: #5f4b00; }
    .profile-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); border-top: 6px solid #008080; }
    .stButton>button { background-color: #008080 !important; color: white !important; font-weight: bold; border-radius: 10px; height: 50px; }
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

menu = st.sidebar.radio("মেনু:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল ও রিপোর্ট", "👨‍🏫 শিক্ষক তালিকা", "🔐 অ্যাডমিন"])

# ১. হোম পেজ (ব্যানার ও নাম)
if menu == "🏠 হোম পেজ":
    st.markdown("<div class='madrasa-name'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    st.markdown("<div class='madrasa-address'>পূর্বপাড় দিঘুলী, খামারবাড়ী মোড়, দিগপাইত, জামালপুর</div>", unsafe_allow_html=True)
    
    banner_url = "https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg"
    st.image(banner_url, use_container_width=True)
    
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        msg = df_n.iloc[-1]['Message']
        st.markdown(f"<div class='notice-card'>📢 <b>জরুরি নোটিশ:</b> {msg}</div>", unsafe_allow_html=True)

# ২. ছাত্র প্রোফাইল (KeyError: Timestamp সমাধানসহ)
elif menu == "🔍 ছাত্র প্রোফাইল ও রিপোর্ট":
    st.header("🔍 ছাত্রের পূর্ণাঙ্গ রিপোর্ট")
    sid = st.text_input("ছাত্রের আইডি (ID) লিখুন:", placeholder="যেমন: 10001")
    
    if sid:
        df_s = load_data("Student_List")
        df_a = load_data("Form_Responses_1")
        df_r = load_data("Result_Sheet")
        
        if df_s is not None:
            sid_col_s = [c for c in df_s.columns if 'ID' in c.upper() or 'আইডি' in c][0]
            student = df_s[df_s[sid_col_s].astype(str) == str(sid)]
            
            if not student.empty:
                s = student.iloc[0]
                col1, col2 = st.columns([1, 2])
                with col1:
                    img = s.get('Photo_URL', "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                    st.image(str(img), width=230)
                with col2:
                    st.markdown(f"""
                    <div class='profile-card'>
                        <h2 style='color:#008080;'>👤 {s.get('Name', s.get('নাম', 'N/A'))}</h2>
                        <p><b>👨‍💼 পিতার নাম:</b> {s.get('Father_Name', 'N/A')}</p>
                        <p><b>📞 মোবাইল:</b> {s.get('Mobile', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("---")
                t1, t2 = st.tabs(["📅 হাজিরার রিপোর্ট", "🎓 পরীক্ষার রেজাল্ট"])
                
                with t1:
                    if df_a is not None:
                        # এখানে আমরা কলামের নাম যাই হোক, সেটি খুঁজে বের করছি
                        time_col = [c for c in df_a.columns if 'Time' in c or 'টাইম' in c or 'সকাল' in c or 'Date' in c or 'তারিখ' in c]
                        id_col_a = [c for c in df_a.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                        status_col = [c for c in df_a.columns if 'অবস্থা' in c or 'Status' in c]
                        
                        if id_col_a and status_col:
                            u_att = df_a[df_a[id_col_a[0]].astype(str) == str(sid)]
                            # Timestamp কলাম না থাকলেও অ্যাপ যেন ক্র্যাশ না করে তার ব্যবস্থা
                            final_cols = []
                            if time_col: final_cols.append(time_col[0])
                            else: final_cols.append(df_a.columns[0]) # প্রথম কলামকে সময় ধরে নেওয়া
                            final_cols.append(status_col[0])
                            
                            st.dataframe(u_att[final_cols], use_container_width=True)

                with t2:
                    if df_r is not None:
                        id_col_r = [c for c in df_r.columns if 'ID' in c.upper() or 'আইডি' in c]
                        if id_col_r:
                            u_res = df_r[df_r[id_col_r[0]].astype(str) == str(sid)]
                            st.table(u_res.drop(columns=[id_col_r[0]]))
            else:
                st.error("আইডি পাওয়া যায়নি।")

# ৩. শিক্ষক তালিকা ও অ্যাডমিন
elif menu == "👨‍🏫 শিক্ষক তালিকা":
    st.header("👨‍🏫 আমাদের শিক্ষকবৃন্দ")
    df_t = load_data("Teacher_List")
    if df_t is not None: st.dataframe(df_t, use_container_width=True)

elif menu == "🔐 অ্যাডমিন":
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        st.success("লগইন সফল")
        st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
