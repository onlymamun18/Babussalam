import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম একাডেমি", layout="wide")

# ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .profile-card { background: white; padding: 20px; border-radius: 15px; border-top: 5px solid #008080; }
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
menu = st.sidebar.radio("মেনু:", ["🏠 হোম পেজ", "🔍 ছাত্র প্রোফাইল (সব তথ্য)"])

if menu == "🏠 হোম পেজ":
    st.title("🕌 বাবুস সালাম ইসলামি একাডেমি")
    st.info("ছাত্র প্রোফাইল সেকশনে গিয়ে আইডি দিয়ে সার্চ করলে ছাত্রের সব তথ্য পাওয়া যাবে।")

elif menu == "🔍 ছাত্র প্রোফাইল (সব তথ্য)":
    st.header("🔍 ছাত্রের পূর্ণাঙ্গ তথ্য অনুসন্ধান")
    search_id = st.text_input("ছাত্রের আইডি (ID) লিখুন:")
    
    if st.button("সার্চ করুন"):
        df_students = load_data("Student_List")
        df_att = load_data("Form_Responses_1")
        df_res = load_data("Result_Sheet")
        
        if df_students is not None:
            student = df_students[df_students['ID'].astype(str) == str(search_id)]
            
            if not student.empty:
                s = student.iloc[0]
                # ছাত্রের ছবি ও তথ্য
                col1, col2 = st.columns([1, 2])
                with col1:
                    img = s.get('Photo_URL', 'https://www.w3schools.com/howto/img_avatar.png')
                    st.image(img, caption=f"আইডি: {search_id}")
                with col2:
                    st.subheader(f"নাম: {s.get('Name')}")
                    st.write(f"পিতার নাম: {s.get('Father_Name')}")
                    st.write(f"মোবাইল: {s.get('Mobile')}")
                    st.write(f"ঠিকানা: {s.get('Address')}")

                # হাজিরা ও রেজাল্ট এক পাতায়
                st.write("---")
                st.subheader("📅 হাজিরার রেকর্ড")
                if df_att is not None:
                    att = df_att[df_att['ID'].astype(str) == str(search_id)]
                    st.dataframe(att, use_container_width=True)

                st.write("---")
                st.subheader("🎓 পরীক্ষার ফলাফল")
                if df_res is not None:
                    res = df_res[df_res['ID'].astype(str) == str(search_id)]
                    st.table(res)
            else:
                st.error("এই আইডি-র কোনো ছাত্র পাওয়া যায়নি।")
