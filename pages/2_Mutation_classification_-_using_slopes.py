import time

import streamlit as st

from recognition_algorithm.utils.hill_count import classify_mutations_slope
from recognition_algorithm.utils.visualization import show_mutation_data
from recognition_algorithm.utils.web_data_prep import data_preparation
from recognition_algorithm.utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="Mutation classification", layout="wide")

smoothed_data_files = data_preparation(by_days=True)

st.markdown("# Mutation classification - slope algorithm")
st.sidebar.header("Mutation classification - slope algorithm")
st.write(
    """Choose parameters to classify mutations as yo-yo, fixated or none using the slope algorithm."""
)

submitted = False
with st.form("parameters", enter_to_submit=False):
    st.write("Please input parameters for mutation classification")
    slope_points = int(st.number_input('Number of points used to calculate the slopes: ', value=5, placeholder='5',
                                       help="The number of data points used to calculate one slope value."
                                            " The parameter can increase or decrease sensitivity of the algorithm."))
    st.divider()
    min_percentage = int(
        st.number_input("Minimal percentage for filtering significant lineages:", value=30, placeholder='30',
                        help="The percentage is used to filter out only the lineages that are significant at the"
                             " time period of the mutation being present."))
    st.divider()
    submitted = st.form_submit_button("Submit")

if submitted:
    st.session_state.slope_form_submitted = True
    st.session_state.slope_points = slope_points
    st.session_state.min_percentage = min_percentage

if st.session_state.get("slope_form_submitted"):
    start = time.time()
    st.session_state.classified_mutations_slope = classify_mutations_slope(smoothed_data_files, slope_points)
    yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_slope)

    st.markdown(f"Number of mutations discovered for the selected parameters: \n"
                f"- **{len(yo_yo_mutations)}** yo-yo mutations\n"
                f"- **{len(fixated_mutations)}** fixated mutations\n")

    all_mutations, yo_yo, fixated = st.tabs(["All", "Yo-yo", "Fixated"])

    with all_mutations:
        with st.form(key='all', enter_to_submit=False):
            options_all = st.multiselect(
                "Choose or search for a mutation",
                st.session_state.classified_mutations_slope.keys()
            )

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_all = options_all
                show_mutation_data(st.session_state.classified_mutations_slope, options_all, st.session_state.min_percentage)

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
