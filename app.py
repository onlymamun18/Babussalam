import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন সেটআপ ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

# অ্যাপ কনফিগারেশন
st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# প্রফেশনাল ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8fbfb; }
    .result-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #008080; max-width: 600px; margin: auto; }
    .subject-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #ddd; }
    .subject-name { font-weight: bold; color: #333; }
    .subject-mark { color: #008080; font-weight: bold; }
    .total-row { background: #e6f2f2; padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 18px; border: 1px solid #008080; text-align: center; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #008080; color: white; height: 45px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ডাটা লোড করার ফাংশন
@st.cache_data(ttl=5)
def load_data(name):
    try:
        data = pd.read_csv(get_url(name))
        data.columns = data.columns.str.strip() # নামের আশেপাশের বাড়তি জায়গা মুছে ফেলবে
        return data
    except Exception as e:
        return None

# --- সাইডবার মেনুবার (আগের সব অপশনসহ) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🕌 মেনুবার</h2>", unsafe_allow_html=True)
    menu = st.radio("পেজ সিলেক্ট করুন:", [
        "🏠 হোম ড্যাশবোর্ড", 
        "🔍 ছাত্র হাজিরা চেক", 
        "🎓 পরীক্ষার ফলাফল", 
        "🔐 অ্যাডমিন কন্ট্রোল"
    ])
    st.markdown("---")
    st.caption("© বাবুস সালাম ইসলামি একাডেমি")

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<h1 style='text-align: center; color: #008080;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1590076214667-c0f3c7e0f2b2?q=80&w=1000", use_container_width=True)
    st.info("মাদরাসার ডিজিটাল ড্যাশবোর্ডে স্বাগতম। অভিভাবকরা এখান থেকে হাজিরা ও রেজাল্ট চেক করতে পারবেন।")

# ২. ছাত্র হাজিরা চেক (আগের সিস্টেম)
elif menu == "🔍 ছাত্র হাজিরা চেক":
    st.header("🔍 ছাত্র হাজিরা রিপোর্ট")
    search_id = st.text_input("ছাত্রের আইডি (ID) নম্বর দিন:")
    
    if st.button("হাজিরা চেক করুন"):
        df_att = load_data("Form_Responses_1")
        if df_att is not None:
            # আইডি কলাম চিনে নেওয়া
            id_col = [c for c in df_att.columns if 'ID' in c.upper() or 'আইডি' in c]
            if id_col:
                res = df_att[df_att[id_col[0]].astype(str) == str(search_id)]
                if not res.empty:
                    st.success(f"আইডি {search_id}-এর হাজিরার তথ্য পাওয়া গেছে।")
                    st.dataframe(res, use_container_width=True)
                else:
                    st.error("কোনো হাজিরার তথ্য পাওয়া যায়নি।")
            else:
                st.error("শিটে আইডি কলাম খুঁজে পাওয়া যায়নি।")

# ৩. পরীক্ষার ফলাফল (নতুন বিষয়ভিত্তিক ডিজাইন)
elif menu == "🎓 পরীক্ষার ফলাফল":
    st.header("🎓 পরীক্ষার রেজাল্ট শিট")
    res_id = st.text_input("ফলাফল দেখতে আইডি (ID) দিন:")
    
    if st.button("রেজাল্ট দেখুন"):
        df_res = load_data("Result_Sheet")
        if df_res is not None:
            id_col = [c for c in df_res.columns if 'ID' in c.upper() or 'আইডি' in c]
            if id_col:
                result = df_res[df_res[id_col[0]].astype(str) == str(res_id)]
                if not result.empty:
                    st.balloons()
                    row = result.iloc[0]
                    st.markdown(f"""
                    <div class='result-card'>
                        <h2 style='text-align: center; color: #008080;'>{row.get('পরীক্ষা', row.get('Exam', 'ফলাফল'))}</h2>
                        <p style='text-align: center;'><b>নাম:</b> {row.get('নাম', row.get('Name', 'N/A'))} | <b>আইডি:</b> {res_id}</p>
                        <hr>
                        <div class='subject-row'><span class='subject-name'>📖 আরবি:</span><span class='subject-mark'>{row.get('আরবি', row.get('Arbi', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>🇧🇩 বাংলা:</span><span class='subject-mark'>{row.get('বাংলা', row.get('Bangla', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>🇺🇸 ইংরেজি:</span><span class='subject-mark'>{row.get('ইংরেজি', row.get('English', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>🔢 গণিত:</span><span class='subject-mark'>{row.get('গণিত', row.get('Gonit', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>📜 হাদিস:</span><span class='subject-mark'>{row.get('হাদিস', row.get('Hadis', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>🕋 কালিমা:</span><span class='subject-mark'>{row.get('কালিমা', row.get('Kalema', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>📖 কুরআন:</span><span class='subject-mark'>{row.get('কুরআন', row.get('Quran', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>🌍 সমাজ বিজ্ঞান:</span><span class='subject-mark'>{row.get('সমাজ বিজ্ঞান', row.get('Somaj', '0'))}</span></div>
                        <div class='subject-row'><span class='subject-name'>💡 সাধারণ জ্ঞান:</span><span class='subject-mark'>{row.get('সাধারণ জ্ঞান', row.get('General_Gen', '0'))}</span></div>
                        <div class='total-row'><b>মোট নম্বর: {row.get('মোট নম্বর', row.get('Total', '0'))}</b> | <b>গ্রেড: {row.get('গ্রেড', row.get('Grade', 'N/A'))}</b></div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("এই আইডির কোনো ফলাফল পাওয়া যায়নি।")

# ৪. অ্যাডমিন কন্ট্রোল
elif menu == "🔐 অ্যাডমিন কন্ট্রোল":
    st.header("🔐 অ্যাডমিন প্যানেল")
    password = st.text_input("পাসওয়ার্ড দিন:", type="password")
    
    if password == "admin123":
        st.success("স্বাগতম অ্যাডমিন!")
        # ছাত্র হাজিরা ফর্ম লিঙ্ক
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform"
        st.markdown(f'<a href="{form_url}" target="_blank"><button>📝 আজকের ছাত্র হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
        st.write("---")
        st.write("শিক্ষকদের হাজিরার জন্য আলাদা ফর্ম এখানে যোগ করতে পারেন।")
    elif password != "":
        st.error("ভুল পাসওয়ার্ড!")
