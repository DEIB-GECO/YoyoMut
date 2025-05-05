import streamlit as st
import sys

sys.path.append("../")

st.set_page_config(page_title="Help", layout="wide")

st.header(f"Additional information")


st.markdown("""
### Data
The data sourced from CoV-Spectrum via [Lapis](https://lapis.cov-spectrum.org/open/v2/docs/getting-started/introduction) webservice
is saved in CSV files (one file for each residue), where each row represents the prevalence of the residue for that 
specific date. Information about the confidence interval is also available for each day. 
""")

st.markdown("""
### Data preparation for the algorithms
To have more consistent data for the classification algorithms input, the data is being smoothed. 
For the classification by relative frequency threshold, the data is grouped until it reaches at least 5000 sequences
in one time frame and then averaged. Because of the difference in sequencing capacity over time, the time periods are 
not uniform.
For the classification by prevalence slope, the data is smoothed over a 7-day time period, as the slope computation
depends on consistent time frames.
""")

st.markdown("""
### Classification of residues by relative frequency threshold
After smoothing the data and inputting the parameters, the algorithm classifies residues into yo-yo, fixated or 
unmutated residues. Residues are classified as fixated if the mutation prevalence went over the threshold and remained 
over the threshold. The residue is classified as yo-yo if the mutation prevalence went over the threshold, remained
prevalent for at least the selected number of days and then fell below the threshold again. Multiple cycles of this
behavior do not change the classification. The residues that do not have either of these patterns are classified
as unmutated.
""")

st.markdown("""
### Classification of residues by prevalence slope analysis
After smoothing the data and inputting the parameters, the algorithm classifies residues into yo-yo, fixated or 
unmutated residues. 
For each residue, the slope is computed over the selected number of timepoints. Then, a residue is classified as a 
fixated mutation if the slope was positive or close to zero, but not negative. To be classified as a yo-yo mutation
the slope needs to be positive and later negative. Each appearance of the mutation later on does not change the 
classification. If none of those patterns are recognized, the residue is classified as unmutated.
""")

