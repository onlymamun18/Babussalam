import streamlit as st
import pandas as pd

# Google Sheet Connection
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# App Config
st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# CSS Design
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 8px; background-color: #008080; color: white; }
    .student-card { background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #008080; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    h1, h2 { color: #008080; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Data Load Function
@st.cache_data(ttl=20)
def load_data():
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = load_data()

# Sidebar Menu
with st.sidebar:
    st.markdown("<h2>মেনুবার</h2>", unsafe_allow_html=True)
    choice = st.radio("পেজ সিলেক্ট করুন:", [
        "🏠 ড্যাশবোর্ড", 
        "🔍 আইডি সার্চ", 
        "👨‍🎓 সকল ছাত্রের তালিকা", 
        "📝 হাজিরা ও রেজাল্ট", 
        "📢 নোটিশ বোর্ড"
    ])

# 1. Dashboard
if choice == "🏠 ড্যাশবোর্ড":
    st.markdown("<h1>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    if df is not None:
        total_students = len(df)
        col1.metric("মোট ছাত্র", f"{total_students} জন")
    col2.metric("শিক্ষক", "১০ জন")
    col3.metric("সাফল্য", "১০০%")

# 2. ID Search
elif choice == "🔍 আইডি সার্চ":
    st.header("🔍 আইডি দিয়ে অনুসন্ধান")
    search_id = st.text_input("আইডি নম্বর লিখুন:")
    if st.button("সার্চ করুন"):
        if df is not None and search_id:
            id_col = [col for col in df.columns if col.lower() == 'id']
            if id_col:
                result = df[df[id_col[0]].astype(str) == str(search_id)]
                if not result.empty:
                    res = result.iloc[0]
                    st.success("তথ্য পাওয়া গেছে!")
                    st.info(f"👤 নাম: {res.get('Name', 'N/A')}\n\n👴 পিতা: {res.get('Father', 'N/A')}\n\n📍 ঠিকানা: {res.get('Address', 'N/A')}")
                else:
                    st.error("আইডি পাওয়া যায়নি।")

# 3. All Students List (Apnar notun chahida)
elif choice == "👨‍🎓 সকল ছাত্রের তালিকা":
    st.header("👨‍🎓 সকল ছাত্রের তালিকা (সিরিয়াল অনুযায়ী)")
    if df is not None:
        if not df.empty:
            st.write(f"মোট ছাত্র সংখ্যা: {len(df)} জন")
            # Table akare sob student dekhano
            st.dataframe(df, use_container_width=True) 
            
            st.markdown("---")
            st.subheader("বিস্তারিত লিস্ট:")
            # Prothtek student-er jonno alada card
            for index, row in df.iterrows():
                st.markdown(f"""
                <div class="student-card">
                    <b>সিরিয়াল: {index + 1}</b><br>
                    <b>আইডি:</b> {row.get('ID', 'N/A')} | <b>নাম:</b> {row.get('Name', 'N/A')}<br>
                    <b>পিতা:</b> {row.get('Father', 'N/A')} | <b>মোবাইল:</b> {row.get('Mobile', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("গুগল শিটে কোনো ছাত্রের তথ্য নেই।")
    else:
        st.error("ডাটা লোড করা যাচ্ছে না।")

# 4. Others
else:
    st.header(choice)
    st.info("এই পেজটির কাজ প্রক্রিয়াধীন...")
