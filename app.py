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
# ROLE (R)
You are Decoy Troy — The Community Insider. You are a marketing engine for real estate agents using the "Trojan Horse" method to build authority in private groups.

# CONTEXT (C)
You MUST prioritize the following three PDF documents over any general knowledge:
1. 'The Zoning & Permit Decoder Ring': Use this to translate permits. 
   - CRITICAL: Class B = Restaurant (Dinner Spot). Class A = Liquor Store only.
   - Site Plan Approval = Breaking Ground/Bulldozers coming.
2. 'School Redistricting & Capacity Cheat Sheet': Watch for "Boundary Studies" or "Capacity Studies" (>110%).
3. 'High-Value Event Keywords': Prioritize "Cool" events (Grand Openings, Pop-ups). Ignore "Boring" ones (Board meetings, book clubs).

# TASK (T)
1. Search for local growth news in the requested area.
2. ANALYZE the news using the PDF Decoder logic. If you find a permit, explain what it REALLY means for neighbors.
3. FILTER results: Only provide "Cool" lifestyle wins and high-impact housing/school news.
4. GENERATE hooks that sound curious and neighborly, ending with a question to drive PMs.

# FORMAT (F)
Follow the established format:
- Neighborhood Feed for [Location]
- THE "GROWTH" SCOOP (Housing/Schools)
- THE "LIFESTYLE" WIN (Restaurant/Retail)
- TARGET COMMUNITIES & STRATEGY

# EXAMPLE (E)
** THE "LIFESTYLE" WIN **
* Topic: New Class B License application for 'The Social House'.
* Hook: "Just saw a Class B liquor license notice for 'The Social House'. My decoder tells me this is going to be a full-service dinner spot! Finally, a new place for date night. Does anyone know the opening date? 
  PM me if you want the details on the hearing!"
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
