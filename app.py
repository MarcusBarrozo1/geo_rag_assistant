import streamlit as st
from geo_rag_agent import GeoRAGAgent

TRANSLATIONS = {
    "PT": {
        "title": "🚜 Assistente de Inteligência AgTech",
        "settings": "⚙️ Configurações",
        "language": "🌐 Idioma / Language",
        "sim_mode": "Modo Simulação (Mock)",
        "sim_help": "Desative para usar a API Real do Gemini",
        "field_sel": "📍 Seleção de Talhão",
        "field_prompt": "Escolha o talhão para monitoramento:",
        "clear_chat": "🧹 Limpar Histórico",
        "status": "**Status Atual:** Conectado ao PostgreSQL (Docker) e ChromaDB.",
        "live_telemetry": "📊 Telemetria em tempo real",
        "chat_placeholder": "Ex: Qual o status atual e o que devo fazer?",
        "thinking": "Consultando manuais e sensores...",
        "init": "Inicializando motores de IA e Bancos de Dados..."
    },
    "EN": {
        "title": "🚜 AgTech Intelligence Assistant",
        "settings": "⚙️ Settings",
        "language": "🌐 Idioma / Language",
        "sim_mode": "Simulation Mode (Mock)",
        "sim_help": "Disable to use the Real Gemini API",
        "field_sel": "📍 Field Selection",
        "field_prompt": "Choose the field to monitor:",
        "clear_chat": "🧹 Clear Chat History",
        "status": "**Current Status:** Connected to PostgreSQL (Docker) and ChromaDB.",
        "live_telemetry": "📊 Live Telemetry",
        "chat_placeholder": "Ex: What is the current status and what should I do?",
        "thinking": "Consulting manuals and sensors...",
        "init": "Initializing AI engines and Databases..."
    }
}

# Page configuration
st.set_page_config(page_title = "Geo-RAG Assistant", page_icon = "🚜", layout = "wide")

if "lang" not in st.session_state:
    st.session_state.lang = "PT"  # Default language Portuguese

# Shortcut for translations dictionary
t = TRANSLATIONS[st.session_state.lang]

# AGENT INITIALIZATION (with caching to avoid re-instantiation on every interaction)
if "agent" not in st.session_state:
    with st.spinner(t["init"]):

        st.session_state.agent = GeoRAGAgent(use_mock=True) 
        st.session_state.messages = []

# SIDEBAR: Config and Status
with st.sidebar:
    st.title(t["settings"])

    new_lang = st.selectbox(
        t["language"], 
        ["PT", "EN"], 
        index=0 if st.session_state.lang == "PT" else 1
    )

    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()  # Refresh the app to update translations

    st.divider()

    # Mock vs Real Toggle
    use_mock = st.toggle(t["sim_mode"], value = True, help=t["sim_help"])
    st.session_state.agent.use_mock = use_mock

    st.divider()
    st.subheader(t["field_sel"])
    field_id = st.selectbox(t["field_prompt"], ["FIELD_GAMMA_03", "FIELD_ALPHA_01", "FIELD_BETA_02"])
    
    st.divider()
    if st.button(t["clear_chat"]):
        st.session_state.messages = []
        st.rerun()

# MAIN INTERFACE
st.title(t["title"])
st.markdown(t["status"])

# Live Telemetry Display
st.subheader(f"{t['live_telemetry']}: {field_id}")
telemetry_data = st.session_state.agent._fetch_live_data(field_id)
st.code(telemetry_data, language="text")

st.divider()

# CHAT INTERFACE
# show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# New question input
if prompt := st.chat_input(t["chat_placeholder"]):
    # Add user message to chat history 
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate agent response
    with st.chat_message("assistant"):
        with st.spinner(t["thinking"]):
            response = st.session_state.agent.generate_recommendation(field_id, prompt)
            st.markdown(response)
    
    # Add agent response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    