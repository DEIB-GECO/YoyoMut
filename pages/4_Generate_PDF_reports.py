import streamlit as st

from utils.hill_count import classify_mutations_threshold, classify_mutations_slope
from utils.results_to_report import results_to_PDF
from utils.web_data_prep import data_preparation
from utils.yo_yo_check import filter_mutations

st.title("Generate PDF reports")
st.markdown("Choose the algorithm you want to use, input the parameters and click submit!"
            " The download buttons will appear when the reports are ready to download.\n\n")

if 'smoothed_data_files_sequences' not in st.session_state:
    st.session_state.smoothed_data_files_sequences = data_preparation(by_days=False)
if 'smoothed_data_files_days' not in st.session_state:
    st.session_state.smoothed_data_files_days = data_preparation(by_days=True)

st.write("Input parameters you want to use for the reports:")

# Input forms for the threshold and slope algorithms
with st.expander("Threshold algorithm"):
    with st.form("parameters-threshold", enter_to_submit=False):
        st.write("Please input parameters for amino acid residue classification")
        threshold = st.number_input('Global relative frequency threshold (0-1):', value=0.3, placeholder='0.3',
                                    help="The threshold defines the minimal proportion of sequences "
                                         "that must contain the mutation for it to be relevant.",
                                    min_value=0.0,
                                    max_value=1.0
                                    )

        min_days = st.number_input('Minimal duration (in days): ', value=30, placeholder='30',
                                   help="Minimal number of days above the selected relative frequency threshold "
                                        "to be considered significant."
                                   )

        submitted_threshold = st.form_submit_button("Submit")

with st.expander("Slope algorithm"):
    with st.form("parameters-slope", enter_to_submit=False):
        st.write("Please input parameters for amino acid residue classification")
        slope_points = int(st.number_input('Number of points used to calculate the slopes: ', value=5, placeholder='5',
                                           help="The number of data points used to calculate one slope value."
                                                " The parameter can increase or decrease sensitivity of the algorithm."))
        submitted_slope = st.form_submit_button("Submit")

# When submit is clicked trigger new computation only if the parameter values changed.
# Then also delete currently saved reports.
if submitted_threshold:
    st.session_state.submitted_threshold = True
    if st.session_state.get('report_threshold_value') != threshold \
            or st.session_state.get('report_min_days_value') != min_days:
        st.session_state.threshold = threshold
        st.session_state.min_days = min_days
        if 'yo_yo_threshold_report_path' in st.session_state:
            del st.session_state['yo_yo_threshold_report_path']
        if 'fixated_threshold_report_path' in st.session_state:
            del st.session_state['fixated_threshold_report_path']
else:
    st.session_state.submitted_threshold = False

if submitted_slope:
    st.session_state.submitted_slope = True
    if st.session_state.get('report_slope_points_value') != slope_points:
        st.session_state.slope_points = slope_points
        if 'yo_yo_slope_report_path' in st.session_state:
            del st.session_state['yo_yo_slope_report_path']
        if 'fixated_slope_report_path' in st.session_state:
            del st.session_state['fixated_slope_report_path']
else:
    st.session_state.submitted_slope = False

# Running the algorithms
if st.session_state.get("submitted_threshold"):
    st.session_state.classified_mutations_threshold = \
        classify_mutations_threshold(st.session_state.smoothed_data_files_sequences,
                                     st.session_state.threshold,
                                     st.session_state.min_days)

    st.session_state.yo_yo_mutations_threshold, st.session_state.fixated_mutations_threshold = \
        filter_mutations(st.session_state.classified_mutations_threshold)

if st.session_state.get("submitted_slope"):
    st.session_state.classified_mutations_slope = \
        classify_mutations_slope(st.session_state.smoothed_data_files_days, slope_points)

    st.session_state.yo_yo_mutations_slope, st.session_state.fixated_mutations_slope = \
        filter_mutations(st.session_state.classified_mutations_slope)

threshold_alg_computed = 'yo_yo_mutations_threshold' in st.session_state \
                         and 'fixated_mutations_threshold' in st.session_state
slope_alg_computed = 'yo_yo_mutations_slope' in st.session_state \
                     and 'fixated_mutations_slope' in st.session_state

