import streamlit as st
from datetime import datetime
import hashlib

# ===============================
# Blockchain Classes
# ===============================
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, str(datetime.now()), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=str(datetime.now()),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.compute_hash() or curr.previous_hash != prev.hash:
                return False
        return True

# ===============================
# Streamlit App
# ===============================
st.set_page_config(page_title="Blockchain Diary", layout="wide")

# Initialize Blockchain in session state
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# ===============================
# Sidebar Navigation
# ===============================
st.sidebar.title("🔗 Blockchain Diary")
page = st.sidebar.radio("Go to", ["📝 New Entry", "📜 Record History"])

# ===============================
# 📝 New Entry Page
# ===============================
if page == "📝 New Entry":
    st.title("📝 Add New Diary Entry")
    st.markdown("Your entries are permanently stored using blockchain technology. Once submitted, they can't be changed.")

    with st.expander("➕ Create a New Entry"):
        entry = st.text_area("✍️ What did you learn or do today?", height=150)
        if st.button("🔐 Save to Blockchain"):
            if entry.strip():
                blockchain.add_block(entry.strip())
                st.success("✅ Entry successfully added to the blockchain.")
            else:
                st.warning("⚠️ Please enter something before submitting.")

    st.info("📜 View your full diary record in the **Record History** tab.")

# ===============================
# 📜 Record History Page
# ===============================
elif page == "📜 Record History":
    st.title("📜 Blockchain Record History")
    st.markdown("Below is the complete, tamper-proof record of your diary entries.")

    if len(blockchain.chain) <= 1:
        st.info("No entries found yet. Add your first entry from the 'New Entry' tab.")
    else:
        for block in reversed(blockchain.chain[1:]):  # Skip Genesis block
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
                    with st.expander("🔍 View Full Entry", expanded=False):
                     st.markdown(f"""
                    <div style='padding: 1rem; background-color: #1e1e1e; border-radius: 10px; color: white;'>
                        {block.data.replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)


        st.markdown("---")
        if blockchain.is_chain_valid():
            st.success("✅ Blockchain is valid.")
        else:
            st.error("❌ Blockchain has been tampered with.")

