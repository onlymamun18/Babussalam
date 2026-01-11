import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ডিজিটাল ক্যাম্পাস", page_icon="🕌", layout="wide")

# ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .madrasa-header { text-align: center; color: #008080; font-size: 38px; font-weight: bold; }
    .stButton>button { background-color: #008080 !important; color: white !important; font-weight: bold; width: 100%; border-radius: 10px; height: 45px; }
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

# মেনু নির্বাচন
menu = st.sidebar.radio("মেনু:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল", "➕ ছাত্র ভর্তি ফরম", "👨‍🏫 শিক্ষক তালিকা", "🔐 অ্যাডমিন"])

# ১. হোম পেজ
if menu == "🏠 হোম পেজ":
    st.markdown("<div class='madrasa-header'>🕌 বাবুস সালাম ইসলামি একাডেমি</div>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    
    df_n = load_data("Notice")
    if df_n is not None and not df_n.empty:
        st.info(f"📢 নোটিশ: {df_n.iloc[-1].values[0]}")

# ২. ছাত্র প্রোফাইল
elif menu == "🔍 ছাত্র প্রোফাইল":
    sid = st.text_input("ছাত্রের আইডি (ID) দিন:")
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
                        photo_url = s.get('Photo_URL', "")
                        avatar = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        try:
                            if pd.isna(photo_url) or not str(photo_url).startswith("http"):
                                st.image(avatar, width=220)
                            else: st.image(str(photo_url), width=220)
                        except: st.image(avatar, width=220)
                    with col2:
                        st.subheader(f"👤 {s.get('Name', 'N/A')}")
                        st.write(f"পিতার নাম: {s.get('Father_Name', 'N/A')}")
                else: st.warning("ছাত্র পাওয়া যায়নি।")

# ৩. ছাত্র ভর্তি ফরম (ফিক্সড ভার্সন)
elif menu == "➕ ছাত্র ভর্তি ফরম":
    st.header("➕ নতুন ছাত্র ভর্তি ফরম")
    # নিচের লিঙ্কটি আমি আপডেট করে দিয়েছি যাতে এটি সঠিকভাবে লোড হয়
    form_id = "1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz"
    embed_url = f"https://docs.google.com/forms/d/e/{form_id}/viewform?embedded=true"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            <iframe src="{embed_url}" width="100%" height="1000" frameborder="0" marginheight="0" marginwidth="0">লোড হচ্ছে...</iframe>
        </div>
    """, unsafe_allow_html=True)

# ৪. শিক্ষক ও ৫. অ্যাডমিন
elif menu == "👨‍🏫 শিক্ষক তালিকা":
    df_t = load_data("Teacher_List")
    if df_t is not None: st.dataframe(df_t, use_container_width=True)

elif menu == "🔐 অ্যাডমিন":
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        hajira_url = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform"
        st.markdown(f'<a href="{hajira_url}" target="_blank"><button>📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
