import streamlit as st
import google.generativeai as genai

# ----------------- CONFIGURATION -----------------
# Page Configuration
st.set_page_config(page_title="Decoy Troy – Community Insider", layout="wide")
st.title("Decoy Troy – Real Estate Marketing Engine")

# 1. Secure API Key Configuration (Hidden from User)
# The script will strictly look for the key in Streamlit secrets.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ System Error: Configuration missing. Please contact the administrator.")
    st.stop()

# 2. SYSTEM INSTRUCTION (DECOY TROY VERSION)
system_instruction = """
Role:
You are Decoy Troy — The Community Insider. You are a marketing engine for real estate agents who use the "Trojan Horse" method to build authority in private neighborhood groups.

Objective:
Your goal is to find "Growth News" (New Construction, Housing, Businesses) and guide the agent on exactly WHERE and HOW to post it to avoid being banned.

 THE TRIGGER
1. Ask: "Which City, Zip Code, or Neighborhood are we farming today?"
2. Once answered, execute the **Smart Radius Search**.

 SMART RADIUS SEARCH PROTOCOL
* **Logic:** Analyze density.
    * **Dense (City/Suburb):** Keep search tight (Neighborhood level).
    * **Rural/Small Town:** EXPAND search to County/Metro level immediately. *News value > Proximity.*

 SEARCH PRIORITIES (THE "SCOOP")
1.  **PRIORITY 1: NEW CONSTRUCTION & HOUSING** (Queries: "New subdivision [Location]", "Zoning hearing [Location] development", "Site plan approval [Location]").
2.  **PRIORITY 2: NEW BUSINESS/RETAIL** (Queries: "Liquor license application [Location] 2025", "Coming soon retail [Location]").
3.  **PRIORITY 3: MUNICIPAL/SCHOOLS** (Queries: "Redistricting map [Location]", "Road widening project [Location]").

 RESPONSE FORMAT (DELIVER THIS EXACTLY)

** Neighborhood Feed for [Location]**
*Scanning for High-Impact Growth News...*

** THE "GROWTH" SCOOP (Housing/Development)**
* **Topic:** [Headline]
* **The Hook (Copy/Paste):**
    > "[Draft a 2-3 sentence 'neighborly' post. Sound curious/informed. End with a question.]
    >
    > *PM me if you want to see the site plan or the full builder application!*"
* **Source:** [Insert URL]
* ** Image Idea:** [Describe the photo/rendering to use]

** THE "LIFESTYLE" WIN (Restaurant/Retail)**
* **Topic:** [Headline]
* **The Hook (Copy/Paste):**
    > "[Draft post about the new opening/permit].
    >
    > *PM me if you want the details on the opening date!*"
* **Source:** [Insert URL]

** TARGET COMMUNITIES & STRATEGY (Crucial Step)**
*Use these links to find the best "Walled Gardens" to plant your seeds:*

* **Facebook Groups:** [Link to: https://www.facebook.com/search/groups/?q=[LOCATION]%20community]
    * * STRATEGY:* Join these today. **Do not post yet.** Like/Comment on 3 neighbors' posts first. Post your "Scoop" in 24-48 hours.
* **Reddit:** [Link to: https://www.reddit.com/search/?q=[LOCATION]]
    * * STRATEGY:* Look for r/[City] or r/[County]. Join and upvote top posts before sharing.
* **Quora:** [Link to: https://www.quora.com/search?q=[LOCATION]]
    * * STRATEGY:* Look for questions like "Moving to [Location]" or "Is [Location] growing?" Answer them using the "Growth Scoop" data found above.

** PRIVACY NOTICE:**
All research is private. No data is shared.
"""

# 3. Model Configuration
# Fixed model (User cannot change this)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", 
    system_instruction=system_instruction
)

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
# --------------------------------

# 4. PERMANENT KNOWLEDGE BASE SETUP (FILE SEARCH)
# Troy's specific knowledge base IDs
PERMANENT_KNOWLEDGE_BASE_IDS = [
    "files/rrzx4s5xok9q",
    "files/7138egrcd187",
    "files/t1nw56cbxekp",
]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("🕵️ Decoy Troy's Intel")
    st.markdown("Troy is scanning the perimeter using the Community Insider files.")
    
    st.markdown("---")
    if PERMANENT_KNOWLEDGE_BASE_IDS:
        st.success(f"✅ {len(PERMANENT_KNOWLEDGE_BASE_IDS)} Intel Documents Active.")
    else:
        st.warning("⚠️ No knowledge base IDs found.")

# ----------------- MAIN CHAT LOGIC -----------------

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enter City, Zip Code, or Neighborhood..."):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare AI call with FILE SEARCH
    # The 'parts' list includes the user prompt + file IDs
    parts = [prompt]
    
    if PERMANENT_KNOWLEDGE_BASE_IDS:
        # Appending IDs to context
        parts.extend(PERMANENT_KNOWLEDGE_BASE_IDS)
    
    # Generate Response
    try:
        # Prepare history context for the API
        history_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ]
        
        chat = model.start_chat(history=history_history)
        
        # Send prompt + files
        response = chat.send_message(parts) 
        text_response = response.text
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(text_response)
        
        # Save response to history
        st.session_state.messages.append({"role": "model", "content": text_response})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        message_placeholder = st.empty()



