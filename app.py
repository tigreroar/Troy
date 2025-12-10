import streamlit as st
import google.generativeai as genai
import os


# Configuración de página
st.set_page_config(
    page_title="Decoy Troy - Community Insider",
    page_icon="🐴",
    layout="wide"
)

# Estilos personalizados (CSS)
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2E86C1;
    }
    div[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE SIDEBAR ---
with st.sidebar:
    st.title("🐴 Decoy Troy")
    st.subheader("The Trojan Horse Marketing Engine")
    
    # Input de API Key
    api_key = st.text_input("Ingresa tu Gemini API Key", type="password")
    
    # Selección de Modelo
    model_choice = st.selectbox(
        "Selecciona el Modelo",
        ["gemini-1.5-pro-latest", "gemini-2.0-flash-exp", "gemini-1.5-flash-latest"],
        index=0,
        help="Se recomienda Pro para razonamiento profundo o Flash 2.0 para velocidad."
    )
    
    st.info("Este agente busca noticias de construcción, licencias y aperturas para crear contenido de autoridad.")
    
    if st.button("Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()

# --- CONFIGURACIÓN DE GEMINI Y SYSTEM PROMPT ---

# IDs de la Base de Conocimiento (Archivos subidos)
# Nota: Para que esto funcione, los archivos deben haber sido subidos con tu misma API Key.
PERMANENT_KNOWLEDGE_BASE_IDS = [
    "files/rrzx4s5xok9q",
    "files/7138egrcd187",
    "files/t1nw56cbxekp"
]

def get_system_instruction():
    return """
    You are Decoy Troy — The Community Insider. You are a marketing engine for real estate agents who use the "Trojan Horse" method to build authority in private neighborhood groups.

    Objective:
    Your goal is to find "Growth News" (New Construction, Housing, Businesses) and guide the agent on exactly WHERE and HOW to post it to avoid being banned.

    THE TRIGGER:
    1. Ask: "Which City, Zip Code, or Neighborhood are we farming today?"
    2. Once answered, execute the **Smart Radius Search**.

    SMART RADIUS SEARCH PROTOCOL:
    * **Logic:** Analyze density.
        * **Dense (City/Suburb):** Keep search tight (Neighborhood level).
        * **Rural/Small Town:** EXPAND search to County/Metro level immediately. *News value > Proximity.*

    SEARCH PRIORITIES (THE "SCOOP"):
    * Use Google Search to find real-time data.
    1.  **PRIORITY 1: NEW CONSTRUCTION & HOUSING** (Queries: "New subdivision [Location]", "Zoning hearing [Location] development", "Site plan approval [Location]").
    2.  **PRIORITY 2: NEW BUSINESS/RETAIL** (Queries: "Liquor license application [Location] 2025", "Coming soon retail [Location]").
    3.  **PRIORITY 3: MUNICIPAL/SCHOOLS** (Queries: "Redistricting map [Location]", "Road widening project [Location]").

    RESPONSE FORMAT (DELIVER THIS EXACTLY):

    **Neighborhood Feed for [Location]**
    *Scanning for High-Impact Growth News...*

    **THE "GROWTH" SCOOP (Housing/Development)**
    * **Topic:** [Headline]
    * **The Hook (Copy/Paste):**
        > "[Draft a 2-3 sentence 'neighborly' post. Sound curious/informed. End with a question.]
        >
        > *PM me if you want to see the site plan or the full builder application!*"
    * **Source:** [Insert URL found in search]
    * **Image Idea:** [Describe the photo/rendering to use]

    **THE "LIFESTYLE" WIN (Restaurant/Retail)**
    * **Topic:** [Headline]
    * **The Hook (Copy/Paste):**
        > "[Draft post about the new opening/permit].
        >
        > *PM me if you want the details on the opening date!*"
    * **Source:** [Insert URL found in search]

    **TARGET COMMUNITIES & STRATEGY (Crucial Step)**
    *Use these links to find the best "Walled Gardens" to plant your seeds:*

    * **Facebook Groups:** [Create dynamic Link: https://www.facebook.com/search/groups/?q=[LOCATION]%20community]
        * *STRATEGY:* Join these today. **Do not post yet.** Like/Comment on 3 neighbors' posts first. Post your "Scoop" in 24-48 hours.
    * **Reddit:** [Create dynamic Link: https://www.reddit.com/search/?q=[LOCATION]]
        * *STRATEGY:* Look for r/[City] or r/[County]. Join and upvote top posts before sharing.
    * **Quora:** [Create dynamic Link: https://www.quora.com/search?q=[LOCATION]]
        * *STRATEGY:* Look for questions like "Moving to [Location]" or "Is [Location] growing?" Answer them using the "Growth Scoop" data found above.

    **PRIVACY NOTICE:**
    All research is private. No data is shared.
    """

# --- LÓGICA DE CHAT ---

if "messages" not in st.session_state:
    # Mensaje inicial de "Trigger"
    st.session_state.messages = [
        {"role": "model", "content": "Which City, Zip Code, or Neighborhood are we farming today?"}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar input del usuario
if prompt := st.chat_input("Ej: Plano, TX o 75024..."):
    
    if not api_key:
        st.error("Por favor ingresa tu API Key en la barra lateral.")
        st.stop()

    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        genai.configure(api_key=api_key)
        
        # Configuración de herramientas (Search + Knowledge Base)
        # Nota: La búsqueda es crucial para este agente.
        tools = [
            {"google_search": {}} # Habilitar búsqueda en Google
        ]

        # Configuración del modelo
        generation_config = {
            "temperature": 0.4, # Baja temperatura para datos precisos
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }

        # Inicializar modelo
        # NOTA: No podemos inyectar los IDs de archivos directamente en el constructor 'model' 
        # sin recuperarlos primero con genai.get_file(), pero esto requiere permisos.
        # Por robustez, pasamos la instrucción en el system prompt y activamos tools.
        # Si tus archivos están cacheados en un endpoint específico, la configuración sería distinta.
        
        model = genai.GenerativeModel(
            model_name=model_choice,
            generation_config=generation_config,
            system_instruction=get_system_instruction(),
            tools=tools
        )

        # Crear chat history compatible con la API
        history_api = []
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            history_api.append({"role": role, "parts": [msg["content"]]})

        # Generar respuesta
        with st.chat_message("model"):
            with st.spinner("Decoy Troy está escaneando permisos de construcción y noticias locales..."):
                chat = model.start_chat(history=history_api[:-1]) # Todo menos el último
                response = chat.send_message(prompt)
                st.markdown(response.text)
                
        # Guardar respuesta
        st.session_state.messages.append({"role": "model", "content": response.text})

    except Exception as e:

        st.error(f"Ocurrió un error: {e}")
