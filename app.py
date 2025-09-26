import streamlit as st
from blockchain import Blockchain

# Initialize Blockchain (only once)
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.set_page_config(page_title="Blockchain Diary", layout="centered")

st.title("📘 Blockchain-based Digital Diary")
st.markdown("""
Write your daily entries. Once saved, they are stored on a tamper-proof blockchain.  
Great for permanent records in hospitals, research, journaling, or education!
""")

entry = st.text_area("✍️ Write your note for today:", height=150)

if st.button("Add to Blockchain"):
    if entry.strip() == "":
        st.warning("Note cannot be empty.")
    else:
        st.session_state.blockchain.add_block(entry)
        st.success("✅ Entry added to blockchain!")

st.markdown("---")
st.subheader("⛓️ Blockchain Timeline")

for block in reversed(st.session_state.blockchain.chain):
    with st.expander(f"📦 Block #{block.index} | {block.timestamp}"):
        st.code(f"""
Data: {block.data}
Hash: {block.hash}
Previous Hash: {block.previous_hash}
        """, language='text')

# Optional: Show validation status
st.markdown("---")
if st.session_state.blockchain.is_chain_valid():
    st.success("✅ Blockchain is valid and secure.")
else:
    st.error("⚠️ Blockchain is invalid. Tampering detected!")
