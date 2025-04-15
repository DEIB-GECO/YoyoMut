import streamlit as st
import sys

sys.path.append("../")

from utils.web_data_prep import data_preparation

st.set_page_config(page_title="Home page", layout="wide")

st.header(f"Welcome!")

st.write("This app is used to classify different mutations on the Spike protein depending on your research needs. "
         "The data used is sourced from [Lapis](https://lapis.cov-spectrum.org/open/v2/docs/getting-started/introduction). ")
st.write("The mutations can be classified into three classes: *yo-yo*, *fixated* "
         "or *unclassified*. In order to get started, you will need to choose certain parameters, such as threshold, "
         "duration and minimal lineage percentage, or choose the number of points to use for slope calculation.")
st.write("These parameters affect how the residues, and specific mutations on residues, are classified into mentioned groups.")
st.write("The classified mutations can be viewed in two ways:")
st.write("""
- **Mutation classification**
  - shows graphs with sequences through time, tables with time frames of the mutations, and lineages that were significant during that time period
""")
st.write("""
- **3D protein model**
  - renders a 3D model of the Spike protein, coloring the residues in different colors depending on their classification
""")

with st.status("Loading data...", expanded=False) as status:
    smoothed_data_files = data_preparation()
    status.update(label="Data loaded successfully!", state="complete", expanded=False)
    st.session_state.smoothed_data_files = smoothed_data_files


