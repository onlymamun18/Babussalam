import streamlit as st
import pandas as pd

# --- ডাটা কানেকশন ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="বাবুস সালাম ডিজিটাল একাডেমি", page_icon="🕌", layout="wide")

# --- প্রিমিয়াম UI ডিজাইন (CSS) ---
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp { background: linear-gradient(to right, #f8f9fa, #e9ecef); }
    
    /* হেডার সেকশন */
    .main-header {
        background: linear-gradient(135deg, #008080 0%, #004d4d 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        margin-bottom: 30px;
    }
    
    /* কার্ড ডিজাইন */
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eef2f3;
        transition: 0.3s;
    }
    .card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    
    /* মেনু স্টাইল */
    .stSidebar { background-color: #ffffff !important; border-right: 1px solid #eee; }
    
    /* বাটন ডিজাইন */
    .stButton>button {
        background: linear-gradient(135deg, #008080 0%, #006666 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 25px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* ট্যাব ও টেবিল */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: transparent; border-radius: 8px; font-weight: bold; }
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

# --- সাইডবার মেনু ---
with st.sidebar:
    st.markdown("<h2 style='color:#008080;'>📋 কন্ট্রোল প্যানেল</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["🏠 হোম ড্যাশবোর্ড", "🔍 স্টুডেন্ট রিপোর্ট", "➕ নতুন ভর্তি", "👨‍🏫 শিক্ষক গ্যালারি", "🔐 অ্যাডমিন অ্যাক্সেস"])

# ১. হোম ড্যাশবোর্ড
if menu == "🏠 হোম ড্যাশবোর্ড":
    st.markdown("""
        <div class='main-header'>
            <h1>🕌 বাবুস সালাম ইসলামি একাডেমি</h1>
            <p style='font-size: 18px; opacity: 0.9;'>ডিজিটাল এডুকেশন ম্যানেজমেন্ট সিস্টেম</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ব্যানার
    st.image("https://raw.githubusercontent.com/Anisurrahmananis/babussalam/main/babu.jpg", use_container_width=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📢 সর্বশেষ আপডেট ও নোটিশ")
        df_n = load_data("Notice")
        if df_n is not None and not df_n.empty:
            msg = df_n.iloc[-1].values[0]
            st.markdown(f"<div class='card' style='border-left: 8px solid #ffa000;'><b>নোটিশ:</b> {msg}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("### 📍 যোগাযোগ")
        st.markdown("<div class='card'>পূর্বপাড় দিঘুলী, খামারবাড়ী মোড়<br>দিগপাইত, জামালপুর।</div>", unsafe_allow_html=True)

# ২. স্টুডেন্ট রিপোর্ট (প্রিমিয়াম লুক)
elif menu == "🔍 স্টুডেন্ট রিপোর্ট":
    st.markdown("<h2 style='color:#008080;'>🔍 ছাত্রের পূর্ণাঙ্গ প্রোফাইল</h2>", unsafe_allow_html=True)
    sid = st.text_input("আইডি (ID) টাইপ করুন:", placeholder="যেমন: 10001")
    
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
                        photo = s.get('Photo_URL', "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                        st.markdown(f"<div style='text-align:center;'><img src='{photo}' width='200' style='border-radius:20px; border: 5px solid #008080; box-shadow: 0 5px 15px rgba(0,0,0,0.2);'></div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div class='card'>
                                <h2 style='color:#008080; margin-bottom:10px;'>{s.get('Name', 'N/A')}</h2>
                                <p><b>👨‍💼 পিতার নাম:</b> {s.get('Father_Name', 'N/A')}</p>
                                <p><b>📞 মোবাইল:</b> {s.get('Mobile', 'N/A')}</p>
                                <p><b>📍 ঠিকানা:</b> {s.get('Address', 'N/A')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    t1, t2 = st.tabs(["📊 হাজিরার পরিসংখ্যান", "🏆 পরীক্ষার রেজাল্ট"])
                    with t1:
                        df_a = load_data("Form_Responses_1")
                        if df_a is not None:
                            st.dataframe(df_a[df_a.iloc[:, 1].astype(str) == str(sid)], use_container_width=True)
                    with t2:
                        df_r = load_data("Result_Sheet")
                        if df_r is not None:
                            st.table(df_r[df_r.iloc[:, 0].astype(str) == str(sid)])
                else: st.error("দুঃখিত, কোনো ছাত্র খুঁজে পাওয়া যায়নি।")

# ৩. নতুন ভর্তি
elif menu == "➕ নতুন ভর্তি":
    st.markdown("<h2 style='color:#008080;'>➕ নতুন ছাত্র ভর্তি ফরম</h2>", unsafe_allow_html=True)
    embed_url = "https://docs.google.com/forms/d/e/1FAIpQLScy-WjL_2p5V9W_l7C8J-uXjVz/viewform?embedded=true"
    st.markdown(f'<div class="card"><iframe src="{embed_url}" width="100%" height="900" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# ৫. অ্যাডমিন
elif menu == "🔐 অ্যাডমিন অ্যাক্সেস":
    st.markdown("<h2 style='color:#008080;'>🔐 সিকিউরড লগইন</h2>", unsafe_allow_html=True)
    if st.text_input("পাসওয়ার্ড:", type="password") == "admin123":
        st.success("লগইন সফল!")
        hajira_url = "https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform"
        st.markdown(f'<a href="{hajira_url}" target="_blank"><button style="width:100%;">📝 ডিজিটাল হাজিরা শুরু করুন</button></a>', unsafe_allow_html=True)
