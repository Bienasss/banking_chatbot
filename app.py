"""
Streamlit web interface for Banking FAQ Chatbot.
"""

import streamlit as st
from chatbot import BankingChatbot

# Page configuration
st.set_page_config(
    page_title="Banking FAQ Chatbot",
    page_icon="🏦",
    layout="centered"
)

# Initialize chatbot
@st.cache_resource
def load_chatbot(use_fasttext=False):
    """Load and cache the chatbot model."""
    return BankingChatbot(use_fasttext=use_fasttext)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Nustatymai")
    use_fasttext = st.checkbox("Naudoti FastText (vietoj Word2Vec)", value=False)
    
    st.markdown("---")
    st.markdown("### 📚 Informacija")
    st.markdown("""
    Šis chatbot naudoja Word2Vec/FastText embeddings 
    semantiniam panašumui nustatyti.
    
    Jis gali atsakyti į klausimus apie:
    - Sąskaitų atidarymą
    - Mokesčius
    - Internetinio banko prieigą
    - Pavedimus
    - Korteles
    - Indėlius
    - ir daugiau...
    """)

# Main interface
st.title("🏦 Banking FAQ Chatbot")
st.markdown("Sveiki! Aš esu jūsų banko asistentas. Užduokite klausimą, ir aš pabandysiu jums padėti.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chatbot = load_chatbot(use_fasttext=use_fasttext)

# Reload chatbot if FastText setting changed
if st.session_state.get("use_fasttext") != use_fasttext:
    st.session_state.chatbot = load_chatbot(use_fasttext=use_fasttext)
    st.session_state.use_fasttext = use_fasttext

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Užduokite klausimą..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Galvoju..."):
            response = st.session_state.chatbot.get_response(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Example questions
st.markdown("---")
st.markdown("### 💡 Pavyzdiniai klausimai:")
example_questions = [
    "Kaip atidaryti sąskaitą?",
    "Kokie yra sąskaitos valdymo mokesčiai?",
    "Kaip gauti internetinio banko prieigą?",
    "Kiek kainuoja pavedimas į kitą banką?",
    "Kaip pakeisti PIN kodą?"
]

cols = st.columns(len(example_questions))
for i, question in enumerate(example_questions):
    with cols[i]:
        if st.button(question, key=f"example_{i}", use_container_width=True):
            # Add example question to chat
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            
            with st.chat_message("assistant"):
                with st.spinner("Galvoju..."):
                    response = st.session_state.chatbot.get_response(question)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

