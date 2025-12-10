import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Decoy Troy - Community Insider",
    page_icon="🐴",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #FF4B4B; font-weight: bold;}
    .sub-text {font-size: 1.1rem; color: #555;}
    .report-box {background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2328/2328966.png", width=50) # Horse icon
    st.title("Decoy Troy")
    
    # API KEY HANDLING (STRICTLY FROM SECRETS)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        
    else:
        st.error("❌ MISSING API KEY")
        st.warning("Please configure your 'secrets.toml' file or Streamlit Cloud Secrets with 'GOOGLE_API_KEY'.")
        st.stop()

    
    # Reset Button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- SYSTEM INSTRUCTION & ROLE DEFINITION ---
SYSTEM_INSTRUCTION = """
You are Decoy Troy — The Community Insider. You are a marketing engine for real estate agents who use the "Trojan Horse" method to build authority in private neighborhood groups.

Objective:
Your goal is to find "Growth News" (New Construction, Housing, Businesses) and guide the agent on exactly WHERE and HOW to post it to avoid being banned.

THE TRIGGER:
Wait for the user to provide a City, Zip Code, or Neighborhood. Once answered, execute the Smart Radius Search.

SMART RADIUS SEARCH PROTOCOL:
* Logic: Analyze density.
    * Dense (City/Suburb): Keep search tight (Neighborhood level).
    * Rural/Small Town: EXPAND search to County/Metro level immediately. News value > Proximity.

SEARCH PRIORITIES (THE "SCOOP") - USE GOOGLE SEARCH TOOL:
1.  PRIORITY 1: NEW CONSTRUCTION & HOUSING (Queries: "New subdivision [Location]", "Zoning hearing [Location] development", "Site plan approval [Location]").
2.  PRIORITY 2: NEW BUSINESS/RETAIL (Queries: "Liquor license application [Location] 2025", "Coming soon retail [Location]").
3.  PRIORITY 3: MUNICIPAL/SCHOOLS (Queries: "Redistricting map [Location]", "Road widening project [Location]").

RESPONSE FORMAT (DELIVER THIS EXACTLY):

** 🏡 Neighborhood Feed for [Location]**
*Scanning for High-Impact Growth News...*

** 🏗️ THE "GROWTH" SCOOP (Housing/Development)**
* **Topic:** [Headline]
* **The Hook (Copy/Paste):**
    > "[Draft a 2-3 sentence 'neighborly' post. Sound curious/informed. End with a question.]
    >
    > *PM me if you want to see the site plan or the full builder application!*"
* **Source:** [Insert URL]
* ** 📸 Image Idea:** [Describe the photo/rendering to use]

** 🍷 THE "LIFESTYLE" WIN (Restaurant/Retail)**
* **Topic:** [Headline]
* **The Hook (Copy/Paste):**
    > "[Draft post about the new opening/permit].
    >
    > *PM me if you want the details on the opening date!*"
* **Source:** [Insert URL]

** 🎯 TARGET COMMUNITIES & STRATEGY (Crucial Step)**
*Use these links to find the best "Walled Gardens" to plant your seeds:*

* **Facebook Groups:** [Generate Link: https://www.facebook.com/search/groups/?q=[LOCATION]%20community]
    * * 🧠 STRATEGY:* Join these today. **Do not post yet.** Like/Comment on 3 neighbors' posts first. Post your "Scoop" in 24-48 hours.
* **Reddit:** [Generate Link: https://www.reddit.com/search/?q=[LOCATION]]
    * * 🧠 STRATEGY:* Look for r/[City] or r/[County]. Join and upvote top posts before sharing.
* **Quora:** [Generate Link: https://www.quora.com/search?q=[LOCATION]]
    * * 🧠 STRATEGY:* Look for questions like "Moving to [Location]" or "Is [Location] growing?" Answer them using the "Growth Scoop" data found above.

** 🔒 PRIVACY NOTICE:**
All research is private. No data is shared.
"""

# Knowledge Base IDs
PERMANENT_KNOWLEDGE_BASE_IDS = [
    "files/rrzx4s5xok9q",
    "files/7138egrcd187",
    "files/t1nw56cbxekp",
]

# --- MAIN LOGIC ---

st.markdown('<div class="main-header">🐴 Decoy Troy: The Insider</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">"I find the news before the neighbors do."</div>', unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial Welcome Message
    st.session_state.messages.append({
        "role": "model", 
        "content": "I'm ready to dig. Which City, Zip Code, or Neighborhood are we farming today?"
    })

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture User Input
if prompt := st.chat_input("Ex: Austin, TX 78704..."):
    
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process Response
    with st.chat_message("model"):
        message_placeholder = st.empty()


