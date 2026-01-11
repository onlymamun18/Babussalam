import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .madrasa-header { text-align: center; color: #008080; font-size: 38px; font-weight: bold; }
    .notice-box { background: #fff8e1; padding: 15px; border-radius: 10px; border-left: 8px solid #ffa000; margin-bottom: 20px; }
    .stButton>button { background-color: #008080 !important; color: white !important; font-weight: bold; width: 100%; height: 45px; border-radius: 10px; }
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

# মেনু
menu = st.sidebar.radio("মেনু:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল", "➕ নতুন ছাত্র ভর্তি", "👨‍🏫 শিক্ষক তালিকা", "🔐 অ্যাডমিন"])

# ১. হোম পেজ
if menu == "🏠 হোম পেজ":
    st.markdown("<div class='madrasa-header'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        st.markdown(f"<div class='notice-box'>📢 নোটিশ: {df_n.iloc[-1].values[0]}</div>", unsafe_allow_html=True)

# ২. ছাত্র প্রোফাইল (ইমেজ এরর ফিক্সড)
elif menu == "🔍 ছাত্র প্রোফাইল":
    sid = st.text_input("ছাত্রের আইডি লিখুন:")
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
                        # ছবির এরর হ্যান্ডেল করার নিরাপদ উপায়
                        photo_url = s.get('Photo_URL', "")
                        default_img = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        try:
                            if pd.isna(photo_url) or str(photo_url).strip() == "" or not str(photo_url).startswith("http"):
                                st.image(default_img, width=230)
                            else:
                                st.image(str(photo_url), width=230)
                        except:
                            st.image(default_img, width=230)
                    with col2:
                        st.subheader(f"👤 {s.get('Name', 'N/A')}")
                        st.write(f"বাবার নাম: {s.get('Father_Name', 'N/A')}")
                        st.write(f"মোবাইল: {s.get('Mobile', 'N/A')}")
                    
                    # হাজিরা ও রেজাল্ট
                    st.write("---")
                    t1, t2 = st.tabs(["📅 হাজিরা", "🎓 রেজাল্ট"])
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
                else: st.error("ছাত্র পাওয়া যায়নি!")

# ৩. ছাত্র ভর্তি ফরম
elif menu == "➕ নতুন ছাত্র ভর্তি":
    st.header("নতুন ছাত্র ভর্তি ফরম")
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform"
    st.markdown(f'<iframe src="{form_url}" width="100%" height="800" frameborder="0"></iframe>', unsafe_allow_html=True)

# ৪. শিক্ষক তালিকা
elif menu == "👨‍🏫 শিক্ষক তালিকা":
    df_t = load_data("Teacher_List")
    if df_t is not None: st.dataframe(df_t, use_container_width=True)

# ৫. অ্যাডমিন প্যানেল
elif menu == "🔐 অ্যাডমিন":
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        hajira_link = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform"
        st.markdown(f'<a href="{hajira_link}" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
        
