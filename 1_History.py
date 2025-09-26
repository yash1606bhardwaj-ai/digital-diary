import streamlit as st
from blockchain import Blockchain

st.set_page_config(page_title="Blockchain History", layout="wide")

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

st.title("📜 Blockchain Record History")

st.markdown("View all past diary entries recorded securely on the blockchain.")

if len(blockchain.chain) <= 1:
    st.info("No entries yet.")
else:
    for block in reversed(blockchain.chain[1:]):  # skip genesis block
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5, 2, 2, 1])
            with col1:
                st.markdown(f"#### 📦 Block #{block.index}")
                st.caption(f"🕒 {block.timestamp[:16]}")
            with col2:
                st.markdown(f"**Entry Summary**: {block.data[:60]}{'...' if len(block.data) > 60 else ''}")
                st.caption(f"🔗 Hash: `{block.hash[:12]}...`")
            with col3:
                st.markdown("**Previous Hash**")
                st.code(block.previous_hash[:16] + "...", language='text')
            with col4:
                with st.expander("🔍 View Full Entry"):
                    st.code(block.data, language='markdown')

# Blockchain status
st.markdown("---")
if blockchain.is_chain_valid():
    st.success("✅ Blockchain is valid.")
else:
    st.error("❌ Blockchain has been tampered with.")
