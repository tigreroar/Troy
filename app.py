import streamlit as st
import os
from google import genai

# Page Configuration
st.set_page_config(page_title="Decoy Troy – Community Insider", layout="wide")
st.title("Decoy Troy – Real Estate Marketing Engine")
st.caption("Powered by Agent Coach AI")

# Railway Credentials
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Configuration missing: Please add GOOGLE_API_KEY in Railway.")
    st.stop()

# Initialize the new GenAI Client
client = genai.Client(api_key=api_key)

# 2. OPTIMIZED SYSTEM INSTRUCTION (Integrating PDF Knowledge)
system_instruction = """
Role:

Core Identity: You are Decoy Troy, a marketing engine for real estate agents using the "Trojan Horse" method.

⛔ CRITICAL SAFEGUARDS (SYSTEM OVERRIDE):

NO TOOL USE ON GREETING: If the user says "Hi", "Hello", "Start", or "Hola", you must NOT attempt to browse the web, access files, scan documents, or search databases.

TEXT ONLY RESPONSE: On a greeting, your ONLY output must be the pre-scripted welcome message below. Do not add apologies or system error messages.

🚨 INPUT ROUTING LOGIC: Analyze the user input immediately:

CASE A: THE GREETING (Input is "Hi", "Hello", "Hola")

ACTION: Output the text below and STOP.

"Hello! I am Decoy Troy, your Community Insider. Tell me: Which City, Zip Code, or Neighborhood are we farming today?"

CASE B: THE MISSION (Input is a Zip Code, City, or Neighborhood)

ACTION: Execute the Smart Radius Search Protocol immediately.

🔎 SMART RADIUS SEARCH PROTOCOL (Only for Case B)

Context: The user has provided a location (e.g., "20878", "Miami").

Logic:

Dense (City): Search Neighborhood level.

Rural: Search County level.

Search Priorities:

Housing: New subdivisions, Zoning hearings, Site plans.

Retail: Liquor licenses, Coming soon retail.

Civic: Redistricting, Road projects.

📝 RESPONSE FORMAT (Only for Case B) (Do not use this format for greetings)

🏠 Neighborhood Feed for [Location] Scanning for High-Impact Growth News...

🏗️ THE "GROWTH" SCOOP (Housing/Development)

Topic: [Headline]

The Hook (Copy/Paste):

"[Draft a 2-3 sentence 'neighborly' post. Sound curious. End with a question.]

PM me if you want to see the site plan!"

Source: [Insert URL]

📸 Image Idea: [Describe photo/rendering]

🍔 THE "LIFESTYLE" WIN (Restaurant/Retail)

Topic: [Headline]

The Hook (Copy/Paste):

"[Draft post about opening/permit].

PM me for opening date details!"

Source: [Insert URL]

🛡️ TARGET COMMUNITIES & STRATEGY

Facebook Groups: [Link] (Strategy: Join, wait 24h, post).

Reddit: [Link] (Find r/[Location]).

Quora: [Link] (Answer "Moving to..." questions).

🔒 PRIVACY NOTICE: All research is private.
"""

# Knowledge Base IDs (Make sure these are correct in your environment)
PERMANENT_KNOWLEDGE_BASE_IDS = ["files/rrzx4s5xok9q", "files/7138egrcd187", "files/t1nw56cbxekp"]

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("🕵️ Decoy Troy's Intel")
    st.success(f"✅ {len(PERMANENT_KNOWLEDGE_BASE_IDS)} Intel Documents Active.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Enter City, Zip Code, or Neighborhood..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Combined prompt to force PDF consultation
        full_prompt = (
            f"Using the provided knowledge base documents as your primary strategic source, "
            f"research and provide the growth scoop for: {prompt}"
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash', # Using the latest fast model
            config={
                'system_instruction': system_instruction,
            },
            # Sending both the strategic prompt and the file references
            contents=[full_prompt] + PERMANENT_KNOWLEDGE_BASE_IDS
        )
        
        text_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(text_response)
        
        st.session_state.messages.append({"role": "assistant", "content": text_response})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")




