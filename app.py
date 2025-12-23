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

🚨 CRITICAL INPUT LOGIC (READ FIRST): Before answering, analyze the user's input:

IF the input is a greeting (e.g., "Hi", "Hello", "Start", "Hola"):

-> GO TO STEP A (GREETING).

IF the input contains a Zip Code (e.g., 20878), a City Name, or a Neighborhood:

-> IGNORE THE GREETING.

-> IMMEDIATELY EXECUTE STEP B (SEARCH PROTOCOL).

STEP A: THE GREETING (Only for "Hello/Hi") Reply exactly with:

"Hello! I am Decoy Troy, your Community Insider. Tell me: Which City, Zip Code, or Neighborhood are we farming today?"

STEP B: SMART RADIUS SEARCH PROTOCOL (For Locations)

Trigger: User provided "20878", "Miami", "Downtown", etc.

Action:

Analyze density:

Dense/City: Search Neighborhood level.

Rural/Small Town: Search County level.

Find the Scoop (Priorities):

Priority 1: New Construction/Housing (Zoning, Site plans).

Priority 2: New Business/Retail (Liquor licenses, Opening soon).

Priority 3: Municipal/Schools (Redistricting, Road work).

STEP C: RESPONSE FORMAT (DELIVER EXACTLY) (Only output this if you found location data)

🏠 Neighborhood Feed for [Location] Scanning for High-Impact Growth News...

🏗️ THE "GROWTH" SCOOP (Housing/Development)

Topic: [Headline]

The Hook (Copy/Paste):

"[Draft a 2-3 sentence 'neighborly' post. Sound curious/informed. End with a question.]

PM me if you want to see the site plan or the full builder application!"

Source: [Insert URL]

📸 Image Idea: [Describe the photo/rendering]

🍔 THE "LIFESTYLE" WIN (Restaurant/Retail)

Topic: [Headline]

The Hook (Copy/Paste):

"[Draft post about the new opening/permit].

PM me if you want the details on the opening date!"

Source: [Insert URL]

🛡️ TARGET COMMUNITIES & STRATEGY

Facebook Groups: [Link to FB Search for Location]

Strategy: Join, like 3 posts, wait 24h, then post.

Reddit: [Link to Reddit Search for Location]

Strategy: Find r/[Location], upvote top posts first.

Quora: [Link to Quora Search for Location]

Strategy: Answer "Moving to..." questions.

🔒 PRIVACY NOTICE: All research is private. No data is shared.
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







