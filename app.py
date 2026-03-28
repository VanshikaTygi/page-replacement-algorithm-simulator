import streamlit as st
from algorithms import fifo, lru, optimal

st.title("Page Replacement Algorithm Simulator")

st.write("Welcome! This tool compares FIFO, LRU, and Optimal algorithms.")

# Input
pages_input = st.text_input("Enter page reference string (space-separatd):")


frames = st.number_input("Enter number of frames: ", min_value=1, step=1)

algorithm = st.selectbox(
    "Choose Algorithm: ", ["FIFO", "LRU", "Optimal"] 
)

if st.button("Run Simulation") :
    
    # step 1: Convert input string to list
    try :
        pages = list(map(int, pages_input.split()))

        # step 2: Show converted list
        st.write("Converted Pages: ", pages)
        st.write("Number of Frames: ", frames)

        if algorithm == "FIFO" :
            # Call FIFO algorithm
            hits, faults = fifo(pages, frames)

        elif algorithm == "LRU" :
            # Call LRU algorithm
            hits, faults = lru(pages, frames)

        elif algorithm == "Optimal" :
            # Call Optimal algorithm
            hits, faults = optimal(pages, frames)

        # Show result 
        st.success(f"{algorithm} Results -> Hits : {hits}, Faults : {faults}")

        total = hits + faults

        if total > 0 :
            hit_ratio = hits / total
            fault_ratio = faults / total
        else :
            hit_ratio = 0
            fault_ratio = 0

        st.info(f"Hit Ratio : {hit_ratio:.2f}")
        st.info(f"Fault Ratio : {fault_ratio:.2f}")

    except Exception as e :
        st.error(f"Error : {e}")

