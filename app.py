import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম একাডেমি", layout="wide")

# প্রফেশনাল ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .profile-card { background: white; padding: 25px; border-radius: 15px; border-top: 6px solid #008080; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .info-text { font-size: 18px; margin-bottom: 10px; color: #333; }
    .stButton>button { background-color: #008080; color: white; height: 50px; font-weight: bold; border-radius: 10px; }
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

# --- মেনু ---
menu = st.sidebar.radio("মেনু নির্বাচন করুন:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল (সব তথ্য)", "🔐 অ্যাডমিন প্যানেল"])

# ১. হোম পেজ
if menu == "🏠 হোম পেজ":
    st.markdown("<h1 style='text-align: center; color: #008080;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590076214667-c0f3c7e0f2b2?q=80&w=1000", use_container_width=True)
    st.success("স্বাগতম! ছাত্রের সব তথ্য পেতে 'ছাত্র প্রোফাইল' মেনুতে যান।")

# ২. ছাত্র প্রোফাইল (এক জায়গায় সব)
elif menu == "🔍 ছাত্র প্রোফাইল (সব তথ্য)":
    st.header("🔍 ছাত্রের পূর্ণাঙ্গ রিপোর্ট অনুসন্ধান")
    search_id = st.text_input("ছাত্রের আইডি (ID) লিখুন:", placeholder="যেমন: 101")
    
    if st.button("সার্চ করুন"):
        # সবগুলো ডাটা একসাথে লোড হবে
        df_students = load_data("Student_List")
        df_att = load_data("Form_Responses_1")
        df_res = load_data("Result_Sheet")
        
        if df_students is not None:
            # ছাত্র খুঁজে বের করা
            student = df_students[df_students['ID'].astype(str) == str(search_id)]
            
            if not student.empty:
                s = student.iloc[0]
                st.balloons()
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    photo = s.get('Photo_URL')
                    default_img = "https://www.w3schools.com/howto/img_avatar.png"
                    try:
                        if pd.isna(photo) or str(photo).strip() == "":
                            st.image(default_img, caption="ছবি নেই", width=250)
                        else:
                            st.image(str(photo), caption=f"আইডি: {search_id}", width=250)
                    except:
                        st.image(default_img, caption="ছবি লোড হয়নি", width=250)
                
                with col2:
                    st.markdown(f"""
                    <div class='profile-card'>
                        <h2 style='color: #008080;'>👤 {s.get('Name', 'নাম নেই')}</h2>
                        <p class='info-text'><b>👨‍💼 পিতার নাম:</b> {s.get('Father_Name', 'তথ্য নেই')}</p>
                        <p class='info-text'><b>📞 মোবাইল:</b> {s.get('Mobile', 'তথ্য নেই')}</p>
                        <p class='info-text'><b>📍 ঠিকানা:</b> {s.get('Address', 'তথ্য নেই')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # একই পেজে নিচে হাজিরা ও রেজাল্ট
                st.write("---")
                tab1, tab2 = st.tabs(["📅 সারা বছরের হাজিরা", "🎓 পরীক্ষার রেজাল্ট"])
                
                with tab1:
                    if df_att is not None:
                        # আইডি কলাম খুঁজে হাজিরা বের করা
                        id_col_att = [c for c in df_att.columns if 'ID' in c.upper() or 'আইডি' in c]
                        if id_col_att:
                            att = df_att[df_att[id_col_att[0]].astype(str) == str(search_id)]
                            if not att.empty: st.dataframe(att, use_container_width=True)
                            else: st.warning("এই ছাত্রের হাজিরার কোনো রেকর্ড নেই।")
                
                with tab2:
                    if df_res is not None:
                        # আইডি কলাম খুঁজে রেজাল্ট বের করা
                        id_col_res = [c for c in df_res.columns if 'ID' in c.upper() or 'আইডি' in c]
                        if id_col_res:
                            res = df_res[df_res[id_col_res[0]].astype(str) == str(search_id)]
                            if not res.empty: st.table(res.drop(columns=[id_col_res[0]]))
                            else: st.warning("এই ছাত্রের কোনো রেজাল্ট পাওয়া যায়নি।")
            else:
                st.error("দুঃখিত, এই আইডি-র কোনো ছাত্রের প্রোফাইল খুঁজে পাওয়া যায়নি।")

# ৩. অ্যাডমিন প্যানেল
elif menu == "🔐 অ্যাডমিন প্যানেল":
    st.header("🔐 অ্যাডমিন কন্ট্রোল")
    if st.text_input("পাসওয়ার্ড দিন:", type="password") == "admin123":
        st.success("লগইন সফল!")
        st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button>📝 আজকের হাজিরা নিন</button></a>', unsafe_allow_html=True)
        st.write("---")
        st.info("ছাত্রের প্রোফাইল তথ্য, ছবি বা রেজাল্ট আপডেট করতে আপনার গুগল শিটটি ব্যবহার করুন।")
