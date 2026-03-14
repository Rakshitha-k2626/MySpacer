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
# CSS STYLING
# -----------------------
st.markdown("""
<style>
/* Right panel styling */
[data-testid="column"]:nth-child(2){
    background:white;
    border-radius:15px;
    height:600px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
    box-shadow:0 8px 20px rgba(0,0,0,0.25);
    padding:0;
}

/* Chat header */
.right-chat-header {
    background: linear-gradient(90deg, #ff4b4b, #ff7b4b);
    color:white;
    font-weight:bold;
    padding:12px;
    border-top-left-radius:15px;
    border-top-right-radius:15px;
    text-align:center;
    font-size:18px;
}

/* Chat messages scrollable area */
.stChatMessage div[role="log"] {
    padding:10px;
    flex-grow:1;
    overflow-y:auto;
    background:#f9f9f9;
}

/* Chat input at bottom */
.stChatInput {
    margin-top:auto !important;
    padding:10px;
    border-top:1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# LAYOUT: LEFT + RIGHT
# -----------------------
left, right = st.columns([3, 1])

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
            "Space Chatbot"
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
        with col1: st.metric("🛰 Satellites", "128")
        with col2: st.metric("☄ Asteroids Detected", "42")
        with col3: st.metric("🌍 ISS Altitude", "408 km")

        st.divider()
        st.subheader("Navigation")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.button("🌌 Solar System")
        with c2: st.button("📸 NASA Images")
        with c3: st.button("🛰 ISS Tracker")
        with c4: st.button("☄ Asteroid Monitor")

        st.image("https://images-assets.nasa.gov/image/PIA12235/PIA12235~orig.jpg", use_column_width=True)
        st.write("""
        Welcome to *Spacer Mission Control*.

        Explore space using real APIs and an AI assistant.

        Features:
        * Solar system explorer  
        * NASA astronomy images  
        * ISS tracker  
        * Asteroid monitor  
        * AI chatbot powered by OpenAI
        """)
        st.markdown("[Visit NASA Website](https://www.nasa.gov)")

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
        st.subheader(planet)
        st.info(planets[planet])

    elif menu == "NASA Image":
        st.title("🌌 NASA Astronomy Picture of the Day")
        url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        try:
            data = requests.get(url, timeout=10).json()
            st.subheader(data["title"])
            st.image(data["url"])
            st.write(data["explanation"])
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
                st.subheader(date)
                for obj in asteroids[date]:
                    name = obj["name"]
                    size = obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
                    danger = obj["is_potentially_hazardous_asteroid"]
                    st.write("Name:", name)
                    st.write("Max Size (m):", round(size, 2))
                    st.write("Hazardous:", "⚠ Yes" if danger else "Safe")
                    st.markdown("---")
        except:
            st.error("Asteroid API failed")

# -----------------------
# RIGHT PANEL: BEAUTIFUL CHATBOT
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