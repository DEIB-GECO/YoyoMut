import time

import streamlit as st

from utils.hill_count import classify_mutations_threshold
from utils.name_conversion import get_positions
from utils.visualization import show_mutation_data
from utils.web_data_prep import data_preparation, sort_by_residue_number
from utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="Mutation classification", layout="wide")

st.title("Classification of residues by relative frequency threshold", anchor=False)

st.sidebar.header("Classification of residues by relative frequency threshold")
st.write(
    """
    Choose parameters to classify amino acid residues as unmutated, yo-yo mutated, or fixated mutation using the threshold algorithm.
    """
)

if 'smoothed_data_files_sequences' not in st.session_state:
    with st.status("Loading data...", expanded=False) as status:
        st.session_state.smoothed_data_files_sequences = data_preparation(by_days=False)
        status.update(label="Data loaded successfully!", state="complete", expanded=False)

submitted = False
with st.form("parameters", enter_to_submit=False):
    st.write("Please input parameters for amino acid residue classification")
    threshold = st.number_input('Global relative frequency threshold (0-1):', value=0.3, placeholder='0.3',
                                min_value=0.0,
                                max_value=1.0,
                                help="The threshold defines the minimal proportion of sequences "
                                     "that must contain the mutation for it to be relevant.")
    st.divider()

    min_days = st.number_input('Minimal duration (in days): ', value=30, placeholder='30',
                               help="Minimal number of days above the selected relative frequency threshold "
                                    "to be considered significant.")

    st.divider()
    min_percentage = st.number_input(
        "Minimum relative prevalence for filtering significant PANGO lineages with the selected mutation:", value=30,
        placeholder='30',
        help="The percentage is used to filter out only the lineages that are significant at the"
             " time period of the mutation being present.")
    st.divider()
    submitted = st.form_submit_button("Submit")

if submitted:
    st.session_state.form_submitted = True
    st.session_state.threshold = threshold
    st.session_state.min_days = min_days
    st.session_state.min_percentage = min_percentage

if st.session_state.get("form_submitted") or 'classify_mutations_threshold' in st.session_state:
    st.session_state.classified_mutations_threshold = classify_mutations_threshold(
        st.session_state.smoothed_data_files_sequences,
        threshold, min_days)
    yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_threshold)

    yo_yo_mutations_general = len(get_positions(yo_yo_mutations.keys()))
    yo_yo_mutations_specific = len(yo_yo_mutations) - yo_yo_mutations_general

    fixated_mutations_general = len(get_positions(fixated_mutations.keys()))
    fixated_mutations_specific = len(fixated_mutations) - fixated_mutations_general

    st.markdown(f"Number of mutations discovered for the selected parameters:: \n"
                f"- **{yo_yo_mutations_general}** general yo-yo mutated residues (any amino acid different than original)\n"
                f"- **{yo_yo_mutations_specific}** specific yo-yo mutations (specific amino acid it mutated to)\n"
                f"- **{fixated_mutations_general}** general fixated residues (any amino acid different than original)\n"
                f"- **{fixated_mutations_specific}** specific fixated mutations (specific amino acid it mutated to\n")

    all_mutations, yo_yo, fixated = st.tabs(["All", "Yo-yo", "Fixated"])

    with all_mutations:
        sorted_keys = sort_by_residue_number(st.session_state.classified_mutations_threshold.keys())
        with st.form(key='all', enter_to_submit=False):
            options_all = st.multiselect(
                "Choose or search for an amino acid residue",
                sorted_keys
            )

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_all = options_all
                show_mutation_data(st.session_state.classified_mutations_threshold, options_all,
                                   st.session_state.min_percentage)

    with yo_yo:
        sorted_keys = sort_by_residue_number(yo_yo_mutations.keys())
        with st.form(key='yo-yo', enter_to_submit=False):
            options_yo_yo = st.multiselect(
                "Choose or search for only yo-yo mutations",
                sorted_keys
            )
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_yo_yo = options_yo_yo
                show_mutation_data(yo_yo_mutations, options_yo_yo, st.session_state.min_percentage)

    with fixated:
        sorted_keys = sort_by_residue_number(fixated_mutations.keys())
        with st.form(key='fixated', enter_to_submit=False):
            options_fixated = st.multiselect(
                "Choose or search for only fixated mutations",
                sorted_keys
            )
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_all = options_all
                show_mutation_data(fixated_mutations, options_fixated, st.session_state.min_percentage)
