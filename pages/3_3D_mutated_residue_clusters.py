import pandas as pd
import streamlit as st
from protein_visualization.protein_3d_model import show_3d_protein
from utils.hill_count import classify_mutations_threshold, classify_mutations_slope
from utils.name_conversion import get_positions
from utils.web_data_prep import data_preparation, get_potential_residues
from utils.yo_yo_check import filter_mutations

st.set_page_config(page_title="3D mutated residue clusters", layout="wide")

sidebar1, sidebar2 = st.sidebar.columns([1, 7], vertical_alignment='center')
with sidebar1:
    st.image("./media/running_icon.gif")
with sidebar2:
    st.write("Our app computes results and visualizations online, please be patient when you see the running "
             "icon at the top right corner.")

st.title("3D mutated residue clusters", anchor=False)
st.write("Choose which algorithm to use for the visualisation of the 3D protein model:")
reset_button_container = st.container()
reset_button_container.write("To run the algorithm with new parameters click the reset button.")
reset_btn1, reset_btn2, _ = st.columns([1, 1, 2])

if 'smoothed_data_files_days' not in st.session_state \
        or 'smoothed_data_files_sequences' not in st.session_state:
    with st.spinner("Loading data..."):
        if 'smoothed_data_files_days' not in st.session_state:
            st.session_state.smoothed_data_files_days = data_preparation(by_days=True)
        if 'smoothed_data_files_sequences' not in st.session_state:
            st.session_state.smoothed_data_files_sequences = data_preparation(by_days=False)

if 'potential_residues' not in st.session_state:
    st.session_state.potential_residues = get_potential_residues(st.session_state.smoothed_data_files_sequences)

if 'threshold_submit_button_disabled' not in st.session_state:
    st.session_state.threshold_submit_button_disabled = False

if 'slope_submit_button_disabled' not in st.session_state:
    st.session_state.slope_submit_button_disabled = False

submitted = False


def submitted_threshold():
    st.session_state.submitted_threshold = True
    st.session_state.form_3d_submitted = True
    st.session_state.threshold_submit_button_disabled = True
    st.session_state.submitted_slope = False


def submitted_slope():
    st.session_state.submitted_slope = True
    st.session_state.form_3d_submitted = True
    st.session_state.slope_submit_button_disabled = True
    st.session_state.submitted_threshold = False


def activate_thr_submit_btn():
    st.session_state.threshold_submit_button_disabled = False
    st.session_state.form_3d_submitted = False
    st.session_state.visualization_form_expanded = True


def activate_slope_submit_btn():
    st.session_state.slope_submit_button_disabled = False
    st.session_state.form_3d_submitted = False
    st.session_state.visualization_form_expanded = True


def get_residue_dataframe(data):
    data.sort()
    df = pd.DataFrame({"Residues": data})
    df["Residues"] = "S:" + df["Residues"].astype(str)
    df.index += 1
    return df


threshold_alg, slope_alg = st.tabs(["Threshold algorithm", "Slope algorithm"])

with threshold_alg:
    with st.form("parameters-threshold", enter_to_submit=False):
        st.write("Please input parameters for amino acid residue classification")
        st.number_input('Global relative frequency threshold (0-1):', value=0.3, placeholder='0.3',
                        min_value=0.0,
                        max_value=1.0,
                        help="The threshold defines the minimal proportion of sequences "
                             "that must contain the mutation for it to be relevant.",
                        key="threshold")

        st.number_input('Minimal duration (in days): ', value=30, placeholder='30',
                        help="Minimal number of days above the selected relative frequency threshold "
                             "to be considered significant.",
                        key='min_days')

        submitted_threshold = st.form_submit_button("Submit", on_click=submitted_threshold,
                                                    disabled=st.session_state.threshold_submit_button_disabled)

reset_btn1.button("Reset threshold algorithm parameters", on_click=activate_thr_submit_btn,
                  disabled=not st.session_state.threshold_submit_button_disabled,
                  key='reset_threshold')

with slope_alg:
    with st.form("parameters-slope", enter_to_submit=False):
        st.write("Please input parameters for amino acid residue classification")
        st.number_input('Number of points used to calculate the slopes: ', value=5, placeholder='5',
                        help="The number of data points used to calculate one slope value."
                             " The parameter can increase or decrease sensitivity of the algorithm.",
                        key="slope_points")
        submitted_slope = st.form_submit_button("Submit", on_click=submitted_slope,
                                                disabled=st.session_state.slope_submit_button_disabled)

reset_btn2.button("Reset slope algorithm parameters", on_click=activate_slope_submit_btn,
                  disabled=not st.session_state.slope_submit_button_disabled,
                  key='reset_slope')

if st.session_state.get("form_3d_submitted"):
    if st.session_state.get("submitted_threshold"):
        st.header("Classification of residues by relative frequency threshold", anchor=False)
        st.session_state.classified_mutations_threshold = classify_mutations_threshold(
            "smoothed_data_files_sequences",
            st.session_state.threshold,
            st.session_state.min_days)
        st.session_state.yo_yo_mutations, st.session_state.fixated_mutations = \
            filter_mutations(st.session_state.classified_mutations_threshold)
    elif st.session_state.get("submitted_slope"):
        st.header("Classification of residues by prevalence slope analysis", anchor=False)
        st.session_state.classified_mutations_slope = classify_mutations_slope(
            "smoothed_data_files_days", st.session_state.slope_points)
        st.session_state.yo_yo_mutations, st.session_state.fixated_mutations = \
            filter_mutations(st.session_state.classified_mutations_slope)

    yo_yo_residues = get_positions(st.session_state.yo_yo_mutations.keys())
    fixated_residues = get_positions(st.session_state.fixated_mutations.keys())

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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**{len(yo_yo_residues)}** residues classified as *yo-yo*:")
        st.dataframe(get_residue_dataframe(yo_yo_residues), hide_index=False)
    with col2:
        st.write(f"**{len(fixated_residues)}** residues classified as *fixated*:")
        st.dataframe(get_residue_dataframe(fixated_residues), hide_index=False)
    with col3:
        st.write(f"**{len(other_residues)}** *unmutated* residues:")
        st.dataframe(get_residue_dataframe(other_residues), hide_index=False)

