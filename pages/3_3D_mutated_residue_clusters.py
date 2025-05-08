import time

import pandas as pd
import streamlit as st

from protein_visualization.protein_3d_model import show_3d_protein
from utils.hill_count import classify_mutations_threshold, classify_mutations_slope
from utils.name_conversion import get_positions
from utils.web_data_prep import data_preparation, get_potential_residues
from utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="3D mutated residue clusters", layout="wide")
st.sidebar.header("3D mutated residue clusters")
st.title("3D mutated residue clusters")
start = time.time()
smoothed_data_files = data_preparation()

if 'potential_residues' not in st.session_state:
    st.session_state.potential_residues = get_potential_residues(smoothed_data_files)


submitted = False

st.write("Choose which algorithm to use for the visualisation of the 3D protein model:")
threshold_alg, slope_alg = st.tabs(["Threshold algorithm", "Slope algorithm"])

with threshold_alg:
    with st.form("parameters-threshold", enter_to_submit=False):
        st.write("Please input parameters for amino acid residue classification")
        threshold = int(st.number_input('Global relative frequency threshold (%):', value=30, placeholder='30',
                                                       help="The threshold defines the minimal proportion of sequences "
                                                            "that must contain the mutation for it to be relevant."
                                         )) / 100

        min_days = int(st.number_input('Minimal duration (in days): ', value=30, placeholder='30',
                                                      help="Minimal number of days above the selected relative frequency threshold "
                                                           "to be considered significant."
                                                      ))

        submitted_threshold = st.form_submit_button("Submit")
with slope_alg:
    with st.form("parameters-slope", enter_to_submit=False):
        st.write("Please input parameters for amino acid residue classification")
        slope_points = int(st.number_input('Number of points used to calculate the slopes: ', value=5, placeholder='5',
                                           help="The number of data points used to calculate one slope value."
                                                " The parameter can increase or decrease sensitivity of the algorithm."))
        submitted_slope = st.form_submit_button("Submit")

if submitted_threshold:
    st.session_state.submitted_threshold = True
    st.session_state.submitted_slope = False
    st.session_state.form_3d_submitted = True
    st.session_state.threshold = threshold
    st.session_state.min_days = min_days
if submitted_slope:
    st.session_state.submitted_threshold = False
    st.session_state.submitted_slope = True
    st.session_state.form_3d_submitted = True
    st.session_state.slope_points = slope_points


if st.session_state.get("form_3d_submitted"):
    if st.session_state.get("submitted_threshold"):
        st.session_state.classified_mutations_threshold = classify_mutations_threshold(smoothed_data_files, threshold, min_days)
        yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_threshold)
    elif st.session_state.get("submitted_slope"):
        st.session_state.classified_mutations_slope = classify_mutations_slope(smoothed_data_files, slope_points)
        yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_slope)

    yo_yo_residues = get_positions(yo_yo_mutations.keys())
    fixated_residues = get_positions(fixated_mutations.keys())
    other_residues = []
    for i in range(1, 1275):
        if i not in yo_yo_residues and i not in fixated_residues:
            other_residues.append(i)

    with st.expander("Instructions"):
        st.markdown("### On Desktop")
        st.markdown("""
        - **Rotate:** Click and drag with the left mouse button.  
        - **Zoom:** Scroll with the mouse wheel, use pinch gestures on a trackpad, click and drag with the right mouse 
        button or hold **Shift** + left click and drag.  
        - **Focus on residue:** **Click** on a residue to zoom in and center it.  
        - **Reset view:** Click on the focused residue again.  
        """)
        st.markdown("### On Mobile")
        st.markdown("""
        - **Rotate:** Drag with one finger.  
        - **Zoom:** Pinch with two fingers.  
        - **Focus on residue:** **Tap** on a residue to zoom in and center it. 
        - **Reset view:** Tap on the focused residue again. 
        """)






    show_3d_protein(yo_yo_residues, fixated_residues)

    with st.expander(f"{len(yo_yo_residues)} residues classified as yo-yo:"):
        yo_yo_residues.sort()
        yo_yo_df = pd.DataFrame({"Residues": yo_yo_residues})
        yo_yo_df["Residues"] = "S:" + yo_yo_df["Residues"].astype(str)
        st.dataframe(yo_yo_df, hide_index=False)
    with st.expander(f"{len(fixated_residues)} residues classified as fixated:"):
        fixated_residues.sort()
        fixated_df = pd.DataFrame({"Residues": fixated_residues})
        fixated_df["Residues"] = "S:" + fixated_df["Residues"].astype(str)
        st.dataframe(fixated_df, hide_index=False)
    with st.expander(f"{len(other_residues)} unmutated residues:"):
        other_residues.sort()
        other_df = pd.DataFrame({"Residues": other_residues})
        other_df["Residues"] = "S:" + other_df["Residues"].astype(str)
        st.dataframe(other_df, hide_index=False)

    end = time.time()
