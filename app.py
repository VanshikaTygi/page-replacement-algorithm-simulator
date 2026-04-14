import streamlit as st
import pandas as pd
import time

from algorithms import fifo_steps, lru, optimal

def render_frames(frame_list):
    html = '<div style="display:flex; gap:10px; margin:10px 0; align-items:center;">'
    
    for val in frame_list:
        html += f"""<div style="
            width:50px;
            height:50px;
            border:2px solid #333;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:18px;
            font-weight:bold;
            border-radius:8px;
            background-color:#f0f2f6;
        ">
            {val}
        </div>"""
    
    html += "</div>"
    return html

st.set_page_config(page_title="Page Replacement Simulator", layout="wide")

st.title("⚡ Page Replacement Simulator")
st.write("Visualize OS Memory Management — FIFO • LRU • Optimal")

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["⚙ Config", "▶ Simulation", "📊 Compare"])

# -------------------------------
# TAB 1 — CONFIG
# -------------------------------
with tab1:
    st.header("Configuration")

    pages_input = st.text_input("Page Reference String", "7 0 1 2 0 3 0 4")
    frames = st.number_input("Number of Frames", 1, 10, 3)
    algorithm = st.selectbox("Algorithm", ["FIFO", "LRU", "Optimal"])

    col1, col2 = st.columns(2)
    run_btn = col1.button("▶ Run Simulation")
    compare_btn = col2.button("📊 Compare All")

    # RUN SIMULATION
    if run_btn:
        pages = list(map(int, pages_input.split()))

        if algorithm == "FIFO":
            hits, faults, steps = fifo_steps(pages, frames)
        elif algorithm == "LRU":
            hits, faults = lru(pages, frames)
            steps = []
        else:
            hits, faults = optimal(pages, frames)
            steps = []

        st.session_state["result"] = {
            "hits": hits,
            "faults": faults,
            "steps": steps,
            "frames": frames
        }

    # COMPARE ALL
    if compare_btn:
        pages = list(map(int, pages_input.split()))

        f_h, f_f, _ = fifo_steps(pages, frames)
        l_h, l_f = lru(pages, frames)
        o_h, o_f = optimal(pages, frames)

        df = pd.DataFrame({
            "Algorithm": ["FIFO", "LRU", "Optimal"],
            "Hits": [f_h, l_h, o_h],
            "Faults": [f_f, l_f, o_f]
        })

        st.session_state["compare"] = df


# -------------------------------
# TAB 2 — SIMULATION
# -------------------------------
with tab2:
    st.header("Simulation")

    if "result" in st.session_state:
        result = st.session_state["result"]

        st.success(f"Hits: {result['hits']} | Faults: {result['faults']}")

        steps = result["steps"]
        frames = result["frames"]

        st.write("### Step-by-Step Execution")

        # 🔥 NEW BUTTON
        if "animate" not in st.session_state:
            st.session_state.animate = False

        if st.button("▶ Start Animation"):
            st.session_state.animate = True

        if st.session_state.animate:

            for i, step in enumerate(steps):
                display = step + ["-"] * (frames - len(step))
                st.write(f"Step {i+1}")

                html = render_frames(display)
                st.markdown(html, unsafe_allow_html=True)
                time.sleep(0.8)

            st.session_state.animate = False

        else:
            st.info("Click 'Start Animation' to visualize steps")

    else:
        st.warning("⚠ Run simulation from Config tab first")


# -------------------------------
# TAB 3 — COMPARE
# -------------------------------
with tab3:
    st.header("Comparison")

    if "compare" in st.session_state:
        st.dataframe(st.session_state["compare"])
    else:
        st.warning("⚠ Click 'Compare All' in Config tab first")