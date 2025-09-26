import streamlit as st
from blockchain import Blockchain

# Initialize the blockchain in session
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

st.set_page_config(page_title="Blockchain Diary", layout="wide")

# =============================
# TOP NAVIGATION BAR
# =============================
with st.container():
    cols = st.columns([1, 1, 1, 1, 1, 2])
    with cols[0]:
        st.markdown("### 🧿 Chronos")
    with cols[1]:
        st.button("📄 Dashboard")
    with cols[2]:
        st.button("📝 New Entry")
    with cols[3]:
        st.button("⚙️ Settings")
    with cols[4]:
        st.button("💬 Support")
    with cols[5]:
        st.button("🔍 View Full Entry")

# =============================
# PAGE HEADER
# =============================
st.markdown("## 📘 Decure Digacy Diary")
st.markdown("A tamper-proof digital diary secured with blockchain.")

# =============================
# NEW ENTRY FORM
# =============================
with st.expander("➕ Add New Entry"):
    st.markdown("Write your daily entry. Once submitted, it will be locked into the blockchain.")
    entry = st.text_area("✍️ Diary Entry", height=150)
    if st.button("🧱 Add Entry to Blockchain"):
        if entry.strip():
            blockchain.add_block(entry.strip())
            st.success("✅ Entry added to blockchain.")
        else:
            st.warning("Entry cannot be empty.")

# =============================
# BLOCKCHAIN RECORDS HISTORY
# =============================
st.markdown("---")
st.markdown("### ⛓️ Blockchain Record History")

if len(blockchain.chain) <= 1:
    st.info("No entries yet. Add your first diary block above.")
else:
    for block in reversed(blockchain.chain[1:]):  # skip genesis
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5, 2, 2, 1])
            with col1:
                st.markdown(f"#### 📦 #{block.index}")
                st.markdown(f"🕓 {block.timestamp[:16]}")
            with col2:
                st.markdown(f"**Entry Summary**: {block.data[:60]}{'...' if len(block.data) > 60 else ''}")
                st.caption(f"Hash: `{block.hash[:12]}...`")
            with col3:
                st.markdown("**Previous Hash**")
                st.code(block.previous_hash[:16] + "...", language='text')
            with col4:
                with st.expander("🔎 View Full Entry"):
                    st.code(block.data, language='markdown')

# =============================
# BLOCKCHAIN STATUS
# =============================
st.markdown("---")
if blockchain.is_chain_valid():
    st.success("✅ Blockchain is valid and untampered.")
else:
    st.error("❌ Blockchain integrity compromised!")
