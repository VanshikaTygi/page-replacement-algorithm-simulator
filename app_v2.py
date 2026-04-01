import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# -----------------------------
# 🎨 GLOBAL STYLE
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #3b82f6, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #94a3b8;
    margin-bottom: 30px;
}

.section {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🚀 HEADER
# -----------------------------
st.markdown('<div class="main-title">⚡ Page Replacement Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Visualize OS Memory Management — FIFO • LRU • Optimal</div>', unsafe_allow_html=True)

# -----------------------------
# 🧭 NAVIGATION (TABS)
# -----------------------------
tab1, tab2, tab3 = st.tabs(["⚙️ Config", "▶ Simulation", "📊 Compare"])

# -----------------------------
# ⚙️ TAB 1 — CONFIG
# -----------------------------
with tab1:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    pages_input = st.text_input("Page Reference String", "7 0 1 2 0 3 0 4")
    frames = st.number_input("Number of Frames", 1, 10, 3)

    algorithm = st.selectbox("Algorithm", ["FIFO", "LRU", "Optimal"])

    col1, col2 = st.columns(2)
    run_btn = col1.button("▶ Run Simulation")
    compare_btn = col2.button("📊 Compare All")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🧠 ALGORITHMS
# -----------------------------
def fifo(pages, capacity):
    memory = []
    faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            faults += 1

    hits = len(pages) - faults
    return hits, faults


def lru(pages, capacity):
    memory = []
    faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            faults += 1
        else:
            memory.remove(page)
            memory.append(page)

    hits = len(pages) - faults
    return hits, faults


def optimal(pages, capacity):
    memory = []
    faults = 0

    for i in range(len(pages)):
        if pages[i] not in memory:
            if len(memory) < capacity:
                memory.append(pages[i])
            else:
                future = pages[i+1:]
                replace = -1
                farthest = -1

                for j in range(len(memory)):
                    if memory[j] not in future:
                        replace = j
                        break
                    else:
                        idx = future.index(memory[j])
                        if idx > farthest:
                            farthest = idx
                            replace = j

                memory[replace] = pages[i]
            faults += 1

    hits = len(pages) - faults
    return hits, faults

# -----------------------------
# ▶ TAB 2 — SIMULATION
# -----------------------------
with tab2:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    if run_btn:
        pages = list(map(int, pages_input.split()))

        if algorithm == "FIFO":
            hits, faults = fifo(pages, frames)
        elif algorithm == "LRU":
            hits, faults = lru(pages, frames)
        else:
            hits, faults = optimal(pages, frames)

        st.success(f"Hits: {hits} | Faults: {faults}")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 📊 TAB 3 — COMPARE
# -----------------------------
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    if compare_btn:
        pages = list(map(int, pages_input.split()))

        f_h, f_f = fifo(pages, frames)
        l_h, l_f = lru(pages, frames)
        o_h, o_f = optimal(pages, frames)

        df = pd.DataFrame({
            "Algorithm": ["FIFO", "LRU", "Optimal"],
            "Hits": [f_h, l_h, o_h],
            "Faults": [f_f, l_f, o_f]
        })

        st.dataframe(df)

    st.markdown('</div>', unsafe_allow_html=True)