import streamlit as st
import sys

sys.path.append("../")

from utils.web_data_prep import data_preparation

st.set_page_config(page_title="Home page", layout="wide")

if 'last_date' not in st.session_state:
    with open("data/metadata/last_date.txt", 'r') as f:
        last_date = f.read()
        st.session_state.last_date = last_date

st.header(f"Welcome!")

st.write("This app is used to classify mutations on the SARS-CoV-2 Spike protein in time at a global level. "
         "The data used is sourced from CoV-Spectrum via [Lapis](https://lapis.cov-spectrum.org/open/v2/docs/getting-started/introduction) webservice. "
         "Files were last-updated on ", st.session_state.last_date,".")
st.write("The amino acid residues can be classified into three classes: *unmutated*, *yo-yo mutations* or *fixated mutations*. "
         "In order to get started, you will need to choose certain parameters, such as threshold, "
         "duration and minimal lineage percentage, or choose the number of points to use for slope calculation.")
st.write("These parameters affect how the residues, and specific mutations on residues, are classified into the above-mentioned groups.")
st.write("The classified mutations can be viewed in two ways:")
st.write("""
- **Mutation classification**
  - shows graphs with relative frequency of mutation at a given amino acid residue in time
""")
st.write("""
- **3D protein model**
  - renders a 3D model of the Spike protein, coloring the residues in different colors depending on their classification
""")
st.write("If you want to save results of a certain configuration, you can generate and download PDF reports using those parameters.")
st.write("Additional details and instructions ca be found in the Help tab.")
with st.status("Loading data...", expanded=False) as status:
    if 'smoothed_data_files_by_days' not in st.session_state:
        st.session_state.smoothed_data_files_days = data_preparation(by_days=True)
    if 'smoothed_data_files_sequences' not in st.session_state:
        st.session_state.smoothed_data_files_sequences = data_preparation(by_days=False)
    status.update(label="Data loaded successfully!", state="complete", expanded=False)


