import streamlit as st
import pandas as pd

# Google Sheet Connection
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# App Config
st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", layout="wide")

# Custom CSS for UI
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #008080; color: white; }
    .profile-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #008080; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .notice-card { background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Data Load
@st.cache_data(ttl=10)
def load_data():
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = load_data()

# --- Sidebar Menu ---
st.sidebar.title("🕌 মেনুবার")
menu = st.sidebar.radio("পেজ সিলেক্ট করুন:", ["📢 নোটিশ বোর্ড", "🔍 আইডি দিয়ে হাজিরা দেখুন", "🔐 অ্যাডমিন প্যানেল"])

# 1. Notice Board (Sobai dekhbe)
if menu == "📢 নোটিশ বোর্ড":
    st.markdown("<h1 style='text-align: center; color: #008080;'>📢 নোটিশ বোর্ড</h1>", unsafe_allow_html=True)
    st.write("---")
    # Ekhane apni notice gulu likhe rakhte paren
    st.markdown("""
    <div class="notice-card">
        <h4>📢 বার্ষিক পরীক্ষার নোটিশ</h4>
        <p>আগামী ২০শে জানুয়ারি থেকে মাদরাসার বার্ষিক পরীক্ষা শুরু হবে। সকল ছাত্রকে উপস্থিত থাকার জন্য বলা হচ্ছে।</p>
        <small>তারিখ: ১০/০১/২০২৬</small>
    </div>
    <div class="notice-card">
        <h4>🌙 জুমার ছুটি</h4>
        <p>প্রতি শুক্রবার মাদরাসা বন্ধ থাকবে।</p>
    </div>
    """, unsafe_allow_html=True)

# 2. Student Search (Guardian-der jonno)
elif menu == "🔍 আইডি দিয়ে হাজিরা দেখুন":
    st.markdown("<h2 style='text-align: center;'>🔍 আপনার সন্তানের আইডি দিন</h2>", unsafe_allow_html=True)
    search_id = st.text_input("ID Number:", placeholder="যেমন: 101")
    
    if st.button("তথ্য দেখুন"):
        if df is not None and search_id:
            result = df[df['ID'].astype(str) == str(search_id)]
            if not result.empty:
                res = result.iloc[0]
                st.success("তথ্য পাওয়া গেছে!")
                st.markdown(f"""
                <div class="profile-card">
                    <h3>👤 নাম: {res.get('Name', 'N/A')}</h3>
                    <p><b>আইডি:</b> {res.get('ID', 'N/A')}</p>
                    <hr>
                    <h4 style='color: {"green" if res.get("Attendance") == "Present" else "red"}'>
                        📊 আজকের হাজিরা: {res.get('Attendance', 'আপডেট নেই')}
                    </h4>
                    <p><b>👴 পিতা:</b> {res.get('Father', 'N/A')}</p>
                    <p><b>📍 ঠিকানা:</b> {res.get('Address', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("দুঃখিত, এই আইডি নম্বরটি সঠিক নয়।")

# 3. Admin Panel (Sudu password diye login kora jabe)
elif menu == "🔐 অ্যাডমিন প্যানেল":
    st.header("🔐 অ্যাডমিন লগইন")
    password = st.text_input("পাসওয়ার্ড দিন:", type="password")
    
    # Ekhane password 'admin123' dewa ache, apni chaile bodlate paren
    if password == "admin123":
        st.success("স্বাগতম অ্যাডমিন!")
        st.subheader("👨‍🎓 সকল ছাত্রের ডাটাবেস")
        if df is not None:
            st.dataframe(df) # Admin sob student-er list ekhane dekhbe
            st.write(f"মোট ছাত্র সংখ্যা: {len(df)}")
    elif password != "":
        st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")

st.sidebar.markdown("---")
st.sidebar.caption("বাবুস সালাম ইসলামি একাডেমি")
