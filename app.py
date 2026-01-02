import streamlit as st
import rag_backend 
import os
import time  # New import for smoothing

st.set_page_config(page_title="Academic Workspace", layout="wide")

if "history_map" not in st.session_state:
    st.session_state.history_map = {}

# --- SIDEBAR ---
with st.sidebar:
    st.title("📚 Library")
    available_pdfs = [f for f in os.listdir(rag_backend.DATA_DIR) if f.endswith('.pdf')]
    selected_book = st.selectbox("Focus Workspace:", ["All"] + available_pdfs)

    if selected_book not in st.session_state.history_map:
        st.session_state.history_map[selected_book] = []

    st.divider()
    if st.session_state.history_map[selected_book]:
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.history_map[selected_book]])
        st.download_button("💾 Download Notes", data=chat_text, file_name=f"{selected_book}_notes.txt")

    uploaded = st.file_uploader("Upload PDF", type="pdf")
    if uploaded and st.button("Index and Sync"):
        with st.spinner("Processing..."):
            with open(os.path.join(rag_backend.DATA_DIR, uploaded.name), "wb") as f:
                f.write(uploaded.getbuffer())
            rag_backend.get_vector_store(force_rebuild=True)
            st.rerun()

# --- MAIN CHAT ---
st.title(f"🤖 Research Assistant: {selected_book}")
history = st.session_state.history_map[selected_book]

# Render persistent history
for m in history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat Input
if prompt := st.chat_input("Ask a question...", key=f"input_{selected_book}"):
    history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # The placeholder is outside the loop to prevent flickering
        placeholder = st.empty()
        full_response = ""
        
        vs = rag_backend.get_vector_store()
        
        # We process the stream from the backend
        for chunk in rag_backend.stream_query(prompt, vs, history, selected_book):
            # Split chunks into words to simulate typing if chunks are too big
            for word in chunk.split(" "):
                full_response += word + " "
                # Update the UI with a typing cursor
                placeholder.markdown(full_response + "▌")
                # THE SECRET SAUCE: A tiny delay (0.02s - 0.05s) creates the smooth flow
                time.sleep(0.03) 
        
        # Final update to remove the cursor
        placeholder.markdown(full_response)
        history.append({"role": "assistant", "content": full_response})