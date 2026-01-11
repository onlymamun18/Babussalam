import streamlit as st
import pandas as pd

# গুগল শিট কানেকশন
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

# অ্যাপ কনফিগারেশন
st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# ডিজাইন উন্নত করার জন্য CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #008080; color: white; height: 3em; }
    .info-box { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); border-left: 5px solid #008080; }
    h1 { color: #008080; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড করার ফাংশন
@st.cache_data(ttl=30)
def load_data():
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip() 
        return data
    except:
        return None

df = load_data()

# সাইডবার মেনু ডিজাইন
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #008080;'>মেনুবার</h2>", unsafe_allow_html=True)
    choice = st.radio("পেজ সিলেক্ট করুন:", ["🏠 ড্যাশবোর্ড", "🔍 আইডি সার্চ", "📝 হাজিরা ও রেজাল্ট", "📢 নোটিশ বোর্ড", "📚 কিতাবখানা"])

# ১. ড্যাশবোর্ড
if choice == "🏠 ড্যাশবোর্ড":
    st.markdown("<h1>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590076214667-c0f3c7e0f2b2?q=80&w=1000", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("মোট ছাত্র", "১২০")
    col2.metric("শিক্ষক", "১০")
    col3.metric("সাফল্য", "১০০%")

# ২. আইডি দিয়ে সার্চ
elif choice == "🔍 আইডি সার্চ":
    st.header("🔍 ছাত্র/শিক্ষকের তথ্য অনুসন্ধান")
    search_id = st.text_input("আইডি নম্বরটি টাইপ করুন:", placeholder="যেমন: 101")
    
    if st.button("সার্চ করুন"):
        if df is not None and search_id:
            id_col = [col for col in df.columns if col.lower() == 'id']
            if id_col:
                result = df[df[id_col[0]].astype(str) == str(search_id)]
                if not result.empty:
                    res = result.iloc[0]
                    st.success("আলহামদুলিল্লাহ! তথ্য পাওয়া গেছে।")
                    
                    st.markdown(f"""
                    <div class="info-box">
                        <h2 style="color: #008080;">👤 নাম: {res.get('Name', 'N/A')}</h2>
                        <hr>
                        <p><b>👴 পিতার নাম:</b> {res.get('Father', 'N/A')}</p>
                        <p><b>👵 মাতার নাম:</b> {res.get('Mother', 'N/A')}</p>
                        <p><b>📞 মোবাইল:</b> {res.get('Mobile', 'N/A')}</p>
                        <p><b>📍 ঠিকানা:</b> {res.get('Address', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("দুঃখিত, এই আইডি দিয়ে কোনো তথ্য পাওয়া যায়নি।")
            else:
                st.error("গুগল শিটে 'ID' কলামটি খুঁজে পাওয়া যায়নি।")
        else:
            st.warning("আইডি নম্বর দিয়ে বাটনে ক্লিক করুন।")

# ৩. হাজিরা ও রেজাল্ট
elif choice == "📝 হাজিরা ও রেজাল্ট":
    st.header("📝 হাজিরা ও রেজাল্ট সেকশন")
    st.info("এই সেকশনটি নিয়ে কাজ চলছে...")

# ৪. নোটিশ বোর্ড
elif choice == "📢 নোটিশ বোর্ড":
    st.header("📢 নোটিশ বোর্ড")
    st.info("জরুরি নোটিশ এখানে দেখা যাবে।")

# ৫. কিতাবখানা
elif choice == "📚 কিতাবখানা":
    st.header("📚 কিতাবখানা")
    st.info("আপনার কিতাবের লিঙ্ক এখানে যোগ করা হবে।")
