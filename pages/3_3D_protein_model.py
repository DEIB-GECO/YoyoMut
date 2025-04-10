import time

import pandas as pd
import streamlit as st

from protein_visualization.protein_3d_model import show_3d_protein
from utils.hill_count import classify_mutations_threshold
from utils.name_conversion import get_residues
from utils.visualization import show_mutation_data
from utils.web_data_prep import data_preparation
from utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="3D protein model", layout="wide")
st.sidebar.header("3D protein model")
st.title("3D model of the Spike protein")
print('started 3d page')
start = time.time()
smoothed_data_files = data_preparation()

@st.cache_data
def classify_mutations(smoothed_data_files, threshold, min_days):
    start = time.time()
    result = classify_mutations_threshold(smoothed_data_files, threshold, min_days)
    end = time.time()
    print('classify mutations ended after: ', end-start)
    return result

submitted = False
with st.form("parameters", enter_to_submit=False):
    st.write("Please input parameters for mutation classification")
    threshold = int(st.number_input('Threshold (%):', value=30, placeholder='30',
                                                   help="The threshold defines the minimal proportion of sequences "
                                                        "that must contain the mutation for it to be relevant."
                                     )) / 100

    min_days = int(st.number_input('Minimum length (in days): ', value=30, placeholder='30',
                                                  help="The minimal number of days the mutation needs to be present "
                                                       "to be considered significant."
                                                  ))

    submitted = st.form_submit_button("Submit", on_click=lambda: classify_mutations(smoothed_data_files, threshold, min_days))

if submitted:
    st.session_state.form_3d_submitted = True
    st.session_state.threshold = threshold
    st.session_state.min_days = min_days

if st.session_state.get("form_3d_submitted"):
    st.session_state.classified_mutations_slope = classify_mutations(smoothed_data_files, threshold, min_days)

    yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_slope)

    yo_yo_residues = get_residues(yo_yo_mutations.keys())
    fixated_residues = get_residues(fixated_mutations.keys())
    other_residues = []
    for i in range(1, 1275):
        if i not in yo_yo_residues and i not in fixated_residues:
            other_residues.append(i)

    with st.expander("Instructions"):
        st.write("- the model can be rotated")
        st.write("- zoom in/out is possible by scrolling")
        st.write("- hovering over a residue shows the amino acid and position")
        st.write("- clicking on a residue focuses and zooms in on the residue, to reset, click on the residue again")
        st.write("- different styles and colors can be chosen for each class of residues")



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
    with st.expander(f"{len(other_residues)} unclassified residues:"):
        other_residues.sort()
        other_df = pd.DataFrame({"Residues": other_residues})
        other_df["Residues"] = "S:" + other_df["Residues"].astype(str)
        st.dataframe(other_df, hide_index=False)

    end = time.time()
    print('finished 3d page in ', end-start)
