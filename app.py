import streamlit as st
import pandas as pd

# --- CONNECTION ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'

def get_url(name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={name}'

st.set_page_config(page_title="Babussalam Digital Campus", layout="wide")

@st.cache_data(ttl=5)
def load_data(name):
    try:
        df = pd.read_csv(get_url(name))
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# Sidebar Menu
menu = st.sidebar.radio("Select Menu:", ["🏠 Home", "🔍 Student Profile & Report", "🔐 Admin"])

if menu == "🏠 Home":
    st.title("🕌 বাবুস সালাম ইসলামি একাডেমি")
    st.info("Student Profile-e ID diye search korle tarikh-shoho hajirar report pawa jabe.")

elif menu == "🔍 Student Profile & Report":
    st.header("🔍 ছাত্রের পূর্ণাঙ্গ রিপোর্ট")
    sid = st.text_input("Student ID Likhun:")
    
    if sid:
        df_students = load_data("Student_List")
        df_att = load_data("Form_Responses_1")
        df_res = load_data("Result_Sheet")
        
        if df_students is not None:
            student = df_students[df_students['ID'].astype(str) == str(sid)]
            
            if not student.empty:
                s = student.iloc[0]
                # Profile Info
                st.subheader(f"👤 নাম: {s.get('Name')}")
                
                # --- HAJIRA SECTION (Advanced) ---
                st.write("---")
                st.subheader("📅 হাজিরার বিস্তারিত ও সামারি")
                
                if df_att is not None:
                    # ID column khuje ber kora
                    id_col = [c for c in df_att.columns if 'ID' in c.upper() or 'আইডি' in c or 'Untitled' in c]
                    status_col = [c for c in df_att.columns if 'অবস্থা' in c or 'Status' in c]
                    
                    if id_col and status_col:
                        # Shudhu ei chhatrer data filter kora
                        att_res = df_att[df_att[id_col[0]].astype(str) == str(sid)].copy()
                        
                        if not att_res.empty:
                            # Calculation
                            total_days = len(att_res)
                            present_days = len(att_res[att_res[status_col[0]].str.contains('উপস্থিত|Present', na=False)])
                            absent_days = total_days - present_days
                            
                            # Summary Dashboard
                            c1, c2, c3 = st.columns(3)
                            c1.metric("মোট ক্লাস", f"{total_days} দিন")
                            c2.metric("উপস্থিত", f"{present_days} দিন", delta_color="normal")
                            c3.metric("অনুপস্থিত", f"{absent_days} দিন", delta="-"+str(absent_days))
                            
                            # Tarikh shoho Table (Timestamp column-e tarikh thake)
                            st.write("**তারিখ অনুযায়ী হাজিরার তালিকা:**")
                            st.dataframe(att_res[['Timestamp', status_col[0]]], use_container_width=True)
                        else:
                            st.warning("Ekhono kono hajira record kora hoyni.")
                
                # Result section niche thakbe...
                if df_res is not None:
                    st.write("---")
                    st.subheader("🎓 রেজাল্ট কার্ড")
                    res_m = df_res[df_res['ID'].astype(str) == str(sid)]
                    if not res_m.empty: st.table(res_m.drop(columns=['ID']))
            else:
                st.error("ID khuje pawa jayni.")

elif menu == "🔐 Admin":
    st.markdown(f'<a href="https://docs.google.com/forms/d/e/1FAIpQLScm285SqA1ByiOzuxAG8bNCCb4-a3ndgrYRiZeZ7JLDXxJJVg/viewform" target="_blank"><button style="width:100%; height:50px; background:#008080; color:white; border-radius:10px;">📝 হাজিরা নিন</button></a>', unsafe_allow_html=True)
