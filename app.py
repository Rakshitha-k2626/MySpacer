import streamlit as st
import requests

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Spacer Mission Control", layout="wide")

# -----------------------
# N8N WEBHOOK
# -----------------------
N8N_WEBHOOK = "https://athri.app.n8n.cloud/webhook/87c4d113-173c-47ba-929a-c48dbcd33cfe/chat"

# -----------------------
# SESSION STATE
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# CSS STYLING: Galaxy + Cards + Mobile-style Chat
# -----------------------
st.markdown("""
<style>
/* Background sky with stars (from Bing link) */
[data-testid="stAppViewContainer"] {
    background: url('https://www.hdwallpapers.in/download/sky_full_of_incandescent_stars_during_nighttime_hd_galaxy-HD.jpg');
    background-size: cover;
    background-attachment: fixed;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Card style */
.card {
    background: rgba(0,0,0,0.6);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.5);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #ff7b4b);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 8px 14px;
    transition: transform 0.2s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Headings */
h1, h2, h3 {
    color: #ffd700;
}

/* Sidebar title */
[data-testid="stSidebar"] h2 {
    color: #ff4b4b;
}

/* Right chat panel styling (mobile style) */
[data-testid="column"]:nth-child(2){
    background: rgba(0,0,0,0.8);
    border-radius:20px;
    height:650px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
    box-shadow:0 8px 25px rgba(0,0,0,0.35);
    padding:0;
    max-width: 380px;
}

/* Chat header */
.right-chat-header {
    background: linear-gradient(90deg, #ff4b4b, #ff7b4b);
    color:white;
    font-weight:bold;
    padding:14px;
    border-top-left-radius:20px;
    border-top-right-radius:20px;
    text-align:center;
    font-size:18px;
}

/* Chat message container with scroll */
.stChatMessage div[role="log"] {
    flex-grow:1;
    overflow-y:auto;
    padding: 10px;
    display:flex;
    flex-direction:column;
}

/* Chat bubbles */
.stChatMessage .userMessage {
    align-self:flex-end;
    background: linear-gradient(120deg, #ff4b4b, #ff7b4b);
    color:white;
    padding:8px 12px;
    border-radius:18px 18px 0 18px;
    margin-bottom:6px;
    max-width:80%;
    word-wrap: break-word;
}
.stChatMessage .assistantMessage {
    align-self:flex-start;
    background: rgba(255,255,255,0.1);
    color:white;
    padding:8px 12px;
    border-radius:18px 18px 18px 0;
    margin-bottom:6px;
    max-width:80%;
    word-wrap: break-word;
}

/* Chat input */
.stChatInput {
    margin-top:auto !important;
    padding:10px;
    border-top:1px solid rgba(255,255,255,0.3);
    background: rgba(0,0,0,0.85);
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# LAYOUT: LEFT + RIGHT
# -----------------------
left, right = st.columns([3,1])

# -----------------------
# SIDEBAR NAVIGATION
# -----------------------
with st.sidebar:
    st.title("🚀 Spacer Mission Control")
    menu = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Solar System",
            "NASA Image",
            "ISS Tracker",
            "Asteroid Monitor",
        ]
    )

# -----------------------
# LEFT PANEL: MAIN APP UI
# -----------------------
with left:
    st.title("🚀 Spacer Mission Control")

    if menu == "Dashboard":
        st.subheader("Real-time Space Monitoring Dashboard")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="card"><h3>🛰 Satellites</h3><p>128 Active</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card"><h3>☄ Asteroids</h3><p>42 Detected</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="card"><h3>🌍 ISS Altitude</h3><p>408 km</p></div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("Quick Navigation")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.button("🌌 Solar System")
        with c2: st.button("📸 NASA Images")
        with c3: st.button("🛰 ISS Tracker")
        with c4: st.button("☄ Asteroid Monitor")

        st.markdown('<div class="card"><img src="https://images-assets.nasa.gov/image/PIA12235/PIA12235~orig.jpg" width="100%"><p>Welcome to Spacer Mission Control! Explore space in real time with APIs and AI.</p></div>', unsafe_allow_html=True)
        st.markdown("[Visit NASA Website](https://www.nasa.gov)", unsafe_allow_html=True)

    elif menu == "Solar System":
        st.title("☀ Solar System Explorer")
        planets = {
            "Mercury":"Closest planet to the Sun",
            "Venus":"Hottest planet with thick atmosphere",
            "Earth":"Our home planet",
            "Mars":"The red planet",
            "Jupiter":"Largest planet",
            "Saturn":"Planet with beautiful rings",
            "Uranus":"Ice giant",
            "Neptune":"Farthest planet"
        }
        planet = st.selectbox("Choose a planet", list(planets.keys()))
        st.markdown(f'<div class="card"><h3>{planet}</h3><p>{planets[planet]}</p></div>', unsafe_allow_html=True)

    elif menu == "NASA Image":
        st.title("🌌 NASA Astronomy Picture of the Day")
        url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        try:
            data = requests.get(url, timeout=10).json()
            st.markdown(f'<div class="card"><h3>{data["title"]}</h3><img src="{data["url"]}" width="100%"><p>{data["explanation"]}</p></div>', unsafe_allow_html=True)
        except:
            st.error("NASA API failed")

    elif menu == "ISS Tracker":
        st.title("🛰 ISS Live Location")
        url = "http://api.open-notify.org/iss-now.json"
        try:
            data = requests.get(url, timeout=10).json()
            lat = float(data["iss_position"]["latitude"])
            lon = float(data["iss_position"]["longitude"])
            col1, col2 = st.columns(2)
            col1.metric("Latitude", lat)
            col2.metric("Longitude", lon)
            st.map({"lat":[lat], "lon":[lon]})
        except:
            st.error("ISS API failed")

    elif menu == "Asteroid Monitor":
        st.title("☄ Near Earth Asteroids")
        url = "https://api.nasa.gov/neo/rest/v1/feed?api_key=DEMO_KEY"
        try:
            data = requests.get(url, timeout=10).json()
            asteroids = data["near_earth_objects"]
            for date in asteroids:
                st.markdown(f'<div class="card"><h3>{date}</h3>', unsafe_allow_html=True)
                for obj in asteroids[date]:
                    name = obj["name"]
                    size = obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
                    danger = obj["is_potentially_hazardous_asteroid"]
                    st.write(f"Name: {name} | Max Size: {round(size,2)} m | Hazardous: {'⚠ Yes' if danger else 'Safe'}")
                st.markdown('</div>', unsafe_allow_html=True)
        except:
            st.error("Asteroid API failed")

# -----------------------
# RIGHT PANEL: N8N CHATBOT (Mobile-style UI)
# -----------------------
with right:
    st.markdown('<div class="right-chat-header">💬 Spacer AI Assistant</div>', unsafe_allow_html=True)

    # Display previous chat messages
    for role, msg in st.session_state.messages:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

    # Chat input
    user_input = st.chat_input("Ask anything about space...")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        try:
            response = requests.post(
                N8N_WEBHOOK,
                json={"chatInput": user_input},
                headers={"Content-Type": "application/json"},
                timeout=20
            )
            raw = response.text
            reply = ""
            parts = raw.split('"content":"')
            for p in parts[1:]:
                reply += p.split('"')[0]
        except Exception as e:
            reply = f"Chatbot error: {e}"
        st.session_state.messages.append(("assistant", reply))