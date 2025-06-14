import time

import streamlit as st

from utils.hill_count import classify_mutations_slope
from utils.name_conversion import get_positions
from utils.visualization import show_mutation_data
from utils.web_data_prep import data_preparation, sort_by_residue_number
from utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="Mutation classification", layout="wide")

sidebar1, sidebar2 = st.sidebar.columns([1,7], vertical_alignment='center')
with sidebar1:
    st.image("./media/running_icon.gif")
with sidebar2:
    st.write("Our app computes results and visualizations online, please be patient when you see the running "
             "icon at the top right corner.")


st.title("Classification of residues by prevalence slope analysis", anchor=False)

st.write(
    """
    Choose parameters to classify amino acid residues as unmutated, yo-yo mutated, or fixated mutation using the slope algorithm.
    """
)

if 'smoothed_data_files_days' not in st.session_state:
    with st.spinner("Loading data..."):
        st.session_state.smoothed_data_files_days = data_preparation(by_days=True)

submitted = False
with st.form("parameters", enter_to_submit=False):
    st.write("Please input parameters for amino acid residue classification")
    slope_points = int(st.number_input('Number of timepoints to calculate the slope: ', value=5, placeholder='5',
                                       help="The number of data points used to calculate one slope value."
                                            " The parameter can increase or decrease sensitivity of the algorithm."))
    st.divider()
    min_percentage = int(
        st.number_input("Minimum relative prevalence for filtering significant PANGO lineages with the selected mutation:",
                        value=30, placeholder='30',
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
    st.session_state.classified_mutations_slope = classify_mutations_slope(
        "smoothed_data_files_days",
        slope_points)
    yo_yo_mutations, fixated_mutations = filter_mutations(st.session_state.classified_mutations_slope)

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
        sorted_keys = sort_by_residue_number(st.session_state.classified_mutations_slope.keys())
        with st.form(key='all', enter_to_submit=False):
            options_all = st.multiselect(
                "Choose or search for a mutation",
                sorted_keys
            )

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.options_all = options_all
                show_mutation_data(st.session_state.classified_mutations_slope, options_all, st.session_state.min_percentage)

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
