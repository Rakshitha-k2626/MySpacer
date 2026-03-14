import streamlit as st
import requests
import pandas as pd
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Spacer Mission Control", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    
    .stApp {
        background: url("https://www.hdwallpapers.in/download/sky_full_of_incandescent_stars_during_nighttime_hd_galaxy-HD.jpg");
        background-size: cover;
    }
    
    .logo-text {
        font-family: 'Orbitron', sans-serif;
        color: #ffd700;
        font-size: 50px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
    }

    .metric-card, .info-card {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin-bottom: 20px;
        color: white;
    }

    h1, h2, h3 { color: #ffd700 !important; font-family: 'Orbitron', sans-serif; }
    
    /* Chat Container Fixes */
    .chat-container {
        height: 600px;
        overflow-y: auto;
        padding: 15px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
    }
    .user-msg {
        background: linear-gradient(90deg, #ff4b2b, #ff416c);
        color: white;
        padding: 12px;
        border-radius: 15px 15px 0 15px;
        margin: 8px 0 8px auto;
        max-width: 80%;
    }
    .bot-msg {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        padding: 12px;
        border-radius: 15px 15px 15px 0;
        margin: 8px auto 8px 0;
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION SYSTEM ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown('<p class="logo-text">SPACER</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            st.text_input("Username", key="login_user")
            st.text_input("Password", type="password", key="login_pass")
            if st.button("Enter Mission Control"):
                st.session_state.logged_in = True
                st.rerun()
        with tab2:
            st.text_input("Email", key="sig_email")
            st.text_input("Choose Username", key="sig_user")
            st.text_input("Choose Password", type="password", key="sig_pass")
            st.button("Create Account")

if not st.session_state.logged_in:
    login_page()
    st.stop()

# --- SIDEBAR ---
st.sidebar.markdown('<p class="logo-text" style="font-size:25px;">SPACER</p>', unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", ["Dashboard", "Solar System", "NASA Image", "ISS Tracker", "Asteroid Monitor"])
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- DATA FETCHING ---
def get_nasa_apod():
    try:
        res = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
        return res.json() if res.status_code == 200 else None
    except: return None

# --- MAIN LAYOUT ---
col_main, col_chat = st.columns([3, 1])

with col_main:
    if page == "Dashboard":
        st.markdown('<p class="logo-text">SPACER</p>', unsafe_allow_html=True)
        st.subheader("Mission Status: Operational")
        
        m1, m2, m3 = st.columns(3)
        m1.markdown('<div class="metric-card"><h3>🛰️ Satellites</h3><h2>128</h2><p>In Active Orbit</p></div>', unsafe_allow_html=True)
        m2.markdown('<div class="metric-card"><h3>☄️ NEOs</h3><h2>42</h2><p>Detected Today</p></div>', unsafe_allow_html=True)
        m3.markdown('<div class="metric-card"><h3>🌍 ISS Alt</h3><h2>408 km</h2><p>Altitude Stable</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
        <h3>🧑‍🚀 NASA — Broad Look (2011–2026)</h3>
        NASA leads U.S. civilian space exploration and planetary defense.
        <br><br>
        <b>Major Achievements:</b><br>
        ✔️ Mars rover missions and orbital studies<br>
        ✔️ Returned asteroid samples (OSIRIS-REx)<br>
        ✔️ Planetary defense tests (DART)<br>
        ✔️ Parker Solar Probe record approaches<br>
        ✔️ Artemis II crewed Moon mission preparation (2026)
        </div>
        """, unsafe_allow_html=True)

    elif page == "Solar System":
        st.header("🌞 Solar System & Planets")
        st.markdown("""
        <div class="info-card">
        <b>Overview:</b> Our system consists of the Sun, eight planets, dwarf planets (Pluto, Eris), and countless small bodies.
        <br><br>
        <b>Exploration Highlights:</b> 
        The Juno mission continues at Jupiter, while New Horizons' Pluto flyby reshaped our understanding of the outer reach. 
        Over the past 15 years, robotic explorers have visited nearly every major body in the system.
        </div>
        """, unsafe_allow_html=True)
        
        planet = st.selectbox("Select Planet Data", ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
        st.info(f"Displaying telemetry for {planet}. NASA missions have measured atmospheres and surface compositions to understand evolution.")

    elif page == "NASA Image":
        st.header("📸 NASA Daily Discovery")
        apod = get_nasa_apod()
        if apod:
            st.image(apod.get('url'), use_container_width=True)
            st.markdown(f'<div class="info-card"><h4>{apod.get("title")}</h4>{apod.get("explanation")}</div>', unsafe_allow_html=True)

    elif page == "ISS Tracker":
        st.header("🛰️ International Space Station (ISS)")
        st.markdown("""
        <div class="info-card">
        <b>Altitude:</b> 370–460 km | <b>Speed:</b> 17,500 mph<br>
        <b>Recent Activity:</b> 2026 Maintenance spacewalks are underway. The Cygnus XL delivered record payloads in 2025. 
        While NASA plans operations until 2030, commercial stations are now in active development.
        </div>
        """, unsafe_allow_html=True)
        st.map(pd.DataFrame({'lat': [40.7], 'lon': [-74.0]})) # Placeholder for map visibility

    elif page == "Asteroid Monitor":
        st.header("☄️ Asteroids & NEOs")
        st.markdown("""
        <div class="info-card">
        <b>Tracking Growth:</b> Over 40,000 known NEOs cataloged by 2026. 
        <br><b>Defensive Wins:</b> The DART mission (2022) successfully altered Dimorphos' orbit.
        <br><b>Near Miss:</b> Asteroid 2026 EG1 passed closer than the Moon in March 2026.
        </div>
        """, unsafe_allow_html=True)

# --- CHATBOT (RIGHT COLUMN) ---
with col_chat:
    st.markdown("### 💬 Spacer AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        div_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        chat_html += f'<div class="{div_class}">{msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input Box
    if prompt := st.chat_input("Ask Mission Control..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            webhook_url = "https://athri.app.n8n.cloud/webhook/87c4d113-173c-47ba-929a-c48dbcd33cfe/chat"
            response = requests.post(webhook_url, json={"chatInput": prompt}, timeout=15)
            
            if response.status_code == 200:
                raw_text = response.text
                # Use regex to find the content parts from the streaming N8N response
                contents = re.findall(r'"content":"(.*?)"', raw_text)
                reply = "".join(contents).replace('\\n', '\n').strip() if contents else raw_text
            else: reply = "Comms error."
        except: reply = "Signal lost."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()