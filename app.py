import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ইসলামি একাডেমি", page_icon="🕌", layout="wide")

# প্রফেশনাল ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8fbfb; }
    .result-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #008080; max-width: 600px; margin: auto; }
    .subject-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #ddd; }
    .subject-name { font-weight: bold; color: #333; font-size: 16px; }
    .subject-mark { color: #008080; font-weight: bold; font-size: 16px; }
    .total-row { background: #e6f2f2; padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 18px; border: 1px solid #008080; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=10)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return data
    except:
        # যদি বাংলায় কলাম নাম পড়তে সমস্যা হয় তার জন্য ব্যাকআপ লোড
        return pd.read_csv(get_url(name))

# --- সাইডবার মেনু ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🕌 মেনুবার</h2>", unsafe_allow_html=True)
    menu = st.radio("পেজ সিলেক্ট করুন:", ["🏠 হোম ড্যাশবোর্ড", "🔍 ছাত্র হাজিরা চেক", "🎓 পরীক্ষার ফলাফল", "🔐 অ্যাডমিন কন্ট্রোল"])

# ৩. পরীক্ষার ফলাফল (পুরো বাংলায়)
if menu == "🎓 পরীক্ষার ফলাফল":
    st.markdown("<h2 style='text-align: center; color: #008080;'>🎓 ছাত্রের ফলাফল অনুসন্ধান</h2>", unsafe_allow_html=True)
    res_id = st.text_input("ফলাফল দেখতে ছাত্রের আইডি (ID) লিখুন:", placeholder="যেমন: 101")
    
    if st.button("ফলাফল দেখুন"):
        df_res = load_data("Result_Sheet")
        if df_res is not None and res_id:
            # শিটে কলামের নাম 'আইডি' হতে হবে
            result = df_res[df_res['আইডি'].astype(str) == str(res_id)]
            
            if not result.empty:
                st.balloons()
                row = result.iloc[0]
                
                st.markdown(f"""
                <div class='result-card'>
                    <h2 style='text-align: center; color: #008080;'>{row.get('পরীক্ষা', 'পরীক্ষার ফলাফল')}</h2>
                    <p style='text-align: center;'><b>নাম:</b> {row.get('নাম', 'N/A')} | <b>আইডি:</b> {row.get('আইডি', 'N/A')}</p>
                    <hr>
                    <div class='subject-row'><span class='subject-name'>📖 আরবি:</span><span class='subject-mark'>{row.get('আরবি', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>🇧🇩 বাংলা:</span><span class='subject-mark'>{row.get('বাংলা', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>🇺🇸 ইংরেজি:</span><span class='subject-mark'>{row.get('ইংরেজি', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>🔢 গণিত:</span><span class='subject-mark'>{row.get('গণিত', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>📜 হাদিস:</span><span class='subject-mark'>{row.get('হাদিস', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>🕋 কালিমা:</span><span class='subject-mark'>{row.get('কালিমা', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>📖 কুরআন:</span><span class='subject-mark'>{row.get('কুরআন', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>🌍 সমাজ বিজ্ঞান:</span><span class='subject-mark'>{row.get('সমাজ বিজ্ঞান', '0')}</span></div>
                    <div class='subject-row'><span class='subject-name'>💡 সাধারণ জ্ঞান:</span><span class='subject-mark'>{row.get('সাধারণ জ্ঞান', '0')}</span></div>
                    
                    <div class='total-row'>
                        <div style='display: flex; justify-content: space-between;'>
                            <b>মোট নম্বর: {row.get('মোট নম্বর', '0')}</b>
                            <b style='color: #d9534f;'>গ্রেড: {row.get('গ্রেড', 'N/A')}</b>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("দুঃখিত, এই আইডির কোনো ফলাফল পাওয়া যায়নি।")
        else:
            st.warning("দয়া করে সঠিক আইডি নম্বর দিন।")

# বাকি অংশ আগের মতোই থাকবে...
elif menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("<h1 style='text-align: center; color: #008080;'>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>", unsafe_allow_html=True)
    st.info("ডিজিটাল ড্যাশবোর্ডে স্বাগতম। বাম পাশের মেনু থেকে কাজ নির্বাচন করুন।")

elif menu == "🔍 ছাত্র হাজিরা চেক":
    st.header("🔍 ছাত্র হাজিরা রিপোর্ট")
    search_id = st.text_input("আইডি নম্বর দিন:")
    if st.button("হাজিরা চেক"):
        df_att = load_data("Form_Responses_1")
        if df_att is not None and search_id:
            # ফর্মে কলাম নাম সাধারণত ID বা আইডি থাকে, সেটি নিশ্চিত করুন
            id_col = [col for col in df_att.columns if 'ID' in col.upper() or 'আইডি' in col]
            if id_col:
                res = df_att[df_att[id_col[0]].astype(str) == str(search_id)]
                st.dataframe(res, use_container_width=True)

elif menu == "🔐 অ্যাডমিন কন্ট্রোল":
    st.header("🔐 অ্যাডমিন প্যানেল")
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        st.success("লগইন সফল!")
        st.write("হাজিরা নিতে ফর্ম ব্যবহার করুন। রেজাল্ট আপডেট করতে গুগল শিটের 'Result_Sheet' ব্যবহার করুন।")
