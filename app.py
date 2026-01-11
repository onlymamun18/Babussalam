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
    .stApp { background-color: #f8fbfb; }
    .result-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #008080; max-width: 600px; margin: auto; }
    .subject-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #ddd; }
    .subject-name { font-weight: bold; color: #333; }
    .subject-mark { color: #008080; font-weight: bold; }
    .total-row { background: #e6f2f2; padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 18px; border: 1px solid #008080; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data(name):
    try:
        data = pd.read_csv(get_url(name))
        data.columns = data.columns.str.strip() # কলামের নামের আসেপাশের স্পেস মুছে ফেলবে
        return data
    except Exception as e:
        return None

# --- মেনু ---
with st.sidebar:
    st.markdown("<h2>🕌 মেনুবার</h2>", unsafe_allow_html=True)
    menu = st.radio("পেজ সিলেক্ট করুন:", ["🏠 হোম ড্যাশবোর্ড", "🔍 ছাত্র হাজিরা চেক", "🎓 পরীক্ষার ফলাফল", "🔐 অ্যাডমিন কন্ট্রোল"])

# --- পরীক্ষার ফলাফল সেকশন ---
if menu == "🎓 পরীক্ষার ফলাফল":
    st.markdown("<h2 style='text-align: center; color: #008080;'>🎓 ছাত্রের ফলাফল অনুসন্ধান</h2>", unsafe_allow_html=True)
    res_id = st.text_input("ফলাফল দেখতে আইডি (ID) নম্বর দিন:")
    
    if st.button("ফলাফল দেখুন"):
        df_res = load_data("Result_Sheet")
        if df_res is not None and not df_res.empty:
            # আইডি কলামটি স্বয়ংক্রিয়ভাবে খুঁজে বের করা (ID বা আইডি যাই থাকুক)
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
                    st.error("দুঃখিত, এই আইডির কোনো ফলাফল পাওয়া যায়নি।")
            else:
                st.error("শিটে 'আইডি' বা 'ID' নামে কোনো কলাম পাওয়া যায়নি।")
        else:
            st.error("গুগল শিট থেকে ডাটা লোড করা যাচ্ছে না। ট্যাব নাম 'Result_Sheet' আছে কি না চেক করুন।")

# অন্যান্য পেজ (আগের মতোই থাকবে)
elif menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<h1 style='text-align: center; color: #008080;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>", unsafe_allow_html=True)
    st.info("ডিজিটাল ড্যাশবোর্ডে স্বাগতম।")

elif menu == "🔍 ছাত্র হাজিরা চেক":
    st.header("🔍 ছাত্র হাজিরা রিপোর্ট")
    search_id = st.text_input("আইডি দিন:")
    if st.button("হাজিরা চেক"):
        df_att = load_data("Form_Responses_1")
        if df_att is not None:
            id_col = [c for c in df_att.columns if 'ID' in c.upper() or 'আইডি' in c]
            if id_col:
                res = df_att[df_att[id_col[0]].astype(str) == str(search_id)]
                st.dataframe(res)

elif menu == "🔐 অ্যাডমিন কন্ট্রোল":
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        st.success("লগইন সফল")
