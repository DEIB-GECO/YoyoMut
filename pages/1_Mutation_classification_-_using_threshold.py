import time

import streamlit as st

from utils.hill_count import classify_mutations_threshold
from utils.visualization import show_mutation_data
from utils.web_data_prep import data_preparation
from utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="Mutation classification", layout="wide")

smoothed_data_files = data_preparation()

st.markdown("# Mutation classification - threshold algorithm")
st.sidebar.header("Mutation classification - threshold algorithm")
st.write(
    """Choose parameters to classify mutations as yo-yo, fixated or none using the threshold algorithm."""
)

submitted = False
with st.form("parameters", enter_to_submit=False):
    st.write("Please input parameters for mutation classification")
    threshold = int(st.number_input('Threshold (%):', value=30, placeholder='30',
                                    help="The threshold defines the minimal proportion of sequences "
                                         "that must contain the mutation for it to be relevant.")) / 100
    st.divider()

    min_days = int(st.number_input('Minimal duration (in days): ', value=30, placeholder='30',
                                   help="The minimal number of days the mutation needs to be present "
                                        "to be considered significant."))

    st.divider()
    min_percentage = int(
        st.number_input("Minimal percentage for filtering significant lineages:", value=30, placeholder='30',
                        help="The percentage is used to filter out only the lineages that are significant at the"
                             " time period of the mutation being present."))
    st.divider()
    submitted = st.form_submit_button("Submit")

if submitted:
    st.session_state.form_submitted = True
    st.session_state.threshold = threshold
    st.session_state.min_days = min_days
    st.session_state.min_percentage = min_percentage

if st.session_state.get("form_submitted") or 'classify_mutations_threshold' in st.session_state:
    st.session_state.classified_mutations_threshold = classify_mutations_threshold(smoothed_data_files, threshold, min_days)

    yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_threshold)

    st.markdown(f"Number of mutations discovered for the selected parameters:: \n"
                f"- **{len(yo_yo_mutations)}** yo-yo mutations\n"
                f"- **{len(fixated_mutations)}** fixated mutations\n")

    all_mutations, yo_yo, fixated = st.tabs(["All", "Yo-yo", "Fixated"])

    with all_mutations:
        with st.form(key='all', enter_to_submit=False):
            options_all = st.multiselect(
                "Choose or search for a mutation",
                st.session_state.classified_mutations_threshold.keys()
            )

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_all = options_all
                show_mutation_data(st.session_state.classified_mutations_threshold, options_all,
                                   st.session_state.min_percentage)

    with yo_yo:
        with st.form(key='yo-yo', enter_to_submit=False):
            options_yo_yo = st.multiselect(
                "Choose or search for only yo-yo mutations",
                yo_yo_mutations.keys()
            )
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_yo_yo = options_yo_yo
                show_mutation_data(yo_yo_mutations, options_yo_yo, st.session_state.min_percentage)

    with fixated:
        with st.form(key='fixated', enter_to_submit=False):
            options_fixated = st.multiselect(
                "Choose or search for only fixated mutations",
                fixated_mutations.keys()
            )
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_all = options_all
                show_mutation_data(fixated_mutations, options_fixated, st.session_state.min_percentage)
