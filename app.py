import streamlit as st

st.title("Page Replacement Algorithm Simulator")

st.write("Welcome! This tool compares FIFO, LRU, and Optimal algorithms.")

# Input
pages_input = st.text_input("Enter page reference string (space-separatd):")


frames = st.number_input("Enter number of frames: ", min_value=1, step=1)

if st.button("Run Simulation") :
    
    # step 1: Convert input string to list
    try :
        pages = list(map(int, pages_input.split()))

        # step 2: Show converted list
        st.write("Converted Pages: ", pages)
        st.write("Number of Frames: ", frames)

    except :
        st.error("Invalid input! Please enter numbers separated by spaces.")