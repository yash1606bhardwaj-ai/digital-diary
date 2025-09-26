import streamlit as st
from blockchain import Blockchain

st.set_page_config(page_title="Blockchain Diary", layout="wide")

# Initialize blockchain in session
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

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
        st.page_link("pages/1_History.py", label="🔍 View Full History", icon="📜")

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

st.markdown("👈 View full diary record from the **History** section.")
