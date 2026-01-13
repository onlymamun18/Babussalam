import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# --- ১. কনফিগারেশন (আপনার দেওয়া লেটেস্ট লিঙ্ক) ---
SHEET_ID = '1TRbxG151RFzNdKbQ7KShWWV1MJHIVxSNdF-rSfLMde0'
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz5TpykMcD6f5ZLIBp26HuxOQ-uGOLdHOL0NJzQLq3ag_MzbtosgkLlXqJ6iK16MuKF/exec"
IMGBB_API_KEY = "67b93a0279c9417855b7662c16263546" 
ADMIN_PIN = "MdmamuN18"

def get_url(sheet_name):
    return f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

st.set_page_config(page_title="Babussalam Smart Campus", page_icon="🕌", layout="wide")

# --- ২. প্রিমিয়াম ডার্ক-ব্লু থিম ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #006699 100%);
        padding: 40px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-bottom: 5px solid #f1c40f;
    }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background: linear-gradient(90deg, #003366, #006699); color: white;
    }
    .big-button {
        display: block; width: 100%; padding: 18px; margin: 10px 0;
        text-align: center; color: white !important; font-size: 18px; font-weight: bold;
        text-decoration: none; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .call-btn { background: #27ae60; }
    .fb-btn { background: #2980b9; }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. ডাটা হ্যান্ডলিং ---
@st.cache_data(ttl=1)
def load_all_data():
    try:
        s_df = pd.read_csv(get_url("Student_List")).astype(str)
        r_df = pd.read_csv(get_url("Result")).astype(str)
        a_df = pd.read_csv(