# After algorithm execution finished generate PDF reports
if threshold_alg_computed:
    if 'yo_yo_threshold_report_path' not in st.session_state:
        st.session_state.yo_yo_threshold_report_path = \
            results_to_PDF(report_path='./reports/',
                           report_title='Yo-yo mutations',
                           additional_info='Classification of residues by relative frequency threshold',
                           report_name='yo_yo_mutations_threshold_analysis',
                           data_dict=st.session_state.yo_yo_mutations_threshold,
                           parameters={'Threshold': st.session_state.threshold,
                                       'Minimum duration (in days)': st.session_state.min_days})
        st.session_state.report_threshold_value = st.session_state.threshold
        st.session_state.report_min_days_value = st.session_state.min_days
    if 'fixated_threshold_report_path' not in st.session_state:
        st.session_state.fixated_threshold_report_path = \
            results_to_PDF(report_path='./reports/',
                           report_title='Fixated mutations',
                           additional_info='Classification of residues by relative frequency threshold',
                           report_name='fixated_mutations_threshold_analysis',
                           data_dict=st.session_state.fixated_mutations_threshold,
                           parameters={'Threshold': st.session_state.threshold,
                                       'Minimum duration (in days)': st.session_state.min_days})

if slope_alg_computed:
    if 'yo_yo_slope_report_path' not in st.session_state:
        st.session_state.yo_yo_slope_report_path = \
            results_to_PDF(report_path='./reports/',
                           report_title='Yo-yo mutations',
                           additional_info='Classification of residues by prevalence slope analysis',
                           report_name='yo_yo_mutations_slope_analysis',
                           data_dict=st.session_state.yo_yo_mutations_slope,
                           parameters={'Time points used to calculate slope': st.session_state.slope_points})
        st.session_state.report_slope_points_value = st.session_state.slope_points
    if 'fixated_slope_report_path' not in st.session_state:
        st.session_state.fixated_slope_report_path = \
            results_to_PDF(report_path='./reports/',
                           report_title='Fixated mutations',
                           additional_info='Classification of residues by prevalence slope analysis',
                           report_name='fixated_mutations_slope_analysis',
                           data_dict=st.session_state.fixated_mutations_slope,
                           parameters={'Time points used to calculate slope': st.session_state.slope_points})

# Show buttons for PDF report download
reports_threshold, reports_slope = st.columns(2)
with reports_threshold:
    st.markdown("### Download threshold algorithm results as PDFs:")
    if 'yo_yo_threshold_report_path' in st.session_state:
        with open(st.session_state.yo_yo_threshold_report_path, "rb") as f:
            report_yo_yo_threshold_data = f.read()
        st.download_button(
            label="Download yo-yo PDF",
            help="Download a PDF report for yo-yo mutations classified by the threshold algorithm",
            data=report_yo_yo_threshold_data,
            file_name=st.session_state.yo_yo_threshold_report_path.split('/')[-1],
            mime="application/pdf",
            icon=":material/download:",
        )
    else:
        st.download_button(
            label="Download yo-yo PDF",
            help="Run the threshold algorithm to generate the PDF reports.",
            data="",
            disabled=True
        )
        st.download_button(
            label="Download fixated PDF",
            help="Run the threshold algorithm to generate the PDF reports.",
            data="",
            disabled=True
        )

    if 'fixated_threshold_report_path' in st.session_state:
        with open(st.session_state.fixated_threshold_report_path, "rb") as f:
            report_fixated_threshold_data = f.read()
        st.download_button(
            label="Download fixated PDF",
            help="Download a PDF report for fixated mutations classified by the threshold algorithm",
            data=report_fixated_threshold_data,
            file_name=st.session_state.fixated_threshold_report_path.split('/')[-1],
            mime="application/pdf",
            icon=":material/download:",
        )

with reports_slope:
    st.markdown("### Download slope algorithm results as PDFs:")
    if 'yo_yo_slope_report_path' in st.session_state:
        with open(st.session_state.yo_yo_slope_report_path, "rb") as f:
            report_yo_yo_slope_data = f.read()
        st.download_button(
            label="Download yo-yo PDF",
            help="Download a PDF report for yo-yo mutations classified by the slope algorithm",
            data=report_yo_yo_slope_data,
            file_name=st.session_state.yo_yo_slope_report_path.split('/')[-1],
            mime="application/pdf",
            icon=":material/download:",
        )
    else:
        st.download_button(
            label="Download yo-yo PDF",
            help="Run the slope algorithm to generate the PDF reports.",
            data="",
            disabled=True
        )
        st.download_button(
            label="Download fixated PDF",
            help="Run the slope algorithm to generate the PDF reports.",
            data="",
            disabled=True
        )

    if 'fixated_slope_report_path' in st.session_state:
        with open(st.session_state.fixated_slope_report_path, "rb") as f:
            report_fixated_slope_data = f.read()
        st.download_button(
            label="Download fixated PDF",
            help="Download a PDF report for fixated mutations classified by the slope algorithm",
            data=report_fixated_slope_data,
            file_name=st.session_state.fixated_slope_report_path.split('/')[-1],
            mime="application/pdf",
            icon=":material/download:",
        )
